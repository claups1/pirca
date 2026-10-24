"""Offline API tests: the agent run and the translation model are replaced by fakes."""

import json
import re
import threading
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from backend.api import plans
from backend.main import app
from tests.test_owner_plan import FACTS, GOOD_PLAN_ES

PROFILE = dict(
    business_type="bodega", district="Castilla", near_water="yes", flooded_before="yes",
    floor_level="ground", higher_storage="none", tenure="rented", stock_value=20000,
    share_stock_below_1m=0.5, perishables=True, cash_on_hand=3000, monthly_fixed_costs=4000,
    weekly_sales=7000, workers=2, days_of_stock=7, prep_budget=500, already_have=[],
    suppliers=[{"product": "abarrotes", "city": "Chiclayo"}],
)
EN_PLAN = (GOOD_PLAN_ES
           .replace("## 1. Tu riesgo", "## 1. Your risk").replace("## 2. Qué hacer y cuándo", "## 2. What to do and when")
           .replace("## 3. Tu mercadería", "## 3. Your stock").replace("## 4. Tu caja de emergencia", "## 4. Your emergency cash")
           .replace("## 5. Tus proveedores", "## 5. Your suppliers")
           .replace("## 6. Compras dentro de tu presupuesto", "## 6. Purchases within your budget")
           .replace("## 7. Lo que revisamos", "## 7. What we checked"))
USAGE = {"input_tokens": 900, "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0},
         "output_tokens": 600, "output_tokens_details": {"reasoning_tokens": 0}}


def fake_result(status="completed"):
    events = [{"seq": 1, "type": "run_started", "agent": "pirca", "totals": {}},
              {"seq": 2, "type": "run_finished", "agent": "pirca", "status": status, "totals": {}}]
    result = {"status": status, "events": events, "facts": FACTS, "usage": {"total_tokens": 10, "cost_usd": 0.01}}
    if status.startswith("completed"):
        result.update(plan_template=GOOD_PLAN_ES, plan={"pen": "plan S/", "usd": "plan $"}, summary_en="ok")
    return result


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.setattr(plans, "PLANS_DIR", tmp_path)
    monkeypatch.setattr(plans, "JOBS", {})
    calls = SimpleNamespace(model=0, run=0)
    gate = threading.Event()

    def fake_run_plan(form, language, today, on_event):
        calls.run += 1
        for e in fake_result()["events"][:1]:
            on_event(e)
        gate.wait(5)  # lets a test look at the job while it is "running"
        return fake_result(fake_run_plan.status)
    fake_run_plan.status = "completed"

    class FakeResponses:
        def create(self, **kw):
            calls.model += 1
            return SimpleNamespace(output_text=EN_PLAN, usage=USAGE)

    monkeypatch.setattr(plans, "run_plan", fake_run_plan)
    monkeypatch.setattr(plans, "make_client", lambda: SimpleNamespace(responses=FakeResponses()))
    return SimpleNamespace(client=TestClient(app), dir=tmp_path, calls=calls, gate=gate, run=fake_run_plan)


def finish(api, code):
    api.gate.set()
    plans.JOBS[code].thread.join(5)


# ---------------------------------------------------------------- codes

def test_codes_have_no_look_alike_characters():
    codes = {plans.new_code() for _ in range(300)}
    assert all(re.fullmatch(r"PIU-[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}", c) for c in codes)
    assert len(codes) == 300
    assert not plans.is_valid_code("PIU-0OI1L2")


# ---------------------------------------------------------------- validate

def test_validate_returns_warnings_for_unverified_district(api, unverified_district):
    r = api.client.post("/api/validate", json={**PROFILE, "district": unverified_district})
    assert r.status_code == 200 and r.json()["valid"]
    assert any("UNVERIFIED" in w for w in r.json()["warnings"])


def test_validate_returns_errors(api):
    r = api.client.post("/api/validate", json={**PROFILE, "workers": 0})
    assert r.status_code == 200 and not r.json()["valid"] and r.json()["errors"]


# ---------------------------------------------------------------- plans

