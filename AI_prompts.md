# AI Prompts Log

## Prompt 1

`Today we will be working in folder final project. Create AI_prompts.md at the start of the assignment and keep it updated as you work . This file is the log of what I typed to you`

## Prompt 2 — Project setup

`we are going to create`

```
MGT 409 final project: "Pirca", an AI agent app that helps small shop owners in Piura, Peru prepare their business for El Niño costero rains and floods.
Setup:

* Python only (no Node). FastAPI backend that also serves a plain HTML/CSS/JS frontend.
* Create a local .venv in this folder and a requirements.txt (fastapi, uvicorn, openai, python-dotenv, pydantic, pytest).
* Load .env from this folder first, then one level above it. Never print or log the key.
* Model: gpt-6-luna through Portkey, using PORTKEY_API_KEY, base_url https://api.portkey.ai/v1, header x-portkey-provider: openai. Put the model name in one config file.
* Make one tiny test call to confirm the key and model work, and print only "OK" plus the token usage.
* Add .gitignore (.env, .venv, pycache, plans/* except plans/examples/), a .env.example with PORTKEY_API_KEY= and no value, and git init.
* Folder layout: backend/ (agents, tools, prompts, API), frontend/, data/, plans/examples/, tests/, output/.
```

## Prompt 3 — Git safe directory

`Yes, add Final Project as a git safe.directory in my global config.`

## Prompt 4 — First commit

`Commit the working tree changes with a sensible message.`

## Prompt 5 — Data files with real sources

```
Build the data files the Pirca agents will use. Every fact must come from a real, citable source; never invent figures. If you can't find a source for something, leave it out or mark it "UNVERIFIED" so I can check it. Keep any downloaded raw files (PDFs, pages) in data/raw/, separate from the code.

1. data/enfen/: the most recent official ENFEN communiqués (comunicados oficiales) about El Niño costero, saved as text. Each one gets an ID (ENFEN-YYYY-NN), date, status (e.g. alert or no alert), and source URL.
2. data/historical_impacts.csv: impacts in Piura from the 1997-98 and 2017 El Niño events (flooded districts, road and bridge cuts, business losses, closure duration, dengue). One row per fact, with an ID (HIST-1998-NN, HIST-2017-NN), district, value, unit, and source URL.
3. data/districts.csv: Piura region districts (Piura, Castilla, Veintiséis de Octubre, Catacaos, Sullana, Paita, Talara, Chulucanas, and others) with a flood hazard level and the HIST IDs that justify it.
4. data/action_catalog.csv: about 15 preparation actions for small shops (raise shelves, sandbags, sealed containers, door barrier, moving stock upstairs, emergency cash, backup of records, supplier stock-up, mosquito control for dengue, insurance, etc.). Each has an ID (CAT-NN), hazards it addresses, cost range in soles, a "protects" factor, and a source URL, or "illustrative estimate" if no source exists.
5. data/exchange_rate.json: one fixed USD/PEN rate from the BCRP (Banco Central de Reserva del Perú) with its date and URL.

At the end, write output/sources.md listing every number with its source URL and whether it is verified, sourced, or an illustrative estimate, so I can check them.
```

## Prompt 6 — Commit data, keep raw downloads local

`Commit the data files and sources.md, but add data/raw/ to .gitignore so the 92 MB of downloads stay local.`

## Prompt 7 — Deterministic agent tools

```
In backend/tools.py (or backend/tools/), write the deterministic tools the Pirca agents will call. All money is computed in soles. Each tool returns JSON with a "facts" object (named numbers, e.g. {"stock_at_risk": 10000}) plus any source IDs it used.

Intake form fields: business type, district, near river/drain/ravine (yes/no/unknown), flooded in 2017 or 2023 (yes/no/unknown), floor level, higher storage available (second floor/mezzanine/none), owned or rented, stock value, share of stock below 1 m, perishables (yes/no), cash on hand, monthly fixed costs, weekly sales, number of workers, up to 3 suppliers (product + city), days of stock on hand, prep budget, and a checklist of things they already have.

Tools:
- validate_profile: required fields, sensible ranges, and warnings when things don't add up (e.g. prep budget larger than cash, ground floor with no higher storage and no budget). If the district's data is UNVERIFIED (currently Paita and Sechura), return a warning saying so.
- score_exposure: exposure score, risk level (high/medium/low), stock_at_risk.
- compute_stock_move: how much stock to move and where.
- compute_cash_buffer: weeks closed (based on the historical data), weekly fixed costs, buffer needed, cash gap.
- compute_supplier_buffer: road-cut risk per supplier city, and extra days of stock to buy.
- get_action_catalog: actions that match the hazards, excluding things the owner already has. Keep each action's "illustrative estimate" flag.
- optimize_budget: pick the best set of actions within the budget (knapsack). Zero-cost actions are always included. Return selected, total, money left, and excluded with a reason. Mark which selected actions use illustrative estimates.
- search_documents and get_historical_impacts: simple keyword search over data/ (never data/raw/) that returns snippets with source IDs.
- run_scenario: recompute numbers for "rains_one_month_early", "long_closure", "main_bridge_cut", "power_cut_week", "worker_sick_dengue".
- verify_draft: flags raw numbers that should be placeholders, unknown {fact_keys}, unknown source IDs, and forbidden content (evacuation orders, the app's own forecasts). Years, months, and digits inside source IDs are allowed.
- fill_placeholders: replace {fact_key} with formatted values in soles (S/ 10,000) or USD ($2,650) using the fixed rate in data/exchange_rate.json.

Write pytest tests for each tool that run offline (no API calls), including a test that an UNVERIFIED district produces a warning and that illustrative-estimate actions stay flagged.
```

## Prompt 8 — Commit tools

`Commit the working tree changes with a sensible message.`
