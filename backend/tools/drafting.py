"""verify_draft and fill_placeholders: keep agent-written text tied to computed facts.

Agents write drafts with placeholders such as {stock_at_risk} instead of numbers.
verify_draft checks the draft before fill_placeholders swaps in formatted values.
Placeholders may pick a currency: {cash_gap|usd} or {cash_gap|pen}.
"""

import re

from backend.tools import data_store
from backend.tools.data_store import FX_SOURCE_ID, SOURCE_ID_PATTERN, normalize

PLACEHOLDER = re.compile(r"\{([A-Za-z][A-Za-z0-9_]*)(?:\|(usd|pen))?\}")

MONEY_FACTS = {
    "stock_value", "stock_at_risk", "stock_to_move", "stock_staying", "weekly_fixed_costs", "buffer_needed",
    "cash_on_hand", "cash_gap", "lost_sales", "extra_stock_value", "budget", "total_cost", "money_left",
    "expected_benefit", "weekly_saving_needed", "sales_at_risk", "prep_budget", "monthly_fixed_costs",
    "weekly_sales",
}

MONTHS = ("enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre|"
          "january|february|march|april|may|june|july|august|september|october|november|december")

# Spans where digits are allowed, blanked out before looking for raw numbers.
ALLOWED_NUMBER_SPANS = [
    re.compile(r"\bnino\s*(?:1\s*\+\s*2|3\.4)"),                       # ENFEN regions Niño 1+2 / 3.4
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                               # ISO dates
    re.compile(r"\b(?:19|20)\d{2}\s*[-–/]\s*\d{2,4}\b"),                # year ranges 1997-98
    re.compile(rf"\b\d{{1,2}}\s+(?:de\s+)?(?:{MONTHS})\b"),             # 12 de marzo
    re.compile(rf"\b(?:{MONTHS})\s+(?:de\s+)?\d{{1,2}}\b(?!\d)"),       # March 12
    re.compile(r"\b(?:19|20)\d{2}\b"),                                  # years
    re.compile(r"(?m)^\s*(?:#{1,6}\s*)?\d+[.)]\s"),                      # list markers and "## 1." headings
]
RAW_NUMBER = re.compile(r"\d+(?:[.,]\d+)*")

FORBIDDEN = [
    ("evacuation_order", re.compile(r"\bevacue(?:n)?\b|\bevacuate\b|\bevacuation orders?\b|\bordenes? de evacuacion\b"
                                    r"|\b(?:debe|deben|tiene que|tienen que|hay que)\s+evacuar\b")),
    ("own_forecast", re.compile(r"\b(?:pirca|we|nosotros)\s+(?:predicts?|forecasts?|pronostica(?:mos)?|predecimos|prevemos)\b"
                                r"|\bour (?:forecast|prediction)\b|\bnuestro pronostico\b"
                                r"|\b(?:llovera|se inundara|will flood|it will rain)\b")),
]


def _blank(text: str, pattern: re.Pattern) -> str:
    return pattern.sub(lambda m: " " * len(m.group(0)), text)


def verify_draft(draft: str, facts: dict) -> dict:
    """Flag raw numbers, unknown {fact_keys}, unknown source IDs and forbidden content."""
    issues = []
    for m in PLACEHOLDER.finditer(draft):
        if m.group(1) not in facts:
            issues.append({"type": "unknown_fact_key", "text": m.group(0),
                           "detail": f"'{m.group(1)}' is not in the computed facts"})
    known = data_store.known_source_ids()
    for m in SOURCE_ID_PATTERN.finditer(draft):
        if m.group(0) not in known:
            issues.append({"type": "unknown_source_id", "text": m.group(0),
                           "detail": "Not a HIST, CAT, ENFEN or BCRP ID in Pirca's data"})

    work = _blank(draft, PLACEHOLDER)
    work = _blank(work, SOURCE_ID_PATTERN)
    work = normalize(work) if len(normalize(work)) == len(work) else work.lower()
    for pattern in ALLOWED_NUMBER_SPANS:
        work = _blank(work, pattern)
    for m in RAW_NUMBER.finditer(work):
        context = draft[max(0, m.start() - 25):m.end() + 25].replace("\n", " ")
        issues.append({"type": "raw_number", "text": m.group(0),
                       "detail": f"Use a {{fact_key}} placeholder instead of a typed number: …{context}…"})

    norm = normalize(draft)
    for kind, pattern in FORBIDDEN:
        for m in pattern.finditer(norm):
            issues.append({"type": "forbidden_content", "text": m.group(0),
                           "detail": "Pirca must not give evacuation orders" if kind == "evacuation_order"
                           else "Pirca must not make its own forecasts; cite ENFEN instead"})

    counts = {t: sum(i["type"] == t for i in issues)
              for t in ("raw_number", "unknown_fact_key", "unknown_source_id", "forbidden_content")}
    return {"tool": "verify_draft", "ok": not issues, "issues": issues,
            "facts": {"issue_count": len(issues), **{f"{k}_count": v for k, v in counts.items()}},
            "sources": sorted({m.group(0) for m in SOURCE_ID_PATTERN.finditer(draft)} & known)}


def _is_money(key: str) -> bool:
    return re.sub(r"^(?:[a-z_]+?__)?(?:baseline_|delta_)?", "", key) in MONEY_FACTS


def _number(value: float, decimals: int) -> str:
    return f"{abs(value):,.{decimals}f}"


def format_value(key: str, value, currency: str = "pen") -> str:
    """S/ 10,000 or $2,650 for money; 40% for *_pct; plain numbers otherwise."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return str(value)
    if _is_money(key):
        amount = value / data_store.exchange_rate()["pen_per_usd"] if currency == "usd" else value
        decimals = 2 if abs(amount) < 100 and amount != int(amount) else 0
        sign = "-" if amount < 0 else ""
        return f"{sign}${_number(amount, decimals)}" if currency == "usd" else f"{sign}S/ {_number(amount, decimals)}"
    if key.endswith("_pct"):
        return f"{value:g}%"
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.1f}"


def fill_placeholders(text: str, facts: dict, currency: str = "pen") -> dict:
    """Replace {fact_key} (or {fact_key|usd}) with formatted values; unknown keys are left as-is."""
    missing, used_usd, count = [], False, 0

    def repl(m):
        nonlocal used_usd, count
        key, cur = m.group(1), (m.group(2) or currency).lower()
        if key not in facts:
            missing.append(key)
            return m.group(0)
        count += 1
        used_usd |= cur == "usd" and _is_money(key)
        return format_value(key, facts[key], cur)

    filled = PLACEHOLDER.sub(repl, text)
    fx = data_store.exchange_rate()
    return {"tool": "fill_placeholders", "text": filled,
            "facts": {"replaced_count": count, "missing_count": len(missing),
                      **({"pen_per_usd": fx["pen_per_usd"]} if used_usd else {})},
            "missing": missing, "sources": [FX_SOURCE_ID] if used_usd else []}
