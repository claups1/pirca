# Pirca

Pirca helps small shop owners in Piura, Peru, prepare their business for El Niño costero. The owner answers a short
step-by-step form; four AI agents (Manager, Risk Analyst, Planner, Critic) read the latest ENFEN alert and Piura's flood
history from 1997-98, 2017 and 2023, and write a plan that fits the money the owner has. Every number in a plan is
computed by code and every fact is cited. MGT 409 (AI Foundations for Managers) final project.

## Run it

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m uvicorn backend.main:app --port 8020
```

Then open http://localhost:8020. Creating a new plan calls the model through Portkey and needs `PORTKEY_API_KEY` in
`.env` (see `.env.example`); never commit the key. Everything else (the start screen, the form's live risk gauge,
the example plans, replaying a trace, switching language or currency) works without the model.

## Try the example plans

These plans are saved in `plans/examples/` and open instantly with their code (no model call):

| Code | Shop | Run language |
|---|---|---|
| **PIU-CAST26** | bodega · Castilla (main example) | Spanish |
| PIU-CASTEN | bodega · Castilla | English |
| PIU-FARMES | botica · Piura | Spanish |
| PIU-FARMEN | botica · Piura | English |
| PIU-FERRES | ferretería · Sullana | Spanish |
| PIU-FERREN | ferretería · Sullana | English |

Every plan is saved in both languages; the language switch shows the other one without a new run.

## Tests

```
.venv\Scripts\python -m pytest            # offline tests (no model calls)
.venv\Scripts\python -m pytest -m live    # the two safety tests that call the model
```

## Data and sources

- `data/` holds every input the tools use. Each figure's source, status (verified, sourced, illustrative estimate,
  UNVERIFIED) and link is listed in [`output/sources.md`](output/sources.md); raw downloads stay in `data/raw/`
  (not committed).
- **District boundaries** on the start-screen map: `data/geo/piura_districts.geojson`, Piura region's 65 districts,
  built by `backend/build_piura_geo.py` from [pe-atlas 0.0.1](https://www.npmjs.com/package/pe-atlas)
  (`districts-100k.json`, MIT license, [github.com/ccalobeto/pe-atlas](https://github.com/ccalobeto/pe-atlas)), a TopoJSON
  redistribution of the 2022 edition of Peru's district boundary shapefiles published by
  [GeoGPS Perú](https://www.geogpsperu.com/) from INEI's limits. The script keeps Piura region (UBIGEO 20…), fixes a
  double-encoded name (PARIÑAS), adds province names from the UBIGEO codes and lightly simplifies the shapes.
- Flood-risk colors come from `data/districts.csv`; dengue 2023 cases per district come from the HIST-2023 rows of
  `data/historical_impacts.csv` (DIRESA Piura).
- Token use and cost per plan: [`output/tokenomics.md`](output/tokenomics.md). Safety tests:
  [`output/safety/summary.md`](output/safety/summary.md). Every prompt given to the coding assistant:
  [`AI_prompts.md`](AI_prompts.md).

Pirca is not an official forecast or a government agency. It never gives evacuation orders; follow ENFEN, SENAMHI,
INDECI and your municipality.
