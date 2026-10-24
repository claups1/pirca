"""Offline tests for the agent system, using a scripted fake model (no API calls)."""

import json
from datetime import date
from types import SimpleNamespace

import pytest

from backend import config
from backend.agents.pirca import run_plan
from backend.agents.usage import cost_usd, usage_from_response
from tests.test_owner_plan import GOOD_PLAN_ES

TODAY = date(2026, 10, 24)
PROFILE = dict(
    business_type="bodega", district="Castilla", near_water="yes", flooded_before="yes",
    floor_level="ground", higher_storage="none", tenure="rented", stock_value=20000,
    share_stock_below_1m=0.5, perishables=True, cash_on_hand=3000, monthly_fixed_costs=4000,
    weekly_sales=7000, workers=2, days_of_stock=7, prep_budget=500, already_have=[],
    suppliers=[{"product": "abarrotes", "city": "Chiclayo"}, {"product": "bebidas", "city": "Piura"}],
)
USAGE = {"input_tokens": 1000, "input_tokens_details": {"cached_tokens": 200, "cache_write_tokens": 100},
         "output_tokens": 50, "output_tokens_details": {"reasoning_tokens": 10}}

GOOD_PLAN = GOOD_PLAN_ES  # a valid seven-section owner plan


# ---------------------------------------------------------------- fake model

class Item(dict):
    def model_dump(self, exclude_none=True):
        return dict(self)


def call(name, **args):
    return ("call", name, args)


def final(obj):
    return ("final", obj)


class FakeResponses:
    """Plays a script per agent; the agent is identified by prompt_cache_key."""

    def __init__(self, scripts, status="completed"):
        self.scripts = {k: list(v) for k, v in scripts.items()}
        self.requests = []
        self.status = status
        self.n = 0

    def create(self, **kw):
        agent = kw["prompt_cache_key"].removeprefix("pirca-")
        self.requests.append((agent, kw))
        step = self.scripts[agent].pop(0)
        if callable(step):
            step = step(kw)
        output, text = [], ""
        if isinstance(step, list):  # several tool calls in one turn
            for _, name, args in step:
                self.n += 1
                output.append(Item(type="function_call", call_id=f"c{self.n}", name=name,
                                   arguments=json.dumps(args)))
        elif step[0] == "call":
            self.n += 1
            output.append(Item(type="function_call", call_id=f"c{self.n}", name=step[1], arguments=json.dumps(step[2])))
        else:
            text = step[1] if isinstance(step[1], str) else json.dumps(step[1])
            output.append(Item(type="message", role="assistant", content=[{"type": "output_text", "text": text}]))
        return SimpleNamespace(output=output, output_text=text, status=self.status, usage=USAGE)


class FakeClient:
    def __init__(self, scripts, status="completed"):
        self.responses = FakeResponses(scripts, status)


def analyst_script():
    return [[call("score_exposure"), call("search_documents", query="alerta El Niño costero")],
            final({"enfen_status": {"status": "Alerta de El Niño Costero", "communique_id": "ENFEN-2026-18"},
                   "exposure": {"risk_level": "high"}, "hazards": [], "supplier_routes": [], "warnings": [],
                   "missing_facts": [], "suspicious_content": []})]


def planner_script():
    return [[call("compute_stock_move"), call("compute_cash_buffer"), call("compute_supplier_buffer"),
             call("get_action_catalog"), call("optimize_budget")],
            final({"phases": {"now": [{"action": "Eleva la mercadería", "catalog_id": "CAT-01"}]},
                   "stock": {"summary": "Mueve {stock_to_move}"}, "missing_facts": [], "suspicious_content": []})]


def critic_script(verdict="approve"):
    return [[call("verify_draft", draft="Mueve {stock_to_move}"),
             call("run_scenario", scenario="rains_one_month_early"),
             call("run_scenario", scenario="main_bridge_cut"),
             call("run_scenario", scenario="long_closure")],
            final({"verdict": verdict, "scenarios": [], "material_gaps": [], "notes": [],
                   "missing_facts": [], "suspicious_content": []})]


