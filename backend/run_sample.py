"""Run one sample shop through the whole Pirca agent system and print the trace.

Run from the Final Project folder (this makes real, paid model calls):
    .venv\\Scripts\\python.exe -m backend.run_sample
    .venv\\Scripts\\python.exe -m backend.run_sample --language en --currency usd
"""

import argparse
import json
import sys
from datetime import date

from backend import config
from backend.agents.pirca import run_plan

DEFAULT_PROFILE = config.PLANS_DIR / "examples" / "sample_shop_castilla.json"


def describe(event: dict) -> str:
    t = event["type"]
    if t == "tool_called":
        args = json.dumps(event["args"], ensure_ascii=False)
        return f"→ {event['tool']}({args if args != '{}' else ''})"
    if t == "tool_result":
        r = event["result"]
        extra = r.get("error") or (f"ok={r['ok']}" if "ok" in r else f"{len(r.get('facts', {}))} facts")
        return f"← {event['tool']}: {extra}"
    if t == "model_call":
        c = event["call"]
        return (f"model call: in {c['input_tokens']:,} (cached {c['cached_input_tokens']:,}, "
                f"cache write {c['cache_write_tokens']:,}), out {c['output_tokens']:,}")
    if t == "agent_started":
        return f"▶ started (run {event['run']})"
    if t == "agent_finished":
        return f"■ finished: {', '.join(event['keys'])}"
    if t == "limit_hit":
        return f"⛔ LIMIT {event['limit']} ({event['action']}): {event['detail']}"
    if t == "final_check":
        kinds = ", ".join(sorted(set(event.get("issues", [])))) or "none"
        return f"verify_draft on final plan (attempt {event['attempt']}): ok={event['ok']}, issues: {kinds}"
    if t in ("run_started", "run_finished"):
        return f"{t} {event.get('status', '')}".strip()
    return t


def print_event(event: dict) -> None:
    tot = event["totals"]
    print(f"[{event['elapsed_s']:6.1f}s] {event['agent']:<12} {describe(event):<75} "
          f"| {tot['total_tokens']:>8,} tok  ${tot['cost_usd']:.4f}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--language", choices=["es", "en"], default="es")
    parser.add_argument("--currency", choices=["pen", "usd"], default="pen")
    parser.add_argument("--example-code", help="Also save the run as plans/examples/{code}.json, e.g. PIU-CAST26")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    profile = json.loads(open(args.profile, encoding="utf-8").read())
    print(f"Pirca sample run · {profile['business_type']} in {profile['district']} · model {config.MODEL_NAME}\n")
    result = run_plan(profile, language=args.language, today=date.today(), on_event=print_event)

    print(f"\nStatus: {result['status']}")
    if result["status"] in ("stopped_by_limit", "error", "invalid_profile"):
        print(result.get("message") or result.get("errors"))
    else:
        print(f"Verification: ok={result['verification']['ok']}, fix attempted={result['verification']['fix_attempted']}")
        print(f"Critic verdict: {result['critic_verdict']} · revision used: {result['revision_used']}")
        a = result["affordability"]
        print(f"Affordability: recommends S/ {a['total']:,.2f} of spending; cash on hand S/ {a['cash_on_hand']:,.2f}; "
              f"within cash: {a['within_cash']}")
        print("\n" + "=" * 80 + f"\nPLAN ({args.currency.upper()})\n" + "=" * 80)
        print(result["plan"][args.currency])
        print("=" * 80)
        print(f"\nSummary: {result['summary_en']}")
        for d in result["decisions"]:
            print(f"Decision: {d.get('decision')} — {d.get('reason')}")
        for issue in result["open_issues"]:
            print(f"Open issue: {issue}")

    print("\nToken usage by agent:")
    for agent, u in result.get("usage_by_agent", {}).items():
        print(f"  {agent:<12} calls {u['model_calls']:>2}  in {u['input_tokens']:>8,}  cached {u['cached_input_tokens']:>7,}"
              f"  cache write {u['cache_write_tokens']:>7,}  out {u['output_tokens']:>7,}  ${u['cost_usd']:.4f}")
    u = result.get("usage", {})
    if u:
        print(f"  {'TOTAL':<12} calls {u['model_calls']:>2}  in {u['input_tokens']:>8,}  cached {u['cached_input_tokens']:>7,}"
              f"  cache write {u['cache_write_tokens']:>7,}  out {u['output_tokens']:>7,}  ${u['cost_usd']:.4f}")

    # Every finished plan is also translated into the other language (one model call, tokens recorded apart).
    from backend.api import plans
    result["form"] = profile
    plans.add_translation(result)
    for lang, tr in result.get("translations", {}).items():
        print(f"  {'TRANSLATION':<12} -> {lang}: calls {tr['usage']['model_calls']}, out {tr['usage']['output_tokens']:,}, "
              f"${tr['usage']['cost_usd']:.4f}, check ok={tr['verification']['ok']}")

    out = config.OUTPUT_DIR / "sample_run.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"\nFull result and trace saved to {out.relative_to(config.PROJECT_ROOT)}")
    if args.example_code:
        if not plans.is_valid_code(args.example_code):
            raise SystemExit(f"Invalid code {args.example_code}: use PIU- plus 6 of {plans.CODE_ALPHABET}")
        example = config.PLANS_DIR / "examples" / f"{args.example_code}.json"
        plans.write_plan(example, plans.plan_record(args.example_code, profile, args.language, result))
        print(f"Example plan saved to {example.relative_to(config.PROJECT_ROOT)}")
    return 0 if result["status"].startswith("completed") else 1


if __name__ == "__main__":
    sys.exit(main())
