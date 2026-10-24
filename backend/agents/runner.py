"""The agent loop: one model conversation with tools, limits, usage tracking and trace events.

Every step emits an event with running token and cost totals so the interface
can show a live trace. Hard limits (agent runs, tool calls, model turns, output
tokens, run token budget) raise LimitHit, which stops the whole run cleanly.
"""

import json
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Callable

from backend import config
from backend.agents.prompts import load_prompt
from backend.agents.usage import Usage, usage_from_response
from backend.tools.profile import ShopProfile


class LimitHit(Exception):
    """A safety limit was reached; the run stops and reports it."""

    def __init__(self, agent: str, limit: str, detail: str):
        super().__init__(f"{agent}: {limit} — {detail}")
        self.agent, self.limit, self.detail = agent, limit, detail


class AgentOutputError(Exception):
    """The model did not return the JSON object its prompt asks for."""


@dataclass
class ToolSpec:
    schema: dict  # function schema shown to the model
    handler: Callable[["RunContext", dict], dict]  # (context, model arguments) -> tool result


def function_schema(name: str, description: str, properties: dict | None = None,
                    required: tuple = ()) -> dict:
    return {"type": "function", "name": name, "description": description,
            "parameters": {"type": "object", "properties": properties or {},
                           "required": list(required), "additionalProperties": False}}


@dataclass
class RunContext:
    """Everything one plan run shares: the shop, the facts gathered so far, usage and the trace."""

    profile: ShopProfile
    language: str
    today: date
    client: Any
    on_event: Callable[[dict], None] | None = None
    facts: dict = field(default_factory=dict)
    sources: set = field(default_factory=set)
    usage: Usage = field(default_factory=Usage)
    usage_by_agent: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    agent_runs: Counter = field(default_factory=Counter)
    state: dict = field(default_factory=dict)
    started: float = field(default_factory=time.monotonic)

    def emit(self, type_: str, agent: str, **detail) -> dict:
        event = {"seq": len(self.events) + 1, "type": type_, "agent": agent,
                 "elapsed_s": round(time.monotonic() - self.started, 2), **detail,
                 "totals": self.usage.as_dict()}
        self.events.append(event)
        if self.on_event:
            self.on_event(event)
        return event

    def record_usage(self, agent: str, usage: Usage) -> None:
        self.usage.add(usage)
        self.usage_by_agent.setdefault(agent, Usage()).add(usage)

    def absorb(self, result: dict) -> None:
        """Keep every fact and source ID a tool returned, for verify_draft and the final plan."""
        if isinstance(result, dict):
            self.facts.update(result.get("facts") or {})
            self.sources.update(result.get("sources") or [])

    def limit(self, agent: str, limit: str, detail: str) -> LimitHit:
        self.emit("limit_hit", agent, limit=limit, detail=detail, action="stopped")
        return LimitHit(agent, limit, detail)


def _strip_urls(value):
    """Drop *_url and raw_files fields: agents cite IDs, and URLs only cost tokens."""
    if isinstance(value, dict):
        return {k: _strip_urls(v) for k, v in value.items() if not k.endswith("_url") and k != "raw_files"}
    if isinstance(value, list):
        return [_strip_urls(v) for v in value]
    return value


def _field(obj, name, default=None):
    return obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)


def _as_input_item(item) -> dict:
    return item.model_dump(exclude_none=True) if hasattr(item, "model_dump") else dict(item)


def _output_text(response) -> str:
    text = _field(response, "output_text", None)
    if text:
        return text
    parts = []
    for item in _field(response, "output", []) or []:
        for c in _field(item, "content", []) or []:
            if _field(c, "type") == "output_text":
                parts.append(_field(c, "text", ""))
    return "".join(parts)


