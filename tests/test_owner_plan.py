"""Offline tests for owner-facing plan rules: units, action names, asterisks, internal words, length."""

from datetime import date

import pytest

from backend.tools import SCENARIOS, TOOLS, fill_placeholders, optimize_budget, run_scenario, verify_draft
from backend.tools.drafting import UNITS, fact_unit, illustrative_action_ids

PROFILE = dict(
    business_type="bodega", district="Castilla", near_water="yes", flooded_before="yes",
    floor_level="ground", higher_storage="none", tenure="rented", stock_value=20000,
    share_stock_below_1m=0.5, perishables=True, cash_on_hand=3000, monthly_fixed_costs=4000,
    weekly_sales=7000, workers=2, days_of_stock=7, prep_budget=500, already_have=[],
    suppliers=[{"product": "a", "city": "Chiclayo"}, {"product": "b", "city": "Piura"}],
)
FACTS = {"stock_at_risk": 10000, "stock_to_move": 10000, "weeks_closed": 4, "buffer_needed": 3692.31,
         "cash_on_hand": 3000, "cash_gap": 692.31, "extra_days_to_buy": 14, "extra_stock_value": 14000,
         "total_cost": 383.49, "money_left": 116.51, "cat_02_cost": 77.0, "cat_10_cost": 36.0,
         "exposure_score": 100}

GOOD_PLAN_ES = """## 1. Tu riesgo
Tu riesgo es alto. ENFEN mantiene la Alerta de El Niño Costero [ENFEN-2026-18]. En 2017 el agua entró al mercado de Castilla [HIST-2017-30]. Tienes {stock_at_risk} en mercadería a menos de un metro del piso.

## 2. Qué hacer y cuándo
- Ahora: mueve tu mercadería y haz tus compras.
- Con alerta de ENFEN o SENAMHI: revisa tus pedidos.
- Durante la inundación: corta la luz solo si es seguro y sigue a INDECI y tu municipalidad.
- Después: elimina el agua estancada.

## 3. Tu mercadería
Sube {stock_to_move} a un lugar seguro.

## 4. Tu caja de emergencia
Si cierras {weeks_closed}, necesitas {buffer_needed}. Tienes {cash_on_hand}; te faltan {cash_gap}. Separa un poco de caja cada día.

## 5. Tus proveedores
Chiclayo tiene riesgo alto de cortes [HIST-1998-07]. Primero completa tu fondo de emergencia; después abastécete de abarrotes no perecibles. Pide el pan en entregas pequeñas y frecuentes.

## 6. Compras dentro de tu presupuesto
- Sacos de arena en la puerta* ({cat_02_cost}) [CAT-02]
- Seguro contra lluvias e inundación ({cat_10_cost}) [CAT-10]

Gastas {total_cost} y te quedan {money_left}. Los estantes elevados no alcanzaron el presupuesto.

## 7. Lo que revisamos
Probamos tu plan con lluvias un mes antes, un puente cortado y una semana sin luz. Aguanta, pero ahorra más rápido si las lluvias se adelantan.
"""


def issues(text, facts=FACTS, language="es"):
    return [i["type"] for i in verify_draft(text, facts, final_plan=True, language=language)["issues"]]


# ---------------------------------------------------------------- units

@pytest.mark.parametrize("key,value,lang,expected", [
    ("extra_days_to_buy", 14, "es", "14 días"),
    ("extra_days_to_buy", 14, "en", "14 days"),
    ("supplier_2_extra_days", 1, "es", "1 día"),
    ("weeks_closed", 3, "es", "3 semanas"),
    ("weeks_closed", 1, "en", "1 week"),
    ("rains_one_month_early__weeks_until_rains", 1.1, "es", "1.1 semanas"),
    ("long_closure__delta_weeks_closed", 9, "en", "9 weeks"),
    ("share_to_move_pct", 40.0, "es", "40%"),
    ("cash_gap", 10000, "es", "S/ 10,000"),
    ("cat_02_cost", 77.0, "es", "S/ 77 por 10 sacos llenos"),
    ("cat_10_cost", 36.0, "es", "S/ 36 al año"),
    ("cat_10_cost", 36.0, "en", "S/ 36 per year"),
    ("cat_09_cost", 5.9, "en", "S/ 5.90 per window screen"),
    ("high_risk_suppliers", 2, "es", "2"),
])
def test_fill_writes_units_in_the_plan_language(key, value, lang, expected):
    assert fill_placeholders("{%s}" % key, {key: value}, language=lang)["text"] == expected


