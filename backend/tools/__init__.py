"""Deterministic tools the Pirca agents call. Every tool returns a JSON-ready dict
with a "facts" object (named numbers) and the "sources" (HIST/CAT/ENFEN/BCRP IDs) it used."""

from backend.tools.actions import get_action_catalog, optimize_budget
from backend.tools.calculations import (
    SCENARIOS,
    compute_cash_buffer,
    compute_stock_move,
    compute_supplier_buffer,
    run_scenario,
    score_exposure,
)
from backend.tools.drafting import fill_placeholders, verify_draft
from backend.tools.profile import ShopProfile, validate_profile
from backend.tools.search import get_historical_impacts, search_documents

TOOLS = {
    f.__name__: f
    for f in (
        validate_profile, score_exposure, compute_stock_move, compute_cash_buffer, compute_supplier_buffer,
        get_action_catalog, optimize_budget, search_documents, get_historical_impacts, run_scenario,
        verify_draft, fill_placeholders,
    )
}

__all__ = ["TOOLS", "SCENARIOS", "ShopProfile", *TOOLS]