def manager_final(plan=GOOD_PLAN):
    return final({"language": "es", "plan_markdown": plan, "summary_en": "One. Two. Three.",
                  "decisions": [{"decision": "approve", "reason": "critic approved"}], "revision_used": False,
                  "critic_verdict": "approve", "open_issues": [], "missing_facts": [], "suspicious_content": []})


def happy_scripts(**overrides):
    scripts = {"manager": [call("run_risk_analyst"), call("run_planner"), call("run_critic"), manager_final()],
               "risk_analyst": analyst_script(), "planner": planner_script(), "critic": critic_script()}
    scripts.update(overrides)
    return scripts


def run(scripts, **kw):
    client = FakeClient(scripts, kw.pop("status", "completed"))
    return run_plan(PROFILE, language="es", today=TODAY, client=client, **kw), client


# ---------------------------------------------------------------- usage

def test_cost_charges_each_token_kind_at_its_rate():
    p = config.PRICES_PER_MILLION
    assert cost_usd(1_000_000, 0, 0, 0) == pytest.approx(p["input"])
    assert cost_usd(1_000_000, 1_000_000, 0, 0) == pytest.approx(p["cached_input"])
    assert cost_usd(1_000_000, 0, 1_000_000, 0) == pytest.approx(p["cache_write"])
    assert cost_usd(0, 0, 0, 1_000_000) == pytest.approx(p["output"])


def test_prices_match_lecture_11():
    assert config.PRICES_PER_MILLION == {"input": 0.10, "cached_input": 0.01, "cache_write": 0.125, "output": 0.50}


def test_usage_reads_all_fields():
    u = usage_from_response(SimpleNamespace(usage=USAGE))
    assert (u.input_tokens, u.cached_input_tokens, u.cache_write_tokens, u.output_tokens) == (1000, 200, 100, 50)
    assert u.cost_usd == pytest.approx((700 * 0.10 + 200 * 0.01 + 100 * 0.125 + 50 * 0.50) / 1e6)


# ---------------------------------------------------------------- happy path

def test_end_to_end_with_fake_model():
    seen = []
    result, client = run(happy_scripts(), on_event=seen.append)
    assert result["status"] == "completed", result.get("message")
    assert "S/ 10,000" in result["plan"]["pen"] and "{" not in result["plan"]["pen"]
    assert "4 semanas" in result["plan"]["pen"] and "S/ 77 por 10 sacos llenos" in result["plan"]["pen"]
    # Safety: the plan never recommends spending more than the owner's cash
    assert result["affordability"]["within_cash"]
    assert result["affordability"]["total"] <= PROFILE["cash_on_hand"]
    assert "Costo o beneficio estimado, no medido." in result["plan"]["pen"]  # footnote: CAT-02 has *
    assert result["plan"]["pen"].rstrip().endswith("tu municipalidad._")  # disclaimer added by code
    assert "$" in result["plan"]["usd"] and "S/" not in result["plan"]["usd"]
    assert result["verification"]["ok"] and not result["verification"]["fix_attempted"]
    assert result["agent_runs"] == {"manager": 1, "risk_analyst": 1, "planner": 1, "critic": 1}
    assert result["open_issues"] == []
    # every model call is counted and priced
    calls = len(client.responses.requests)
    assert result["usage"]["model_calls"] == calls
    assert result["usage"]["input_tokens"] == 1000 * calls
    assert result["usage"]["cost_usd"] == pytest.approx(calls * usage_from_response(SimpleNamespace(usage=USAGE)).cost_usd, abs=1e-6)
    # live trace: same events streamed and returned, with running totals that never go down
    assert seen == result["events"]
    types = {e["type"] for e in seen}
    assert {"agent_started", "tool_called", "tool_result", "agent_finished", "model_call", "final_check"} <= types
    totals = [e["totals"]["total_tokens"] for e in seen]
    assert totals == sorted(totals)
    assert {e["agent"] for e in seen if e["type"] == "agent_started"} == {"manager", "risk_analyst", "planner", "critic"}


def test_workers_get_only_the_context_they_need():
    _, client = run(happy_scripts())
    first_msg = {}
    for agent, kw in client.responses.requests:
        first_msg.setdefault(agent, kw["input"][0]["content"])
    for agent in ("risk_analyst", "planner", "manager"):
        for secret in ("cash_on_hand", "monthly_fixed_costs", "weekly_sales", "stock_value", "prep_budget"):
            assert secret not in first_msg[agent], f"{agent} saw {secret}"
    assert "planner_draft" in first_msg["critic"]


