"""Exposure, stock, cash, supplier and scenario tools. All money is in soles."""

from datetime import date

from backend.tools import assumptions as A
from backend.tools import data_store
from backend.tools.profile import ShopProfile, district_hist_ids, district_level, parse_profile

WEEKS_PER_MONTH = 52 / 12

# Supplier routes with a documented cut or damage in Piura's history.
SOUTH = ("high", ["HIST-1998-07", "HIST-2017-21"],
         "Panamericana Piura–Lambayeque was cut at Mórrope for weeks in 1998; 15 bridges were destroyed in 2017")
ROUTES = {
    "tumbes": ("high", ["HIST-1998-06"], "Panamericana Tumbes–Piura was cut for three months in 1998"),
    "chiclayo": SOUTH, "lambayeque": SOUTH, "trujillo": SOUTH, "lima": SOUTH,
    "talara": ("high", ["HIST-1998-09"], "The Paita–Talara road was cut in 10 sections in 1998"),
    "chulucanas": ("high", ["HIST-1998-07"], "The Motupe–Chulucanas–Piura detour was cut by a bridge collapse in 1998"),
    "morropon": ("high", ["HIST-1998-08"], "The Piura–Morropón road was damaged and bridges collapsed in 1998"),
    "sullana": ("medium", ["HIST-1998-08"], "The Piura–La Arena–Sullana road was damaged in 1998"),
}
LEVEL_TO_ROUTE_RISK = {"high": "high", "medium": "medium", "UNVERIFIED": "unknown"}


def _money(x: float) -> float:
    return round(float(x), 2)


def _envelope(tool: str, facts: dict, sources, assumption_names=(), **extra) -> dict:
    srcs = set(sources) | set(A.sources_of(*assumption_names))
    return {"tool": tool, "facts": facts, "sources": sorted(srcs),
            "assumptions": A.describe(*assumption_names), **extra}


def score_exposure(profile: dict | ShopProfile) -> dict:
    """Exposure score (0-100), risk level and the value of stock within 1 m of the floor."""
    p = parse_profile(profile)
    w = A.value("exposure_weights")
    level = district_level(p)
    parts = {
        "district_points": w["district"][level],
        "near_water_points": w["near_water"][p.near_water],
        "flooded_before_points": w["flooded_before"][p.flooded_before],
        "floor_level_points": w["floor_level"][p.floor_level],
        "higher_storage_points": w["higher_storage"][p.higher_storage],
    }
    score = sum(parts.values())
    cut = A.value("risk_level_cutoffs")
    risk = "high" if score >= cut["high"] else "medium" if score >= cut["medium"] else "low"
    stock_at_risk = p.stock_value * p.share_stock_below_1m
    facts = {"exposure_score": score, **parts, "stock_value": _money(p.stock_value),
             "stock_at_risk": _money(stock_at_risk)}
    return _envelope("score_exposure", facts, district_hist_ids(p),
                     ("exposure_weights", "risk_level_cutoffs", "flood_depth_threshold_m"),
                     risk_level=risk, district_hazard_level=level)


def compute_stock_move(profile: dict | ShopProfile) -> dict:
    """How much stock to lift above 1 m and where it should go."""
    p = parse_profile(profile)
    stock_to_move = p.stock_value * p.share_stock_below_1m
    if p.higher_storage == "second_floor":
        destination, actions = "second floor", ["CAT-05"]
    elif p.higher_storage == "mezzanine":
        destination, actions = "mezzanine", ["CAT-05"]
    else:
        destination = "shelves above 1 m, sealed containers, or a safe space outside the flood zone"
        actions = ["CAT-01", "CAT-03", "CAT-05"]
    notes = []
    if p.perishables:
        notes.append("Sell down perishables before the rains instead of moving them.")
    facts = {"stock_to_move": _money(stock_to_move),
             "stock_staying": _money(p.stock_value - stock_to_move),
             "share_to_move_pct": round(p.share_stock_below_1m * 100, 1)}
    return _envelope("compute_stock_move", facts, actions, ("flood_depth_threshold_m",),
                     destination=destination, related_actions=actions, notes=notes)


def _weeks_closed(p: ShopProfile, override: float | None = None) -> float:
    if override is not None:
        return override
    table = A.value("weeks_closed")
    return table["high"] if p.flooded_before == "yes" else table[district_level(p)]


def compute_cash_buffer(profile: dict | ShopProfile, weeks_closed: float | None = None) -> dict:
    """Cash needed to keep paying fixed costs while closed, and the gap versus cash on hand."""
    p = parse_profile(profile)
    weeks = _weeks_closed(p, weeks_closed)
    weekly_fixed = p.monthly_fixed_costs / WEEKS_PER_MONTH
    buffer_needed = weekly_fixed * weeks
    facts = {"weeks_closed": weeks,
             "weekly_fixed_costs": _money(weekly_fixed),
             "buffer_needed": _money(buffer_needed),
             "cash_on_hand": _money(p.cash_on_hand),
             "cash_gap": _money(max(0.0, buffer_needed - p.cash_on_hand)),
             "lost_sales": _money(p.weekly_sales * weeks)}
    names = ("long_closure_weeks",) if weeks_closed is not None else ("weeks_closed",)
    return _envelope("compute_cash_buffer", facts, ["CAT-06"], names)


