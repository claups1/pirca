"""Pirca FastAPI app: serves the API under /api and the frontend at /.

Run from the Final Project folder:
    .venv\\Scripts\\python.exe -m uvicorn backend.main:app --reload --port 8020
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend import config
from backend.api.routes import router

app = FastAPI(title="Pirca")
app.include_router(router)

# Mounted last so /api routes take priority over static files.
app.mount("/", StaticFiles(directory=config.FRONTEND_DIR, html=True), name="frontend")