def test_each_agent_is_offered_only_its_tools():
    _, client = run(happy_scripts())
    offered = {}
    for agent, kw in client.responses.requests:
        offered[agent] = {t["name"] for t in kw["tools"]}
    from backend.agents import TOOLSETS
    for agent, tools in offered.items():
        assert tools == set(TOOLSETS[agent])


def test_tool_outside_toolset_is_refused():
    scripts = happy_scripts(risk_analyst=[call("compute_cash_buffer")] + analyst_script())
    result, _ = run(scripts)
    assert result["status"] == "completed"
    refused = [e for e in result["events"] if e["type"] == "tool_result" and e["tool"] == "compute_cash_buffer"
               and e["agent"] == "risk_analyst"]
    assert refused and "not available" in refused[0]["result"]["error"]


# ---------------------------------------------------------------- limits

def _assert_stopped(result, limit):
    assert result["status"] == "stopped_by_limit"
    assert result["stopped_by"]["limit"] == limit
    assert "Stopped by limit" in result["message"]
    assert any(e["type"] == "limit_hit" and e["limit"] == limit for e in result["events"])


def test_run_token_budget(monkeypatch):
    monkeypatch.setattr(config, "RUN_TOKEN_BUDGET", 2500)
    result, _ = run(happy_scripts())
    _assert_stopped(result, "run_token_budget")


def test_risk_analyst_runs_at_most_once():
    scripts = happy_scripts(manager=[call("run_risk_analyst"), call("run_risk_analyst")])
    result, _ = run(scripts)
    _assert_stopped(result, "max_agent_runs")
    assert result["stopped_by"]["agent"] == "risk_analyst"


def test_planner_and_critic_allow_one_revision_only():
    scripts = happy_scripts(
        manager=[call("run_risk_analyst"), call("run_planner"), call("run_critic"),
                 call("run_planner", revision_notes=["fix cash"]), call("run_critic"),
                 call("run_planner", revision_notes=["again"])],
        planner=planner_script() * 3, critic=critic_script("revise") * 2)
    result, _ = run(scripts)
    _assert_stopped(result, "max_agent_runs")
    assert result["agent_runs"]["planner"] == 3 and result["agent_runs"]["critic"] == 2


def test_max_tool_calls(monkeypatch):
    monkeypatch.setitem(config.MAX_TOOL_CALLS, "planner", 2)
    result, _ = run(happy_scripts())
    _assert_stopped(result, "max_tool_calls")


def test_max_output_tokens():
    result, _ = run(happy_scripts(), status="incomplete")
    _assert_stopped(result, "max_output_tokens")


def test_search_cap_refuses_extra_calls_but_run_continues():
    searches = [call("score_exposure")] + [call("search_documents", query=f"q{i}") for i in range(5)]
    scripts = happy_scripts(risk_analyst=[searches, analyst_script()[1]])
    result, _ = run(scripts)
    assert result["status"] == "completed"
    assert any(e["type"] == "limit_hit" and e["action"] == "refused" for e in result["events"])


# ---------------------------------------------------------------- final verification

def test_failed_plan_gets_one_fix():
    bad = GOOD_PLAN + "Compra sacos por S/ 77.\n"
    scripts = happy_scripts(manager=[call("run_risk_analyst"), call("run_planner"), call("run_critic"),
                                     manager_final(bad), manager_final(GOOD_PLAN)])
    result, client = run(scripts)
    assert result["status"] == "completed"
    assert result["verification"]["fix_attempted"]
    fix_request = [kw for agent, kw in client.responses.requests if agent == "manager"][-1]["input"]
    assert any("verify_draft" in str(m.get("content", "")) for m in fix_request if isinstance(m, dict))


def test_plan_still_failing_shows_visible_warning():
    bad = GOOD_PLAN + "Compra sacos por S/ 77.\n"
    scripts = happy_scripts(manager=[call("run_risk_analyst"), call("run_planner"), call("run_critic"),
                                     manager_final(bad), manager_final(bad)])
    result, _ = run(scripts)
    assert result["status"] == "completed_with_warning"
    assert result["plan"]["pen"].startswith("> ⚠️") and result["plan"]["usd"].startswith("> ⚠️")
    assert result["warning"] and not result["verification"]["ok"]


