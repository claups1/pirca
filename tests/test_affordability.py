"""Offline tests: the app never recommends spending money the owner doesn't have,
and perishable products are never stocked up."""

import pytest

from backend.tools import compute_supplier_buffer, optimize_budget, verify_draft
from backend.tools.calculations import is_perishable
from backend.tools.drafting import check_affordability, recommended_spending
from backend.tools.profile import Supplier

BASE = dict(
    business_type="bodega", district="Castilla", near_water="yes", flooded_before="yes",
    floor_level="ground", higher_storage="none", tenure="rented", stock_value=20000,
    share_stock_below_1m=0.5, perishables=True, cash_on_hand=3000, monthly_fixed_costs=4000,
    weekly_sales=7000, workers=2, days_of_stock=7, prep_budget=500, already_have=[],
    suppliers=[{"product": "abarrotes", "city": "Chiclayo"}, {"product": "bebidas", "city": "Piura"},
               {"product": "pan", "city": "Sullana"}],
)


def profile(**kw):
    return {**BASE, **kw}


# ---------------------------------------------------------------- perishables

@pytest.mark.parametrize("product,expected", [
    ("pan", True), ("panes y pasteles", True), ("leche", True), ("lácteos", True), ("frutas", True),
    ("huevos", True), ("bread", True), ("abarrotes", False), ("bebidas", False), ("arroz", False),
    ("pañales", False),  # not "pan"
])
def test_perishable_is_inferred_from_the_product(product, expected):
    assert is_perishable(Supplier(product=product, city="Piura")) is expected


def test_owner_mark_overrides_inference():
    assert is_perishable(Supplier(product="pan", city="Piura", perishable=False)) is False
    assert is_perishable(Supplier(product="arroz", city="Piura", perishable=True)) is True


def test_perishable_supplier_gets_zero_days_and_small_deliveries():
    r = compute_supplier_buffer(profile(cash_on_hand=50000))
    bread = next(s for s in r["suppliers"] if s["product"] == "pan")
    assert bread["perishable"] and bread["extra_days"] == 0 and bread["advice"] == "small_frequent_deliveries"
    assert r["facts"]["supplier_3_extra_days"] == 0
    assert r["facts"]["supplier_1_extra_days"] > 0  # non-perishables still get a stock-up


# ---------------------------------------------------------------- stock-up affordability

def test_no_stock_up_when_emergency_fund_is_not_complete():
    r = compute_supplier_buffer(profile())  # cash 3000 < emergency fund needed
    assert r["stock_up_status"] == "complete_emergency_fund_first"
    assert r["facts"]["extra_stock_value"] == 0 and r["facts"]["extra_days_to_buy"] == 0
    assert r["facts"]["extra_stock_needed"] > 0  # the need is still reported


def test_partial_stock_up_is_capped_at_money_left():
    r = compute_supplier_buffer(profile(cash_on_hand=6000))
    f = r["facts"]
    assert r["stock_up_status"] == "partly_affordable"
    assert 0 < f["extra_stock_value"] <= f["stock_up_money_available"] < f["extra_stock_needed"]


def test_full_stock_up_when_affordable():
    r = compute_supplier_buffer(profile(cash_on_hand=50000))
    assert r["stock_up_status"] == "affordable"
    assert r["facts"]["extra_stock_value"] == r["facts"]["extra_stock_needed"]


def test_prep_budget_is_capped_at_cash_on_hand():
    r = optimize_budget(profile(cash_on_hand=200, prep_budget=5000))
    assert r["facts"]["budget"] == 200 and r["facts"]["total_cost"] <= 200


@pytest.mark.parametrize("cash,budget", [(0, 500), (300, 500), (3000, 500), (6000, 2000), (50000, 5000),
                                         (4500, 4500)])
def test_tools_never_recommend_more_than_cash(cash, budget):
    p = profile(cash_on_hand=cash, prep_budget=budget)
    spent = optimize_budget(p)["facts"]["total_cost"] + compute_supplier_buffer(p)["facts"]["extra_stock_value"]
    assert spent <= cash


# ---------------------------------------------------------------- the code check

FACTS = {"cash_on_hand": 3000, "cat_02_cost": 77.0, "cat_10_cost": 36.0, "cat_04_cost": 500.0,
         "extra_stock_value": 14000.0, "supplier_3_extra_days": 0.0, "supplier_1_extra_days": 14.0}


def test_spending_within_cash_passes():
    draft = "- Sacos* ({cat_02_cost}) [CAT-02]\n- Seguro ({cat_10_cost}) [CAT-10]"
    assert recommended_spending(draft, FACTS)["total"] == 113
    assert check_affordability(draft, FACTS) == []


def test_spending_over_cash_fails():
    draft = "- Sacos* ({cat_02_cost}) [CAT-02]\n- Compra {extra_stock_value} de abarrotes."
    issues = check_affordability(draft, FACTS)
    assert [i["type"] for i in issues] == ["spending_exceeds_cash"]
    assert "14,077" in issues[0]["text"]


def test_spending_over_cash_fails_verify_draft_for_final_plans():
    draft = "## 5. Tus proveedores\nCompra {extra_stock_value} de abarrotes."
    r = verify_draft(draft, FACTS, final_plan=True)
    assert "spending_exceeds_cash" in [i["type"] for i in r["issues"]]


def test_each_purchase_counts_once():
    draft = "{cat_04_cost} ... {cat_04_cost} ... {cat_04_cost}"
    assert recommended_spending(draft, FACTS)["total"] == 500


def test_zero_stock_up_must_not_be_shown():
    facts = {**FACTS, "extra_stock_value": 0.0}
    issues = check_affordability("Compra {extra_stock_value}. Pan: {supplier_3_extra_days}.", facts)
    assert [i["type"] for i in issues] == ["zero_stock_up_mentioned", "zero_stock_up_mentioned"]


def test_spending_without_cash_fact_is_flagged():
    issues = check_affordability("{cat_02_cost}", {"cat_02_cost": 77.0})
    assert [i["type"] for i in issues] == ["affordability_unknown"]
