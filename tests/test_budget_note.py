"""Offline tests for the plan's unspent-budget note (optimize_budget re-run on the plan's form; no model)."""

import copy

from backend.api import plans
from backend.tools import data_store

COSTS = {a["id"]: a["cost_min_pen"] for a in data_store.action_catalog()}


def test_cast26_left_money_because_the_next_action_does_not_fit():
    record = plans.load_plan("PIU-CAST26")
    note = plans.budget_note(record)
    assert note["reason"] == "nothing_fits" and note["money_left"] == record["facts"]["money_left"]
    assert note["cheapest_left"] == COSTS["CAT-01"] > note["money_left"]  # raised shelves, left out of the plan
    assert note["cash_gap"] == record["facts"]["cash_gap"] > 0


def test_plan_with_every_useful_action_says_so():
    assert plans.budget_note(plans.load_plan("PIU-FARMES"))["reason"] == "nothing_left"


def test_no_note_when_nothing_is_left_or_the_data_changed():
    record = plans.load_plan("PIU-CAST26")
    spent = copy.deepcopy(record)
    spent["facts"]["money_left"] = 0
    assert plans.budget_note(spent) is None
    changed = copy.deepcopy(record)
    changed["facts"]["total_cost"] += 10  # no longer what optimize_budget computes for this form
    assert plans.budget_note(changed) is None


def test_plan_status_includes_the_note():
    assert plans.plan_status("PIU-CAST26")["result"]["budget_note"]["reason"] == "nothing_fits"
