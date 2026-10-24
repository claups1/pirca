"""Plain-language details for source IDs (HIST, CAT, ENFEN, BCRP), for the plan's footnotes.

The plan keeps raw IDs such as [HIST-2017-30]; the interface turns them into numbered
footnotes and shows these details. Everything comes from the data files.
"""

import json
import re
from functools import lru_cache

from backend import config
from backend.tools import data_store
from backend.tools.data_store import FX_SOURCE_ID, SOURCE_ID_PATTERN


@lru_cache
def enfen_index() -> list[dict]:
    return json.loads((config.DATA_DIR / "enfen" / "index.json").read_text(encoding="utf-8"))["communiques"]


def latest_enfen() -> dict:
    """The most recent ENFEN communiqué in data/enfen/index.json (never hard-coded)."""
    c = max(enfen_index(), key=lambda x: x["date"])
    number = re.sub(r"^ENFEN-(\d{4})-(\d+)$", r"\2-\1", c["id"])
    return {"id": c["id"], "number": number, "date": c["date"], "status": c["status"],
            "headline": c["headline"], "source_url": c["source_url"]}


def _hist(row: dict) -> dict:
    return {"id": row["id"], "kind": "history", "title": row["source_title"], "date": row["event"],
            "fact_en": row["fact"], "fact_es": row["quote"], "quote": row["quote"], "url": row["source_url"],
            "status": row["confidence"]}


def _cat(row: dict) -> dict:
    return {"id": row["id"], "kind": "action", "title": {"es": row["name_es"], "en": row["name_en"]},
            "date": "", "fact_en": row["action"], "fact_es": row["recommendation_quote"],
            "quote": row["recommendation_quote"], "url": row["recommendation_source_url"],
            "status": row["cost_status"]}


def _enfen(c: dict) -> dict:
    number = re.sub(r"^ENFEN-(\d{4})-(\d+)$", r"\2-\1", c["id"])
    return {"id": c["id"], "kind": "enfen", "title": f"Comunicado Oficial ENFEN N° {number}", "date": c["date"],
            "fact_en": f"{c['status']}: {c['headline']}", "fact_es": c["key_quote"], "quote": c["key_quote"],
            "url": c["source_url"], "status": "verified"}


def _fx() -> dict:
    fx = data_store.exchange_rate()
    text = f"S/ {fx['pen_per_usd']} per US$ ({fx['series_name']})"
    return {"id": FX_SOURCE_ID, "kind": "exchange_rate", "title": fx["publisher"], "date": fx["date"],
            "fact_en": text, "fact_es": f"S/ {fx['pen_per_usd']} por US$ ({fx['series_name']})", "quote": "",
            "url": fx["human_readable_url"], "status": "verified"}


SPANISH_HINTS = re.compile(r"\b(de|la|el|los|las|que|en|del|por|para|con|una|se|su)\b|[ñáéíóú]", re.IGNORECASE)
ENGLISH_HINTS = re.compile(r"\b(the|and|of|to|with|is|are|in|for|your|from|by|at)\b", re.IGNORECASE)


def text_language(text: str) -> str:
    """'es' or 'en', from simple word hints; used to tell the owner when a quote is in the other language."""
    es, en = len(SPANISH_HINTS.findall(text or "")), len(ENGLISH_HINTS.findall(text or ""))
    return "es" if es >= en else "en"


def _with_languages(d: dict) -> dict:
    """fact_en is Pirca's own English summary for history and catalog rows; only verbatim quotes are guessed."""
    if d["kind"] in ("history", "action"):
        d["lang_en"] = "en"
        d["lang_es"] = text_language(d["fact_es"])
    elif d["kind"] == "enfen":
        d["lang_en"] = d["lang_es"] = "es"  # ENFEN publishes in Spanish only
    else:
        d["lang_en"], d["lang_es"] = "en", "es"
    return d


def describe_sources(ids) -> dict[str, dict]:
    """Details for each known ID; unknown IDs are skipped (verify_draft reports them).
    fact_en / fact_es are the texts to show in each interface language; lang_en / lang_es say
    which language each text is really in (a quote stays in its original language)."""
    hist = {r["id"]: r for r in data_store.historical_impacts()}
    cat = {r["id"]: r for r in data_store.action_catalog()}
    enfen = {c["id"]: c for c in enfen_index()}
    out = {}
    for i in ids:
        if i in hist:
            out[i] = _hist(hist[i])
        elif i in cat:
            out[i] = _cat(cat[i])
        elif i in enfen:
            out[i] = _enfen(enfen[i])
        elif i == FX_SOURCE_ID:
            out[i] = _fx()
    return {k: _with_languages(v) for k, v in out.items()}


def cited_ids(*texts: str) -> list[str]:
    """Source IDs cited in the given texts, in order of first appearance."""
    seen = []
    for text in texts:
        for m in SOURCE_ID_PATTERN.finditer(text or ""):
            if m.group(0) not in seen:
                seen.append(m.group(0))
    return seen
