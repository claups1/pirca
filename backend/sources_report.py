"""Generate output/sources.md from the data files so it always matches them.

Run from the Final Project folder:
    .venv\\Scripts\\python.exe -m backend.sources_report
"""
import csv
import json

from backend import config

ROOT = config.PROJECT_ROOT
D = config.DATA_DIR


def read(name):
    with open(D / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


hist, dist, cat = read("historical_impacts.csv"), read("districts.csv"), read("action_catalog.csv")
fx = json.loads((D / "exchange_rate.json").read_text(encoding="utf-8"))
enfen = json.loads((D / "enfen" / "index.json").read_text(encoding="utf-8"))

L = []
a = L.append
a("# Pirca data sources\n")
a("Every number in `data/`, with its source and status. Generated 2026-10-24.\n")
a("**Status legend**")
a("- **verified**: read in an official / primary / peer-reviewed document saved in `data/raw/`, and spot-checked against that file.")
a("- **sourced**: read in a real source, but a secondary one (press, chamber of commerce, retail listing), or used as a proxy / derived value.")
a("- **illustrative estimate**: no source found; a placeholder for the app's math. Replace when you find a source.")
a("- **UNVERIFIED**: no source found; needs your check before use.\n")

a("## 1. ENFEN communiqués (`data/enfen/`)\n")
a("All four are official PDFs from the Comisión Multisectorial ENFEN (verified). Status in all four: **Alerta de El Niño Costero**.\n")
a("| ID | Date | Number(s) quoted | Status | Source |")
a("|---|---|---|---|---|")
nums = {"ENFEN-2026-15": "≥62% probability of extraordinary magnitude Sep 2026–Jan 2027 (Niño 1+2); ≥58% very strong (Niño 3.4)",
        "ENFEN-2026-18": "Reservoirs at 58% of national hydraulic capacity",
        "ENFEN-2026-17": "—", "ENFEN-2026-16": "—"}
for c in enfen["communiques"]:
    a(f"| {c['id']} | {c['date']} | {nums[c['id']]} | verified | [PDF]({c['source_url']}) |")
a("\nNext communiqué announced for 2026-10-30; re-check https://enfen.imarpe.gob.pe/comunicados/ before relying on these.\n")

a("## 2. Exchange rate (`data/exchange_rate.json`)\n")
a("| Number | Meaning | Status | Source |")
a("|---|---|---|---|")
a(f"| {fx['pen_per_usd']} | S/ per US$, {fx['series_name']}, {fx['date']} (raw {fx['raw_value']}) | verified | [BCRPData {fx['series_code']}]({fx['human_readable_url']}) |\n")

a("## 3. Historical impacts (`data/historical_impacts.csv`)\n")
a("| ID | District | Value | Unit | Fact | Status | Source |")
a("|---|---|---|---|---|---|---|")
for r in hist:
    a(f"| {r['id']} | {esc(r['district'])} | {r['value']} | {esc(r['unit'])} | {esc(r['fact'])} | {r['confidence']} | [{esc(r['source_title'].split(',')[0])}]({r['source_url']}) |")
a("")
a("**Figures seen but NOT included (UNVERIFIED or conflicting; check before using):**")
for t in [
    "\"120,000 damnificados/afectados in Piura\" for 1997-98: one El Peruano piece says 1997-98, another places it in 1983.",
    "1998 Río Piura peak \"casi 3,900 m3/s\" (La República 2026, quoting an engineer) vs 4,424 m3/s in CAF and PAHO.",
    "1983 Río Piura peak: CAF 2,478 m3/s vs PAHO 2,300 m3/s.",
    "1998 Miraflores station 777.3 mm (PAHO citing UDEP): period unclear.",
    "2017 Río Piura flow in press: \"3,100 m3/s según Senamhi\", \"excedió 2,500\" vs INDECI's 3,468 m3/s.",
    "2017 COEN totals for Piura vary by cut-off date: 14,933/211,184 (mid-Mar); 18,996/225,492 (Mar); 41,925/349,471 (21 Apr); 91,835/310,570 (El Comercio 2018); 97,708/427,693 (Peru21, not fetched). The CSV uses the 21 Apr figures for roads/bridges and the El Comercio figures for people.",
    "2017 Piura dengue deaths: press/IGP say 33, 53 or 61; DIRESA says 14 by week 25 and 17 for the outbreak (CSV uses 17).",
    "2017 losses of S/10,000 million (Agraria.pe), US$400 million to 10 Apr (Camcopiura), and Piura's 31% share of 15,129 SBS insurance claims: not read in a source.",
    "School restart date of 20 Mar 2017 in Piura: not confirmed for 2017; the confirmed 20 Mar postponement is 2023 (HIST-2023-31).",
    "Not found: duration of the 2017 Piura airport closure; days the Panamericana Piura–Chiclayo was closed in 2017.",
    "OCHA Sitrep 06 (Apr 2017) \"318,871 affected in Piura\": ReliefWeb blocked (403).",
    "ARCC/PIRCC Piura counts (170 roads, 117 bridges): Congreso PDF 404. MCLCP confirms only \"Presupuesto inicial ... 7,541 millones\".",
    "2023 rain deaths: INDECI's table gives 12 (cut 19 Jul 2023, HIST-2023-08); MINSA COE Salud gives 21 (7 Jun 2023). They count different things; the CSV uses INDECI.",
    "2023 dengue: 79,643 cases / 148 deaths (calendar year, DIRESA SE 20-2024; used) vs 79,998 / 153 at the 13 Dec 2023 cut (SE 49): likely later reclassification, not confirmed.",
    "2023 rain on 24 Mar: 94.5 mm (Infomercado citing SENAMHI; used) vs 101.8 mm in a truncated SENAMHI social-media post that does not name the station.",
    "2023 INDECI road lengths (1,045,739.82 m affected / 364,172.4 m destroyed): left out because the table columns could be rural paths or highways.",
    "2023 district damage beyond damnificados and afectados (homes destroyed, uninhabitable) was left out: blank cells make the later columns ambiguous in the extracted table.",
    "Not confirmed (search summaries only, not used): 82 dengue deaths and 42,415 cases in June 2023; 222 schools damaged; 227 damnificados on 10 Mar 2023; Río Piura 1,204 m3/s; Huarmaca 94.5 mm; S/13,000 million losses (Piura, Lambayeque and Tumbes combined).",
    "Not found for 2023: an exact closure in days of the Panamericana Norte (Piura–Chiclayo, Sullana–Talara, Piura–Chulucanas); any sourced effect of dengue on work, schools or businesses.",
]:
    a(f"- {t}")
a("")

a("## 4. Districts (`data/districts.csv`)\n")
a("The flood hazard level is **derived by Pirca from the HIST rows above, not an official CENEPRED rating**.")
a("Rule: **high** = district named as flooded in a HIST row, or a HIST row with ≥5,000 people in damaged homes; "
  "**medium** = other district-level impacts only; **UNVERIFIED** = no district-level evidence found.\n")
a("| District | Province | Level | Flood HIST IDs | Other HIST IDs |")
a("|---|---|---|---|---|")
for r in dist:
    a(f"| {r['district']} | {r['province']} | {r['flood_hazard_level']} | {r['flood_hist_ids'].replace(';', ', ') or '—'} | {r['other_hist_ids'].replace(';', ', ') or '—'} |")
unverified = [r["district"] for r in dist if r["flood_hazard_level"] == "UNVERIFIED"]
a("\nChanges from adding 2023 (Prompt 26): **Paita UNVERIFIED → high** (INDECI field report: \"varias zonas aún continúan "
  "inundadas\", HIST-2023-27; 1,311 damnificados, HIST-2023-26) and **Sechura UNVERIFIED → medium** (district impacts "
  "without a flooding statement: HIST-2023-28 and the PE-04 road cut HIST-2023-29). No other level changed.")
a(f"\nUNVERIFIED districts now: {', '.join(unverified) if unverified else 'none'}. CENEPRED's scenario study "
  "(linked from ENFEN-2026-18: https://sigrid.cenepred.gob.pe/sigridv3/documento/22787) remains the best source to "
  "check the derived levels against.\n")

a("## 5. Action catalog (`data/action_catalog.csv`)\n")
a("Retail prices are Promart's public catalog (VTEX API) as seen on 2026-10-24; the API JSON is saved in `data/raw/actions/`. "
  "\"protects\" = share of the targeted loss the action avoids (0–1). Every recommendation quote was read in the linked source.\n")
a("| ID | Action | Cost S/ | Cost status | Cost source | Protects | Protects status | Protects source |")
a("|---|---|---|---|---|---|---|---|")
for r in cat:
    lo, hi = r["cost_min_pen"], r["cost_max_pen"]
    cost = "—" if not lo and not hi else (lo if lo == hi or not hi else f"{lo}–{hi}")
    if not hi and lo:
        cost = f"{lo}+"
    csrc = f"[link]({r['cost_source_url']})" if r["cost_source_url"] else "—"
    psrc = f"[link]({r['protects_source_url']})" if r["protects_source_url"] else "—"
    a(f"| {r['id']} | {esc(r['action'])} | {cost} ({esc(r['cost_unit'])}) | {r['cost_status']} | {csrc} | {r['protects']} | {r['protects_status']} | {psrc} |")
a("")
a("**Caveats to check**")
for t in [
    "All sourced \"protects\" factors come from non-Peruvian studies (German floods: Kreibich et al. 2005; global dengue meta-analysis: Bowman et al. 2016). Several are proxies (e.g. 'flood adapted use' stands in for raised shelves).",
    "CAT-09's 0.78 is 1 − odds ratio 0.22 for house screening (95% CI 0.05–0.93): an odds reduction, not a risk reduction.",
    "CAT-10's 0.95 is derived from Mapfre's 5% deductible (min S/500); insurance transfers loss rather than preventing it, and only up to the sum insured.",
    "CAT-04's S/500 is a municipal quebrada barrier in Trujillo, not a shop-door product. No Peruvian retail flood door barrier was found.",
    "CAT-07's Google One price is from Dec 2023; Google reportedly raised Peru prices in 2025 (no S/ figure found).",
    "Quantities in CAT-02, CAT-09 and CAT-11 (number of sacks, screens, sheets) are illustrative; the unit prices are sourced.",
    "No sourced recommendation was found for disaster-time theft/looting protection, so it is not in the catalog.",
]:
    a(f"- {t}")
a("")

a("## 6. URLs that failed during research\n")
for u in [
    "congreso.gob.pe ARCC Piura PDF (404); scioteca.caf.com (bot-blocked; CAF volume taken from dipecholac.net mirror)",
    "BCRP Piura síntesis Mar/Apr 2017 PDFs (bot-blocked); ReliefWeb OCHA sitreps (403); IEP Argumentos PDF (expired TLS certificate)",
    "indeci.gob.pe/recomendaciones (DNS); fema.gov fact sheets (403); ready.gov business flood pages (404); SELA continuity guide (404); NIBS Mitigation Saves (404)",
    "Mercado Libre Perú (captcha/403); SUNAT emprender (403); WhatsApp Business (400)",
]:
    a(f"- {u}")

(ROOT / "output" / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("wrote", len(L), "lines")
