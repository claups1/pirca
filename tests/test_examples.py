"""The saved example plans stay consistent with the current tools and wording rules (offline, no model calls)."""

import json
import re
from datetime import date

import pytest

from backend import config
from backend.agents.pirca import _with_footer
from backend.tools import SCENARIOS, TOOLS, run_scenario
from backend.tools.drafting import fill_placeholders

EXAMPLES = sorted((config.PLANS_DIR / "examples").glob("PIU-*.json"))
CODES = [p.stem for p in EXAMPLES]
MONTH = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
# A northern season name next to a year ("fall 2027", "autumn of 2027") without its southern months
# right after it, e.g. "(March–June)". Peru is in the southern hemisphere.
SEASON_WITHOUT_MONTHS = re.compile(
    rf"\b(?:fall|autumn|spring|summer|winter)\b(?!\s*\({MONTH}\s*[–-]\s*{MONTH}\))(?=[^.\n]{{0,15}}\b20\d\d\b)", re.I)


def load(code):
    return json.loads((config.PLANS_DIR / "examples" / f"{code}.json").read_text(encoding="utf-8"))


def english_texts(record):
    """Every English plan text the owner can see: the original (if English) or the translation."""
    holders = [record] if record["language"] == "en" else []
    holders += [t for lang, t in record.get("translations", {}).items() if lang == "en"]
    return [text for h in holders for text in (h["plan_template"], *h["plan"].values())]


@pytest.mark.parametrize("text, flagged", [
    ("could extend through fall 2027", True),
    ("into autumn of 2027", True),
    ("until the southern autumn (March–June) of 2027", False),
    ("prices may fall in 2027", True),            # conservative: a year right after "fall" is flagged
    ("rain will fall on the roof.", False),
])
def test_season_pattern(text, flagged):
    assert bool(SEASON_WITHOUT_MONTHS.search(text)) == flagged


@pytest.mark.parametrize("code", CODES)
def test_no_english_plan_names_a_season_without_its_months(code):
    for text in english_texts(load(code)):
        m = SEASON_WITHOUT_MONTHS.search(text)
        assert not m, f"{code}: '{text[max(0, m.start() - 40):m.end() + 20]}'"


def test_translator_prompt_gives_southern_months():
    prompt = (config.PROMPTS_DIR / "translator.md").read_text(encoding="utf-8")
    assert "southern autumn (March–June)" in prompt and "otoño (marzo–junio)" in prompt


@pytest.mark.parametrize("code", CODES)
def test_saved_facts_match_the_current_tools(code):
    record = load(code)
    form, saved = record["form"], record["facts"]
    now = {}
    for name in ("score_exposure", "compute_stock_move", "compute_cash_buffer", "compute_supplier_buffer",
                 "get_action_catalog", "optimize_budget"):
        now.update(TOOLS[name](form)["facts"])
    for s in SCENARIOS:
        now.update(run_scenario(form, s, today=date.fromisoformat(record["created_at"][:10]))["facts"])
    differ = {k: (saved[k], v) for k, v in now.items()
              if k in saved and abs(float(saved[k]) - float(v)) > 0.005}
    assert not differ, f"{code}: saved vs current {differ}"


@pytest.mark.parametrize("code", CODES)
def test_saved_plan_text_is_its_template_filled_with_its_facts(code):
    record = load(code)
    holders = [(record["language"], record)] + list(record.get("translations", {}).items())
    for lang, h in holders:
        for cur in ("pen", "usd"):
            fresh = _with_footer(fill_placeholders(h["plan_template"], record["facts"], currency=cur, language=lang)["text"], lang)
            assert h["plan"][cur] == fresh, f"{code} {lang}/{cur} is stale: refill it from its template"
