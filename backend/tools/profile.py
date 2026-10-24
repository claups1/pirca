"""Shop intake profile and the validate_profile tool."""

from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from backend.tools import data_store

YesNoUnknown = Literal["yes", "no", "unknown"]


class Supplier(BaseModel):
    product: str = Field(min_length=1)
    city: str = Field(min_length=1)
    perishable: bool | None = None  # None: inferred from the product name (pan, leche, fruta…)


class ShopProfile(BaseModel):
    """One shop's answers to the Pirca intake form. Money is in soles."""

    business_type: str = Field(min_length=1)
    district: str = Field(min_length=1)
    near_water: YesNoUnknown  # near a river, drain or ravine (quebrada)
    flooded_before: YesNoUnknown  # flooded in 2017 or 2023
    floor_level: Literal["ground", "raised", "upper"]
    higher_storage: Literal["second_floor", "mezzanine", "none"]
    tenure: Literal["owned", "rented"]
    stock_value: float = Field(ge=0)
    share_stock_below_1m: float = Field(ge=0, le=1)
    perishables: bool
    cash_on_hand: float = Field(ge=0)
    monthly_fixed_costs: float = Field(ge=0)
    weekly_sales: float = Field(ge=0)
    workers: int = Field(ge=1, le=500)  # including the owner
    suppliers: list[Supplier] = Field(default_factory=list, max_length=3)
    days_of_stock: float = Field(ge=0, le=365)
    prep_budget: float = Field(ge=0)
    already_have: list[str] = Field(default_factory=list)  # CAT IDs from the checklist


def parse_profile(profile: dict | ShopProfile) -> ShopProfile:
    return profile if isinstance(profile, ShopProfile) else ShopProfile.model_validate(profile)


def district_level(p: ShopProfile) -> str:
    """Flood hazard level from districts.csv; unknown districts count as UNVERIFIED."""
    row = data_store.find_district(p.district)
    return row["flood_hazard_level"] if row else "UNVERIFIED"


def district_hist_ids(p: ShopProfile) -> list[str]:
    row = data_store.find_district(p.district)
    if not row:
        return []
    return [i for i in (row["flood_hist_ids"] + ";" + row["other_hist_ids"]).split(";") if i]


def validate_profile(profile: dict) -> dict:
    """Check required fields and ranges, then warn about answers that don't add up."""
    try:
        p = parse_profile(profile)
    except ValidationError as e:
        errors = [f"{'.'.join(str(x) for x in err['loc'])}: {err['msg']}" for err in e.errors()]
        return {"tool": "validate_profile", "valid": False, "errors": errors, "warnings": [],
                "facts": {"error_count": len(errors)}, "sources": []}

    errors, warnings, sources = [], [], []
    row = data_store.find_district(p.district)
    if row is None:
        known = ", ".join(r["district"] for r in data_store.districts().values())
        errors.append(f"district: '{p.district}' is not in Pirca's data. Known districts: {known}")
    else:
        sources += district_hist_ids(p)
        if row["flood_hazard_level"] == "UNVERIFIED":
            warnings.append(f"District data for {row['district']} is UNVERIFIED: Pirca found no sourced "
                            "district-level flood history, so its hazard level is a placeholder. "
                            "Treat the exposure result with caution.")

    known_ids = {a["id"] for a in data_store.action_catalog()}
    unknown_have = [i for i in p.already_have if i not in known_ids]
    if unknown_have:
        warnings.append(f"Ignoring unknown checklist items: {', '.join(unknown_have)}")

    if p.prep_budget > p.cash_on_hand:
        warnings.append("Prep budget is larger than cash on hand; the plan may need financing or a smaller budget.")
    if p.floor_level == "ground" and p.higher_storage == "none" and p.prep_budget == 0:
        warnings.append("Ground-floor shop with no higher storage and no prep budget: "
                        "only zero-cost actions can be planned.")
    if p.share_stock_below_1m > 0 and p.stock_value == 0:
        warnings.append("Share of stock below 1 m is set but stock value is 0.")
    if p.monthly_fixed_costs > 0 and p.weekly_sales * 52 / 12 < p.monthly_fixed_costs:
        warnings.append("Monthly sales look lower than monthly fixed costs; please double-check both numbers.")
    if p.near_water == "unknown" or p.flooded_before == "unknown":
        warnings.append("Some flood questions were answered 'unknown'; Pirca scores them as partial risk.")
    if p.flooded_before == "yes" and row and row["flood_hazard_level"] != "high":
        warnings.append("The shop flooded before although its district is not rated high; the shop's own history is used.")
    if not p.suppliers:
        warnings.append("No suppliers listed; the supplier buffer cannot be computed.")

    return {"tool": "validate_profile", "valid": not errors, "errors": errors, "warnings": warnings,
            "facts": {"error_count": len(errors), "warning_count": len(warnings)},
            "sources": sorted(set(sources)), "profile": p.model_dump()}
