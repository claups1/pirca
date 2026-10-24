"""Pirca's multi-agent run: the Manager calls the Risk Analyst, Planner and Critic as tools.

Each worker sees only the slice of the shop profile it needs; tools that need the
full profile get it from the run context, never from the model.
"""

import json
import re
from datetime import date

from backend import config
from backend.agents import TOOLSETS
from backend.agents.runner import (
    AgentOutputError,
    AgentSession,
    LimitHit,
    RunContext,
    ToolSpec,
    function_schema,
)
from backend.tools import (
    SCENARIOS,
    compute_cash_buffer,
    compute_stock_move,
    compute_supplier_buffer,
    fill_placeholders,
    get_action_catalog,
    get_historical_impacts,
    optimize_budget,
    run_scenario,
    score_exposure,
    search_documents,
    validate_profile,
    verify_draft,
)
from backend.tools.drafting import recommended_spending
from backend.tools.profile import district_level, parse_profile

# ---------------------------------------------------------------- worker tools

NO_ARGS = "Uses the shop profile of this run; takes no arguments."

WORKER_TOOLS = {
    "score_exposure": ToolSpec(
        function_schema("score_exposure", f"Exposure score, risk level and stock within 1 m of the floor. {NO_ARGS}"),
        lambda ctx, a: score_exposure(ctx.profile)),
    "get_historical_impacts": ToolSpec(
        function_schema("get_historical_impacts",
                        "Historical impacts in Piura from 1997-98 and 2017, filtered by any of the arguments.",
                        {"district": {"type": "string"}, "event": {"type": "string", "description": "1997-98 or 2017"},
                         "topic": {"type": "string", "description": "flooding, roads_bridges, business_losses, "
                                   "economic_losses, closure_duration, dengue, people_affected, housing, rainfall, "
                                   "river_flow, other"},
                         "keyword": {"type": "string"},
                         "include_region": {"type": "boolean", "description": "Also return region-wide rows"}}),
        # Empty strings from the model mean "no filter", not "match nothing".
        lambda ctx, a: get_historical_impacts(**{k: v for k, v in a.items() if v not in ("", None)})),
    "search_documents": ToolSpec(
        function_schema("search_documents", "Keyword search over Pirca's curated data; returns snippets with source IDs.",
                        {"query": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 8}},
                        ("query",)),
        lambda ctx, a: search_documents(a["query"], min(int(a.get("limit", 5)), 8))),
    "compute_stock_move": ToolSpec(
        function_schema("compute_stock_move", f"How much stock to lift above 1 m and where. {NO_ARGS}"),
        lambda ctx, a: compute_stock_move(ctx.profile)),
    "compute_cash_buffer": ToolSpec(
        function_schema("compute_cash_buffer", f"Weeks closed, weekly fixed costs, buffer needed, cash gap. {NO_ARGS}"),
        lambda ctx, a: compute_cash_buffer(ctx.profile)),
    "compute_supplier_buffer": ToolSpec(
        function_schema("compute_supplier_buffer", f"Road-cut risk per supplier city and extra days of stock. {NO_ARGS}"),
        lambda ctx, a: compute_supplier_buffer(ctx.profile)),
    "get_action_catalog": ToolSpec(
        function_schema("get_action_catalog", f"Catalog actions for this shop's hazards, minus what it has. {NO_ARGS}"),
        lambda ctx, a: get_action_catalog(ctx.profile)),
    "optimize_budget": ToolSpec(
        function_schema("optimize_budget", f"Best set of actions within the prep budget. {NO_ARGS}"),
        lambda ctx, a: optimize_budget(ctx.profile)),
    "verify_draft": ToolSpec(
        function_schema("verify_draft", "Code checks on a draft: typed numbers, unknown placeholders, units next "
                        "to placeholders, unknown source IDs, evacuation orders, own forecasts. Set final_plan "
                        "true for the owner's plan to also check action names, asterisks, internal terms, "
                        "grammar, length and section 7. The facts come from this run.",
                        {"draft": {"type": "string"}, "final_plan": {"type": "boolean"}}, ("draft",)),
        lambda ctx, a: verify_draft(a["draft"], ctx.facts, final_plan=bool(a.get("final_plan")),
                                    district_unverified=_district_unverified(ctx),
                                    language=ctx.language)),
    "run_scenario": ToolSpec(
        function_schema("run_scenario", "Recompute this shop's numbers under one stress scenario.",
                        {"scenario": {"type": "string", "enum": list(SCENARIOS)}}, ("scenario",)),
        lambda ctx, a: run_scenario(ctx.profile, a["scenario"], today=ctx.today)),
}