def test_fill_usd_uses_dollar_sign_without_soles():
    text = fill_placeholders("{cat_02_cost}", {"cat_02_cost": 3447.0}, currency="usd", language="en")["text"]
    assert text == "$1,000 for 10 filled sacks"


def test_every_fact_the_tools_produce_has_a_unit():
    keys = set()
    for name in ("score_exposure", "compute_stock_move", "compute_cash_buffer", "compute_supplier_buffer",
                 "get_action_catalog", "optimize_budget"):
        keys |= set(TOOLS[name](PROFILE)["facts"])
    for s in SCENARIOS:
        keys |= set(run_scenario(PROFILE, s, today=date(2026, 10, 24))["facts"])
    assert all(fact_unit(k) in UNITS for k in keys)
    expected = {"stock_at_risk": "soles", "cash_gap": "soles", "cat_02_cost": "soles", "weeks_closed": "weeks",
                "extra_days_to_buy": "days", "supplier_1_extra_days": "days", "share_to_move_pct": "percent",
                "long_closure__cash_gap": "soles", "rains_one_month_early__weeks_until_rains": "weeks",
                "power_cut_week__power_cut_days": "days", "selected_count": "count"}
    for k, unit in expected.items():
        assert k in keys and fact_unit(k) == unit, k


@pytest.mark.parametrize("text", ["S/ {cash_gap}", "{weeks_closed} semanas", "{extra_days_to_buy} days",
                                  "{share_to_move_pct}%", "${cash_gap}", "{cash_gap} soles"])
def test_unit_written_next_to_placeholder_is_flagged(text):
    r = verify_draft(text, {"cash_gap": 1, "weeks_closed": 1, "extra_days_to_buy": 1, "share_to_move_pct": 1})
    assert "unit_next_to_placeholder" in [i["type"] for i in r["issues"]]


# ---------------------------------------------------------------- action names and costs

def test_optimizer_returns_names_and_cost_facts():
    r = optimize_budget(PROFILE)
    for s in r["selected"]:
        assert s["name_es"] and s["name_en"]
        if s["cost_used"]:
            assert s["cost_fact_key"] in r["facts"]
            assert r["facts"][s["cost_fact_key"]] == pytest.approx(s["cost_used"])


def test_free_actions_have_no_cost_fact():
    r = optimize_budget(PROFILE)
    free = [s for s in r["selected"] if not s["cost_used"]]
    assert free and all(s["cost_fact_key"] is None for s in free)
    assert "cat_05_cost" not in r["facts"]


def test_citations_do_not_count_toward_length():
    from backend.tools.drafting import plan_word_count
    # "1.", "Tu", "riesgo", "Riesgo", "alto": the citation and the "##" mark don't count
    assert plan_word_count("## 1. Tu riesgo\nRiesgo alto [HIST-2017-02, HIST-2017-30, ENFEN-2026-18].") == 5


def test_good_owner_plan_passes():
    assert issues(GOOD_PLAN_ES) == []


@pytest.mark.parametrize("line", [
    "- CAT-02 ({cat_02_cost})",                       # code alone
    "- [CAT-02] Sacos de arena ({cat_02_cost})",      # citation before the name
    "Compra sacos de arena (CAT-02).",                # parentheses, not brackets
    "CAT-02, CAT-10 y CAT-05 fueron elegidos.",       # list of codes
])
def test_bare_catalog_ids_are_flagged(line):
    assert "bare_catalog_id" in issues(GOOD_PLAN_ES + "\n" + line)


def test_catalog_id_after_name_is_allowed():
    assert "bare_catalog_id" not in issues(GOOD_PLAN_ES.replace(
        "Los estantes elevados", "Los estantes elevados [CAT-01]"))


