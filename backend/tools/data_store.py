"""Read-only access to the curated files in data/ (never data/raw/)."""

import csv
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

from backend import config

FX_SOURCE_ID = "BCRP-USDPEN"
SOURCE_ID_PATTERN = re.compile(r"\b(?:HIST-\d{4}-\d{2}|CAT-\d{2}|ENFEN-\d{4}-\d{2}|BCRP-[A-Z]+)\b")


def normalize(text: str) -> str:
    """Lowercase and strip accents so 'Veintiséis' matches 'veintiseis'."""
    text = unicodedata.normalize("NFKD", str(text))
    return "".join(c for c in text if not unicodedata.combining(c)).lower().strip()


def _read_csv(name: str) -> list[dict]:
    with open(config.DATA_DIR / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@lru_cache
def historical_impacts() -> list[dict]:
    return _read_csv("historical_impacts.csv")


@lru_cache
def districts() -> dict[str, dict]:
    """District rows keyed by normalized name."""
    return {normalize(r["district"]): r for r in _read_csv("districts.csv")}


@lru_cache
def action_catalog() -> list[dict]:
    rows = _read_csv("action_catalog.csv")
    for r in rows:
        r["hazards"] = r["hazards"].split(";")
        r["cost_min_pen"] = float(r["cost_min_pen"]) if r["cost_min_pen"] else None
        r["cost_max_pen"] = float(r["cost_max_pen"]) if r["cost_max_pen"] else None
        r["protects"] = float(r["protects"]) if r["protects"] else None
    return rows


@lru_cache
def exchange_rate() -> dict:
    return json.loads((config.DATA_DIR / "exchange_rate.json").read_text(encoding="utf-8"))


@lru_cache
def enfen_documents() -> list[dict]:
    """ENFEN communiqués with their header fields and body text."""
    docs = []
    for path in sorted((config.DATA_DIR / "enfen").glob("ENFEN-*.txt")):
        header, _, body = path.read_text(encoding="utf-8").partition("\n---\n")
        meta = dict(line.split(": ", 1) for line in header.splitlines() if ": " in line)
        docs.append({**meta, "body": body, "path": path})
    return docs


@lru_cache
def known_source_ids() -> frozenset[str]:
    ids = {r["id"] for r in historical_impacts()}
    ids |= {r["id"] for r in action_catalog()}
    ids |= {d["id"] for d in enfen_documents()}
    ids.add(FX_SOURCE_ID)
    return frozenset(ids)


def find_district(name: str) -> dict | None:
    return districts().get(normalize(name))


def data_files() -> list[Path]:
    """Every searchable file under data/, skipping data/raw/."""
    raw = config.DATA_DIR / "raw"
    return [p for p in sorted(config.DATA_DIR.rglob("*"))
            if p.is_file() and raw not in p.parents and p.suffix in {".csv", ".txt", ".json"}]