def toolset(agent: str, extra: dict | None = None) -> dict[str, ToolSpec]:
    available = {**WORKER_TOOLS, **(extra or {})}
    return {name: available[name] for name in TOOLSETS[agent]}


# ------------------------------------------------------- worker context slices

def _shop(ctx: RunContext, fields: tuple) -> dict:
    data = ctx.profile.model_dump()
    return {k: data[k] for k in fields}


def _message(**parts) -> str:
    return "\n\n".join(f"## {k}\n{json.dumps(v, ensure_ascii=False, indent=1, default=str)}" for k, v in parts.items())


def risk_analyst_message(ctx: RunContext) -> str:
    shop = _shop(ctx, ("business_type", "district", "near_water", "flooded_before", "floor_level",
                       "higher_storage", "perishables"))
    shop["supplier_cities"] = [s.city for s in ctx.profile.suppliers]
    return _message(today=ctx.today.isoformat(), shop=shop, profile_warnings=ctx.state["warnings"])


def planner_message(ctx: RunContext, revision_notes: list[str] | None) -> str:
    analysis = ctx.state["analysis"]
    keep = ("enfen_status", "exposure", "hazards", "supplier_routes", "warnings")
    parts = dict(today=ctx.today.isoformat(),
                 shop=_shop(ctx, ("business_type", "district", "tenure", "workers", "higher_storage",
                                  "perishables", "suppliers", "already_have")),
                 risk_analysis={k: analysis[k] for k in keep if k in analysis})
    if revision_notes:
        parts["revision_notes"] = revision_notes
    return _message(**parts)


def critic_message(ctx: RunContext) -> str:
    return _message(today=ctx.today.isoformat(),
                    shop=_shop(ctx, ("business_type", "district", "tenure", "workers", "perishables")),
                    district_warnings=ctx.state["analysis"].get("warnings", []),
                    planner_draft=ctx.state["draft"], facts=ctx.facts)


def _district_unverified(ctx: RunContext) -> bool:
    return district_level(ctx.profile) == "UNVERIFIED"


def manager_message(ctx: RunContext) -> str:
    # The district's real hazard level comes from code, so the Manager never has to guess it.
    district = {"name": ctx.profile.district, "hazard_level": district_level(ctx.profile),
                "unverified": _district_unverified(ctx)}
    return _message(language=ctx.language, today=ctx.today.isoformat(),
                    shop=_shop(ctx, ("business_type",)), district=district,
                    profile_warnings=ctx.state["warnings"])


# ------------------------------------------------------------- manager tools

def _run_risk_analyst(ctx: RunContext, args: dict) -> dict:
    analysis = AgentSession(ctx, "risk_analyst", toolset("risk_analyst")).send(risk_analyst_message(ctx))
    ctx.state["analysis"] = analysis
    return {"risk_analysis": analysis}


def _run_planner(ctx: RunContext, args: dict) -> dict:
    if "analysis" not in ctx.state:
        return {"error": "Run run_risk_analyst first."}
    notes = [str(n) for n in args.get("revision_notes") or []]
    draft = AgentSession(ctx, "planner", toolset("planner")).send(planner_message(ctx, notes))
    ctx.state["draft"] = draft
    return {"planner_draft": draft, "available_facts": dict(ctx.facts)}