def test_asterisk_earlier_in_the_same_sentence_counts():
    plan = GOOD_PLAN_ES.replace("Sube {stock_to_move} a un lugar seguro.",
                                "Subir la mercadería a un lugar seguro*: lleva {stock_to_move} a estantes altos, "
                                "cajas selladas o un espacio fuera de la zona inundable [CAT-05].")
    assert "missing_asterisk" not in issues(plan)
    assert "missing_asterisk" in issues(plan.replace("seguro*:", "seguro. Ahora"))


def test_illustrative_action_without_asterisk_is_flagged():
    assert "CAT-02" in illustrative_action_ids() and "CAT-10" not in illustrative_action_ids()
    plan = GOOD_PLAN_ES.replace("Sacos de arena en la puerta*", "Sacos de arena en la puerta")
    assert "missing_asterisk" in issues(plan)


# ---------------------------------------------------------------- owner language

@pytest.mark.parametrize("phrase", [
    "El optimizador seleccionó estas compras.", "El planificador sugiere esto.", "El crítico probó el plan.",
    "Nuestros agentes revisaron todo.", "Tu puntaje de exposición es alto.", "Este costo es ilustrativo.",
    "The optimizer chose these.", "The critic approved.", "Your exposure score is high.",
])
def test_internal_words_are_banned_in_owner_plan(phrase):
    assert "internal_term" in issues(GOOD_PLAN_ES.replace("Separa un poco de caja cada día.", phrase))


def test_exposure_score_placeholder_is_banned_in_owner_plan():
    assert "internal_term" in issues(GOOD_PLAN_ES.replace("Tu riesgo es alto.", "Tu riesgo es {exposure_score}."))


def test_internal_words_allowed_in_working_drafts():
    r = verify_draft("El optimizador eligió [CAT-02].", {}, final_plan=False)
    assert r["ok"]


def test_tu_plus_imperative_is_flagged():
    assert "grammar" in issues(GOOD_PLAN_ES.replace("Sube {stock_to_move}", "Tú mueve {stock_to_move}"))
    assert "grammar" not in issues(GOOD_PLAN_ES)  # "tu mercadería" (possessive) is fine


def test_plan_over_about_300_words_is_flagged():
    long_plan = GOOD_PLAN_ES.replace("Separa un poco de caja cada día.", "Separa caja cada día. " * 60)
    assert "too_long" in issues(long_plan)


def test_section_7_allows_at_most_two_sentences():
    plan = GOOD_PLAN_ES.rstrip() + " También probamos un cierre largo. Y un trabajador con dengue.\n"
    assert "section_7_too_long" in issues(plan)


def test_missing_section_is_flagged():
    assert "missing_section" in issues(GOOD_PLAN_ES.replace("## 3. Tu mercadería", "## 3. Stock"))


def test_english_plan_checks_english_headings():
    assert "missing_section" in issues(GOOD_PLAN_ES, language="en")


# ---------------------------------------------------------------- unverified-district claims

WRONG_SENTENCE = "ENFEN no menciona Castilla; no hay historia distrital verificada y el nivel es provisional."


@pytest.mark.parametrize("claim", [
    WRONG_SENTENCE,  # the sentence from the 2026-10-24 sample run
    "Los datos de tu distrito no están verificados.",
    "El nivel de tu distrito es provisional.",
    "Pirca found no sourced flood history for this district.",
    "Your district's data is unverified.",
])
def test_unverified_claim_is_flagged_for_a_verified_district(claim):
    plan = GOOD_PLAN_ES.replace("Tu riesgo es alto.", "Tu riesgo es alto. " + claim)
    r = verify_draft(plan, FACTS, final_plan=True, district_unverified=False)
    assert "false_unverified_claim" in [i["type"] for i in r["issues"]]


