"""Offline tests for the 2023 historical rows (Cyclone Yaku rains, 2023 El Niño costero alert, 2023 dengue)."""

import csv
import re
from datetime import date

import pytest

from backend import config
from backend.build_districts import build
from backend.tools import (
    compute_cash_buffer,
    compute_supplier_buffer,
    get_historical_impacts,
    run_scenario,
    score_exposure,
    verify_draft,
)
from backend.tools import assumptions as A
from backend.tools import data_store
from backend.tools.calculations import ROUTES

DISTRICT_NAMES = {d["district"] for d in data_store.districts().values()}


def rows_2023() -> list[dict]:
    return [r for r in data_store.historical_impacts() if r["event"] == "2023"]


def profile(**kw):
    p = dict(business_type="bodega", district="Castilla", near_water="yes", flooded_before="yes",
             floor_level="ground", higher_storage="none", tenure="rented", stock_value=20000,
             share_stock_below_1m=0.5, perishables=True, cash_on_hand=3000, monthly_fixed_costs=4000,
             weekly_sales=7000, workers=2, days_of_stock=7, prep_budget=500, already_have=[],
             suppliers=[{"product": "abarrotes", "city": "Chiclayo"}, {"product": "arroz", "city": "Paita"}])
    p.update(kw)
    return p


# ---------------------------------------------------------------- the rows themselves

def test_2023_rows_are_numbered_and_complete():
    rows = rows_2023()
    assert len(rows) >= 40
    assert [r["id"] for r in rows] == [f"HIST-2023-{i:02d}" for i in range(1, len(rows) + 1)]
    for r in rows:
        assert r["confidence"] in {"verified", "sourced"}, r["id"]
        assert r["source_url"].startswith("https://"), r["id"]
        assert r["quote"].strip() and r["fact"].strip() and r["value"].strip(), r["id"]
        assert r["raw_file"].startswith("data/raw/historical_2023/"), r["id"]


def test_2023_rows_cover_the_four_requested_topics():
    topics = {r["topic"] for r in rows_2023()}
    assert {"enfen_alert", "people_affected", "roads_bridges", "dengue", "closure_duration", "business_losses",
            "flooding"} <= topics


def test_2023_district_names_match_pirca_districts():
    for r in rows_2023():
        for d in r["district"].split(";"):
            assert d in DISTRICT_NAMES or "region" in d or "province" in d, (r["id"], d)


def test_enfen_2023_alert_dates():
    by_id = {r["id"]: r for r in rows_2023()}
    assert by_id["HIST-2023-01"]["value"] == "2023-03-16" and by_id["HIST-2023-02"]["value"] == "2024-04-05"


def test_raw_files_exist_when_present_locally():
    # data/raw/ is not committed; on a fresh clone this test only checks paths.
    if not (config.DATA_DIR / "raw" / "historical_2023").exists():
        pytest.skip("raw files not downloaded on this machine")
    missing = [r["id"] for r in rows_2023() if not (config.PROJECT_ROOT / r["raw_file"]).exists()]
    assert missing == []


# ---------------------------------------------------------------- districts

def test_districts_csv_matches_the_rule():
    with open(config.DATA_DIR / "districts.csv", encoding="utf-8") as f:
        current = list(csv.DictReader(f))
    assert build(list(data_store.historical_impacts())) == current


def test_paita_and_sechura_now_have_2023_evidence():
    paita, sechura = data_store.find_district("Paita"), data_store.find_district("Sechura")
    assert paita["flood_hazard_level"] == "high" and "HIST-2023-27" in paita["flood_hist_ids"]
    assert sechura["flood_hazard_level"] == "medium" and "HIST-2023-29" in sechura["other_hist_ids"]
    assert not [d for d in data_store.districts().values() if d["flood_hazard_level"] == "UNVERIFIED"]


def test_every_district_has_2023_ids():
    for d in data_store.districts().values():
        assert "HIST-2023-" in d["flood_hist_ids"] + d["other_hist_ids"], d["district"]


# ---------------------------------------------------------------- tools use the 2023 rows

def test_get_historical_impacts_filters_2023():
    r = get_historical_impacts(event="2023")
    assert r["facts"]["result_count"] == len(rows_2023())
    paita = get_historical_impacts(district="Paita", event="2023")
    assert {"HIST-2023-26", "HIST-2023-27", "HIST-2023-45"} <= set(paita["sources"])
    dengue = get_historical_impacts(topic="dengue", event="2023", district="Castilla")
    assert [row["value"] for row in dengue["results"]] == ["11192"]


def test_score_exposure_cites_2023_rows():
    assert any(s.startswith("HIST-2023-") for s in score_exposure(profile())["sources"])


def test_paita_shop_no_longer_scored_as_unverified():
    r = score_exposure(profile(district="Paita"))
    assert r["district_hazard_level"] == "high" and r["facts"]["district_points"] == 30


def test_cash_buffer_closure_basis_cites_2023():
    assert {"HIST-2023-30", "HIST-2023-31"} <= set(compute_cash_buffer(profile())["sources"])


def test_dengue_scenario_cites_2023():
    r = run_scenario(profile(), "worker_sick_dengue", today=date(2026, 10, 24))
    assert {"HIST-2023-36", "HIST-2023-37"} <= set(r["sources"])


def test_supplier_routes_use_2023():
    r = compute_supplier_buffer(profile())
    routes = {s["city"]: s for s in r["suppliers"]}
    assert "HIST-2023-29" in routes["Chiclayo"]["sources"]
    assert routes["Paita"]["road_cut_risk"] == "high" and routes["Paita"]["sources"] == ["HIST-2023-30"]


def test_every_cited_history_id_exists_with_the_right_topic():
    rows = {r["id"]: r for r in data_store.historical_impacts()}
    cited = {i for a in A.ASSUMPTIONS.values() for i in a["sources"] if i.startswith("HIST-")}
    cited |= {i for _, ids, _ in ROUTES.values() for i in ids}
    assert cited <= set(rows)
    assert rows["HIST-2023-30"]["topic"] == rows["HIST-2023-31"]["topic"] == "closure_duration"
    assert rows["HIST-2023-36"]["topic"] == rows["HIST-2023-37"]["topic"] == "dengue"
    assert rows["HIST-2023-29"]["district"] == "Sechura"


def test_2023_ids_are_valid_citations():
    assert verify_draft("En 2023 hubo zonas inundadas en Paita [HIST-2023-27].", {})["ok"]
    assert not verify_draft("[HIST-2023-99]", {})["ok"]
