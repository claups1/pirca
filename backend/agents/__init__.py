"""Pirca agents: a Manager that delegates to a Risk Analyst, a Planner and a Critic."""

# Tools the Manager calls to run the other agents. They are implemented by the
# agent loop, not in backend/tools/, because each one runs a whole agent.
AGENT_TOOLS = ("run_risk_analyst", "run_planner", "run_critic")

# Which tools each agent may call. Anything else is refused by the agent loop.
TOOLSETS = {
    "manager": ("run_risk_analyst", "run_planner", "run_critic", "verify_draft"),
    "risk_analyst": ("score_exposure", "get_historical_impacts", "search_documents"),
    "planner": ("compute_stock_move", "compute_cash_buffer", "compute_supplier_buffer",
                "get_action_catalog", "optimize_budget"),
    "critic": ("verify_draft", "run_scenario"),
}

AGENTS = tuple(TOOLSETS)
