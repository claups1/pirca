"""Model parameters used by the tools, each with its basis and status.

Status follows output/sources.md: "sourced" values come from the data files;
"illustrative estimate" values are Pirca's own placeholders and are reported
back to the agent so it never presents them as facts.
"""

from datetime import date

ASSUMPTIONS = {
    "flood_depth_threshold_m": dict(
        value=1.0, status="sourced",
        basis="Stock below 1 m is treated as reachable by floodwater; water reached 1.20 m in Castilla's market in 2017",
        sources=["HIST-2017-30"]),
    "exposure_weights": dict(
        value={"district": {"high": 30, "medium": 15, "UNVERIFIED": 15},
               "near_water": {"yes": 20, "unknown": 10, "no": 0},
               "flooded_before": {"yes": 25, "unknown": 10, "no": 0},
               "floor_level": {"ground": 15, "raised": 5, "upper": 0},
               "higher_storage": {"none": 10, "mezzanine": 3, "second_floor": 0}},
        status="illustrative estimate",
        basis="Points out of 100; weights are Pirca's judgment, not from a study", sources=[]),
    "risk_level_cutoffs": dict(
        value={"high": 60, "medium": 30}, status="illustrative estimate",
        basis="score >= 60 high, >= 30 medium, else low", sources=[]),
    "weeks_closed": dict(
        value={"high": 4, "medium": 2, "UNVERIFIED": 2}, status="illustrative estimate",
        basis="Anchored on 'several weeks' road cuts and water outages in 1998; a shop that flooded before uses the high value",
        sources=["HIST-1998-07", "HIST-1998-10"]),
    "long_closure_weeks": dict(
        value=13, status="sourced",
        basis="Panamericana Tumbes–Piura was cut for three months in 1998 (3 months ≈ 13 weeks)",
        sources=["HIST-1998-06"]),
    "target_stock_days": dict(
        value={"high": 21, "medium": 14, "unknown": 14, "low": 7}, status="illustrative estimate",
        basis="Days of stock to hold per supplier road-cut risk", sources=[]),
    "rain_start": dict(
        value=date(2026, 11, 1), status="sourced",
        basis="ENFEN expects above-normal rain and river flows on the north coast from November",
        sources=["ENFEN-2026-16", "ENFEN-2026-18"]),
    "dengue_sick_weeks": dict(
        value=1, status="illustrative estimate",
        basis="One sick worker is out for about a week; duration not in Pirca's data", sources=["HIST-2017-25"]),
    "power_cut_days": dict(
        value=7, status="illustrative estimate", basis="Scenario definition: one week without power", sources=[]),
    "action_benefit_model": dict(
        value="protects x loss basis (flood/rain: stock_at_risk; closure/cash/supply: buffer_needed; "
              "dengue: one worker-week of sales; power: one week of sales if perishables)",
        status="illustrative estimate",
        basis="Used only to rank actions inside the budget", sources=[]),
}


def value(name: str):
    return ASSUMPTIONS[name]["value"]


def describe(*names: str) -> list[dict]:
    """Assumption records for a tool's output (dates rendered as ISO strings)."""
    out = []
    for n in names:
        a = ASSUMPTIONS[n]
        v = a["value"].isoformat() if isinstance(a["value"], date) else a["value"]
        out.append({"name": n, "value": v, "status": a["status"], "basis": a["basis"], "sources": a["sources"]})
    return out


def sources_of(*names: str) -> list[str]:
    return [s for n in names for s in ASSUMPTIONS[n]["sources"]]