def test_create_plan_returns_code_then_runs_in_background(api):
    r = api.client.post("/api/plans", json={"profile": PROFILE, "language": "es"})
    assert r.status_code == 202
    code = r.json()["code"]
    assert plans.is_valid_code(code) and r.json()["status"] == "running"

    running = api.client.get(f"/api/plans/{code}").json()
    assert running["status"] == "running" and running["result"] is None
    assert [e["type"] for e in running["events"]] == ["run_started"]

    finish(api, code)
    done = api.client.get(f"/api/plans/{code}").json()
    assert done["status"] == "done"
    assert done["result"]["plan_template"] == GOOD_PLAN_ES
    assert "events" not in done["result"]  # events are returned once, at the top level

    saved = json.loads((api.dir / f"{code}.json").read_text(encoding="utf-8"))
    for key in ("code", "form", "language", "plan_template", "facts", "events", "usage", "translations"):
        assert key in saved
    assert saved["form"]["district"] == "Castilla"


def test_events_after_returns_only_new_events(api):
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    finish(api, code)
    events = api.client.get(f"/api/plans/{code}?after=1").json()["events"]
    assert [e["seq"] for e in events] == [2, 3] and events[-1]["type"] == "translation"


def test_invalid_profile_is_rejected_without_starting_a_run(api):
    r = api.client.post("/api/plans", json={"profile": {**PROFILE, "district": "Lima"}})
    assert r.status_code == 422 and api.calls.run == 0 and plans.JOBS == {}


def test_stopped_run_is_reported_as_stopped(api):
    api.run.status = "stopped_by_limit"
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    finish(api, code)
    assert api.client.get(f"/api/plans/{code}").json()["status"] == "stopped"


def test_crashing_run_is_saved_as_error(api, monkeypatch):
    monkeypatch.setattr(plans, "run_plan", lambda *a, **k: 1 / 0)
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    plans.JOBS[code].thread.join(5)
    body = api.client.get(f"/api/plans/{code}").json()
    assert body["status"] == "error" and "ZeroDivisionError" in body["result"]["message"]


@pytest.mark.parametrize("code", ["PIU-ZZZZZZ", "nope", "PIU-000000"])
def test_unknown_or_malformed_code_is_404(api, code):
    assert api.client.get(f"/api/plans/{code}").status_code == 404


def test_saved_plan_opens_after_restart(api):
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    finish(api, code)
    plans.JOBS.clear()  # as if the server restarted
    assert api.client.get(f"/api/plans/{code}").json()["status"] == "done"


def test_example_plans_open_without_running_agents(api):
    (api.dir / "examples").mkdir()
    record = plans.plan_record("PIU-DEMA22", PROFILE, "es", fake_result())
    plans.write_plan(api.dir / "examples" / "PIU-DEMA22.json", record)
    body = api.client.get("/api/plans/PIU-DEMA22").json()
    assert body["status"] == "done" and api.calls.run == 0


# ---------------------------------------------------------------- translate

def test_finished_plan_has_both_languages(api):
    """Every finished run is translated automatically into the other language, with one model call."""
    code = api.client.post("/api/plans", json={"profile": PROFILE, "language": "es"}).json()["code"]
    finish(api, code)
    saved = json.loads((api.dir / f"{code}.json").read_text(encoding="utf-8"))
    assert saved["language"] == "es" and set(saved["translations"]) == {"en"}
    assert saved["plan_template"] and saved["translations"]["en"]["plan_template"]
    assert {"pen", "usd"} <= set(saved["plan"]) and {"pen", "usd"} <= set(saved["translations"]["en"]["plan"])
    assert api.calls.model == 1


def test_translation_uses_one_call_then_is_free(api):
    code = api.client.post("/api/plans", json={"profile": PROFILE, "language": "es"}).json()["code"]
    finish(api, code)
    first = api.client.post(f"/api/plans/{code}/translate").json()  # already made at the end of the run
    assert first["language"] == "en" and first["cached"] and api.calls.model == 1
    assert first["usage"]["model_calls"] == 1 and first["usage"]["output_tokens"] == 600
    assert first["verification"]["ok"], first["verification"]["issues"]
    assert "## 1. Your risk" in first["plan"]["pen"] and "S/ 10,000" in first["plan"]["pen"]
    assert "Estimated cost or benefit" in first["plan"]["pen"]

    second = api.client.post(f"/api/plans/{code}/translate").json()
    assert second["cached"] and api.calls.model == 1  # no second model call
    saved = json.loads((api.dir / f"{code}.json").read_text(encoding="utf-8"))
    assert saved["translations"]["en"]["usage"]["output_tokens"] == 600
    assert saved["usage"] == {"total_tokens": 10, "cost_usd": 0.01}  # run usage kept separate


