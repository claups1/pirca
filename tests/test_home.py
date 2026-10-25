"""Offline tests for /api/home: every number and fact on the start screen comes from the data files."""

import csv
import json

from fastapi.testclient import TestClient

from backend import config
from backend.main import app


def read_csv(name):
    with open(config.DATA_DIR / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


HIST = {r["id"]: r for r in read_csv("historical_impacts.csv")}
DISTRICTS = {r["district"]: r for r in read_csv("districts.csv")}


def home():
    r = TestClient(app).get("/api/home")
    assert r.status_code == 200
    return r.json()


def test_every_district_has_a_dot_with_its_hazard_level():
    body = home()
    assert {d["name"]: d["hazard_level"] for d in body["districts"]} == \
        {name: r["flood_hazard_level"] for name, r in DISTRICTS.items()}


def test_district_facts_are_its_own_records_one_per_event_year():
    for d in home()["districts"]:
        row = DISTRICTS[d["name"]]
        own = set((row["flood_hist_ids"] + ";" + row["other_hist_ids"]).split(";")) - {""}
        events = [f["event"] for f in d["facts"]]
        assert len(events) == len(set(events)) and set(events) <= {"1997-98", "2017", "2023"}
        for f in d["facts"]:
            assert f["id"] in own and HIST[f["id"]]["event"] == f["event"]


def test_why_it_matters_numbers_match_the_csv():
    impacts = home()["impacts"]
    for key, hid in {"business_losses": "HIST-2023-32", "transport_cost": "HIST-2023-33", "dengue_cases": "HIST-2023-36"}.items():
        assert impacts[key]["id"] == hid
        assert (impacts[key]["value"], impacts[key]["unit"]) == (HIST[hid]["value"], HIST[hid]["unit"])


def test_timeline_covers_the_three_events_and_the_latest_enfen_communique():
    body = home()
    assert [t["event"] for t in body["timeline"]] == ["1997-98", "2017", "2023"]
    for t in body["timeline"]:
        assert t["value"] == HIST[t["id"]]["value"] and t["event"] == HIST[t["id"]]["event"]
    index = json.loads((config.DATA_DIR / "enfen" / "index.json").read_text(encoding="utf-8"))["communiques"]
    latest = max(index, key=lambda c: c["date"])
    assert body["enfen"]["id"] == latest["id"] and body["enfen"]["status"] == latest["status"]


def test_every_cited_id_has_source_details():
    body = home()
    cited = {f["id"] for d in body["districts"] for f in d["facts"]} | {i["id"] for i in body["impacts"].values()} \
        | {t["id"] for t in body["timeline"]} | {body["enfen"]["id"]}
    assert cited <= set(body["source_details"])
    for i in cited:
        assert body["source_details"][i]["url"].startswith("http")


# ---------------------------------------------------------------- province map

PROVINCES = {"Piura", "Sullana", "Paita", "Talara", "Sechura", "Morropón", "Ayabaca", "Huancabamba"}
ORDER = {"low": 1, "medium": 2, "high": 3}


def test_map_has_the_eight_provinces_of_piura_region():
    body = home()
    provinces = body["map"]["provinces"]
    assert {p["name"] for p in provinces} == PROVINCES and all(p["ubigeo"].startswith("20") for p in provinces)
    assert "pe-atlas" in body["map"]["source"] and "provinces" in body["map"]["source"]


def test_every_pirca_district_is_listed_in_exactly_one_province():
    listed = [d["name"] for p in home()["map"]["provinces"] for d in p["districts"]]
    assert sorted(listed) == sorted(DISTRICTS)
    for p in home()["map"]["provinces"]:
        for d in p["districts"]:
            assert DISTRICTS[d["name"]]["province"] == p["name"] and DISTRICTS[d["name"]]["flood_hazard_level"] == d["hazard_level"]


def test_province_flood_level_is_the_highest_among_its_districts():
    for p in home()["map"]["provinces"]:
        levels = [DISTRICTS[d["name"]]["flood_hazard_level"] for d in p["districts"]]
        levels = [lv for lv in levels if lv in ORDER]
        assert p["flood_level"] == (max(levels, key=ORDER.get) if levels else None)
    by = {p["name"]: p["flood_level"] for p in home()["map"]["provinces"]}
    assert by["Ayabaca"] is None and by["Huancabamba"] is None  # no Pirca data


def test_province_dengue_sums_only_the_districts_with_data():
    dengue = {r["district"]: int(r["value"]) for r in HIST.values() if r["event"] == "2023" and r["topic"] == "dengue" and r["unit"] == "cases"}
    for p in home()["map"]["provinces"]:
        names = [d["name"] for d in p["districts"] if d["name"] in dengue]
        if not names:
            assert p["dengue"] is None
            continue
        assert p["dengue"]["cases"] == sum(dengue[n] for n in names) and sorted(p["dengue"]["districts"]) == sorted(names)


def test_province_boundaries_are_inside_piura_region():
    for p in home()["map"]["provinces"]:
        for poly in p["coordinates"]:
            for ring in poly:
                assert len(ring) >= 4 and all(-81.5 < x < -79.0 and -6.5 < y < -3.9 for x, y in ring)


def test_dengue_2023_values_match_the_csv():
    dengue = home()["dengue"]
    rows = {r["district"]: r for r in HIST.values() if r["event"] == "2023" and r["topic"] == "dengue" and r["unit"] == "cases"}
    assert set(dengue) <= set(DISTRICTS) and len(dengue) == 15
    for name, v in dengue.items():
        assert HIST[v["id"]]["value"] == v["value"] and rows[name]["id"] == v["id"]
