"""Write output/tokenomics.md from measured runs only (the saved example plans).

Run from the Final Project folder:
    .venv\\Scripts\\python.exe -m backend.tokenomics_report
"""

import json
from statistics import mean

from backend import config
from backend.agents import AGENT_TOOLS
from backend.tools.data_store import exchange_rate
from backend.tools.drafting import MAX_PLAN_WORDS, plan_word_count

RUN_CODES = ["PIU-CAST26", "PIU-CASTEN", "PIU-FARMES", "PIU-FARMEN", "PIU-FERRES", "PIU-FERREN"]
AGENTS = [("manager", "Manager"), ("risk_analyst", "Risk Analyst"), ("planner", "Planner"), ("critic", "Critic")]
P = config.PRICES_PER_MILLION

# Measured before the 300-word limit (Prompt 14): `git show 8bba882:output/sample_run.json`.
BASELINE_COMMIT = "8bba882"
BASELINE_PROSE_WORDS = 524
BASELINE_FINAL_MANAGER_OUTPUT = 1440

# PIU-CASTEN repeated a request already made in the browser (PIU-SGEMMT: same shop, language and day), so the
# Portkey gateway replayed the saved responses: same plan, same token counts, 0.3 s per call instead of ~3 s.
# Its numbers are the measurement of the original PIU-SGEMMT run, counted once.
GATEWAY_REPLAYS = {"PIU-CASTEN": "PIU-SGEMMT"}

# ---- Assumptions (labelled in the report) ----
RUNS_PER_SHOP_PER_MONTH = 2   # 1 new plan + 1 update, each a full agent run
SHOP_COUNTS = (100, 10_000)


def load(code: str) -> dict:
    return json.loads((config.PLANS_DIR / "examples" / f"{code}.json").read_text(encoding="utf-8"))


def input_cost(u: dict) -> float:
    regular = u["input_tokens"] - u["cached_input_tokens"] - u["cache_write_tokens"]
    return (regular * P["input"] + u["cached_input_tokens"] * P["cached_input"]
            + u["cache_write_tokens"] * P["cache_write"]) / 1e6


def output_cost(u: dict) -> float:
    return u["output_tokens"] * P["output"] / 1e6


def usd(x: float, d: int = 4) -> str:
    return f"${x:,.{d}f}"


def pen(x_usd: float, d: int = 2) -> str:
    return f"S/ {x_usd * exchange_rate()['pen_per_usd']:,.{d}f}"


def n(x) -> str:
    return f"{x:,.0f}"


