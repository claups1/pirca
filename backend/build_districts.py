"""Rebuild data/districts.csv from data/historical_impacts.csv with Pirca's fixed rule.

The flood hazard level is derived by Pirca, not an official CENEPRED rating:
- high: the district is named as flooded in a HIST row, or a HIST row reports >= 5,000 people
  living in damaged homes there;
- medium: other district-level impacts only (roads, water, rainfall, dengue, smaller housing counts);
- UNVERIFIED: no district-level evidence found.

Run from the Final Project folder:
    .venv\\Scripts\\python.exe -m backend.build_districts
"""

import csv

from backend import config

DISTRICTS = [  # (district, province)
    ("Piura", "Piura"), ("Castilla", "Piura"), ("Veintiséis de Octubre", "Piura"), ("Catacaos", "Piura"),
    ("Cura Mori", "Piura"), ("La Arena", "Piura"), ("La Unión", "Piura"), ("El Tallán", "Piura"),
    ("Tambogrande", "Piura"), ("Chulucanas", "Morropón"), ("Sullana", "Sullana"), ("Bellavista", "Sullana"),
    ("Paita", "Paita"), ("Talara", "Talara"), ("Sechura", "Sechura"),
]
HOUSING_THRESHOLD = 5000


def _year(row: dict) -> str:
    return row["id"].split("-")[1]


def build(rows: list[dict]) -> list[dict]:
    out = []
    for name, province in DISTRICTS:
        mine = [r for r in rows if name in r["district"].split(";")]
        flood = [r for r in mine if r["topic"] == "flooding"]
        big_housing = [r for r in mine if r["topic"] == "housing" and r["unit"] == "persons"
                       and float(r["value"]) >= HOUSING_THRESHOLD]
        used = {r["id"] for r in flood + big_housing}
        other = [r for r in mine if r["id"] not in used]
        housing_years = sorted({_year(r) for r in big_housing})
        housing_label = "INEI 2017" if housing_years == ["2017"] else ", ".join(housing_years)
        if flood or big_housing:
            level = "high"
            basis = "Named as flooded in the historical record" if flood else \
                f"≥5,000 people in damaged homes ({housing_label})"
            if flood and big_housing:
                basis += f" and ≥5,000 people in damaged homes ({housing_label})"
        elif other:
            level = "medium"
            basis = "District-level impacts recorded (housing <5,000, roads, water, rainfall or dengue) but not named as flooded"
        else:
            level = "UNVERIFIED"
            basis = "No district-level impact found in sourced data; needs checking (e.g. CENEPRED scenario maps)"
        out.append({"district": name, "province": province, "flood_hazard_level": level, "basis": basis,
                    "flood_hist_ids": ";".join(r["id"] for r in flood + big_housing),
                    "other_hist_ids": ";".join(r["id"] for r in other)})
    return out


def main() -> None:
    with open(config.DATA_DIR / "historical_impacts.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    path = config.DATA_DIR / "districts.csv"
    with open(path, encoding="utf-8") as f:
        before = {r["district"]: r for r in csv.DictReader(f)}
    after = build(rows)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(after[0]))
        w.writeheader()
        w.writerows(after)
    for r in after:
        old = before.get(r["district"], {})
        if old.get("flood_hazard_level") != r["flood_hazard_level"]:
            print(f"LEVEL CHANGE {r['district']}: {old.get('flood_hazard_level')} -> {r['flood_hazard_level']}")
        added = set((r["flood_hist_ids"] + ";" + r["other_hist_ids"]).split(";")) - \
            set((old.get("flood_hist_ids", "") + ";" + old.get("other_hist_ids", "")).split(";")) - {""}
        if added:
            print(f"{r['district']}: added {sorted(added)}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
