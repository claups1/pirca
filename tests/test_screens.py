"""Mosquito screens (CAT-09) are priced from the owner's window and door count (offline, no model calls)."""

import json

import pytest

from backend import config
from backend.tools import data_store
from backend.tools.actions import optimize_budget, screen_cost
from backend.tools.drafting import fill_placeholders, recommended_spending

PROFILE = json.loads((config.PLANS_DIR / "examples" / "sample_shop_castilla.json").read_text(encoding="utf-8"))
PRICES = next(a for a in data_store.action_catalog() if a["id"] == "CAT-09")["unit_prices"]


def shop(windows, doors, **extra):
    return {**PROFILE, "windows": windows, "doors": doors, **extra}


def test_catalog_has_window_and_door_screen_prices():
    assert PRICES == {"window": 5.90, "door": 10.90}  # Promart, 2026-10-24 (re-checked 2026-10-25)


@pytest.mark.parametrize("windows, doors, expected", [
    (3, 1, 3 * 5.90 + 1 * 10.90),   # S/ 28.60
    (1, 0, 5.90),
    (0, 2, 21.80),
    (2, None, 11.80),               # the empty answer counts as 0 once the other one is given
    (None, 1, 10.90),
    (0, 0, 0.0),
])
def test_screen_cost_is_windows_times_window_price_plus_doors_times_door_price(windows, doors, expected):
    r = screen_cost(shop(windows, doors))
    assert r["known"] and r["cost"] == pytest.approx(expected)


def test_no_count_means_unit_price_and_no_cost():
    r = screen_cost(shop(None, None))
    assert r == {"known": False, "windows": None, "doors": None, "window_price": 5.90, "door_price": 10.90, "cost": None}


def test_known_count_puts_the_screen_total_in_the_budget():
    r = optimize_budget(shop(3, 1))
    f = r["facts"]
    assert f["cat_09_cost"] == 28.60 and "cat_09_unit_price" not in f
    assert (f["screen_windows"], f["screen_doors"]) == (3, 1)
    assert f["total_cost"] == pytest.approx(sum(v for k, v in f.items() if k.endswith("_cost") and k.startswith("cat_")))


def test_no_count_leaves_screens_out_of_the_budget_total():
    known, unknown = optimize_budget(shop(1, 0)), optimize_budget(shop(None, None))
    f = unknown["facts"]
    assert "cat_09_cost" not in f and f["cat_09_unit_price"] == 5.90
    cat09 = next(s for s in unknown["selected"] if s["id"] == "CAT-09")
    assert cat09["cost_fact_key"] is None and cat09["unit_price_fact_key"] == "cat_09_unit_price"
    # The 5.90 is not spent: the total is the known-count plan's total without the one screen
    assert f["total_cost"] == pytest.approx(known["facts"]["total_cost"] - 5.90)
    # and a plan showing the price per window does not count it as money to spend.
    assert recommended_spending("{cat_09_unit_price}", f)["total"] == 0


def test_unit_price_is_written_per_window_and_total_for_screens():
    es = fill_placeholders("{cat_09_unit_price}", {"cat_09_unit_price": 5.90}, language="es")["text"]
    en = fill_placeholders("{cat_09_cost}", {"cat_09_cost": 28.60}, language="en")["text"]
    assert es == "S/ 5.90 por ventana" and en == "S/ 28.60 for window and door screens"


def test_owner_who_already_has_screens_gets_no_screen_facts():
    f = optimize_budget(shop(3, 1, already_have=[*PROFILE["already_have"], "CAT-09"]))["facts"]
    assert not {"cat_09_cost", "cat_09_unit_price", "screen_windows"} & set(f)


@pytest.mark.parametrize("bad", [{"windows": -1}, {"doors": 21}, {"windows": 1.5}])
def test_counts_are_validated(bad):
    from backend.tools.profile import validate_profile
    assert not validate_profile({**PROFILE, **bad})["valid"]
