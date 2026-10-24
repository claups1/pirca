"""Action catalog and budget optimizer tools."""

import math

from backend.tools import assumptions as A
from backend.tools import data_store
from backend.tools.calculations import compute_cash_buffer, score_exposure
from backend.tools.profile import ShopProfile, parse_profile

LANDLORD_ACTIONS = {"CAT-04", "CAT-11", "CAT-12"}


def _is_illustrative(status: str) -> bool:
    return "illustrative" in status


def active_hazards(p: ShopProfile) -> list[str]:
    """Hazards that apply to this shop. Rain, dengue, road cuts and cash strain apply region-wide."""
    hazards = {"heavy_rain", "dengue", "road_closure", "supply_shortage", "cash_flow"}
    low_flood = (score_exposure(p)["risk_level"] == "low"
                 and p.near_water == "no" and p.flooded_before == "no")
    if not low_flood:
        hazards.add("flood")
    if p.perishables:
        hazards.add("power_outage")
    return sorted(hazards)


def _action_view(a: dict, p: ShopProfile) -> dict:
    view = {k: a[k] for k in ("id", "action", "name_es", "name_en", "hazards", "cost_min_pen", "cost_max_pen",
                              "cost_unit", "cost_unit_es", "cost_unit_en",
                              "cost_status", "protects", "protects_status",
                              "cost_source_url", "protects_source_url", "recommendation_source_url")}
    view["cost_is_illustrative"] = _is_illustrative(a["cost_status"])
    view["protects_is_illustrative"] = _is_illustrative(a["protects_status"])
    view["illustrative_estimate"] = view["cost_is_illustrative"] or view["protects_is_illustrative"]
    if p.tenure == "rented" and a["id"] in LANDLORD_ACTIONS:
        view["note"] = "Rented premises: agree this change with the landlord first."
    return view


def get_action_catalog(profile: dict | ShopProfile, hazards: list[str] | None = None) -> dict:
    """Catalog actions matching the shop's hazards, minus what the owner already has."""
    p = parse_profile(profile)
    hazards = hazards or active_hazards(p)
    actions, excluded = [], []
    for a in data_store.action_catalog():
        if a["id"] in p.already_have:
            excluded.append({"id": a["id"], "action": a["action"], "reason": "owner already has it"})
        elif not set(a["hazards"]) & set(hazards):
            excluded.append({"id": a["id"], "action": a["action"],
                             "reason": f"addresses {', '.join(a['hazards'])}, not this shop's hazards"})
        else:
            actions.append(_action_view(a, p))
    facts = {"matching_actions": len(actions), "excluded_actions": len(excluded),
             "illustrative_actions": sum(a["illustrative_estimate"] for a in actions)}
    return {"tool": "get_action_catalog", "facts": facts, "sources": [a["id"] for a in actions],
            "hazards": hazards, "actions": actions, "excluded": excluded}


def _loss_bases(p: ShopProfile) -> dict[str, float]:
    stock = score_exposure(p)["facts"]["stock_at_risk"]
    buffer = compute_cash_buffer(p)["facts"]["buffer_needed"]
    week = p.weekly_sales
    return {"flood": stock, "heavy_rain": stock,
            "road_closure": buffer, "cash_flow": buffer, "supply_shortage": buffer,
            "dengue": week / p.workers, "power_outage": week if p.perishables else 0.0, "theft": 0.0}


def cost_key(action_id: str) -> str:
    """Fact key for an action's cost: CAT-02 -> cat_02_cost."""
    return action_id.lower().replace("-", "_") + "_cost"


def _knapsack(items: list[dict], budget: int) -> set[str]:
    """0/1 knapsack on whole soles; returns the IDs that maximize total benefit."""
    n = len(items)
    best = [0.0] * (budget + 1)
    keep = [bytearray(budget + 1) for _ in range(n)]
    for i, it in enumerate(items):
        c = it["cost_int"]
        for b in range(budget, c - 1, -1):
            if best[b - c] + it["expected_benefit"] > best[b]:
                best[b] = best[b - c] + it["expected_benefit"]
                keep[i][b] = 1
    chosen, b = set(), budget
    for i in range(n - 1, -1, -1):
        if keep[i][b]:
            chosen.add(items[i]["id"])
            b -= items[i]["cost_int"]
    return chosen


def optimize_budget(profile: dict | ShopProfile, budget: float | None = None) -> dict:
    """Best set of catalog actions within the prep budget (zero-cost actions always included)."""
    p = parse_profile(profile)
    requested = p.prep_budget if budget is None else budget
    budget = min(requested, p.cash_on_hand)  # never plan to spend money the owner doesn't have
    catalog = get_action_catalog(p)
    bases = _loss_bases(p)

    selected, excluded, items = [], list(catalog["excluded"]), []
    for a in catalog["actions"]:
        cost = a["cost_min_pen"]
        benefit = round((a["protects"] or 0) * max(bases.get(h, 0.0) for h in a["hazards"]), 2)
        entry = {**a, "cost_used": cost, "expected_benefit": benefit}
        if cost is None:
            excluded.append({"id": a["id"], "action": a["action"], "name_es": a["name_es"], "name_en": a["name_en"],
                             "reason": "cost depends on the shop; sized by compute_cash_buffer / compute_supplier_buffer"})
        elif cost == 0:
            selected.append({**entry, "why": "zero cost, always included"})
        else:
            items.append({**entry, "cost_int": math.ceil(cost)})

    chosen = _knapsack(items, int(budget)) if items and budget >= 1 else set()
    spent = 0.0
    for it in items:
        it.pop("cost_int")
        if it["id"] in chosen:
            selected.append({**it, "why": "best value within the budget"})
            spent += it["cost_used"]
        else:
            reason = (f"costs S/ {it['cost_used']:,.2f}, more than the S/ {budget:,.2f} budget"
                      if it["cost_used"] > budget else "lower value per sol than the selected actions for this budget")
            excluded.append({"id": it["id"], "action": it["action"], "name_es": it["name_es"],
                             "name_en": it["name_en"], "reason": reason})

    notes = ["Costs use each action's lowest sourced price (cost_min_pen)."]
    if budget < requested:
        notes.append(f"The prep budget was capped at cash on hand (S/ {budget:,.2f}).")
    if any(s["id"] == "CAT-10" for s in selected):
        notes.append("CAT-10 at S/ 36/year is the minimum microcredit-linked micro-insurance premium; "
                     "a stand-alone SME multirriesgo policy costs up to S/ 1,944/year.")
    illustrative = [s["id"] for s in selected if s["illustrative_estimate"]]
    facts = {"budget": round(budget, 2), "total_cost": round(spent, 2), "money_left": round(budget - spent, 2),
             "selected_count": len(selected), "excluded_count": len(excluded),
             "expected_benefit": round(sum(s["expected_benefit"] for s in selected), 2),
             "illustrative_selected_count": len(illustrative)}
    # One cost fact per costed action, e.g. {cat_02_cost}, so the plan can show "Sacos de arena (S/ 77)".
    # Only selected purchases get a cost fact, so every {cat_NN_cost} in a plan is recommended spending.
    for it in selected:
        if it.get("cost_used"):
            facts[cost_key(it["id"])] = round(it["cost_used"], 2)
    for s in selected:
        s["cost_fact_key"] = cost_key(s["id"]) if s.get("cost_used") else None  # free actions have no cost fact
    return {"tool": "optimize_budget", "facts": facts, "sources": [s["id"] for s in selected],
            "assumptions": A.describe("action_benefit_model"),
            "selected": selected, "excluded": excluded, "illustrative_selected": illustrative,
            "notes": notes}
