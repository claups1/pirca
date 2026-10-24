"""Keyword search over the curated files in data/ (never data/raw/)."""

import csv
import io
import json

from backend.tools import data_store
from backend.tools.data_store import FX_SOURCE_ID, normalize


def _records() -> list[dict]:
    """Searchable records: one per CSV row, ENFEN paragraph, or JSON file, each with source IDs."""
    out = []
    for path in data_store.data_files():
        name = path.name
        if path.suffix == ".csv":
            for row in csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))):
                ids = [row["id"]] if "id" in row else [
                    i for i in (row.get("flood_hist_ids", "") + ";" + row.get("other_hist_ids", "")).split(";") if i]
                out.append({"file": name, "text": " | ".join(f"{k}: {v}" for k, v in row.items()), "sources": ids})
        elif name.startswith("ENFEN-"):
            doc = next(d for d in data_store.enfen_documents() if d["path"] == path)
            for para in doc["body"].split("\n"):
                if para.strip():
                    out.append({"file": name, "text": f"[{doc['date']}] {para.strip()}", "sources": [doc["id"]]})
        elif name == "exchange_rate.json":
            out.append({"file": name, "text": path.read_text(encoding="utf-8"), "sources": [FX_SOURCE_ID]})
        elif name == "index.json":
            for c in json.loads(path.read_text(encoding="utf-8"))["communiques"]:
                out.append({"file": name, "text": json.dumps(c, ensure_ascii=False), "sources": [c["id"]]})
    return out


def _snippet(text: str, terms: list[str], width: int = 220) -> str:
    norm = normalize(text)
    pos = min((norm.find(t) for t in terms if t in norm), default=0)
    start = max(0, pos - width // 3)
    snippet = text[start:start + width].strip()
    return ("…" if start else "") + snippet + ("…" if start + width < len(text) else "")


def search_documents(query: str, limit: int = 5) -> dict:
    """Rank records by how many query words they contain; return snippets with source IDs."""
    terms = [t for t in normalize(query).split() if len(t) > 2]
    hits = []
    for r in _records():
        norm = normalize(r["text"])
        score = sum(norm.count(t) for t in set(terms))
        matched = sum(t in norm for t in set(terms))
        if matched:
            hits.append((matched, score, r))
    hits.sort(key=lambda h: (-h[0], -h[1]))
    results = [{"file": r["file"], "snippet": _snippet(r["text"], terms), "sources": r["sources"]}
               for _, _, r in hits[:limit]]
    return {"tool": "search_documents", "query": query, "facts": {"result_count": len(results)},
            "sources": sorted({s for r in results for s in r["sources"]}), "results": results}


def get_historical_impacts(district: str | None = None, event: str | None = None,
                           topic: str | None = None, keyword: str | None = None,
                           include_region: bool = False) -> dict:
    """Filter historical_impacts.csv by district, event (1997-98 / 2017), topic or keyword."""
    rows = []
    for r in data_store.historical_impacts():
        districts = [normalize(d) for d in r["district"].split(";")]
        if district:
            in_district = normalize(district) in districts
            if not (in_district or (include_region and "piura region" in districts)):
                continue
        if event and normalize(event) not in (normalize(r["event"]), normalize(r["id"].split("-")[1])):
            continue
        if topic and normalize(topic) != normalize(r["topic"]):
            continue
        if keyword and normalize(keyword) not in normalize(r["fact"] + " " + r["quote"]):
            continue
        rows.append({k: r[k] for k in ("id", "event", "district", "topic", "fact", "value", "unit",
                                       "confidence", "source_url", "quote")})
    return {"tool": "get_historical_impacts", "facts": {"result_count": len(rows)},
            "sources": [r["id"] for r in rows], "results": rows}
