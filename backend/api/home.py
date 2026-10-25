"""Data for the start screen: district map, "why it matters" numbers and the El Niño timeline.

Everything is read from data/districts.csv, data/historical_impacts.csv, data/enfen/index.json and
data/geo/piura_districts.geojson (built by backend/build_piura_geo.py); no number is typed here.
Only the choice of which rows to feature lives in this file.
"""

import json
from functools import lru_cache

from backend import config
from backend.tools import data_store
from backend.tools.source_info import describe_sources, latest_enfen

EVENTS = ("1997-98", "2017", "2023")

# "Why it matters": business losses from closures, transport cost rise, dengue cases (all 2023).
IMPACT_IDS = {"business_losses": "HIST-2023-32", "transport_cost": "HIST-2023-33", "dengue_cases": "HIST-2023-36"}

# One short fact per past event for the timeline.
TIMELINE_IDS = {"1997-98": "HIST-1998-01", "2017": "HIST-2017-01", "2023": "HIST-2023-09"}


# Boundary names that differ from Pirca's district names (INEI spelling; Talara city is Pariñas district).
BOUNDARY_ALIASES = {"PARIÑAS": "Talara", "TAMBO GRANDE": "Tambogrande"}


@lru_cache
def district_boundaries() -> dict:
    return json.loads((config.DATA_DIR / "geo" / "piura_districts.geojson").read_text(encoding="utf-8"))


def map_features() -> list[dict]:
    """Every Piura district boundary, with the Pirca district it matches (or None: no data in Pirca)."""
    out = []
    for f in district_boundaries()["features"]:
        name = f["properties"]["name"]
        row = data_store.find_district(BOUNDARY_ALIASES.get(name, name))
        out.append({"ubigeo": f["properties"]["ubigeo"], "name": name, "province": f["properties"]["province"],
                    "district": row["district"] if row else None, "coordinates": f["geometry"]["coordinates"]})
    return out


def dengue_2023(hist: dict[str, dict]) -> dict[str, dict]:
    """Dengue cases in 2023 per Pirca district, from the HIST-2023 dengue rows."""
    out = {}
    for r in hist.values():
        if r["event"] == "2023" and r["topic"] == "dengue" and r["unit"] == "cases":
            row = data_store.find_district(r["district"])
            if row:
                out[row["district"]] = {"id": r["id"], "value": r["value"]}
    return out


def _row_view(row: dict) -> dict:
    return {"id": row["id"], "event": row["event"], "topic": row["topic"], "value": row["value"], "unit": row["unit"]}


def district_facts(row: dict, hist: dict[str, dict]) -> list[dict]:
    """One cited fact per event year the district has, preferring its flood records."""
    ids = [i for i in (row["flood_hist_ids"] + ";" + row["other_hist_ids"]).split(";") if i]
    facts = []
    for event in EVENTS:
        pick = next((i for i in ids if i in hist and hist[i]["event"] == event), None)
        if pick:
            facts.append({"event": event, "id": pick, "topic": hist[pick]["topic"], "value": hist[pick]["value"],
                          "unit": hist[pick]["unit"]})
    return facts


def home_data() -> dict:
    hist = {r["id"]: r for r in data_store.historical_impacts()}
    districts = [{"name": r["district"], "province": r["province"], "hazard_level": r["flood_hazard_level"],
                  "facts": district_facts(r, hist)} for r in data_store.districts().values()]
    impacts = {key: _row_view(hist[i]) for key, i in IMPACT_IDS.items()}
    timeline = [_row_view(hist[i]) for i in TIMELINE_IDS.values()]
    enfen = latest_enfen()
    dengue = dengue_2023(hist)
    cited = [f["id"] for d in districts for f in d["facts"]] + list(IMPACT_IDS.values()) + list(TIMELINE_IDS.values())
    cited += [v["id"] for v in dengue.values()] + [enfen["id"]]
    geo = district_boundaries()
    return {"districts": districts, "impacts": impacts, "timeline": timeline, "enfen": enfen, "dengue": dengue,
            "map": {"features": map_features(), "source": geo["source"], "source_url": geo["source_url"]},
            "source_details": describe_sources(dict.fromkeys(cited))}
