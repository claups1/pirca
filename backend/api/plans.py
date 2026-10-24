"""Plan codes, saved plan files, background runs and one-call translations.

Every plan lives in plans/{code}.json (examples in plans/examples/{code}.json) and uses
the same format as output/sample_run.json, plus code, form, created_at and translations.
"""

import json
import re
import secrets
import threading
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

from backend import config
from backend.agents.pirca import _with_footer, run_plan
from backend.agents.usage import usage_from_response
from backend.tools import fill_placeholders, score_exposure, verify_draft
from backend.tools.drafting import PLACEHOLDER
from backend.tools.profile import district_level, parse_profile
from backend.tools.source_info import cited_ids, describe_sources

# No look-alikes: 0/O, 1/I/L are left out.
CODE_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
CODE_PATTERN = re.compile(rf"^PIU-[{CODE_ALPHABET}]{{6}}$")
STATUS_FROM_RESULT = {"completed": "done", "completed_with_warning": "done", "stopped_by_limit": "stopped"}

PLANS_DIR: Path = config.PLANS_DIR
_code_locks: dict[str, threading.Lock] = defaultdict(threading.Lock)  # one writer per plan file


def make_client():
    """Model client for translations (tests replace this)."""
    from backend.llm import get_client
    return get_client()


# ------------------------------------------------------------------ codes and files

def new_code() -> str:
    while True:
        code = "PIU-" + "".join(secrets.choice(CODE_ALPHABET) for _ in range(6))
        if code not in JOBS and find_plan_file(code) is None:
            return code


def is_valid_code(code: str) -> bool:
    return bool(CODE_PATTERN.match(code))


def plan_path(code: str) -> Path:
    return PLANS_DIR / f"{code}.json"


def find_plan_file(code: str) -> Path | None:
    for path in (PLANS_DIR / f"{code}.json", PLANS_DIR / "examples" / f"{code}.json"):
        if path.is_file():
            return path
    return None


def load_plan(code: str) -> dict | None:
    path = find_plan_file(code) if is_valid_code(code) else None
    return json.loads(path.read_text(encoding="utf-8")) if path else None


def write_plan(path: Path, data: dict) -> None:
    """Write atomically so a reader never sees half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    tmp.replace(path)


def plan_record(code: str, form: dict, language: str, result: dict) -> dict:
    """The saved file: run_plan's result (same as output/sample_run.json) plus who/when/translations."""
    return {"code": code, "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "form": form, "language": language, **result, "translations": result.get("translations", {})}


def status_of(record: dict) -> str:
    return STATUS_FROM_RESULT.get(record.get("status"), "error")


# ------------------------------------------------------------------ background runs

@dataclass
class Job:
    code: str
    form: dict
    language: str
    status: str = "running"
    events: list = field(default_factory=list)
    thread: threading.Thread | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)


JOBS: dict[str, Job] = {}


def _run_job(job: Job) -> None:
    def on_event(event: dict) -> None:
        with job.lock:
            job.events.append(event)

    try:
        result = run_plan(job.form, language=job.language, today=date.today(), on_event=on_event)
    except Exception as e:  # never leave a job stuck in "running"
        result = {"status": "error", "message": f"{type(e).__name__}: {e}", "events": list(job.events)}
    record = plan_record(job.code, job.form, job.language, result)
    add_translation(record, on_event=on_event)  # every finished plan is saved in both languages
    with _code_locks[job.code]:
        write_plan(plan_path(job.code), record)
    with job.lock:
        job.status = status_of(record)


def start_plan(form: dict, language: str) -> str:
    """Create a code now and run the agents in a background thread (survives the page closing)."""
    code = new_code()
    job = Job(code=code, form=form, language=language)
    JOBS[code] = job
    job.thread = threading.Thread(target=_run_job, args=(job,), name=f"pirca-{code}", daemon=True)
    job.thread.start()
    return code


def plan_status(code: str, after: int = 0) -> dict | None:
    """Status, events after sequence number `after`, and the result once finished."""
    job = JOBS.get(code)
    if job is not None:
        with job.lock:
            status, events = job.status, [e for e in job.events if e["seq"] > after]
        if status == "running":
            return {"code": code, "status": "running", "events": events, "result": None}
    record = load_plan(code)
    if record is None:
        return None
    events = [e for e in record.get("events", []) if e["seq"] > after]
    result = {k: v for k, v in record.items() if k != "events"}
    # Plain-language details for every cited source, so the interface can show footnotes instead of raw IDs.
    texts = [record.get("plan_template", "")] + [t.get("plan_template", "") for t in record.get("translations", {}).values()]
    result["source_details"] = describe_sources(cited_ids(*texts))
    if record.get("form"):  # deterministic risk level for the badge (never the model's wording)
        try:
            result["risk_level"] = score_exposure(record["form"])["risk_level"]
        except ValueError:
            result["risk_level"] = None
    return {"code": code, "status": status_of(record), "events": events, "result": result}


