"""HTTP endpoints for the Pirca frontend."""

from fastapi import APIRouter

from backend import config

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "app": "Pirca", "model": config.MODEL_NAME}
