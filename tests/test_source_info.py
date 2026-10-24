"""Offline tests for the footnote source details."""

from backend.tools.data_store import FX_SOURCE_ID
from backend.tools.source_info import cited_ids, describe_sources, latest_enfen


def test_describes_each_kind_of_source():
    d = describe_sources(["HIST-2017-30", "CAT-02", "ENFEN-2026-18", FX_SOURCE_ID, "HIST-2017-99"])
    assert set(d) == {"HIST-2017-30", "CAT-02", "ENFEN-2026-18", FX_SOURCE_ID}  # unknown IDs are skipped
    assert d["HIST-2017-30"]["date"] == "2017" and "1.20" in d["HIST-2017-30"]["quote"] or d["HIST-2017-30"]["quote"]
    assert d["CAT-02"]["title"] == {"es": "Sacos de arena en la puerta", "en": "Sandbags at the door"}
    assert d["ENFEN-2026-18"]["title"] == "Comunicado Oficial ENFEN N° 18-2026" and d["ENFEN-2026-18"]["date"] == "2026-10-16"
    assert "3.447" in d[FX_SOURCE_ID]["fact_en"]


def test_cited_ids_in_order_of_first_appearance():
    text = "A [HIST-2017-02, HIST-2017-30]. B [ENFEN-2026-18]. C [HIST-2017-30] [CAT-05]"
    assert cited_ids(text) == ["HIST-2017-02", "HIST-2017-30", "ENFEN-2026-18", "CAT-05"]


def test_latest_enfen_is_the_newest_communique():
    e = latest_enfen()
    assert e["id"] == "ENFEN-2026-18" and e["number"] == "18-2026" and e["status"] == "Alerta de El Niño Costero"


def test_catalog_quotes_are_verbatim_without_notes():
    d = describe_sources(["CAT-14"])["CAT-14"]
    assert "pandemic context" not in d["quote"]


def test_detail_says_which_language_each_text_is_in():
    d = describe_sources(["CAT-05", "HIST-2017-30", "ENFEN-2026-18"])
    assert d["CAT-05"]["lang_es"] == "en"        # Ready.gov quote stays in English
    assert d["HIST-2017-30"]["lang_es"] == "es" and d["HIST-2017-30"]["lang_en"] == "en"
    assert d["ENFEN-2026-18"]["lang_en"] == "es"  # ENFEN text is only in Spanish


def test_english_summaries_are_never_marked_spanish():
    # Spanish place names with accents must not make Pirca's own English summary look Spanish.
    d = describe_sources(["HIST-2017-02"])["HIST-2017-02"]
    assert "Sánchez" in d["fact_en"] and d["lang_en"] == "en"