# The Critic checks the Planner's internal draft, which is not an owner plan, so its
# verify_draft never applies the owner-plan rules (sections, names, length...).
CRITIC_TOOLS = {
    "verify_draft": ToolSpec(
        function_schema("verify_draft", "Code checks on the Planner's draft: typed numbers, unknown placeholders, "
                        "units next to placeholders, unknown source IDs, evacuation orders, own forecasts.",
                        {"draft": {"type": "string"}}, ("draft",)),
        lambda ctx, a: verify_draft(a["draft"], ctx.facts)),
}


def _run_critic(ctx: RunContext, args: dict) -> dict:
    if "draft" not in ctx.state:
        return {"error": "Run run_planner first."}
    critique = AgentSession(ctx, "critic", toolset("critic", CRITIC_TOOLS)).send(critic_message(ctx))
    ctx.state["critique"] = critique
    return {"critique": critique, "available_facts": dict(ctx.facts)}


MANAGER_TOOLS = {
    "run_risk_analyst": ToolSpec(
        function_schema("run_risk_analyst", "Run the Risk Analyst once. Returns its JSON."), _run_risk_analyst),
    "run_planner": ToolSpec(
        function_schema("run_planner", "Run the Planner. Pass revision_notes only when asking for a revision.",
                        {"revision_notes": {"type": "array", "items": {"type": "string"}}}), _run_planner),
    "run_critic": ToolSpec(
        function_schema("run_critic", "Run the Critic on the latest Planner draft. Returns its JSON."), _run_critic),
}

# ------------------------------------------------------------------ the run

# The backslash keeps Markdown from turning the footnote into a bullet point.
FOOTNOTE = {"es": r"\* Costo o beneficio estimado, no medido.",
            "en": r"\* Estimated cost or benefit, not measured."}
DISCLAIMER = {
    "es": "_Pirca no es una agencia oficial. Sigue los avisos de ENFEN, SENAMHI, INDECI y tu municipalidad._",
    "en": "_Pirca is not an official agency. Follow ENFEN, SENAMHI, INDECI and your municipality._",
}

WARNING_TEXT = {
    "es": "⚠️ **Aviso:** este plan no pasó la verificación automática de Pirca. Revisa los números y las fuentes "
          "antes de usarlo, y sigue siempre a ENFEN, SENAMHI, INDECI y tu municipalidad.",
    "en": "⚠️ **Warning:** this plan did not pass Pirca's automatic check. Review its numbers and sources before "
          "using it, and always follow ENFEN, SENAMHI, INDECI and your municipality.",
}


def _with_footer(plan: str, language: str) -> str:
    """Add the estimate footnote (only if an action is marked with *) and the disclaimer."""
    body = re.sub(r"\*\*[^*\n]+\*\*", "", plan)  # ignore **bold**
    lines = [plan.rstrip(), ""]
    if "*" in body:
        lines.append(FOOTNOTE[language])
        lines.append("")
    lines.append(DISCLAIMER[language])
    return "\n".join(lines) + "\n"


def _fix_message(issues: list[dict]) -> str:
    return ("Code ran verify_draft on your plan_markdown and found these issues:\n"
            + json.dumps(issues, ensure_ascii=False, indent=1)
            + "\n\nFix every issue and return the complete JSON object again. "
              "Do not call run_risk_analyst, run_planner or run_critic.")


def _workflow_gaps(ctx: RunContext) -> list[str]:
    gaps = [f"The {name} never ran." for name in ("risk_analyst", "planner", "critic") if not ctx.agent_runs[name]]
    return gaps


def _base_result(ctx: RunContext) -> dict:
    return {"facts": ctx.facts, "sources": sorted(ctx.sources), "usage": ctx.usage.as_dict(),
            "usage_by_agent": {k: v.as_dict() for k, v in ctx.usage_by_agent.items()},
            "agent_runs": dict(ctx.agent_runs), "events": ctx.events,
            "worker_outputs": {k: ctx.state.get(k) for k in ("analysis", "draft", "critique")}}


