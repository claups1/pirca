"""Load agent system prompts from backend/prompts/.

Each system prompt is shared_rules.md followed by the agent's own file. Both are
static, so the whole system prompt can be cached; per-run inputs (profile, tool
results, revision notes) go in the user message instead.
"""

from functools import lru_cache

from backend import config
from backend.agents import AGENTS


@lru_cache
def load_prompt(agent: str) -> str:
    if agent not in AGENTS:
        raise ValueError(f"Unknown agent '{agent}'. Choose one of: {', '.join(AGENTS)}")
    shared = (config.PROMPTS_DIR / "shared_rules.md").read_text(encoding="utf-8")
    own = (config.PROMPTS_DIR / f"{agent}.md").read_text(encoding="utf-8")
    return f"{shared.rstrip()}\n\n---\n\n{own.strip()}\n"
