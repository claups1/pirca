"""Shared test fixtures."""

import pytest

from backend.tools import data_store

TEST_DISTRICT = "Distrito Sin Datos"


@pytest.fixture
def unverified_district(monkeypatch):
    """A test-only district with no sourced history. Since 2023 data was added, every real district has
    evidence, but Pirca must still warn about UNVERIFIED districts if one appears."""
    fake = dict(data_store.districts())
    fake[data_store.normalize(TEST_DISTRICT)] = {
        "district": TEST_DISTRICT, "province": "Prueba", "flood_hazard_level": "UNVERIFIED",
        "basis": "No district-level impact found in sourced data", "flood_hist_ids": "", "other_hist_ids": ""}
    monkeypatch.setattr(data_store, "districts", lambda: fake)
    return TEST_DISTRICT