def _route_risk(city: str) -> tuple[str, list[str], str]:
    key = data_store.normalize(city)
    if key in ROUTES:
        return ROUTES[key]
    row = data_store.find_district(city)
    if row:
        ids = [i for i in row["flood_hist_ids"].split(";") if i]
        return (LEVEL_TO_ROUTE_RISK[row["flood_hazard_level"]], ids,
                f"{row['district']} district flood hazard is {row['flood_hazard_level']}")
    return ("unknown", [], "No road-cut history for this city in Pirca's data")


def compute_supplier_buffer(profile: dict | ShopProfile, force_risk: str | None = None) -> dict:
    """Road-cut risk per supplier city and extra days of stock to buy before the rains."""
    p = parse_profile(profile)
    targets = A.value("target_stock_days")
    daily_sales = p.weekly_sales / 7
    suppliers, sources = [], ["CAT-08"]
    for i, s in enumerate(p.suppliers, 1):
        risk, ids, basis = _route_risk(s.city)
        if force_risk:
            risk, basis = force_risk, f"Scenario: route forced to {force_risk} risk"
        extra = max(0.0, targets[risk] - p.days_of_stock)
        suppliers.append({"supplier": i, "product": s.product, "city": s.city, "road_cut_risk": risk,
                          "basis": basis, "sources": ids, "target_days": targets[risk], "extra_days": extra})
        sources += ids
    extra_days = max((s["extra_days"] for s in suppliers), default=0.0)
    facts = {"supplier_count": len(suppliers), "days_of_stock": p.days_of_stock,
             "extra_days_to_buy": extra_days,
             "extra_stock_value": _money(daily_sales * extra_days),
             "high_risk_suppliers": sum(s["road_cut_risk"] == "high" for s in suppliers)}
    for s in suppliers:
        facts[f"supplier_{s['supplier']}_extra_days"] = s["extra_days"]
    notes = ["extra_stock_value is valued at sales prices (weekly sales / 7 per day)."]
    if p.perishables:
        notes.append("Stock up only on non-perishables; buy perishables in smaller amounts more often.")
    return _envelope("compute_supplier_buffer", facts, sources, ("target_stock_days",),
                     suppliers=suppliers, notes=notes)


SCENARIOS = ("rains_one_month_early", "long_closure", "main_bridge_cut", "power_cut_week", "worker_sick_dengue")


def _compare(baseline: dict, scenario: dict) -> dict:
    facts = {}
    for k, v in scenario.items():
        facts[k] = v
        if k in baseline and isinstance(v, (int, float)):
            facts[f"baseline_{k}"] = baseline[k]
            facts[f"delta_{k}"] = round(v - baseline[k], 2)
    return facts


def _weeks_until(start: date, today: date) -> float:
    return round(max(0, (start - today).days) / 7, 1)


def run_scenario(profile: dict | ShopProfile, scenario: str, today: date | None = None) -> dict:
    """Recompute the plan's numbers under a stress scenario."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario '{scenario}'. Choose one of: {', '.join(SCENARIOS)}")
    p = parse_profile(profile)
    today = today or date.today()
    base_cash = compute_cash_buffer(p)

    if scenario == "rains_one_month_early":
        start = A.value("rain_start")
        early = start.replace(month=start.month - 1) if start.month > 1 else start.replace(year=start.year - 1, month=12)
        gap = base_cash["facts"]["cash_gap"]

        def plan(weeks):
            return {"weeks_until_rains": weeks, "weekly_saving_needed": _money(gap / weeks if weeks else gap)}
        facts = _compare(plan(_weeks_until(start, today)), plan(_weeks_until(early, today)))
        return _envelope("run_scenario", facts, base_cash["sources"], ("rain_start", "weeks_closed"),
                         scenario=scenario, rain_start_baseline=start.isoformat(), rain_start_scenario=early.isoformat())

    if scenario == "long_closure":
        long_cash = compute_cash_buffer(p, weeks_closed=A.value("long_closure_weeks"))
        facts = _compare(base_cash["facts"], long_cash["facts"])
        return _envelope("run_scenario", facts, long_cash["sources"], ("weeks_closed", "long_closure_weeks"),
                         scenario=scenario)

    if scenario == "main_bridge_cut":
        base = compute_supplier_buffer(p)
        cut = compute_supplier_buffer(p, force_risk="high")
        facts = _compare(base["facts"], cut["facts"])
        return _envelope("run_scenario", facts, base["sources"] + ["HIST-2017-21"], ("target_stock_days",),
                         scenario=scenario, suppliers=cut["suppliers"])

    if scenario == "power_cut_week":
        days = A.value("power_cut_days")
        facts = {"power_cut_days": days, "sales_at_risk": _money(p.weekly_sales * days / 7),
                 "perishables": int(p.perishables)}
        notes = ["sales_at_risk is an upper bound: a full week of sales if the shop cannot sell without power."]
        if p.perishables:
            notes.append("Perishable stock is also at risk; its value is not in the intake form, so ask the owner.")
        return _envelope("run_scenario", facts, ["CAT-15", "CAT-12"], ("power_cut_days",),
                         scenario=scenario, notes=notes)

    # worker_sick_dengue
    weeks = A.value("dengue_sick_weeks")
    share = 1 / p.workers
    facts = {"workers": p.workers, "sick_weeks": weeks, "capacity_lost_pct": round(share * 100, 1),
             "sales_at_risk": _money(p.weekly_sales * share * weeks)}
    notes = ["With one worker the shop closes while they are sick."] if p.workers == 1 else []
    return _envelope("run_scenario", facts, ["CAT-09", "HIST-2017-25"], ("dengue_sick_weeks",),
                     scenario=scenario, notes=notes)
