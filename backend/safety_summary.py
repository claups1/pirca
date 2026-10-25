"""Write output/safety/summary.md from the results the safety tests saved.

Run from the Final Project folder after the tests:
    .venv\\Scripts\\python.exe -m pytest tests/test_safety.py            (offline: 2, 3, 5, 6)
    .venv\\Scripts\\python.exe -m pytest -m live tests/test_safety.py    (live: 1, 4)
    .venv\\Scripts\\python.exe -m backend.safety_summary
"""

import json

from backend import config

SAFETY_DIR = config.OUTPUT_DIR / "safety"
TITLES = {
    "1_prompt_injection": ("Prompt injection", "live"),
    "2_invented_number": ("Invented number and fake source", "offline"),
    "3_unaffordable_plan": ("Unaffordable plan", "offline"),
    "4_token_budget_limit": ("Token-budget limit", "live"),
    "5_no_evacuation_orders": ("No evacuation orders", "offline"),
    "6_risk_level_matches": ("Risk level matches the calculation", "offline"),
}


def calls(n: int) -> str:
    return f"{n} model call{'s' if n != 1 else ''}"


def key_evidence(name: str, e: dict) -> str:
    if name == "1_prompt_injection":
        excerpt = (e.get("suspicious_content") or [{}])[0].get("excerpt", "")
        return (f"Fake communiqué shown to the agent: {e['fake_document_shown_to_agent']}; instruction followed: "
                f"{e['instruction_followed']}; reported as suspicious: \"{excerpt}\" "
                f"({calls(e['usage']['model_calls'])}, ${e['usage']['cost_usd']:.4f}).")
    if name == "2_invented_number":
        found = ", ".join(f"{i['type']} `{i['text']}`" for i in e["verify_draft_issues"])
        return (f"verify_draft found {found}. Critic model said \"{e['critic_model_said']}\"; final verdict "
                f"\"{e['final_verdict']}\" (forced by code: {e['verdict_forced_by_code']}).")
    if name == "3_unaffordable_plan":
        issue = e["affordability_issues"][0]["detail"] if e["affordability_issues"] else "none"
        t = e["tools_with_200_cash"]
        return (f"{issue}. With S/ 200 cash the tools recommend S/ {t['recommended_spending']:,.2f}.")
    if name == "4_token_budget_limit":
        u = e.get("usage") or {}
        return (f"Status `{e['status']}`: \"{e['message']}\" ({calls(u.get('model_calls', 0))}, "
                f"${u.get('cost_usd', 0):.4f}).")
    if name == "5_no_evacuation_orders":
        caught = {lang: [i["text"] for i in issues] for lang, issues in e["issues"].items()}
        return f"Blocked phrases: {caught}. Pointing to INDECI allowed: {e['allowed_example_ok']}."
    if name == "6_risk_level_matches":
        run = e["run"]
        return (f"Shop risk `{e['shop_risk_level']}`. \"{e['wrong_section_1']}\" states `{e['wrong_stated']}` and "
                f"fails (risk_level_mismatch); \"{e['right_section_1']}\" states `{e['right_stated']}` first and "
                f"passes (ok: {e['right_ok']}). In a scripted run the first final check found "
                f"{run['final_checks'][0]['issues']}, the Manager's fix step ran ({run['fix_attempted']}) and the "
                f"run ended `{run['status']}`.")
    return ""


def main() -> None:
    lines = ["# Pirca safety checks", "",
             "Each test saves its evidence as JSON in this folder. Tests 2, 3, 5 and 6 run offline with every "
             "`pytest`; tests 1 and 4 make real model calls and run with `pytest -m live`.", "",
             "| # | Test | Type | What it checks | Result | Run at (UTC) |", "|---|---|---|---|---|---|"]
    details = []
    for name, (title, kind) in TITLES.items():
        path = SAFETY_DIR / f"{name}.json"
        if not path.exists():
            lines.append(f"| {name[0]} | {title} | {kind} | not run yet | — | — |")
            continue
        r = json.loads(path.read_text(encoding="utf-8"))
        lines.append(f"| {name[0]} | {title} | {kind} | {r['checks']} | **{r['result']}** | {r['run_at']} |")
        details.append(f"- **{name[0]}. {title}:** {key_evidence(name, r['evidence'])} Evidence: `{path.name}`.")
    lines += ["", "## Key evidence", "", *details, "",
              "## Shared computers", "",
              "The intake form keeps an owner's answers in the browser only until the plan is submitted; submitting, or "
              "\"+ Nuevo\", deletes them, so the next person on a shared computer starts with a blank form. If unfinished "
              "answers exist, the form still opens blank and asks \"¿Continuar donde quedaste?\" (Continuar / Empezar de "
              "nuevo). The sample shop fills the form for that visit only and is never saved. Checked in the browser on "
              "2026-10-24 (submit, \"+ Nuevo\", the resume banner and the sample shop).", ""]
    (SAFETY_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {SAFETY_DIR / 'summary.md'}")


if __name__ == "__main__":
    main()
