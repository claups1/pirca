"""Offline checks for the project skeleton (no API calls)."""

from fastapi.testclient import TestClient

from backend import config
from backend.main import app

client = TestClient(app)


def test_model_name_lives_in_config():
    assert config.MODEL_NAME == "gpt-6-luna"


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "app": "Pirca", "model": config.MODEL_NAME}


def test_frontend_is_served():
    res = client.get("/")
    assert res.status_code == 200
    assert "Pirca" in res.text
