"""Offline tests for the deterministic Pirca tools (no API calls)."""

import json
import math
from datetime import date

import pytest

from backend.tools import (
    SCENARIOS,
    TOOLS,
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
from backend.tools import data_store

TODAY = date(2026, 10, 24)


def make_profile(**overrides) -> dict:
    """A ground-floor bodega in Castilla that flooded in 2017."""
    profile = dict(
        business_type="bodega", district="Castilla", near_water="yes", flooded_before="yes",
        floor_level="ground", higher_storage="none", tenure="rented",
        stock_value=20000, share_stock_below_1m=0.5, perishables=True,
        cash_on_hand=3000, monthly_fixed_costs=4000, weekly_sales=7000, workers=2,
        suppliers=[{"product": "abarrotes", "city": "Chiclayo"},
                   {"product": "bebidas", "city": "Piura"},
                   {"product": "pan", "city": "Lugar Desconocido"}],
        days_of_stock=7, prep_budget=500, already_have=["CAT-13"],
    )
    profile.update(overrides)
    return profile


def low_risk_profile() -> dict:
    return make_profile(district="Bellavista", near_water="no", flooded_before="no", floor_level="upper",
                        higher_storage="second_floor", perishables=False)


# ---- every tool: JSON-ready with facts and sources ----

@pytest.mark.parametrize("name", ["validate_profile", "score_exposure", "compute_stock_move", "compute_cash_buffer",
                                  "compute_supplier_buffer", "get_action_catalog", "optimize_budget"])
def test_profile_tools_return_json_with_facts_and_sources(name):
    result = TOOLS[name](make_profile())
    json.dumps(result)  # must be serializable for the agents
    assert isinstance(result["facts"], dict) and result["facts"]
    assert all(isinstance(v, (int, float)) for v in result["facts"].values())
    assert isinstance(result["sources"], list)
    assert set(result["sources"]) <= data_store.known_source_ids()


# ---- validate_profile ----

def test_validate_accepts_good_profile():
    r = validate_profile(make_profile())
    assert r["valid"] and r["errors"] == []


def test_validate_reports_missing_and_out_of_range_fields():
    bad = make_profile(share_stock_below_1m=1.5, workers=0)
    del bad["district"]
    r = validate_profile(bad)
    assert not r["valid"]
    text = " ".join(r["errors"])
    assert "district" in text and "share_stock_below_1m" in text and "workers" in text


def test_validate_rejects_unknown_district():
    r = validate_profile(make_profile(district="Lima"))
    assert not r["valid"] and "not in Pirca's data" in r["errors"][0]


@pytest.mark.parametrize("district", ["Paita", "Sechura"])
def test_unverified_district_produces_warning(district):
    r = validate_profile(make_profile(district=district))
    assert r["valid"]
    assert any("UNVERIFIED" in w for w in r["warnings"])


def test_validate_warns_when_answers_dont_add_up():
    r = validate_profile(make_profile(prep_budget=5000, cash_on_hand=1000))
    assert any("larger than cash" in w for w in r["warnings"])
    r = validate_profile(make_profile(prep_budget=0))
    assert any("no higher storage and no prep budget" in w for w in r["warnings"])


def test_validate_matches_district_without_accents():
    assert validate_profile(make_profile(district="Veintiseis de Octubre"))["valid"]


# ---- score_exposure / compute_stock_move ----

def test_score_exposure_high_risk_shop():
    r = score_exposure(make_profile())
    assert r["risk_level"] == "high"
    assert r["facts"]["exposure_score"] == 100
    assert r["facts"]["stock_at_risk"] == 10000
    assert "HIST-2017-30" in r["sources"]


def test_score_exposure_low_risk_shop():
    r = score_exposure(low_risk_profile())
    assert r["risk_level"] == "low"
    assert r["facts"]["exposure_score"] < 30


def test_stock_move_destination_depends_on_storage():
    none = compute_stock_move(make_profile())
    assert none["facts"]["stock_to_move"] == 10000
    assert none["facts"]["stock_staying"] == 10000
    assert "shelves" in none["destination"] and "CAT-01" in none["related_actions"]
    upstairs = compute_stock_move(make_profile(higher_storage="second_floor"))
    assert upstairs["destination"] == "second floor"


# ---- compute_cash_buffer ----

def test_cash_buffer_numbers():
    f = compute_cash_buffer(make_profile())["facts"]
    assert f["weeks_closed"] == 4  # flooded before -> high
    assert f["weekly_fixed_costs"] == pytest.approx(4000 * 12 / 52, abs=0.01)
    assert f["buffer_needed"] == pytest.approx(f["weekly_fixed_costs"] * 4, abs=0.02)
    assert f["cash_gap"] == pytest.approx(f["buffer_needed"] - 3000, abs=0.02)


def test_cash_buffer_no_gap_when_cash_covers_it():
    assert compute_cash_buffer(make_profile(cash_on_hand=50000))["facts"]["cash_gap"] == 0


def test_cash_buffer_weeks_come_from_historical_ids():
    r = compute_cash_buffer(make_profile())
    assert {"HIST-1998-07", "HIST-1998-10"} <= set(r["sources"])


# ---- compute_supplier_buffer ----

def test_supplier_buffer_risk_per_city():
    r = compute_supplier_buffer(make_profile())
    risks = {s["city"]: s["road_cut_risk"] for s in r["suppliers"]}
    assert risks == {"Chiclayo": "high", "Piura": "high", "Lugar Desconocido": "unknown"}
    assert r["facts"]["extra_days_to_buy"] == 14  # 21 target - 7 on hand
    assert r["facts"]["extra_stock_value"] == 14000  # 7000/7 per day * 14
    assert "HIST-1998-07" in r["sources"]


def test_supplier_buffer_no_extra_days_when_well_stocked():
    assert compute_supplier_buffer(make_profile(days_of_stock=30))["facts"]["extra_days_to_buy"] == 0


# ---- get_action_catalog ----

def test_catalog_excludes_what_owner_has():
    r = get_action_catalog(make_profile())
    ids = {a["id"] for a in r["actions"]}
    assert "CAT-13" not in ids
    assert any(e["id"] == "CAT-13" and "already has" in e["reason"] for e in r["excluded"])


def test_catalog_drops_flood_only_actions_for_low_risk_shop():
    r = get_action_catalog(low_risk_profile())
    assert "flood" not in r["hazards"]
    assert "CAT-04" not in {a["id"] for a in r["actions"]}  # door barrier addresses flood only


def test_illustrative_actions_stay_flagged_in_catalog():
    actions = {a["id"]: a for a in get_action_catalog(make_profile(already_have=[]))["actions"]}
    assert actions["CAT-03"]["illustrative_estimate"]  # protects factor is illustrative
    assert actions["CAT-05"]["cost_is_illustrative"]
    assert not actions["CAT-10"]["illustrative_estimate"]  # fully sourced
    for a in actions.values():
        source = next(x for x in data_store.action_catalog() if x["id"] == a["id"])
        expected = "illustrative" in source["cost_status"] or "illustrative" in source["protects_status"]
        assert a["illustrative_estimate"] == expected


def test_rented_shop_gets_landlord_note():
    actions = {a["id"]: a for a in get_action_catalog(make_profile())["actions"]}
    assert "landlord" in actions["CAT-11"]["note"]


# ---- optimize_budget ----

def test_optimizer_stays_within_budget_and_includes_zero_cost():
    r = optimize_budget(make_profile(), budget=500)
    f = r["facts"]
    assert f["total_cost"] <= 500
    assert f["money_left"] == pytest.approx(500 - f["total_cost"], abs=0.01)
    selected = {s["id"] for s in r["selected"]}
    assert {"CAT-05", "CAT-14"} <= selected  # zero-cost actions


def test_optimizer_zero_budget_selects_only_free_actions():
    r = optimize_budget(make_profile(), budget=0)
    assert all(s["cost_used"] == 0 for s in r["selected"])
    assert r["facts"]["total_cost"] == 0


def test_optimizer_excluded_actions_have_reasons():
    r = optimize_budget(make_profile(), budget=100)
    assert r["excluded"] and all(e["reason"] for e in r["excluded"])
    assert any(e["id"] == "CAT-06" and "depends on the shop" in e["reason"] for e in r["excluded"])


def test_optimizer_marks_illustrative_selected_actions():
    r = optimize_budget(make_profile(), budget=5000)
    flagged = {s["id"] for s in r["selected"] if s["illustrative_estimate"]}
    assert set(r["illustrative_selected"]) == flagged
    assert "CAT-03" in flagged
    assert r["facts"]["illustrative_selected_count"] == len(flagged)


@pytest.mark.parametrize("budget", [100, 300, 600])
def test_optimizer_matches_brute_force(budget):
    from itertools import combinations
    profile = make_profile(already_have=[])
    # With an unlimited budget every costed action is selected, giving the full candidate list.
    everything = optimize_budget(profile, budget=10**5)["selected"]
    costed = [a for a in everything if a["cost_used"] > 0]
    free = sum(a["expected_benefit"] for a in everything if a["cost_used"] == 0)
    best = max(sum(a["expected_benefit"] for a in combo)
               for k in range(len(costed) + 1) for combo in combinations(costed, k)
               if sum(math.ceil(a["cost_used"]) for a in combo) <= budget)
    r = optimize_budget(profile, budget=budget)
    assert r["facts"]["expected_benefit"] == pytest.approx(best + free, abs=0.01)


# ---- search_documents / get_historical_impacts ----

def test_search_returns_snippets_with_source_ids():
    r = search_documents("Catacaos inundación")
    assert r["results"]
    assert all(res["sources"] for res in r["results"])
    assert any(s.startswith("HIST-") for s in r["sources"])


def test_search_finds_enfen_and_exchange_rate():
    assert any(s.startswith("ENFEN-") for s in search_documents("Niño costero magnitud extraordinaria")["sources"])
    assert "BCRP-USDPEN" in search_documents("tipo de cambio interbancario")["sources"]


def test_search_never_reads_raw_folder():
    assert all("raw" not in p.relative_to(data_store.config.DATA_DIR).parts for p in data_store.data_files())


def test_historical_impacts_filters():
    r = get_historical_impacts(district="Catacaos")
    assert "HIST-2017-07" in r["sources"]
    assert all("Catacaos" in row["district"] for row in r["results"])
    dengue = get_historical_impacts(topic="dengue", event="2017")
    assert dengue["results"] and all(row["topic"] == "dengue" for row in dengue["results"])


# ---- run_scenario ----

def scenario_facts(profile, scenario, today=TODAY) -> dict:
    """Scenario facts with the '<scenario>__' prefix removed."""
    facts = run_scenario(profile, scenario, today=today)["facts"]
    return {k.removeprefix(f"{scenario}__"): v for k, v in facts.items()}


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_every_scenario_runs(scenario):
    r = run_scenario(make_profile(), scenario, today=TODAY)
    json.dumps(r)
    assert r["scenario"] == scenario and r["facts"]
    assert all(k.startswith(f"{scenario}__") for k in r["facts"])  # never collides with baseline facts


def test_long_closure_uses_three_months():
    f = scenario_facts(make_profile(), "long_closure")
    assert f["weeks_closed"] == 13 and f["baseline_weeks_closed"] == 4
    assert f["cash_gap"] > f["baseline_cash_gap"]


def test_rains_early_leaves_less_time():
    f = scenario_facts(make_profile(), "rains_one_month_early", today=date(2026, 9, 1))
    assert f["weeks_until_rains"] < f["baseline_weeks_until_rains"]
    assert f["weekly_saving_needed"] > f["baseline_weekly_saving_needed"]


def test_bridge_cut_raises_all_routes():
    r = run_scenario(make_profile(), "main_bridge_cut", today=TODAY)
    assert all(s["road_cut_risk"] == "high" for s in r["suppliers"])
    f = r["facts"]
    assert f["main_bridge_cut__supplier_3_extra_days"] > f["main_bridge_cut__baseline_supplier_3_extra_days"]


def test_dengue_with_one_worker_loses_whole_week():
    f = scenario_facts(make_profile(workers=1), "worker_sick_dengue")
    assert f["sales_at_risk"] == 7000


def test_unknown_scenario_raises():
    with pytest.raises(ValueError):
        run_scenario(make_profile(), "meteor")


# ---- verify_draft ----

def test_verify_clean_draft_passes():
    draft = ("Tu stock en riesgo es {stock_at_risk}. En 2017 el agua llegó al mercado de Castilla (HIST-2017-30). "
             "ENFEN mantiene la alerta (ENFEN-2026-18) para el 16 de octubre y la región Niño 1+2.\n"
             "1. Eleva la mercadería (CAT-01)")
    r = verify_draft(draft, {"stock_at_risk": 10000})
    assert r["ok"], r["issues"]


def test_verify_flags_raw_numbers_unknown_keys_and_ids():
    r = verify_draft("Necesitas S/ 500 por 3 semanas, {made_up}, ver HIST-2017-99.", {})
    types = [i["type"] for i in r["issues"]]
    assert types.count("raw_number") == 2
    assert "unknown_fact_key" in types and "unknown_source_id" in types


def test_verify_allows_numbered_markdown_headings():
    r = verify_draft("## 1. Tu riesgo\nTexto.\n### 7) Lo que revisamos\n", {})
    assert r["ok"], r["issues"]


def test_verify_allows_years_months_and_id_digits():
    r = verify_draft("En 1997-98 y el 12 de marzo de 2017 (HIST-1998-06, CAT-10) y March 12.", {})
    assert r["ok"], r["issues"]


@pytest.mark.parametrize("text", ["Evacúe su tienda ahora.", "You must evacuate.", "Pirca predicts heavy rain.",
                                  "Nuestro pronóstico: lloverá en noviembre."])
def test_verify_flags_forbidden_content(text):
    r = verify_draft(text, {})
    assert any(i["type"] == "forbidden_content" for i in r["issues"])


# ---- fill_placeholders ----

def test_fill_formats_soles_and_usd():
    rate = data_store.exchange_rate()["pen_per_usd"]
    r = fill_placeholders("Stock {stock_at_risk} = {stock_at_risk|usd}", {"stock_at_risk": 10000})
    assert r["text"] == f"Stock S/ 10,000 = ${10000 / rate:,.0f}"
    assert "BCRP-USDPEN" in r["sources"]


def test_fill_handles_non_money_and_missing_keys():
    r = fill_placeholders("{weeks_closed} semanas, {share_to_move_pct}, {delta_cash_gap}, {nope}",
                          {"weeks_closed": 4, "share_to_move_pct": 50.0, "delta_cash_gap": -1500})
    assert r["text"] == "4 semanas, 50%, -S/ 1,500, {nope}"
    assert r["missing"] == ["nope"]


def test_fill_formats_prefixed_scenario_money():
    r = fill_placeholders("{long_closure__cash_gap} vs {long_closure__baseline_cash_gap}",
                          {"long_closure__cash_gap": 9000, "long_closure__baseline_cash_gap": 692.31})
    assert r["text"] == "S/ 9,000 vs S/ 692"


def test_fill_whole_draft_in_usd():
    r = fill_placeholders("{cash_gap}", {"cash_gap": 3447}, currency="usd")
    assert r["text"] == "$1,000"
