"""Central settings for Pirca. Change the model name here and nowhere else."""

from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env from this project folder first, then from the folder above it.
# load_dotenv does not override values that are already set, so the
# project-level .env wins whenever both define the same variable.
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT.parent / ".env")

MODEL_NAME = "gpt-6-luna"
REASONING_EFFORT = "low"

PORTKEY_BASE_URL = "https://api.portkey.ai/v1"
PORTKEY_PROVIDER = "openai"

# gpt-6-luna prices in USD per 1M tokens, from the MGT 409 Lecture 11 Tokenomics slides.
# Each kind of token is charged at its own rate; "input" applies to input tokens that
# were neither read from nor written to the prompt cache.
PRICES_PER_MILLION = {
    "input": 0.10,
    "cached_input": 0.01,
    "cache_write": 0.125,
    "output": 0.50,
}

# ---- Safety limits for one plan run ----
# How many times each agent may run. The Planner and Critic get one revision each.
MAX_AGENT_RUNS = {"manager": 1, "risk_analyst": 1, "planner": 2, "critic": 2}
# Tool calls each agent may make in one run (the Manager's include running the workers).
MAX_TOOL_CALLS = {"manager": 10, "risk_analyst": 12, "planner": 8, "critic": 10}
# Per-tool caps inside an agent, on top of MAX_TOOL_CALLS. Extra calls are refused, not fatal.
MAX_CALLS_PER_TOOL = {"risk_analyst": {"score_exposure": 1, "search_documents": 4},
                      "manager": {"verify_draft": 3}}
# Model calls per agent run (each tool round trip is one model call).
MAX_MODEL_TURNS = 10
# Cap on each model response, reasoning tokens included.
MAX_OUTPUT_TOKENS = 8000
# Input + output tokens across every model call in one run.
RUN_TOKEN_BUDGET = 400_000

FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
PLANS_DIR = PROJECT_ROOT / "plans"
OUTPUT_DIR = PROJECT_ROOT / "output"
PROMPTS_DIR = PROJECT_ROOT / "backend" / "prompts"
