"""Live risk preview for the intake wizard: code tools only (validate_profile + score_exposure).

It never calls the model, so it costs 0 tokens. The owner may have answered only some questions,
so missing fields are filled with neutral placeholders just to run the tools, and only errors and
warnings about fields the owner actually answered are returned (each tagged with its wizard step).
"""

from backend.tools import score_exposure, validate_profile
from backend.tools.profile import ShopProfile

# The answers score_exposure needs before it can give a risk level.
EXPOSURE_FIELDS = ("district", "near_water", "flooded_before", "floor_level", "higher_storage")

# Placeholders used only to run the code tools; never shown and never saved.
PLACEHOLDERS = {
    "business_type": "-", "district": "-", "near_water": "unknown", "flooded_before": "unknown",
    "floor_level": "ground", "higher_storage": "none", "tenure": "rented", "stock_value": 0,
    "share_stock_below_1m": 0, "perishables": False, "cash_on_hand": 0, "monthly_fixed_costs": 0,
    "weekly_sales": 0, "workers": 1, "suppliers": [], "days_of_stock": 0, "prep_budget": 0, "already_have": [],
}

# Wizard step of each field (same groups as the form).
STEP_OF = {
    **dict.fromkeys(("business_type", "district", "near_water", "flooded_before", "floor_level",
                     "higher_storage", "tenure", "workers"), "business"),
    **dict.fromkeys(("stock_value", "share_stock_below_1m", "perishables", "days_of_stock"), "stock"),
    **dict.fromkeys(("cash_on_hand", "monthly_fixed_costs", "weekly_sales"), "money"),
    "suppliers": "suppliers",
    **dict.fromkeys(("prep_budget", "already_have"), "prep"),
}

# validate_profile's warnings (by their first words), the fields each depends on, and where to show it:
# a warning is returned only when every field it depends on was answered.
WARNING_FIELDS = [
    ("District data for", ("district",), "business"),
    ("Ignoring unknown checklist items", ("already_have",), "prep"),
    ("Prep budget is larger than cash on hand", ("prep_budget", "cash_on_hand"), "prep"),
    ("Ground-floor shop with no higher storage and no prep budget", ("floor_level", "higher_storage", "prep_budget"), "prep"),
    ("Share of stock below 1 m is set but stock value is 0", ("share_stock_below_1m", "stock_value"), "stock"),
    ("Monthly sales look lower than monthly fixed costs", ("monthly_fixed_costs", "weekly_sales"), "money"),
    ("Some flood questions were answered 'unknown'", ("near_water", "flooded_before"), "business"),
    ("The shop flooded before although its district is not rated high", ("flooded_before", "district"), "business"),
    ("No suppliers listed", ("suppliers",), "suppliers"),
]


def _answered(partial: dict) -> set[str]:
    return {k for k, v in partial.items() if k in ShopProfile.model_fields and v is not None and v != ""}


def _flood_answers_partial(partial: dict, answered: set[str]) -> bool:
    """The 'unknown' warning needs only one of the two flood questions answered 'unknown'."""
    return any(f in answered and partial[f] == "unknown" for f in ("near_water", "flooded_before"))


def preview_profile(partial: dict) -> dict:
    answered = _answered(partial)
    profile = {**PLACEHOLDERS, **{k: partial[k] for k in answered}}
    check = validate_profile(profile)

    errors = []
    for e in check["errors"]:
        field = e.split(":", 1)[0].split(".", 1)[0]
        if field in answered:
            errors.append({"field": field, "step": STEP_OF.get(field), "text": e})

    warnings = []
    for w in check["warnings"]:
        rule = next((r for r in WARNING_FIELDS if w.startswith(r[0])), None)
        if rule is None:
            continue
        prefix, fields, step = rule
        ok = _flood_answers_partial(partial, answered) if prefix.startswith("Some flood") else set(fields) <= answered
        if ok:
            warnings.append({"fields": list(fields), "step": step, "text": w})

    bad = {e["field"] for e in errors}
    missing = [f for f in EXPOSURE_FIELDS if f not in answered]
    result = {"ready": not missing and not (bad & set(EXPOSURE_FIELDS)), "missing": missing,
              "errors": errors, "warnings": warnings, "model_calls": 0, "tokens": 0}
    if result["ready"]:
        # An invalid answer elsewhere (e.g. a share above 100%) must not block the gauge.
        score = score_exposure({**profile, **{f: PLACEHOLDERS[f] for f in bad}})
        result.update(risk_level=score["risk_level"], district_hazard_level=score["district_hazard_level"])
        if {"stock_value", "share_stock_below_1m"} <= answered and not ({"stock_value", "share_stock_below_1m"} & bad):
            result["stock_at_risk"] = score["facts"]["stock_at_risk"]
    return result
