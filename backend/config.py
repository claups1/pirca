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

PORTKEY_BASE_URL = "https://api.portkey.ai/v1"
PORTKEY_PROVIDER = "openai"

FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
PLANS_DIR = PROJECT_ROOT / "plans"
OUTPUT_DIR = PROJECT_ROOT / "output"
PROMPTS_DIR = PROJECT_ROOT / "backend" / "prompts"