# ---------------------------------------------------------------- other paths

def test_invalid_profile_makes_no_model_calls():
    client = FakeClient({})
    result = run_plan({**PROFILE, "district": "Lima"}, today=TODAY, client=client)
    assert result["status"] == "invalid_profile" and client.responses.requests == []


def test_non_json_answer_gets_one_reminder():
    scripts = happy_scripts(risk_analyst=[analyst_script()[0], final("Here is my analysis!"), analyst_script()[1]])
    result, _ = run(scripts)
    assert result["status"] == "completed"


def test_missing_critic_is_reported_as_open_issue():
    scripts = happy_scripts(manager=[call("run_risk_analyst"), call("run_planner"), manager_final()])
    result, _ = run(scripts)
    assert "The critic never ran." in result["open_issues"]


def test_manager_is_told_the_real_district_level():
    _, client = run(happy_scripts())
    first = next(kw["input"][0]["content"] for agent, kw in client.responses.requests if agent == "manager")
    assert '"hazard_level": "high"' in first and '"unverified": false' in first


def test_manager_is_told_when_district_is_unverified(unverified_district):
    client = FakeClient(happy_scripts())
    run_plan({**PROFILE, "district": unverified_district}, language="es", today=TODAY, client=client)
    first = next(kw["input"][0]["content"] for agent, kw in client.responses.requests if agent == "manager")
    assert '"hazard_level": "UNVERIFIED"' in first and '"unverified": true' in first


def test_false_unverified_claim_triggers_the_fix_step():
    bad = GOOD_PLAN.replace("Tu riesgo es alto.", "Tu riesgo es alto. No hay historia distrital verificada.")
    scripts = happy_scripts(manager=[call("run_risk_analyst"), call("run_planner"), call("run_critic"),
                                     manager_final(bad), manager_final(GOOD_PLAN)])
    result, _ = run(scripts)
    assert result["status"] == "completed" and result["verification"]["fix_attempted"]
    first_check = next(e for e in result["events"] if e["type"] == "final_check")
    assert "false_unverified_claim" in first_check["issues"]


def test_wrong_risk_level_triggers_the_fix_step():
    bad = GOOD_PLAN.replace("Tu riesgo es alto.", "Tu riesgo es medio.")  # the gauge says high
    scripts = happy_scripts(manager=[call("run_risk_analyst"), call("run_planner"), call("run_critic"),
                                     manager_final(bad), manager_final(GOOD_PLAN)])
    result, _ = run(scripts)
    assert result["status"] == "completed" and result["verification"]["fix_attempted"]
    first_check = next(e for e in result["events"] if e["type"] == "final_check")
    assert first_check["issues"] == ["risk_level_mismatch"]


def test_manager_is_told_the_shops_risk_level():
    _, client = run(happy_scripts())
    first = next(kw["input"][0]["content"] for agent, kw in client.responses.requests if agent == "manager")
    assert '"risk_level": "high"' in first


def test_critic_cannot_apply_owner_plan_rules_to_the_planner_draft():
    _, client = run(happy_scripts())
    critic_tools = next(kw["tools"] for agent, kw in client.responses.requests if agent == "critic")
    verify = next(t for t in critic_tools if t["name"] == "verify_draft")
    assert "final_plan" not in verify["parameters"]["properties"]
    manager_tools = next(kw["tools"] for agent, kw in client.responses.requests if agent == "manager")
    assert "final_plan" in next(t for t in manager_tools if t["name"] == "verify_draft")["parameters"]["properties"]


def test_manager_self_checks_are_capped_but_run_continues():
    checks = [call("verify_draft", draft=GOOD_PLAN, final_plan=True) for _ in range(4)]
    scripts = happy_scripts(manager=[call("run_risk_analyst"), call("run_planner"), call("run_critic"),
                                     *checks, manager_final()])
    result, _ = run(scripts)
    assert result["status"] == "completed"
    refused = [e for e in result["events"] if e["type"] == "limit_hit" and e["agent"] == "manager"]
    assert len(refused) == 1 and refused[0]["action"] == "refused"