def test_translation_that_drops_placeholders_is_flagged(api, monkeypatch):
    class Lossy:
        def create(self, **kw):
            return SimpleNamespace(output_text=EN_PLAN.replace("{cash_gap}", "some money"), usage=USAGE)
    monkeypatch.setattr(plans, "make_client", lambda: SimpleNamespace(responses=Lossy()))
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    finish(api, code)
    body = api.client.post(f"/api/plans/{code}/translate").json()
    assert "placeholders_changed" in [i["type"] for i in body["verification"]["issues"]]


def test_unfinished_or_unknown_plan_cannot_be_translated(api):
    assert api.client.post("/api/plans/PIU-ZZZZZZ/translate").status_code == 404
    api.run.status = "stopped_by_limit"
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    finish(api, code)
    assert api.client.post(f"/api/plans/{code}/translate").status_code == 409


# ---------------------------------------------------------------- frontend

def test_frontend_is_served_at_root(api):
    r = api.client.get("/")
    assert r.status_code == 200 and "Pirca" in r.text


def test_translation_is_not_held_to_the_length_limit(api, monkeypatch):
    longer = EN_PLAN.replace("Separa un poco de caja cada día.", "Set aside a little cash every day. " * 12)

    class Wordy:
        def create(self, **kw):
            return SimpleNamespace(output_text=longer, usage=USAGE)
    monkeypatch.setattr(plans, "make_client", lambda: SimpleNamespace(responses=Wordy()))
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    finish(api, code)
    body = api.client.post(f"/api/plans/{code}/translate").json()
    assert body["verification"]["ok"], body["verification"]["issues"]


def test_meta_gives_the_form_what_it_needs(api):
    m = api.client.get("/api/meta").json()
    names = {d["name"]: d["hazard_level"] for d in m["districts"]}
    assert names["Castilla"] == "high" and names["Paita"] == "high" and names["Sechura"] == "medium"
    assert len(m["actions"]) == 15 and all(a["name_es"] and a["name_en"] for a in m["actions"])
    assert m["example_code"] == "PIU-CAST26" and m["pen_per_usd"] > 0


def test_finished_plan_includes_deterministic_risk_level(api):
    code = api.client.post("/api/plans", json={"profile": PROFILE}).json()["code"]
    finish(api, code)
    assert api.client.get(f"/api/plans/{code}").json()["result"]["risk_level"] == "high"


def test_meta_enfen_status_comes_from_the_index_file():
    import json as _json
    from backend import config
    index = _json.loads((config.DATA_DIR / "enfen" / "index.json").read_text(encoding="utf-8"))["communiques"]
    latest = max(index, key=lambda c: c["date"])
    e = TestClient(app).get("/api/meta").json()["enfen"]
    assert e["id"] == latest["id"] and e["date"] == latest["date"] and e["status"] == latest["status"]


def test_example_plan_has_details_for_every_cited_source():
    from backend.tools.source_info import cited_ids
    body = TestClient(app).get("/api/plans/PIU-CAST26").json()["result"]
    ids = cited_ids(body["plan_template"])
    assert ids and set(ids) == set(body["source_details"])
    for d in body["source_details"].values():
        assert d["title"] and d["url"].startswith("https://") and (d["fact_en"] or d["fact_es"])
    assert "[HIST-" in body["plan_template"]  # the saved plan keeps the raw IDs


def test_every_example_plan_has_both_languages():
    from backend import config
    for path in sorted((config.PLANS_DIR / "examples").glob("PIU-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        other = "en" if record["language"] == "es" else "es"
        assert other in record.get("translations", {}), path.name
        assert record["translations"][other]["plan"]["pen"], path.name