def test_unverified_claim_is_allowed_for_an_unverified_district():
    plan = GOOD_PLAN_ES.replace("Tu riesgo es alto.", "Tu riesgo es alto. Pirca no encontró historia de "
                                "inundaciones con fuente para tu distrito; su nivel es provisional.")
    r = verify_draft(plan, FACTS, final_plan=True, district_unverified=True)
    assert "false_unverified_claim" not in [i["type"] for i in r["issues"]]


def test_good_plan_passes_for_a_verified_district():
    assert verify_draft(GOOD_PLAN_ES, FACTS, final_plan=True, district_unverified=False)["ok"]


def test_asterisk_must_belong_to_the_cited_action():
    # From the 2026-10-24 run: the * after "seguro" and the **bold** marks must not cover CAT-07.
    line = "- **Ahora:** Sube mercadería a un lugar seguro* [CAT-05], respalda registros [CAT-07] y ahorra."
    plan = GOOD_PLAN_ES.replace("- Ahora: mueve tu mercadería y haz tus compras.", line)
    found = [i for i in verify_draft(plan, FACTS, final_plan=True)["issues"] if i["type"] == "missing_asterisk"]
    assert [i["text"] for i in found] == ["CAT-07"]
    fixed = plan.replace("respalda registros [CAT-07]", "Copia de seguridad de tus registros* [CAT-07]")
    assert "missing_asterisk" not in issues(fixed)


# ---------------------------------------------------------------- shop risk level in section 1

def risk_issues(section_1, risk_level, language="es"):
    heading = "## 1. Tu riesgo\n" if language == "es" else "## 1. Your risk\n"
    plan = heading + section_1 + "\n\n## 2. " + GOOD_PLAN_ES.split("## 2. ", 1)[1]
    return [i for i in verify_draft(plan, FACTS, final_plan=True, language=language, risk_level=risk_level)["issues"]
            if i["type"] == "risk_level_mismatch"]


def test_plan_saying_alto_fails_when_shop_risk_is_medium():
    # The PIU-C5TP6C bug: the district's hazard level written as if it were the shop's risk.
    found = risk_issues("Riesgo alto de inundación en Piura. ENFEN mantiene la Alerta [ENFEN-2026-18].", "medium")
    assert [i["text"] for i in found] == ["alto"]


def test_plan_stating_both_levels_correctly_passes():
    section = ("Tu riesgo: medio. Piura tiene riesgo alto de inundación, pero tu negocio está en un piso alto "
               "y lejos del río. ENFEN mantiene la Alerta [ENFEN-2026-18].")
    assert risk_issues(section, "medium") == []


def test_english_plan_stating_both_levels_correctly_passes():
    section = ("Your risk: medium. Piura has a high flood risk, but your shop is on an upper floor and far from "
               "the river [ENFEN-2026-18].")
    assert risk_issues(section, "medium", language="en") == []


@pytest.mark.parametrize("section,language", [
    ("High flood risk in Piura [ENFEN-2026-18].", "en"),
    ("The district hazard is high; your shop's risk is medium.", "en"),        # district first
    ("El peligro del distrito es alto; el riesgo de tu negocio es medio.", "es"),
])
def test_district_level_stated_first_fails(section, language):
    assert risk_issues(section, "medium", language=language)


def test_section_1_without_a_risk_level_fails():
    assert risk_issues("ENFEN mantiene la Alerta [ENFEN-2026-18]. Tienes {stock_at_risk} en riesgo.", "high")


@pytest.mark.parametrize("section,level", [
    ("Tu riesgo es alto. Hay {stock_at_risk} en riesgo.", "high"),
    ("**Riesgo bajo.** En Bajo Piura hubo inundaciones [HIST-2017-01].", "low"),  # a place name, not a level
    ("Tu riesgo de inundación es medio.", "medium"),
])
def test_matching_level_passes(section, level):
    assert risk_issues(section, level) == []


def test_risk_level_is_only_checked_when_given():
    plan = GOOD_PLAN_ES.replace("Tu riesgo es alto.", "Tu riesgo es bajo.")
    assert "risk_level_mismatch" not in issues(plan)
    found = verify_draft(plan, FACTS, final_plan=True, risk_level="high")["issues"]
    assert [i["type"] for i in found] == ["risk_level_mismatch"]