# ------------------------------------------------------------------ translation

def _placeholders(text: str) -> Counter:
    return Counter(m.group(1) for m in PLACEHOLDER.finditer(text))


# Length limits apply to the original plan; a faithful translation may not drop sentences to fit them.
LENGTH_ISSUES = {"too_long", "section_7_too_long"}


def _translation_issues(template: str, record: dict, target: str, unverified: bool) -> list[dict]:
    check = verify_draft(template, record.get("facts", {}), final_plan=True, language=target,
                         district_unverified=unverified)
    issues = [i for i in check["issues"] if i["type"] not in LENGTH_ISSUES]
    if _placeholders(template) != _placeholders(record["plan_template"]):
        issues.append({"type": "placeholders_changed", "text": "",
                       "detail": "The translation does not keep the same placeholders as the original plan"})
    return issues


def translate_plan(code: str) -> dict:
    """Translate the final plan to the other language with one model call; cache it in the plan file."""
    path = find_plan_file(code) if is_valid_code(code) else None
    if path is None:
        raise LookupError(code)
    with _code_locks[code]:  # a second click waits, then gets the cached translation
        record = json.loads(path.read_text(encoding="utf-8"))
        if status_of(record) != "done" or not record.get("plan_template"):
            raise ValueError("Only finished plans can be translated.")
        target = other_language(record)
        cached = record.setdefault("translations", {}).get(target)
        if cached:
            return {"code": code, "language": target, "cached": True, **cached}
        translation = translate_record(record)
        write_plan(path, record)
    return {"code": code, "language": target, "cached": False, **translation}


def other_language(record: dict) -> str:
    return "en" if record["language"] == "es" else "es"


def translate_record(record: dict, client=None) -> dict:
    """One model call: translate the final plan template, check it, fill it in both currencies,
    and store it in record["translations"][target] with its own token usage."""
    source, target = record["language"], other_language(record)
    response = (client or make_client()).responses.create(
        model=config.MODEL_NAME, instructions=(config.PROMPTS_DIR / "translator.md").read_text(encoding="utf-8"),
        input=[{"role": "user", "content": f"Translate from {source} to {target}:\n\n{record['plan_template']}"}],
        max_output_tokens=config.MAX_OUTPUT_TOKENS, reasoning={"effort": config.REASONING_EFFORT},
    )
    template = (getattr(response, "output_text", "") or "").strip().removeprefix("```markdown").strip("`").strip()
    usage = usage_from_response(response).as_dict()
    facts = record.get("facts", {})
    unverified = district_level(parse_profile(record["form"])) == "UNVERIFIED"
    issues = _translation_issues(template, record, target, unverified)
    plan = {cur: _with_footer(fill_placeholders(template, facts, currency=cur, language=target)["text"], target)
            for cur in ("pen", "usd")}
    translation = {"plan_template": template, "plan": plan, "usage": usage,
                   "verification": {"ok": not issues, "issues": issues},
                   "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    record.setdefault("translations", {})[target] = translation
    return translation


def add_translation(record: dict, on_event=None, client=None) -> None:
    """After a finished run: translate into the other language so every plan has both.
    A failure is recorded in the plan instead of losing the run."""
    if status_of(record) != "done" or not record.get("plan_template") or record.get("translations"):
        return
    events = record.setdefault("events", [])
    last = events[-1] if events else {"seq": 0, "elapsed_s": 0, "totals": {}}
    started = time.monotonic()
    try:
        tr = translate_record(record, client=client)
        detail = {"language": other_language(record), "usage": tr["usage"], "ok": tr["verification"]["ok"]}
    except Exception as e:  # keep the plan even if the translation fails
        record["translation_error"] = f"{type(e).__name__}: {e}"
        detail = {"language": other_language(record), "error": record["translation_error"]}
    event = {"seq": last.get("seq", len(events)) + 1, "type": "translation", "agent": "pirca",
             "elapsed_s": round(last.get("elapsed_s", 0) + time.monotonic() - started, 2), **detail,
             "totals": last.get("totals", {})}
    events.append(event)
    if on_event:
        on_event(event)
