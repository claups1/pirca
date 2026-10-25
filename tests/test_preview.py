"""Offline tests for /api/preview: the wizard's live risk gauge runs code tools only (0 tokens)."""

import json

import pytest
from fastapi.testclient import TestClient

from backend import config, llm
from backend.api import plans
from backend.main import app
from backend.tools import score_exposure

SAMPLE = json.loads((config.PLANS_DIR / "examples" / "sample_shop_castilla.json").read_text(encoding="utf-8"))
EXPOSURE = {k: SAMPLE[k] for k in ("district", "near_water", "flooded_before", "floor_level", "higher_storage")}


@pytest.fixture
def client(monkeypatch):
    def no_model(*a, **k):
        raise AssertionError("the preview must never call the model")
    monkeypatch.setattr(llm, "get_client", no_model)
    monkeypatch.setattr(plans, "make_client", no_model)
    return TestClient(app)


def preview(client, profile):
    r = client.post("/api/preview", json=profile)
    assert r.status_code == 200
    return r.json()


def test_full_profile_matches_score_exposure_and_costs_nothing(client):
    body = preview(client, SAMPLE)
    expected = score_exposure(SAMPLE)
    assert body["ready"] and body["risk_level"] == expected["risk_level"]
    assert body["district_hazard_level"] == expected["district_hazard_level"]
    assert body["stock_at_risk"] == expected["facts"]["stock_at_risk"]
    assert body["model_calls"] == 0 and body["tokens"] == 0
    assert "exposure_score" not in body  # the owner sees the level word only


def test_empty_answers_are_not_ready_and_list_what_is_missing(client):
    body = preview(client, {})
    assert not body["ready"] and "risk_level" not in body
    assert body["missing"] == ["district", "near_water", "flooded_before", "floor_level", "higher_storage"]
    assert body["errors"] == [] and body["warnings"] == []


def test_gauge_appears_once_the_five_exposure_answers_are_in(client):
    partial = {"district": SAMPLE["district"], "near_water": "yes", "flooded_before": "yes", "floor_level": "ground"}
    assert not preview(client, partial)["ready"]
    body = preview(client, {**partial, "higher_storage": "none"})
    assert body["ready"] and body["risk_level"] == "high"
    assert "stock_at_risk" not in body  # stock answers not given yet


def test_level_changes_as_answers_change(client):
    risky = preview(client, {**EXPOSURE, "near_water": "yes", "flooded_before": "yes", "floor_level": "ground",
                             "higher_storage": "none"})
    safer = preview(client, {**EXPOSURE, "near_water": "no", "flooded_before": "no", "floor_level": "upper",
                             "higher_storage": "second_floor"})
    order = ["low", "medium", "high"]
    assert order.index(safer["risk_level"]) < order.index(risky["risk_level"])


def test_placeholders_never_produce_warnings_for_unanswered_fields(client):
    # Unanswered floor/storage/budget/suppliers/money would trigger warnings if placeholders leaked through.
    body = preview(client, {"district": SAMPLE["district"], "near_water": "no"})
    assert body["warnings"] == []


def test_warnings_are_tagged_with_their_step_once_their_fields_are_answered(client):
    body = preview(client, {**SAMPLE, "prep_budget": 5000, "cash_on_hand": 200})
    steps = {w["step"] for w in body["warnings"] if w["text"].startswith("Prep budget is larger")}
    assert steps == {"prep"}
    body = preview(client, {**SAMPLE, "monthly_fixed_costs": 50000, "weekly_sales": 100})
    assert any(w["step"] == "money" for w in body["warnings"])


def test_no_suppliers_warning_only_after_the_suppliers_step(client):
    without = {k: v for k, v in SAMPLE.items() if k != "suppliers"}
    assert not any(w["step"] == "suppliers" for w in preview(client, without)["warnings"])
    answered = preview(client, {**without, "suppliers": []})
    assert any(w["step"] == "suppliers" for w in answered["warnings"])


def test_unknown_flood_answer_warns_on_the_business_step(client):
    body = preview(client, {"district": SAMPLE["district"], "near_water": "unknown"})
    assert [w["step"] for w in body["warnings"]] == ["business"]


def test_invalid_answer_is_reported_on_its_step_without_breaking_the_gauge(client):
    body = preview(client, {**SAMPLE, "share_stock_below_1m": 1.5})
    assert [(e["field"], e["step"]) for e in body["errors"]] == [("share_stock_below_1m", "stock")]
    assert body["ready"] and body["risk_level"] == score_exposure(SAMPLE)["risk_level"]
    assert "stock_at_risk" not in body


def test_unknown_district_blocks_the_gauge_with_a_business_error(client):
    body = preview(client, {**EXPOSURE, "district": "Lima"})
    assert not body["ready"] and body["errors"][0]["field"] == "district" and body["errors"][0]["step"] == "business"