def run_plan(profile: dict, language: str = "es", today: date | None = None, client=None, on_event=None) -> dict:
    """Run the whole Pirca pipeline for one shop and return the plan, trace and usage."""
    if language not in ("es", "en"):
        raise ValueError("language must be 'es' or 'en'")
    validation = validate_profile(profile)
    if not validation["valid"]:
        return {"status": "invalid_profile", "errors": validation["errors"], "warnings": validation["warnings"]}

    if client is None:
        from backend.llm import get_client
        client = get_client()
    ctx = RunContext(profile=parse_profile(profile), language=language, today=today or date.today(),
                     client=client, on_event=on_event)
    ctx.state["warnings"] = validation["warnings"]
    ctx.emit("run_started", "pirca", language=language, district=ctx.profile.district,
             limits={"max_agent_runs": config.MAX_AGENT_RUNS, "run_token_budget": config.RUN_TOKEN_BUDGET,
                     "max_output_tokens": config.MAX_OUTPUT_TOKENS})

    try:
        manager = AgentSession(ctx, "manager", toolset("manager", MANAGER_TOOLS))
        final = manager.send(manager_message(ctx))
        check = verify_draft(final.get("plan_markdown", ""), ctx.facts, final_plan=True, language=language,
                             district_unverified=_district_unverified(ctx))
        ctx.emit("final_check", "pirca", attempt=1, ok=check["ok"], issue_count=len(check["issues"]),
                 issues=[i["type"] for i in check["issues"]])
        fix_attempted = False
        if not check["ok"]:
            fix_attempted = True
            final = manager.send(_fix_message(check["issues"]))
            check = verify_draft(final.get("plan_markdown", ""), ctx.facts, final_plan=True, language=language,
                                 district_unverified=_district_unverified(ctx))
            ctx.emit("final_check", "pirca", attempt=2, ok=check["ok"], issue_count=len(check["issues"]),
                     issues=[i["type"] for i in check["issues"]])
    except LimitHit as e:
        ctx.emit("run_finished", "pirca", status="stopped_by_limit")
        return {"status": "stopped_by_limit",
                "stopped_by": {"agent": e.agent, "limit": e.limit, "detail": e.detail},
                "message": f"Stopped by limit: {e.limit} ({e.agent}). {e.detail}. No plan was produced.",
                **_base_result(ctx)}
    except AgentOutputError as e:
        ctx.emit("run_finished", "pirca", status="error")
        return {"status": "error", "message": str(e), **_base_result(ctx)}

    template = final.get("plan_markdown", "")
    plan = {cur: _with_footer(fill_placeholders(template, ctx.facts, currency=cur, language=language)["text"],
                              language)
            for cur in ("pen", "usd")}
    warning = None if check["ok"] else WARNING_TEXT[language]
    if warning:
        plan = {cur: f"> {warning}\n\n{text}" for cur, text in plan.items()}
    status = "completed" if check["ok"] else "completed_with_warning"
    ctx.emit("run_finished", "pirca", status=status)
    return {
        "status": status,
        "language": language,
        "plan_template": template,
        "plan": plan,  # {"pen": ..., "usd": ...}: the interface's currency toggle picks one
        "warning": warning,
        "verification": {"ok": check["ok"], "issues": check["issues"], "fix_attempted": fix_attempted},
        "affordability": recommended_spending(template, ctx.facts),
        "summary_en": final.get("summary_en", ""),
        "decisions": final.get("decisions", []),
        "open_issues": list(final.get("open_issues", [])) + _workflow_gaps(ctx),
        "missing_facts": final.get("missing_facts", []),
        "suspicious_content": final.get("suspicious_content", []),
        "critic_verdict": final.get("critic_verdict"),
        "revision_used": ctx.agent_runs["planner"] > 1,
        "profile_warnings": validation["warnings"],
        **_base_result(ctx),
    }
