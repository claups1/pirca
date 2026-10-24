"""verify_draft and fill_placeholders: keep agent-written text tied to computed facts.

Agents write drafts with placeholders such as {stock_at_risk} instead of numbers.
verify_draft checks the draft before fill_placeholders swaps in formatted values.
Placeholders are always plain {fact_key}: every fact has a unit (soles, days, weeks,
percent or count) and fill_placeholders writes the unit in the plan's language.
The currency (soles or USD) is chosen only when the plan is displayed.
"""

import re

from backend.tools import data_store
from backend.tools.data_store import FX_SOURCE_ID, SOURCE_ID_PATTERN, normalize

PLACEHOLDER = re.compile(r"\{([A-Za-z][A-Za-z0-9_]*)\}")
# Anything else in braces with a suffix, e.g. {cash_gap|usd}: agents must not pick formats or currencies.
INVALID_PLACEHOLDER = re.compile(r"\{[A-Za-z][A-Za-z0-9_]*\|[^{}]*\}")

# ---------------------------------------------------------------- units

MONEY_FACTS = {
    "stock_value", "stock_at_risk", "stock_to_move", "stock_staying", "weekly_fixed_costs", "buffer_needed",
    "cash_on_hand", "cash_gap", "lost_sales", "extra_stock_value", "budget", "total_cost", "money_left",
    "expected_benefit", "weekly_saving_needed", "sales_at_risk", "prep_budget", "monthly_fixed_costs",
    "weekly_sales", "planned_purchases", "cash_after_purchases", "extra_stock_needed", "stock_up_money_available",
}
DAY_FACTS = {"days_of_stock", "extra_days_to_buy", "extra_days_needed", "power_cut_days"}
WEEK_FACTS = {"weeks_closed", "weeks_until_rains", "sick_weeks"}
UNITS = ("soles", "days", "weeks", "percent", "count")
UNIT_WORDS = {
    "days": {"es": ("día", "días"), "en": ("day", "days")},
    "weeks": {"es": ("semana", "semanas"), "en": ("week", "weeks")},
}


def base_key(key: str) -> str:
    """Strip the scenario prefix and baseline_/delta_ so a key maps to its unit."""
    return re.sub(r"^(?:[a-z0-9_]+?__)?(?:baseline_|delta_)?", "", key)


def fact_unit(key: str) -> str:
    """Unit of a fact: soles, days, weeks, percent or count."""
    b = base_key(key)
    if b in MONEY_FACTS or re.fullmatch(r"cat_\d{2}_cost", b):
        return "soles"
    if b.endswith("_pct"):
        return "percent"
    if b in DAY_FACTS or b.endswith("_days"):
        return "days"
    if b in WEEK_FACTS or b.endswith("_weeks"):
        return "weeks"
    return "count"


def cost_unit(key: str, language: str) -> str:
    """Catalog cost unit for a {cat_NN_cost} fact, e.g. 'al año' / 'per year'; '' for other keys."""
    m = re.fullmatch(r"cat_(\d{2})_cost", base_key(key))
    if not m:
        return ""
    row = next((a for a in data_store.action_catalog() if a["id"] == f"CAT-{m.group(1)}"), {})
    return row.get(f"cost_unit_{language}", "")


def _number(value: float, decimals: int) -> str:
    return f"{abs(value):,.{decimals}f}"


def _plain(value) -> str:
    return f"{int(value):,}" if float(value).is_integer() else f"{value:,.1f}"


