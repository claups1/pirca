# Pirca tokenomics

Every number below is measured from 6 real end-to-end runs of the Pirca agent system (model `gpt-6-luna` through Portkey), saved in `plans/examples/`, unless it is marked **Assumption**. Prices are the course's gpt-6-luna prices from the MGT 409 Lecture 11 Tokenomics slides, in USD per 1M tokens: input $0.1, cached input $0.01, cache write $0.125, output $0.5. Soles use the fixed BCRP rate of S/ 3.447 per US$ (2026-10-22, series PD04638PD).

Costs cover model tokens only. **Assumption:** hosting, storage, staff and outreach costs are not included.

## 1. Cost per run

| Run | Shop | Lang | Result | Model calls | Input | Cached input | Cache write | Output | Run cost | Translation | Plan cost |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PIU-CAST26 | bodega · Castilla | es | verified | 23 | 200,515 | 139,846 | 60,600 | 14,352 | $0.0162 | $0.0007 | $0.0168 |
| PIU-CASTEN† | bodega · Castilla | en | verified | 24 | 221,968 | 163,504 | 58,392 | 15,016 | $0.0164 | $0.0007 | $0.0171 |
| PIU-FARMES | botica · Piura | es | verified | 32 | 260,538 | 206,961 | 53,481 | 17,697 | $0.0176 | $0.0006 | $0.0182 |
| PIU-FARMEN | botica · Piura | en | verified | 31 | 243,893 | 189,209 | 54,591 | 18,682 | $0.0181 | $0.0006 | $0.0186 |
| PIU-FERRES | ferretería · Sullana | es | verified | 27 | 266,308 | 201,782 | 64,445 | 19,037 | $0.0196 | $0.0007 | $0.0203 |
| PIU-FERREN | ferretería · Sullana | en | verified | 31 | 287,321 | 219,386 | 67,842 | 18,863 | $0.0201 | $0.0008 | $0.0209 |
| **Average** | | | | 28.0 | 246,757 | 186,781 | 59,892 | 17,274 | $0.0180 | $0.0007 | $0.0187 |
| Min | | | | 23.0 | 200,515 | 139,846 | 53,481 | 14,352 | $0.0162 | $0.0006 | $0.0168 |
| Max | | | | 32.0 | 287,321 | 219,386 | 67,842 | 19,037 | $0.0201 | $0.0008 | $0.0209 |

† PIU-CASTEN sent exactly the same requests as an earlier browser run (PIU-SGEMMT: same shop, language and day), so the Portkey gateway replayed the saved responses (24 calls in 8.6 s instead of 60–160 s). Its numbers are the measurement of PIU-SGEMMT's original run and are counted once. Our counter prices replayed calls at full price; whether the gateway bills them was not verified.

PIU-CAST26 was run earlier the same day (Prompt 18), before the Critic's code check was enforced in code; prompts and model were the same. The other five runs used the current code.

An agent run costs **$0.0180 on average** (S/ 0.062), between $0.0162 and $0.0201 across the 6 runs. 6 of 6 runs used the one allowed Planner revision after the Critic asked for changes.

Every finished plan is now also translated automatically into the other language (one model call, tokens recorded separately). Each run's translation is measured above; the average is $0.0007. **A complete bilingual plan therefore costs $0.0187 on average** (S/ 0.064), between $0.0168 and $0.0209.

## 2. Cost by agent

Summed over all runs. Input-side cost includes regular, cached and cache-write input tokens.

| Agent | Model calls | Input | Output | Input-side cost | Output cost | Total | Share |
|---|---:|---:|---:|---:|---:|---:|---:|
| Manager | 52 | 699,428 | 20,205 | $0.0203 | $0.0101 | $0.0304 | 28% |
| Risk Analyst | 28 | 147,552 | 10,380 | $0.0061 | $0.0052 | $0.0113 | 10% |
| Planner | 52 | 323,030 | 44,948 | $0.0151 | $0.0225 | $0.0376 | 35% |
| Critic | 36 | 310,533 | 28,114 | $0.0147 | $0.0141 | $0.0287 | 27% |

**The Planner costs the most** (35% of all spending). 60% of its cost is output: it writes long JSON drafts and reasons before answering, and output tokens cost 5× more than input tokens. It made 52 model calls across 6 runs, because each tool round trip is a new call that resends the growing conversation. Its main cost driver is **output tokens**.

