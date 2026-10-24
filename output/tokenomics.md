# Pirca tokenomics

Every number below is measured from 6 real end-to-end runs of the Pirca agent system (model `gpt-6-luna` through Portkey), saved in `plans/examples/`, unless it is marked **Assumption**. Prices are the course's gpt-6-luna prices from the MGT 409 Lecture 11 Tokenomics slides, in USD per 1M tokens: input $0.1, cached input $0.01, cache write $0.125, output $0.5. Soles use the fixed BCRP rate of S/ 3.447 per US$ (2026-10-22, series PD04638PD).

Costs cover model tokens only. **Assumption:** hosting, storage, staff and outreach costs are not included.

## 1. Cost per run

| Run | Shop | Lang | Result | Model calls | Input | Cached input | Cache write | Output | Cost (USD) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| PIU-CAST26 | bodega · Castilla | es | verified | 23 | 200,515 | 139,846 | 60,600 | 14,352 | $0.0162 |
| PIU-CASTEN† | bodega · Castilla | en | verified | 24 | 221,968 | 163,504 | 58,392 | 15,016 | $0.0164 |
| PIU-FARMES | botica · Piura | es | verified | 32 | 260,538 | 206,961 | 53,481 | 17,697 | $0.0176 |
| PIU-FARMEN | botica · Piura | en | verified | 31 | 243,893 | 189,209 | 54,591 | 18,682 | $0.0181 |
| PIU-FERRES | ferretería · Sullana | es | warning shown | 28 | 247,777 | 191,582 | 56,111 | 16,979 | $0.0174 |
| PIU-FERREN | ferretería · Sullana | en | verified | 23 | 204,950 | 149,889 | 54,992 | 15,306 | $0.0160 |
| **Average** | | | | 26.8 | 229,940 | 173,498 | 56,361 | 16,339 | $0.0170 |
| Min | | | | 23.0 | 200,515 | 139,846 | 53,481 | 14,352 | $0.0160 |
| Max | | | | 32.0 | 260,538 | 206,961 | 60,600 | 18,682 | $0.0181 |

† PIU-CASTEN sent exactly the same requests as an earlier browser run (PIU-SGEMMT: same shop, language and day), so the Portkey gateway replayed the saved responses (24 calls in 8.6 s instead of 60–160 s). Its numbers are the measurement of PIU-SGEMMT's original run and are counted once. Our counter prices replayed calls at full price; whether the gateway bills them was not verified.

PIU-CAST26 was run earlier the same day (Prompt 18), before the Critic's code check was enforced in code; prompts and model were the same. The other five runs used the current code.

A full plan costs **$0.0170 on average** (S/ 0.058), between $0.0160 and $0.0181 across the 6 runs. 6 of 6 runs used the one allowed Planner revision after the Critic asked for changes.

## 2. Cost by agent

Summed over all runs. Input-side cost includes regular, cached and cache-write input tokens.

| Agent | Model calls | Input | Output | Input-side cost | Output cost | Total | Share |
|---|---:|---:|---:|---:|---:|---:|---:|
| Manager | 51 | 661,648 | 19,917 | $0.0192 | $0.0100 | $0.0291 | 29% |
| Risk Analyst | 30 | 143,268 | 9,850 | $0.0052 | $0.0049 | $0.0101 | 10% |
| Planner | 44 | 276,618 | 43,674 | $0.0145 | $0.0218 | $0.0364 | 36% |
| Critic | 36 | 298,107 | 24,591 | $0.0139 | $0.0123 | $0.0262 | 26% |

**The Planner costs the most** (36% of all spending). 60% of its cost is output: it writes long JSON drafts and reasons before answering, and output tokens cost 5× more than input tokens. It made 44 model calls across 6 runs, because each tool round trip is a new call that resends the growing conversation. Its main cost driver is **output tokens**.

- **Manager:** 29% of cost, 51 calls, 34% of it from output tokens.
- **Risk Analyst:** 10% of cost, 30 calls, 49% of it from output tokens.
- **Critic:** 26% of cost, 36 calls, 47% of it from output tokens.