def format_value(key: str, value, currency: str = "pen", language: str = "es") -> str:
    """S/ 10,000 or $2,650 for money; 40% for percent; '14 días' / '14 days'; plain counts."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return str(value)
    unit = fact_unit(key)
    if unit == "soles":
        amount = value / data_store.exchange_rate()["pen_per_usd"] if currency == "usd" else value
        decimals = 2 if abs(amount) < 100 and amount != int(amount) else 0
        sign = "-" if amount < 0 else ""
        text = f"{sign}${_number(amount, decimals)}" if currency == "usd" else f"{sign}S/ {_number(amount, decimals)}"
        unit = cost_unit(key, language)
        return f"{text} {unit}" if unit else text
    if unit == "percent":
        return f"{value:g}%"
    if unit in UNIT_WORDS:
        singular, plural = UNIT_WORDS[unit][language]
        return f"{_plain(value)} {singular if abs(value) == 1 else plural}"
    return _plain(value)


# ---------------------------------------------------------------- checks

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

# Units and currency symbols must come from fill_placeholders, never from the agent.
UNIT_AFTER = re.compile(r"\{[A-Za-z][A-Za-z0-9_]*\}\s*(%|d[ií]as?\b|days?\b|semanas?\b|weeks?\b|soles\b|"
                        r"d[oó]lares\b|dollars?\b|usd\b|percent\b|por ?ciento\b)", re.IGNORECASE)
UNIT_BEFORE = re.compile(r"(S/\.?|US\$|\$|USD)\s*\{[A-Za-z]", re.IGNORECASE)

# ---- owner-plan checks (final_plan=True) ----

INTERNAL_TERMS = re.compile(
    r"\boptimi[sz]\w*|\bplanificador\w*|\bplanners?\b|\bel critico\b|\bla critica\b|\bcritics?\b|\bagentes?\b"
    r"|\bagents?\b|\bpuntaje\b|\bscores?\b|\bexposure\b|\bilustrativ\w*|\billustrative\b|\bfact_key\b")
INTERNAL_PLACEHOLDERS = {"exposure_score", "district_points", "near_water_points", "flooded_before_points",
                         "floor_level_points", "higher_storage_points", "expected_benefit", "issue_count"}
TU_PLUS_IMPERATIVE = re.compile(
    r"\btú\s+(mueve|sube|compra|guarda|revisa|ahorra|habilita|pide|separa|elimina|vende|protege|corta|limpia|"
    r"coloca|instala|cubre|ten|haz|sigue|abastécete|prepara)\b", re.IGNORECASE)
# Claims that the district's data is unverified/provisional/missing (matched on accent-free text).
# Allowed only when the district really is UNVERIFIED in districts.csv.
UNVERIFIED_CLAIM = re.compile(
    r"\bno (?:(?:esta|estan|es|son|fue|fueron) )?verificad\w*|\bsin verificar\b|\bunverified\b|\bnot verified\b"
    r"|\bprovisional\w*"
    r"|\bno (?:hay|existe|tiene|tenemos) (?:historia|historial|datos|registros?)\b"
    r"|\bno se (?:hallo|encontro|encontraron) (?:historia|historial|datos|registros?)\b"
    r"|\bno (?:sourced |district-level )?(?:flood )?history\b")
CATALOG_ID = re.compile(r"\bCAT-\d{2}\b")
SECTION_7 = {"es": "## 7. Lo que revisamos", "en": "## 7. What we checked"}
SECTIONS = {
    "es": ["Tu riesgo", "Qué hacer y cuándo", "Tu mercadería", "Tu caja de emergencia", "Tus proveedores",
           "Compras dentro de tu presupuesto", "Lo que revisamos"],
    "en": ["Your risk", "What to do and when", "Your stock", "Your emergency cash", "Your suppliers",
           "Purchases within your budget", "What we checked"],
}
MAX_PLAN_WORDS = 330  # "about 300"
MAX_SECTION_7_SENTENCES = 2


def _blank(text: str, pattern: re.Pattern) -> str:
    return pattern.sub(lambda m: " " * len(m.group(0)), text)


def illustrative_action_ids() -> set[str]:
    return {a["id"] for a in data_store.action_catalog()
            if "illustrative" in a["cost_status"] or "illustrative" in a["protects_status"]}


def _bracket_around(text: str, start: int, end: int) -> tuple[int, int] | None:
    """(open, close) of the [...] group containing text[start:end] on the same line, if any."""
    open_ = text.rfind("[", 0, start)
    close = text.find("]", end)
    if open_ == -1 or close == -1:
        return None
    if "\n" in text[open_:close] or "]" in text[open_ + 1:start] or "[" in text[end:close]:
        return None
    return open_, close


def plan_word_count(draft: str) -> int:
    """Words the owner reads: source-ID citations in brackets and Markdown heading marks don't count."""
    prose = re.sub(r"\[[^\]\n]*\]", " ", draft)
    prose = re.sub(r"(?m)^\s*#{1,6}\s*", "", prose)
    return len([w for w in prose.split() if re.search(r"\w", w)])


def recommended_spending(draft: str, facts: dict) -> dict:
    """Money the plan tells the owner to spend: every purchase cost it shows ({cat_NN_cost}) plus
    the largest supplier stock-up it shows ({extra_stock_value} or a scenario variant)."""
    used = {m.group(1) for m in PLACEHOLDER.finditer(draft)} & set(facts)
    purchases = {k: facts[k] for k in used if re.fullmatch(r"cat_\d{2}_cost", k)}
    stock_up = max((facts[k] for k in used if base_key(k) == "extra_stock_value"), default=0.0)
    total = round(sum(purchases.values()) + stock_up, 2)
    cash = facts.get("cash_on_hand")
    return {"purchases": purchases, "stock_up": stock_up, "total": total, "cash_on_hand": cash,
            "within_cash": cash is not None and total <= cash + 0.005}