- **Manager:** 28% of cost, 52 calls, 33% of it from output tokens.
- **Risk Analyst:** 10% of cost, 28 calls, 46% of it from output tokens.
- **Critic:** 27% of cost, 36 calls, 49% of it from output tokens.

## 3. Caching savings

Across all runs, **76% of input tokens were read from the cache** (1,120,688 of 1,480,543).

| Scenario | Cost of all runs | Per run |
|---|---:|---:|
| Actual (measured) | $0.1080 | $0.0180 |
| Cached tokens charged at the full input price | $0.2089 | $0.0348 |
| No caching at all (also no cache-write premium) | $0.1999 | $0.0333 |

Charging every cached token at the full input price would have cost $0.2089 instead of $0.1080: **caching saved 48%** ($0.1009 on these runs). Writing to the cache costs $0.125 instead of $0.1 per 1M tokens; counting that premium, the net saving against no caching at all is 46%.

## 4. Cost-cutting measures and their evidence

1. **Caching of static prompts.** Each agent's system prompt is static (shared rules + its own file) and every call sends a `prompt_cache_key` per agent; run data goes in the user message. Evidence: 76% of input tokens were cached reads, saving $0.1009 (48%) on these runs (section 3).
2. **Numbers computed in code, not by the model.** On average each run made 26.3 deterministic tool calls that produced 125 facts (amounts, days, weeks, percentages) at zero model tokens; the model only writes `{fact_key}` placeholders, and `verify_draft` rejects typed numbers. The model never spends output tokens doing arithmetic.
3. **Saved plans reopen for 0 tokens.** `GET /api/plans/{code}` reads `plans/{code}.json`; no model is called (offline test `test_example_plans_open_without_running_agents` asserts zero runs). Reopening, switching currency and replaying the trace are free.
4. **Translation instead of rerunning.** Each plan's second language comes from one translation call, not a second agent run. Measured translations: PIU-CAST26 → en: $0.0007 (1 call); PIU-CASTEN → es: $0.0007 (1 call); PIU-FARMES → en: $0.0006 (1 call); PIU-FARMEN → es: $0.0006 (1 call); PIU-FERRES → en: $0.0007 (1 call); PIU-FERREN → es: $0.0008 (1 call). Average $0.0007, which is **3.6% of an average agent run** ($0.0180) — about 28× cheaper than running the agents again in the other language. Switching language afterwards costs 0 tokens.
5. **The 300-word plan limit.** Before the limit (commit `8bba882`), the final plan had 524 prose words and the Manager's final call produced 1,440 output tokens. With the limit, plans averaged 312 words (max 327) and the final call averaged 998 output tokens. Other prompt changes landed at the same time, so this is a before/after observation, not a controlled experiment.

## 5. Cost at scale

**Assumption:** each shop gets **2 full agent runs per month** (1 new plan + 1 update), each priced at the measured average bilingual plan cost (agent run + automatic translation). Reopening saved plans is free; hosting is not included.

| Shops | Per month (USD) | Per month (S/) | Per year (USD) | Per year (S/) | Range per year (USD) |
|---:|---:|---:|---:|---:|---|
| 1 | $0.0373 | S/ 0.129 | $0.4477 | S/ 1.54 | $0.4041–$0.5016 |
| 100 | $3.73 | S/ 12.86 | $44.77 | S/ 154.32 | $40.41–$50.16 |
| 10,000 | $373.08 | S/ 1,286.00 | $4,476.92 | S/ 15,431.94 | $4,040.88–$5,016.48 |

## 6. Organization view

A municipality or chamber of commerce offering Pirca to **10,000 shops** would pay about **$4,477 (S/ 15,432) per year in model costs**, under the assumption above (2 bilingual plans per shop per month, model tokens only — hosting, support and outreach would be extra).

Comparison with a consultant-written plan: **no sourced figure was found.** Searches on 2026-10-24 for consultant prices for a small-business continuity or contingency plan in Peru (in soles) and internationally returned only academic theses, legal guidance (Ley N° 28551, RM N° 188-2015-PCM) and one 2009 UK figure that bundles equipment, so no comparison is made.

## Assumptions in this report

- 2 full runs per shop per month (1 plan + 1 update), each costing the measured average.
- Each plan includes its automatic translation; model token costs only (hosting, storage, staff and outreach excluded).
- Prices fixed at the Lecture 11 gpt-6-luna rates; exchange rate fixed at S/ 3.447 per US$.
- 6 runs is a small sample: real costs vary with how often the Critic asks for a revision and how many tools each agent calls.