## 3. Caching savings

Across all runs, **75% of input tokens were read from the cache** (1,040,991 of 1,379,641).

| Scenario | Cost of all runs | Per run |
|---|---:|---:|
| Actual (measured) | $0.1017 | $0.0170 |
| Cached tokens charged at the full input price | $0.1954 | $0.0326 |
| No caching at all (also no cache-write premium) | $0.1870 | $0.0312 |

Charging every cached token at the full input price would have cost $0.1954 instead of $0.1017: **caching saved 48%** ($0.0937 on these runs). Writing to the cache costs $0.125 instead of $0.1 per 1M tokens; counting that premium, the net saving against no caching at all is 46%.

## 4. Cost-cutting measures and their evidence

1. **Caching of static prompts.** Each agent's system prompt is static (shared rules + its own file) and every call sends a `prompt_cache_key` per agent; run data goes in the user message. Evidence: 75% of input tokens were cached reads, saving $0.0937 (48%) on these runs (section 3).
2. **Numbers computed in code, not by the model.** On average each run made 26.5 deterministic tool calls that produced 121 facts (amounts, days, weeks, percentages) at zero model tokens; the model only writes `{fact_key}` placeholders, and `verify_draft` rejects typed numbers. The model never spends output tokens doing arithmetic.
3. **Saved plans reopen for 0 tokens.** `GET /api/plans/{code}` reads `plans/{code}.json`; no model is called (offline test `test_example_plans_open_without_running_agents` asserts zero runs). Reopening, switching currency and replaying the trace are free.
4. **Translation instead of rerunning.** Measured translations: PIU-CAST26 → en: $0.0006 (1 call); PIU-FARMES → en: $0.0006 (1 call). Average $0.0006, which is **3.5% of an average full run** ($0.0170) — about 29× cheaper. A second request returns the saved translation for 0 tokens.
5. **The 300-word plan limit.** Before the limit (commit `8bba882`), the final plan had 524 prose words and the Manager's final call produced 1,440 output tokens. With the limit, plans averaged 313 words (max 331) and the final call averaged 1,037 output tokens. Other prompt changes landed at the same time, so this is a before/after observation, not a controlled experiment. One run (PIU-FERRES, 331 words) still went over the limit after its fix attempt and is shown with a warning.

## 5. Cost at scale

**Assumption:** each shop gets **2 full agent runs per month** (1 new plan + 1 update), priced at the measured average run cost. Translations, reopening saved plans and hosting are not included.

| Shops | Per month (USD) | Per month (S/) | Per year (USD) | Per year (S/) | Range per year (USD) |
|---:|---:|---:|---:|---:|---|
| 1 | $0.0339 | S/ 0.117 | $0.4070 | S/ 1.40 | $0.3848–$0.4336 |
| 100 | $3.39 | S/ 11.69 | $40.70 | S/ 140.29 | $38.48–$43.36 |
| 10,000 | $339.15 | S/ 1,169.05 | $4,069.80 | S/ 14,028.60 | $3,847.92–$4,335.84 |

## 6. Organization view

A municipality or chamber of commerce offering Pirca to **10,000 shops** would pay about **$4,070 (S/ 14,029) per year in model costs**, under the assumption above (2 runs per shop per month, model tokens only — hosting, support and outreach would be extra).

Comparison with a consultant-written plan: **no sourced figure was found.** Searches on 2026-10-24 for consultant prices for a small-business continuity or contingency plan in Peru (in soles) and internationally returned only academic theses, legal guidance (Ley N° 28551, RM N° 188-2015-PCM) and one 2009 UK figure that bundles equipment, so no comparison is made.

## Assumptions in this report

- 2 full runs per shop per month (1 plan + 1 update), each costing the measured average.
- Model token costs only: hosting, storage, staff, outreach and translations are excluded from the scale figures.
- Prices fixed at the Lecture 11 gpt-6-luna rates; exchange rate fixed at S/ 3.447 per US$.
- 6 runs is a small sample: real costs vary with how often the Critic asks for a revision and how many tools each agent calls.