def check_affordability(draft: str, facts: dict) -> list[dict]:
    """Safety check: the app never recommends spending money the owner doesn't have."""
    issues = []
    spend = recommended_spending(draft, facts)
    if spend["cash_on_hand"] is None:
        if spend["total"] > 0:
            issues.append({"type": "affordability_unknown", "text": f"S/ {spend['total']:,.2f}",
                           "detail": "Cash on hand is not in the facts, so recommended spending cannot be checked"})
    elif not spend["within_cash"]:
        issues.append({"type": "spending_exceeds_cash", "text": f"S/ {spend['total']:,.2f}",
                       "detail": f"The plan recommends spending S/ {spend['total']:,.2f} but the owner has "
                                 f"S/ {spend['cash_on_hand']:,.2f} in cash"})
    used = {m.group(1) for m in PLACEHOLDER.finditer(draft)} & set(facts)
    for k in sorted(used):
        b = base_key(k)
        if (b in ("extra_stock_value", "extra_days_to_buy") or re.fullmatch(r"supplier_\d+_extra_days", b)) \
                and not facts[k]:
            issues.append({"type": "zero_stock_up_mentioned", "text": "{" + k + "}",
                           "detail": "This stock-up is 0 (not affordable, or a perishable product): say "
                                     "'primero completa tu fondo de emergencia' or 'pide entregas pequeñas y "
                                     "frecuentes' instead of showing it"})
    return issues


def _name_before_citation(before: str) -> str:
    """Text that names the cited action: back to the previous citation or sentence end, without **bold**."""
    segment = re.split(r"[.!?]\s|\]", before)[-1]
    return re.sub(r"\*\*[^*]*\*\*", "", segment)


def _owner_plan_issues(draft: str, language: str, district_unverified: bool | None) -> list[dict]:
    issues = []
    if district_unverified is False:
        for m in UNVERIFIED_CLAIM.finditer(normalize(draft)):
            issues.append({"type": "false_unverified_claim", "text": m.group(0),
                           "detail": "This district has sourced flood history; do not call its data unverified, "
                                     "provisional or missing"})
    illustrative = illustrative_action_ids()
    for m in CATALOG_ID.finditer(draft):
        group = _bracket_around(draft, m.start(), m.end())
        line_start = draft.rfind("\n", 0, m.start()) + 1
        before = draft[line_start:group[0]] if group else ""
        if group is None or not re.sub(r"^\s*(?:[-*+]|\d+[.)])?\s*", "", before).strip():
            issues.append({"type": "bare_catalog_id", "text": m.group(0),
                           "detail": "Name the action in the owner's language; a catalog ID may only follow "
                                     "the name as a citation in brackets"})
        elif m.group(0) in illustrative and "*" not in _name_before_citation(before):
            issues.append({"type": "missing_asterisk", "text": m.group(0),
                           "detail": "This action uses an estimated cost or benefit: mark its name with *"})
    norm = normalize(draft)
    for m in INTERNAL_TERMS.finditer(norm):
        issues.append({"type": "internal_term", "text": m.group(0),
                       "detail": "Owner plans never mention internal terms (optimizer, planner, critic, agents, "
                                 "score, 'illustrative'); use * for estimates and the risk level word"})
    for m in PLACEHOLDER.finditer(draft):
        if base_key(m.group(1)) in INTERNAL_PLACEHOLDERS:
            issues.append({"type": "internal_term", "text": m.group(0),
                           "detail": "Show the risk level word (alto/medio/bajo), not internal numbers"})
    for m in TU_PLUS_IMPERATIVE.finditer(draft):
        issues.append({"type": "grammar", "text": m.group(0),
                       "detail": "Use the imperative without 'tú': 'Mueve tu mercadería', not 'Tú mueve'"})
    words = plan_word_count(draft)
    if words > MAX_PLAN_WORDS:
        issues.append({"type": "too_long", "text": f"{words} words",
                       "detail": f"Keep the plan to about 300 words (limit {MAX_PLAN_WORDS}): cut at least "
                                 f"{words - 280} words, e.g. shorter bullets and fewer repeated citations"})
    for i, title in enumerate(SECTIONS[language], 1):
        if f"## {i}. {title}" not in draft:
            issues.append({"type": "missing_section", "text": f"## {i}. {title}", "detail": "Required heading"})
    heading = SECTION_7[language]
    if heading in draft:
        body = draft.split(heading, 1)[1]
        body = PLACEHOLDER.sub("x", SOURCE_ID_PATTERN.sub("", body))
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", body.strip()) if s.strip()]
        if len(sentences) > MAX_SECTION_7_SENTENCES:
            issues.append({"type": "section_7_too_long", "text": f"{len(sentences)} sentences",
                           "detail": "Section 7 has at most 2 sentences about the situations the plan was tested against"})
    return issues


