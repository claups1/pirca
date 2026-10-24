"""Offline checks that the agent prompts only reference real tools, fact keys and source IDs."""

import re
from datetime import date

import pytest

from backend import config
from backend.agents import AGENT_TOOLS, AGENTS, TOOLSETS
from backend.agents.prompts import load_prompt
from backend.tools import SCENARIOS, TOOLS, run_scenario, verify_draft
from backend.tools.data_store import SOURCE_ID_PATTERN, known_source_ids
from backend.tools.drafting import PLACEHOLDER

PROMPT_FILES = ["shared_rules", *AGENTS]
KNOWN_TOOLS = set(TOOLS) | set(AGENT_TOOLS)
CALLED = re.compile(r"\b([a-z][a-z0-9_]*)\(\)")
TOOL_LIKE = re.compile(r"\b(?:run|compute|get|score|validate|optimize|search|verify|fill)_[a-z0-9_]+\b")

PROFILE = dict(
    business_type="bodega", district="Castilla", near_water="yes", flooded_before="yes",
    floor_level="ground", higher_storage="none", tenure="rented", stock_value=20000,
    share_stock_below_1m=0.5, perishables=True, cash_on_hand=3000, monthly_fixed_costs=4000,
    weekly_sales=7000, workers=2, days_of_stock=7, prep_budget=500, already_have=[],
    suppliers=[{"product": "a", "city": "Chiclayo"}, {"product": "b", "city": "Piura"},
               {"product": "c", "city": "Sullana"}],
)


def read(name: str) -> str:
    return (config.PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def all_fact_keys() -> set[str]:
    """Every fact key the tools can produce for a shop with three suppliers."""
    keys = set()
    for name in ("validate_profile", "score_exposure", "compute_stock_move", "compute_cash_buffer",
                 "compute_supplier_buffer", "get_action_catalog", "optimize_budget"):
        keys |= set(TOOLS[name](PROFILE)["facts"])
    for s in SCENARIOS:
        keys |= set(run_scenario(PROFILE, s, today=date(2026, 10, 24))["facts"])
    keys |= set(TOOLS["search_documents"]("lluvia")["facts"])
    keys |= set(TOOLS["get_historical_impacts"]()["facts"])
    keys |= set(verify_draft("x", {})["facts"])
    keys |= set(TOOLS["fill_placeholders"]("x", {})["facts"])
    return keys


@pytest.mark.parametrize("name", PROMPT_FILES)
def test_prompt_file_exists_and_is_not_empty(name):
    assert len(read(name)) > 200


@pytest.mark.parametrize("name", PROMPT_FILES)
def test_every_tool_name_mentioned_exists(name):
    text = read(name)
    mentioned = set(CALLED.findall(text)) | set(TOOL_LIKE.findall(text))
    unknown = mentioned - KNOWN_TOOLS
    assert not unknown, f"{name}.md mentions tools that don't exist: {sorted(unknown)}"


def test_toolsets_only_contain_real_tools():
    for agent, tools in TOOLSETS.items():
        assert set(tools) <= KNOWN_TOOLS, agent


@pytest.mark.parametrize("agent", AGENTS)
def test_agent_prompt_calls_exactly_its_toolset(agent):
    called = set(CALLED.findall(read(agent)))
    assert called == set(TOOLSETS[agent]), f"{agent}: calls {sorted(called)}, toolset {sorted(TOOLSETS[agent])}"


def test_shared_rules_call_no_tools():
    assert not CALLED.findall(read("shared_rules"))


@pytest.mark.parametrize("name", PROMPT_FILES)
def test_placeholders_are_real_fact_keys(name):
    keys = all_fact_keys()
    used = {m.group(1) for m in PLACEHOLDER.finditer(read(name))} - {"fact_key"}
    unknown = used - keys
    assert not unknown, f"{name}.md uses unknown fact keys: {sorted(unknown)}"


@pytest.mark.parametrize("name", PROMPT_FILES)
def test_source_ids_in_prompts_exist(name):
    ids = set(SOURCE_ID_PATTERN.findall(read(name)))
    assert ids <= known_source_ids(), f"{name}.md cites unknown IDs: {sorted(ids - known_source_ids())}"


def test_scenarios_named_in_critic_exist_and_required_ones_present():
    text = read("critic")
    named = {s for s in re.findall(r"`([a-z_]+)`", text) if s in SCENARIOS or s.endswith(("_early", "_cut", "_week"))}
    assert named <= set(SCENARIOS)
    assert "rains_one_month_early" in text and "main_bridge_cut" in text


@pytest.mark.parametrize("agent", AGENTS)
def test_system_prompt_is_static_and_starts_with_shared_rules(agent):
    prompt = load_prompt(agent)
    assert prompt.startswith(read("shared_rules").rstrip())
    assert read(agent).strip() in prompt
    assert "{{" not in prompt  # no template slots; per-run data goes in the user message


def test_manager_lists_all_sections_in_both_languages():
    text = read("manager")
    es = ["Tu riesgo", "Qué hacer y cuándo", "Tu mercadería", "Tu caja de emergencia", "Tus proveedores",
          "Compras dentro de tu presupuesto", "Lo que revisamos"]
    en = ["Your risk", "What to do and when", "Your stock", "Your emergency cash", "Your suppliers",
          "Purchases within your budget", "What we checked"]
    for i, (s, e) in enumerate(zip(es, en), 1):
        assert f"## {i}. {s}" in text and f"## {i}. {e}" in text


def test_shared_rules_cover_required_topics():
    text = read("shared_rules").lower()
    for phrase in ("missing_facts", "suspicious_content", "evacuat", "enfen", "senamhi", "indeci",
                   "municipal", "illustrative estimate", "unverified", "only the json object"):
        assert phrase in text, phrase


def test_unknown_agent_rejected():
    with pytest.raises(ValueError):
        load_prompt("intern")
