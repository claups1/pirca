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