ISSUE_TYPES = ("raw_number", "unknown_fact_key", "invalid_placeholder", "unit_next_to_placeholder",
               "unknown_source_id", "forbidden_content", "bare_catalog_id", "missing_asterisk", "internal_term",
               "grammar", "too_long", "missing_section", "section_7_too_long", "false_unverified_claim",
               "spending_exceeds_cash", "zero_stock_up_mentioned", "affordability_unknown")


def verify_draft(draft: str, facts: dict, final_plan: bool = False, language: str = "es",
                 district_unverified: bool | None = None) -> dict:
    """Flag raw numbers, unknown {fact_keys}, units next to placeholders, unknown source IDs and
    forbidden content. With final_plan=True, also apply the owner-plan rules (names not codes,
    asterisks for estimates, no internal terms, plain imperatives, length, section 7) and the
    affordability check (recommended spending never exceeds cash on hand). When
    district_unverified is False, a claim that the district's data is unverified is an error."""
    issues = []
    for m in INVALID_PLACEHOLDER.finditer(draft):
        issues.append({"type": "invalid_placeholder", "text": m.group(0),
                       "detail": "Write a plain {fact_key}; the currency is chosen when the plan is displayed"})
    for m in PLACEHOLDER.finditer(draft):
        if m.group(1) not in facts:
            issues.append({"type": "unknown_fact_key", "text": m.group(0),
                           "detail": f"'{m.group(1)}' is not in the computed facts"})
    for pattern in (UNIT_AFTER, UNIT_BEFORE):
        for m in pattern.finditer(draft):
            issues.append({"type": "unit_next_to_placeholder", "text": m.group(0),
                           "detail": "Write the placeholder alone; the app adds units and currency"})
    known = data_store.known_source_ids()
    for m in SOURCE_ID_PATTERN.finditer(draft):
        if m.group(0) not in known:
            issues.append({"type": "unknown_source_id", "text": m.group(0),
                           "detail": "Not a HIST, CAT, ENFEN or BCRP ID in Pirca's data"})

    work = _blank(_blank(draft, PLACEHOLDER), INVALID_PLACEHOLDER)
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

    if final_plan:
        issues += _owner_plan_issues(draft, language, district_unverified)
        issues += check_affordability(draft, facts)

    counts = {t: sum(i["type"] == t for i in issues) for t in ISSUE_TYPES}
    return {"tool": "verify_draft", "ok": not issues, "issues": issues,
            "facts": {"issue_count": len(issues), **{f"{k}_count": v for k, v in counts.items()}},
            "sources": sorted({m.group(0) for m in SOURCE_ID_PATTERN.finditer(draft)} & known)}


# ---------------------------------------------------------------- filling

def fill_placeholders(text: str, facts: dict, currency: str = "pen", language: str = "es") -> dict:
    """Replace every {fact_key} with its value and unit, in the chosen currency ("pen" or "usd")
    and language ("es" or "en"). Unknown keys are left as-is and reported in "missing"."""
    currency, language = currency.lower(), language.lower()
    if currency not in ("pen", "usd"):
        raise ValueError("currency must be 'pen' or 'usd'")
    if language not in ("es", "en"):
        raise ValueError("language must be 'es' or 'en'")
    missing, used_usd, count = [], False, 0

    def repl(m):
        nonlocal used_usd, count
        key = m.group(1)
        if key not in facts:
            missing.append(key)
            return m.group(0)
        count += 1
        used_usd |= currency == "usd" and fact_unit(key) == "soles"
        return format_value(key, facts[key], currency, language)

    filled = PLACEHOLDER.sub(repl, text)
    fx = data_store.exchange_rate()
    return {"tool": "fill_placeholders", "text": filled,
            "facts": {"replaced_count": count, "missing_count": len(missing),
                      **({"pen_per_usd": fx["pen_per_usd"]} if used_usd else {})},
            "missing": missing, "sources": [FX_SOURCE_ID] if used_usd else []}