def main() -> None:
    fx = exchange_rate()
    runs = []
    for code in RUN_CODES:
        r = load(code)
        final_manager = [e for e in r["events"] if e["type"] == "model_call" and e["agent"] == "manager"][-1]["call"]
        runs.append({
            "code": code, "shop": f"{r['form']['business_type']} · {r['form']['district']}", "lang": r["language"],
            "status": r["status"], "verified": (r.get("verification") or {}).get("ok"), "usage": r["usage"],
            "by_agent": r["usage_by_agent"], "facts": len(r.get("facts", {})),
            "code_tools": sum(1 for e in r["events"] if e["type"] == "tool_called" and e["tool"] not in AGENT_TOOLS),
            "words": plan_word_count(r.get("plan_template", "")), "final_manager_output": final_manager["output_tokens"],
            "translations": r.get("translations", {}), "revision": r.get("revision_used"),
        })
    U = [r["usage"] for r in runs]
    cols = ["model_calls", "input_tokens", "cached_input_tokens", "cache_write_tokens", "output_tokens", "cost_usd"]
    totals = {c: sum(u[c] for u in U) for c in cols}
    avg_cost = mean(u["cost_usd"] for u in U)
    min_cost, max_cost = min(u["cost_usd"] for u in U), max(u["cost_usd"] for u in U)
    # Every finished plan is now translated automatically, so a plan = one agent run + one translation.
    tr = [(c["code"], lang, t["usage"]) for c in runs for lang, t in c["translations"].items()]
    avg_tr = mean(u["cost_usd"] for _, _, u in tr)
    tr_cost = {c["code"]: sum(t["usage"]["cost_usd"] for t in c["translations"].values()) for c in runs}
    plan_costs = [r["usage"]["cost_usd"] + tr_cost[r["code"]] for r in runs]
    avg_plan, min_plan, max_plan = mean(plan_costs), min(plan_costs), max(plan_costs)

    L = []
    a = L.append
    a("# Pirca tokenomics")
    a("")
    a(f"Every number below is measured from {len(runs)} real end-to-end runs of the Pirca agent system "
      f"(model `{config.MODEL_NAME}` through Portkey), saved in `plans/examples/`, unless it is marked **Assumption**. "
      "Prices are the course's gpt-6-luna prices from the MGT 409 Lecture 11 Tokenomics slides, in USD per 1M tokens: "
      f"input ${P['input']}, cached input ${P['cached_input']}, cache write ${P['cache_write']}, output ${P['output']}. "
      f"Soles use the fixed BCRP rate of S/ {fx['pen_per_usd']} per US$ ({fx['date']}, series {fx['series_code']}).")
    a("")
    a("Costs cover model tokens only. **Assumption:** hosting, storage, staff and outreach costs are not included.")
    a("")

    # 1 ---------------------------------------------------------------- per run
    a("## 1. Cost per run")
    a("")
    a("| Run | Shop | Lang | Result | Model calls | Input | Cached input | Cache write | Output | Run cost | Translation | Plan cost |")
    a("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in runs:
        u = r["usage"]
        result = "verified" if r["verified"] else "warning shown"
        label = f"{r['code']}†" if r["code"] in GATEWAY_REPLAYS else r["code"]
        a(f"| {label} | {r['shop']} | {r['lang']} | {result} | {u['model_calls']} | {n(u['input_tokens'])} | "
          f"{n(u['cached_input_tokens'])} | {n(u['cache_write_tokens'])} | {n(u['output_tokens'])} | {usd(u['cost_usd'])} | "
          f"{usd(tr_cost[r['code']])} | {usd(u['cost_usd'] + tr_cost[r['code']])} |")
    tr_vals = list(tr_cost.values())
    for label, fn in (("**Average**", mean), ("Min", min), ("Max", max)):
        vals = {c: fn([u[c] for u in U]) for c in cols}
        a(f"| {label} | | | | {vals['model_calls']:.1f} | {n(vals['input_tokens'])} | {n(vals['cached_input_tokens'])} | "
          f"{n(vals['cache_write_tokens'])} | {n(vals['output_tokens'])} | {usd(vals['cost_usd'])} | {usd(fn(tr_vals))} | "
          f"{usd(fn(plan_costs))} |")
    a("")
    for code, original in GATEWAY_REPLAYS.items():
        a(f"† {code} sent exactly the same requests as an earlier browser run ({original}: same shop, language and day), "
          f"so the Portkey gateway replayed the saved responses (24 calls in 8.6 s instead of 60–160 s). Its numbers are "
          f"the measurement of {original}'s original run and are counted once. Our counter prices replayed calls at full "
          "price; whether the gateway bills them was not verified.")
        a("")
    a("PIU-CAST26 was run earlier the same day (Prompt 18), before the Critic's code check was enforced in code; "
      "prompts and model were the same. The other five runs used the current code.")
    a("")
    a(f"An agent run costs **{usd(avg_cost)} on average** ({pen(avg_cost, 3)}), between {usd(min_cost)} and "
      f"{usd(max_cost)} across the {len(runs)} runs. {sum(1 for r in runs if r['revision'])} of {len(runs)} runs used the "
      "one allowed Planner revision after the Critic asked for changes.")
    a("")
    a(f"Every finished plan is now also translated automatically into the other language (one model call, tokens recorded "
      f"separately). Each run's translation is measured above; the average is {usd(avg_tr)}. "
      f"**A complete bilingual plan therefore costs {usd(avg_plan)} on average** ({pen(avg_plan, 3)}), between "
      f"{usd(min_plan)} and {usd(max_plan)}.")
    a("")

    # 2 ---------------------------------------------------------------- by agent
    a("## 2. Cost by agent")
    a("")
    a("Summed over all runs. Input-side cost includes regular, cached and cache-write input tokens.")
    a("")
    a("| Agent | Model calls | Input | Output | Input-side cost | Output cost | Total | Share |")
    a("|---|---:|---:|---:|---:|---:|---:|---:|")
    agent_rows = []
    for key, name in AGENTS:
        us = [r["by_agent"][key] for r in runs if key in r["by_agent"]]
        agg = {c: sum(u[c] for u in us) for c in cols}
        ic, oc = sum(input_cost(u) for u in us), sum(output_cost(u) for u in us)
        agent_rows.append((name, agg, ic, oc))
        a(f"| {name} | {agg['model_calls']} | {n(agg['input_tokens'])} | {n(agg['output_tokens'])} | {usd(ic)} | "
          f"{usd(oc)} | {usd(agg['cost_usd'])} | {agg['cost_usd'] / totals['cost_usd']:.0%} |")
    a("")
    top = max(agent_rows, key=lambda x: x[1]["cost_usd"])
    name, agg, ic, oc = top
    driver = "output tokens" if oc > ic else "input tokens"
    a(f"**The {name} costs the most** ({agg['cost_usd'] / totals['cost_usd']:.0%} of all spending). "
      f"{oc / (ic + oc):.0%} of its cost is output: it writes long JSON drafts and reasons before answering, and output "
      f"tokens cost {P['output'] / P['input']:.0f}× more than input tokens. "
      f"It made {agg['model_calls']} model calls across {len(runs)} runs, because each tool round trip is a new call "
      f"that resends the growing conversation. Its main cost driver is **{driver}**.")
    a("")
    for nm, ag, i_c, o_c in agent_rows:
        if nm == name:
            continue
        a(f"- **{nm}:** {ag['cost_usd'] / totals['cost_usd']:.0%} of cost, {ag['model_calls']} calls, "
          f"{o_c / (i_c + o_c):.0%} of it from output tokens.")
    a("")

    # 3 ---------------------------------------------------------------- caching
    cached, written = totals["cached_input_tokens"], totals["cache_write_tokens"]
    actual = totals["cost_usd"]
    full_cached = actual + cached * (P["input"] - P["cached_input"]) / 1e6
    no_cache = full_cached - written * (P["cache_write"] - P["input"]) / 1e6
    a("## 3. Caching savings")
    a("")
    a(f"Across all runs, **{cached / totals['input_tokens']:.0%} of input tokens were read from the cache** "
      f"({n(cached)} of {n(totals['input_tokens'])}).")
    a("")
    a("| Scenario | Cost of all runs | Per run |")
    a("|---|---:|---:|")
    a(f"| Actual (measured) | {usd(actual)} | {usd(actual / len(runs))} |")
    a(f"| Cached tokens charged at the full input price | {usd(full_cached)} | {usd(full_cached / len(runs))} |")
    a(f"| No caching at all (also no cache-write premium) | {usd(no_cache)} | {usd(no_cache / len(runs))} |")
    a("")
    a(f"Charging every cached token at the full input price would have cost {usd(full_cached)} instead of "
      f"{usd(actual)}: **caching saved {(full_cached - actual) / full_cached:.0%}** ({usd(full_cached - actual)} on these "
      "runs). Writing to the cache costs "
      f"${P['cache_write']} instead of ${P['input']} per 1M tokens; counting that premium, the net saving against no "
      f"caching at all is {(no_cache - actual) / no_cache:.0%}.")
    a("")

    # 4 ---------------------------------------------------------------- measures
    a("## 4. Cost-cutting measures and their evidence")
    a("")
    a(f"1. **Caching of static prompts.** Each agent's system prompt is static (shared rules + its own file) and every "
      f"call sends a `prompt_cache_key` per agent; run data goes in the user message. Evidence: "
      f"{cached / totals['input_tokens']:.0%} of input tokens were cached reads, saving {usd(full_cached - actual)} "
      f"({(full_cached - actual) / full_cached:.0%}) on these runs (section 3).")
    a(f"2. **Numbers computed in code, not by the model.** On average each run made "
      f"{mean(r['code_tools'] for r in runs):.1f} deterministic tool calls that produced {mean(r['facts'] for r in runs):.0f} "
      "facts (amounts, days, weeks, percentages) at zero model tokens; the model only writes `{fact_key}` placeholders, "
      "and `verify_draft` rejects typed numbers. The model never spends output tokens doing arithmetic.")
    a("3. **Saved plans reopen for 0 tokens.** `GET /api/plans/{code}` reads `plans/{code}.json`; no model is called "
      "(offline test `test_example_plans_open_without_running_agents` asserts zero runs). Reopening, switching currency "
      "and replaying the trace are free.")
    if tr:
        rows = "; ".join(f"{code} → {lang}: {usd(u['cost_usd'])} ({u['model_calls']} call)" for code, lang, u in tr)
        a(f"4. **Translation instead of rerunning.** Each plan's second language comes from one translation call, "
          f"not a second agent run. Measured translations: {rows}. Average {usd(avg_tr)}, which is "
          f"**{avg_tr / avg_cost:.1%} of an average agent run** ({usd(avg_cost)}) — about {avg_cost / avg_tr:.0f}× cheaper "
          "than running the agents again in the other language. Switching language afterwards costs 0 tokens.")
    a(f"5. **The 300-word plan limit.** Before the limit (commit `{BASELINE_COMMIT}`), the final plan had "
      f"{BASELINE_PROSE_WORDS} prose words and the Manager's final call produced {n(BASELINE_FINAL_MANAGER_OUTPUT)} output "
      f"tokens. With the limit, plans averaged {mean(r['words'] for r in runs):.0f} words "
      f"(max {max(r['words'] for r in runs)}) and the final call averaged "
      f"{n(mean(r['final_manager_output'] for r in runs))} output tokens. Other prompt changes landed at the same time, so "
      "this is a before/after observation, not a controlled experiment."
      + "".join(f" {r['code']} ({r['words']} words) still went over the limit after its fix attempt and is shown "
                "with a warning." for r in runs if r["words"] > MAX_PLAN_WORDS and not r["verified"]))
    a("")

    # 5 ---------------------------------------------------------------- scale
    per_shop_month = RUNS_PER_SHOP_PER_MONTH * avg_plan
    a("## 5. Cost at scale")
    a("")
    a(f"**Assumption:** each shop gets **{RUNS_PER_SHOP_PER_MONTH} full agent runs per month** (1 new plan + 1 update), "
      "each priced at the measured average bilingual plan cost (agent run + automatic translation). Reopening saved plans "
      "is free; hosting is not included.")
    a("")
    a("| Shops | Per month (USD) | Per month (S/) | Per year (USD) | Per year (S/) | Range per year (USD) |")
    a("|---:|---:|---:|---:|---:|---|")
    a(f"| 1 | {usd(per_shop_month)} | {pen(per_shop_month, 3)} | {usd(per_shop_month * 12)} | {pen(per_shop_month * 12)} | "
      f"{usd(RUNS_PER_SHOP_PER_MONTH * min_plan * 12)}–{usd(RUNS_PER_SHOP_PER_MONTH * max_plan * 12)} |")
    for shops in SHOP_COUNTS:
        m = per_shop_month * shops
        a(f"| {shops:,} | {usd(m, 2)} | {pen(m)} | {usd(m * 12, 2)} | {pen(m * 12)} | "
          f"{usd(RUNS_PER_SHOP_PER_MONTH * min_plan * 12 * shops, 2)}–{usd(RUNS_PER_SHOP_PER_MONTH * max_plan * 12 * shops, 2)} |")
    a("")

    # 6 ---------------------------------------------------------------- organization
    year_10k = per_shop_month * 12 * 10_000
    a("## 6. Organization view")
    a("")
    a(f"A municipality or chamber of commerce offering Pirca to **10,000 shops** would pay about **{usd(year_10k, 0)} "
      f"({pen(year_10k, 0)}) per year in model costs**, under the assumption above (2 bilingual plans per shop per month, "
      "model tokens only — hosting, support and outreach would be extra).")
    a("")
    a("Comparison with a consultant-written plan: **no sourced figure was found.** Searches on 2026-10-24 for consultant "
      "prices for a small-business continuity or contingency plan in Peru (in soles) and internationally returned only "
      "academic theses, legal guidance (Ley N° 28551, RM N° 188-2015-PCM) and one 2009 UK figure that bundles equipment, "
      "so no comparison is made.")
    a("")
    a("## Assumptions in this report")
    a("")
    a(f"- {RUNS_PER_SHOP_PER_MONTH} full runs per shop per month (1 plan + 1 update), each costing the measured average.")
    a("- Each plan includes its automatic translation; model token costs only (hosting, storage, staff and outreach excluded).")
    a(f"- Prices fixed at the Lecture 11 gpt-6-luna rates; exchange rate fixed at S/ {fx['pen_per_usd']} per US$.")
    a(f"- {len(runs)} runs is a small sample: real costs vary with how often the Critic asks for a revision and how "
      "many tools each agent calls.")
    a("")
    (config.OUTPUT_DIR / "tokenomics.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {config.OUTPUT_DIR / 'tokenomics.md'}")


if __name__ == "__main__":
    main()
