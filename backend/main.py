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
from backend.api.routes import router
from backend.tools import validate_profile

app = FastAPI(title="Pirca", description="El Niño costero preparation plans for small shops in Piura")
app.include_router(router)


class PlanRequest(BaseModel):
    profile: dict
    language: Literal["es", "en"] = "es"


@app.post("/api/validate")
def validate(profile: dict = Body(...)) -> dict:
    """Check the intake form before running: errors block the run, warnings are shown to the owner."""
    result = validate_profile(profile)
    return {"valid": result["valid"], "errors": result["errors"], "warnings": result["warnings"]}


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