def parse_json_object(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object found")
    data = json.loads(text[start:end + 1])
    if not isinstance(data, dict):
        raise ValueError("top-level JSON is not an object")
    return data


def _summarize(result: dict) -> dict:
    """Short view of a tool result for the trace."""
    if not isinstance(result, dict):
        return {}
    summary = {"facts": result.get("facts", {}), "sources": result.get("sources", [])}
    for key in ("ok", "risk_level", "verdict", "status", "error"):
        if key in result:
            summary[key] = result[key]
    return summary


class AgentSession:
    """One run of one agent. send() can be called again to continue the same conversation."""

    def __init__(self, ctx: RunContext, agent: str, tools: dict[str, ToolSpec]):
        self.ctx, self.agent, self.tools = ctx, agent, tools
        ctx.agent_runs[agent] += 1
        allowed = config.MAX_AGENT_RUNS[agent]
        if ctx.agent_runs[agent] > allowed:
            raise ctx.limit(agent, "max_agent_runs", f"{agent} may run at most {allowed} time(s) per plan")
        self.instructions = load_prompt(agent)
        self.input: list = []
        self.tool_calls = 0
        self.per_tool = Counter()
        ctx.emit("agent_started", agent, run=ctx.agent_runs[agent])

    def send(self, message: str) -> dict:
        ctx, agent = self.ctx, self.agent
        self.input.append({"role": "user", "content": message})
        asked_for_json = False
        for _ in range(config.MAX_MODEL_TURNS):
            if ctx.usage.total_tokens >= config.RUN_TOKEN_BUDGET:
                raise ctx.limit(agent, "run_token_budget",
                                f"{ctx.usage.total_tokens:,} of {config.RUN_TOKEN_BUDGET:,} tokens used")
            response = ctx.client.responses.create(
                model=config.MODEL_NAME, instructions=self.instructions, input=self.input,
                tools=[t.schema for t in self.tools.values()], max_output_tokens=config.MAX_OUTPUT_TOKENS,
                reasoning={"effort": config.REASONING_EFFORT}, prompt_cache_key=f"pirca-{agent}",
            )
            usage = usage_from_response(response)
            ctx.record_usage(agent, usage)
            ctx.emit("model_call", agent, call=usage.as_dict())
            if _field(response, "status") == "incomplete":
                raise ctx.limit(agent, "max_output_tokens",
                                f"response cut off at {config.MAX_OUTPUT_TOKENS:,} output tokens")

            output = list(_field(response, "output", []) or [])
            self.input.extend(_as_input_item(o) for o in output)
            calls = [o for o in output if _field(o, "type") == "function_call"]
            if not calls:
                try:
                    data = parse_json_object(_output_text(response))
                except ValueError as e:
                    if asked_for_json:
                        raise AgentOutputError(f"{agent} did not return a JSON object: {e}") from e
                    asked_for_json = True
                    self.input.append({"role": "user", "content": "Return only the JSON object your role describes."})
                    continue
                ctx.emit("agent_finished", agent, keys=sorted(data), usage=ctx.usage_by_agent[agent].as_dict())
                return data
            for call in calls:
                result = self._run_tool(call)
                self.input.append({"type": "function_call_output", "call_id": _field(call, "call_id"),
                                   "output": json.dumps(_strip_urls(result), ensure_ascii=False, default=str)})
        raise ctx.limit(agent, "max_model_turns", f"{config.MAX_MODEL_TURNS} model calls without a final answer")

    def _run_tool(self, call) -> dict:
        ctx, agent = self.ctx, self.agent
        name = _field(call, "name")
        try:
            args = json.loads(_field(call, "arguments") or "{}")
        except json.JSONDecodeError:
            args = {}
        ctx.emit("tool_called", agent, tool=name, args=args)

        if name not in self.tools:
            result = {"error": f"Tool '{name}' is not available to the {agent}. "
                               f"Available: {', '.join(self.tools)}"}
            ctx.emit("tool_result", agent, tool=name, result=_summarize(result))
            return result

        self.tool_calls += 1
        cap = config.MAX_TOOL_CALLS[agent]
        if self.tool_calls > cap:
            raise ctx.limit(agent, "max_tool_calls", f"{agent} may make at most {cap} tool calls")
        self.per_tool[name] += 1
        tool_cap = config.MAX_CALLS_PER_TOOL.get(agent, {}).get(name)
        if tool_cap is not None and self.per_tool[name] > tool_cap:
            # Soft limit: refuse this call and let the agent finish with what it has.
            ctx.emit("limit_hit", agent, limit="max_calls_per_tool", action="refused",
                     detail=f"{name} may be called at most {tool_cap} time(s)")
            result = {"error": f"Limit reached: {name} may be called at most {tool_cap} time(s). "
                               "Finish with the results you already have."}
            ctx.emit("tool_result", agent, tool=name, result=_summarize(result))
            return result

        try:
            result = self.tools[name].handler(ctx, args)
        except (LimitHit, AgentOutputError):
            raise
        except Exception as e:  # bad arguments from the model: report back instead of crashing
            result = {"error": f"{type(e).__name__}: {e}"}
        ctx.absorb(result)
        ctx.emit("tool_result", agent, tool=name, result=_summarize(result))
        return result
