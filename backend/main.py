"""Pirca FastAPI app: the API under /api and the frontend at /.

Run from the Final Project folder:
    .venv\\Scripts\\uvicorn backend.main:app
(add --reload --port 8020 while developing)
"""

from typing import Literal

from fastapi import Body, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend import config
from backend.api import plans
from backend.api.home import home_data
from backend.api.preview import preview_profile
from backend.api.routes import router
from backend.tools import data_store, validate_profile
from backend.tools.source_info import latest_enfen

app = FastAPI(title="Pirca", description="El Niño costero preparation plans for small shops in Piura")
app.include_router(router)


@app.middleware("http")
async def revalidate_frontend(request, call_next):
    """Browsers must re-check the frontend files on each load, so an update is never hidden by a cache."""
    response = await call_next(request)
    if not request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-cache"
    return response


class PlanRequest(BaseModel):
    profile: dict
    language: Literal["es", "en"] = "es"


EXAMPLE_CODE = "PIU-CAST26"


@app.get("/api/meta")
def meta() -> dict:
    """What the form needs: districts (with hazard level), the checklist of catalog actions,
    the example plan code, and the fixed exchange rate for formatting amounts."""
    districts = [{"name": d["district"], "province": d["province"], "hazard_level": d["flood_hazard_level"]}
                 for d in data_store.districts().values()]
    actions = [{"id": a["id"], "name_es": a["name_es"], "name_en": a["name_en"], "cost_unit_es": a["cost_unit_es"],
                "cost_unit_en": a["cost_unit_en"], "unit_prices": a["unit_prices"]} for a in data_store.action_catalog()]
    fx = data_store.exchange_rate()
    return {"districts": districts, "actions": actions, "example_code": EXAMPLE_CODE, "enfen": latest_enfen(),
            "pen_per_usd": fx["pen_per_usd"], "fx_date": fx["date"], "model": config.MODEL_NAME}


@app.get("/api/home")
def home() -> dict:
    """Start screen data (district dots, "why it matters" numbers, El Niño timeline), read from the data files."""
    return home_data()


@app.post("/api/validate")
def validate(profile: dict = Body(...)) -> dict:
    """Check the intake form before running: errors block the run, warnings are shown to the owner."""
    result = validate_profile(profile)
    return {"valid": result["valid"], "errors": result["errors"], "warnings": result["warnings"]}


@app.post("/api/preview")
def preview(profile: dict = Body(...)) -> dict:
    """Live risk preview while the owner fills in the wizard: code tools only (validate_profile +
    score_exposure), never the model, so it costs 0 tokens. Accepts partial answers."""
    return preview_profile(profile)


@app.post("/api/plans", status_code=202)
def create_plan(request: PlanRequest) -> dict:
    """Return a plan code immediately; the agents run in a background thread."""
    check = validate_profile(request.profile)
    if not check["valid"]:
        raise HTTPException(status_code=422, detail={"errors": check["errors"], "warnings": check["warnings"]})
    code = plans.start_plan(check["profile"], request.language)
    return {"code": code, "status": "running", "warnings": check["warnings"]}


@app.get("/api/plans/{code}")
def get_plan(code: str, after: int = 0) -> dict:
    """running / done / stopped / error, the trace events after `after`, and the result once finished."""
    status = plans.plan_status(code, after=after) if plans.is_valid_code(code) else None
    if status is None:
        raise HTTPException(status_code=404, detail=f"No plan with code {code}")
    return status


@app.post("/api/plans/{code}/translate")
def translate_plan(code: str) -> dict:
    """Translate the final plan to the other language once; later calls return the saved translation."""
    try:
        return plans.translate_plan(code)
    except LookupError:
        raise HTTPException(status_code=404, detail=f"No plan with code {code}")
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


# Mounted last so /api routes take priority over static files.
app.mount("/", StaticFiles(directory=config.FRONTEND_DIR, html=True), name="frontend")
