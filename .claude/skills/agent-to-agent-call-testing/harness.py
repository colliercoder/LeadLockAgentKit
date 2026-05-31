#!/usr/bin/env python3
"""Agent-to-agent call testing — real-call functional harness.

Two real Leadlock agents call each other over real Twilio so call-time features
(e.g. {{caller_phone}}, custom functions, end_call) are verified against the
TRUE production call path — not faked by a simulator or the browser playground.

Why this exists: bot-vs-bot simulation and the browser voice playground do NOT
create a call_log with a real `from_number`, so they give a FALSE PASS for
anything that depends on call metadata (the {{caller_phone}} variable, contact
intelligence, outbound context). The only path that exercises those is a real
Twilio call — which is exactly what this harness places.

```
[user-sim agent +1AAA] --outbound call--> [agent-under-test +1BBB]
        |  (real Twilio call, From=+1AAA, To=+1BBB)        |
        |                                                   v
        |                              inbound call_log.from_number = +1AAA
        |                              {{caller_phone}} resolves to +1AAA
        v
   transcript pulled via GET /calls/{id}  -->  verify the feature fired
```

Auth: API key only (X-API-Key). Reads LEADLOCK_API_KEY + LEADLOCK_API_URL from
.env in the kit root. Tenant is inferred from the key; pass --sub-account-id for
an agency key that should act on a specific sub-account.

Stdlib only (urllib) — no pip install needed, same as the rest of the kit.

Usage:
    python harness.py --verify-contract                       # contract self-check
    python harness.py --user-number-id A --under-number-id B --dry-run
    python harness.py --user-number-id A --under-number-id B --only caller_phone
    python harness.py --user-number-id A --under-number-id B   # full sweep

A and B are phone_numbers.id values (two voice-capable numbers on your account).
The harness records each number's current agent before borrowing it and restores
it in a finally block, so a production assignment is put back even if the run
crashes. Prefer UNASSIGNED numbers — see the SKILL.md safety notes.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from test_cases import TEST_CASES, expand_placeholders


# ---------------------------------------------------------------------------
# Config (.env in the kit root — same convention as the rest of the kit)
# ---------------------------------------------------------------------------


def _load_env() -> dict[str, str]:
    """Read .env from the kit root. Walk up from this file until one is found."""
    env: dict[str, str] = {}
    here = Path(__file__).resolve()
    candidates = [here.parent / ".env"] + [p / ".env" for p in here.parents]
    for path in candidates:
        if path.is_file():
            for line in path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
            break
    for k in ("LEADLOCK_API_KEY", "LEADLOCK_API_URL", "LEADLOCK_API_BASE", "LEADLOCK_SUB_ACCOUNT_ID"):
        if os.environ.get(k):  # process env overrides .env file values
            env[k] = os.environ[k]
    return env


class Cfg:
    _env = _load_env()
    api_key = _env.get("LEADLOCK_API_KEY", "").strip()
    api_url = _env.get("LEADLOCK_API_BASE", _env.get("LEADLOCK_API_URL", "https://leadlock-app.onrender.com")).rstrip("/")
    sub_id = _env.get("LEADLOCK_SUB_ACCOUNT_ID", "").strip()  # optional, agency keys
    # Optional Twilio creds — used ONLY as a runaway backstop to force-end a call
    # if two AI agents fail to hang up on their own. The agents' own end_call tool
    # + a goal-driven user-sim are the primary end mechanism.
    twilio_sid = _env.get("LEADLOCK_TWILIO_SID", "").strip()
    twilio_auth = _env.get("LEADLOCK_TWILIO_AUTH", "").strip()

    # Resolved at runtime from the two --*-number-id flags (or their env fallbacks):
    num_under_pid = ""
    num_under_e164 = ""
    num_under_restore = ""  # agent_id the number had before we borrowed it
    num_user_pid = ""
    num_user_e164 = ""
    num_user_restore = ""


def require_api_key() -> None:
    if not Cfg.api_key:
        sys.exit(
            "Missing LEADLOCK_API_KEY. Copy .env.example to .env in the kit root "
            "and paste your key (Settings -> API Keys in the Leadlock dashboard)."
        )


# ---------------------------------------------------------------------------
# Minimal HTTP client (stdlib urllib, X-API-Key auth)
# ---------------------------------------------------------------------------


class Resp:
    """Tiny response wrapper so callers can use .status_code/.text/.json()/.raise_for_status()."""

    def __init__(self, status: int, body: bytes) -> None:
        self.status_code = status
        self._body = body

    @property
    def text(self) -> str:
        return self._body.decode("utf-8", "replace")

    def json(self):
        return json.loads(self._body or b"null")

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}: {self.text[:300]}")


class Api:
    def __init__(self) -> None:
        self.base = Cfg.api_url

    def h(self, json_body: bool) -> dict[str, str]:
        hdr = {"X-API-Key": Cfg.api_key}
        if json_body:
            hdr["Content-Type"] = "application/json"
        if Cfg.sub_id:
            hdr["X-Sub-Account-Id"] = Cfg.sub_id
        return hdr

    def req(self, method: str, path: str, body: dict | None = None) -> Resp:
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(
            self.base + path, data=data, method=method, headers=self.h(body is not None)
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as r:
                resp = Resp(r.status, r.read())
        except urllib.error.HTTPError as e:
            resp = Resp(e.code, e.read())
        if resp.status_code >= 400:
            print(f"  {method} {path} -> {resp.status_code}: {resp.text[:280]}")
        return resp

    def openapi(self) -> dict:
        request = urllib.request.Request(self.base + "/openapi.json", headers={"X-API-Key": Cfg.api_key})
        with urllib.request.urlopen(request, timeout=60) as r:
            return json.loads(r.read())


REQUIRED_PATHS = {
    "/agents": "post",
    "/agents/{agent_id}": "patch",
    "/outbound/agents/{agent_id}/call": "post",
    "/calls/{call_log_id}": "get",
    "/phone-numbers/{phone_number_id}": "patch",
}


def verify_contract(api: Api) -> list[str]:
    paths = api.openapi().get("paths", {})
    problems = []
    for path, method in REQUIRED_PATHS.items():
        prefix = path.split("{")[0]
        if not any(p.split("{")[0] == prefix and method in paths[p] for p in paths):
            problems.append(f"MISSING: {method.upper()} {path}")
    return problems


# ---------------------------------------------------------------------------
# Phone-number resolution (borrow two numbers, remember how to restore them)
# ---------------------------------------------------------------------------


def resolve_number(api: Api, phone_number_id: str) -> tuple[str, str]:
    """Return (e164, current_agent_id) for a phone_numbers.id, so we can place the
    call and restore the prior assignment afterward.

    current_agent_id is "" when the number is currently unassigned (the safe case).
    """
    r = api.req("GET", f"/phone-numbers/{phone_number_id}")
    if r.status_code >= 400:
        sys.exit(
            f"Could not load phone number {phone_number_id} ({r.status_code}). "
            "Pass a valid phone_numbers.id from GET /phone-numbers."
        )
    data = r.json()
    e164 = data.get("phone_number") or data.get("number") or ""
    agent_id = data.get("agent_id") or ""
    if not e164:
        sys.exit(f"Phone number {phone_number_id} has no E.164 number on record.")
    return e164, agent_id


def load_numbers(api: Api, user_id: str, under_id: str) -> None:
    """Resolve both borrowed numbers and warn if either is on a live agent."""
    Cfg.num_user_pid = user_id
    Cfg.num_under_pid = under_id
    Cfg.num_user_e164, Cfg.num_user_restore = resolve_number(api, user_id)
    Cfg.num_under_e164, Cfg.num_under_restore = resolve_number(api, under_id)
    for label, pid, restore in (
        ("user-sim", user_id, Cfg.num_user_restore),
        ("under-test", under_id, Cfg.num_under_restore),
    ):
        if restore:
            print(
                f"  [warn] {label} number {pid} is currently assigned to agent "
                f"{restore}. It will be borrowed for the test and restored after. "
                "Inbound calls to it during the test (~1-2 min) would hit the test "
                "agent. Prefer an UNASSIGNED number."
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def spoken(e164: str) -> str:
    if e164.startswith("+1") and len(e164) == 12:
        return f"({e164[2:5]}) {e164[5:8]}-{e164[8:]}"
    return e164


def transcript_text(call: dict) -> str:
    t = call.get("transcript")
    if isinstance(t, str):
        try:
            t = json.loads(t)
        except (ValueError, TypeError):
            return t
    if isinstance(t, list):
        return "\n".join(
            f"{x.get('role', '?')}: {x.get('content', '')}" if isinstance(x, dict) else str(x)
            for x in t
        )
    return ""


# Agent field defaults that avoid the create-time validation traps. Both agents
# always get end_call so the scenario can hang up once the user-sim's goal is met
# — two AI agents otherwise chat until max duration.
UNDER_BASE = {
    "agent_mode": "inbound",
    "voice_provider": "xai",
    "ai_speaks_first": True,
    "tools_enabled": ["end_call"],
    "max_call_duration_minutes": 2,
}
USER_BASE = {
    "agent_mode": "outbound",
    "voice_provider": "xai",
    "ai_speaks_first": False,  # outbound agent: no inbound greeting needed
    "ai_speaks_first_outbound": True,
    "greeting": "Hello.",  # dummy so create passes
    "tools_enabled": ["end_call"],
    "max_call_duration_minutes": 2,
}


def _merge_tools(base: dict, override: dict) -> dict:
    """Merge agent config, UNIONing tools_enabled so end_call is never dropped."""
    merged = {**base, **override}
    tools = set(base.get("tools_enabled") or []) | set(override.get("tools_enabled") or [])
    if tools:
        merged["tools_enabled"] = sorted(tools)
    return merged


def _poll_until_complete(api: "Api", agent_id: str, settle_s: int = 75, max_s: int = 240) -> dict | None:
    """Poll the agent's latest call_log to a terminal status.

    Two AI agents may not hang up on their own, so after `settle_s` of the call
    being live we force-end it via the optional Twilio backstop, then keep polling
    so the terminal log (transcript + transitions + performance_metrics) is
    captured. Returns the terminal call dict, the last live call, or None.
    """
    deadline = time.monotonic() + max_s
    live: dict | None = None
    forced = False
    TERMINAL = ("completed", "failed", "no-answer", "busy", "canceled")
    while time.monotonic() < deadline:
        lr = api.req("GET", f"/calls?agent_id={agent_id}&limit=1")
        items = lr.json()
        items = items if isinstance(items, list) else items.get("items") or items.get("calls") or []
        if items:
            full = api.req("GET", f"/calls/{items[0]['id']}").json()
            live = full
            if full.get("status") in TERMINAL:
                return full
            if not forced and full.get("twilio_call_sid"):
                if time.monotonic() > deadline - max_s + settle_s:
                    print(f"  [backstop] force-ending live call after {settle_s}s: {force_end_call(full)}")
                    forced = True
        time.sleep(10)
    return live


def force_end_call(call: dict) -> str:
    """Runaway backstop: end a still-live call via the Twilio API.

    No-op (returns 'no-twilio-creds') if Twilio creds aren't configured — the
    agents' end_call tool is the primary mechanism.
    """
    sid = call.get("twilio_call_sid") or call.get("provider_call_sid")
    if not sid:
        return "no-sid"
    if not (Cfg.twilio_sid and Cfg.twilio_auth):
        return "no-twilio-creds"
    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{Cfg.twilio_sid}/Calls/{sid}.json"
        data = urllib.parse.urlencode({"Status": "completed"}).encode()
        auth = base64.b64encode(f"{Cfg.twilio_sid}:{Cfg.twilio_auth}".encode()).decode()
        request = urllib.request.Request(
            url,
            data=data,
            method="POST",
            headers={"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(request, timeout=30) as r:
            return f"twilio-end-{r.status}"
    except Exception as e:  # noqa: BLE001 - backstop must never raise
        return f"twilio-end-error:{e}"


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


def run_case(api: Api, case: dict, dry_run: bool) -> dict:
    name = case["name"]
    ph = {
        "user_sim_number_spoken": spoken(Cfg.num_user_e164),
        "under_test_number_spoken": spoken(Cfg.num_under_e164),
    }
    under_cfg = _merge_tools(UNDER_BASE, {"name": "LOOPTEST-under", **expand_placeholders(case["under_test"], ph)})
    user_cfg = _merge_tools(USER_BASE, {"name": "LOOPTEST-user", **expand_placeholders(case["user_sim"], ph)})

    under_id = user_id = None
    try:
        r = api.req("POST", "/agents", under_cfg)
        r.raise_for_status()
        under_id = r.json()["id"]
        r = api.req("POST", "/agents", user_cfg)
        r.raise_for_status()
        user_id = r.json()["id"]

        api.req("PATCH", f"/phone-numbers/{Cfg.num_under_pid}", {"agent_id": under_id}).raise_for_status()
        api.req("PATCH", f"/phone-numbers/{Cfg.num_user_pid}", {"agent_id": user_id}).raise_for_status()

        if dry_run:
            return {"name": name, "keyword_passed": True, "keyword_detail": "dry-run: configured, call skipped"}

        r = api.req(
            "POST",
            f"/outbound/agents/{user_id}/call",
            {"to_number": Cfg.num_under_e164, "from_phone_number_id": Cfg.num_user_pid},
        )
        r.raise_for_status()

        call = _poll_until_complete(api, under_id)
        if not call:
            return {"name": name, "keyword_passed": False, "keyword_detail": "no call_log appeared within timeout"}

        text = transcript_text(call)
        expected = [
            e.replace("{user_sim_number_spoken}", ph["user_sim_number_spoken"]).replace(
                "{under_test_number_spoken}", ph["under_test_number_spoken"]
            )
            for e in case.get("expect_in_transcript", [])
        ]
        missing = [e for e in expected if e.lower() not in text.lower()]
        # keyword_passed is only a cheap pre-signal. The REAL verdict is the
        # Claude Code session judging the transcript against judge_question.
        return {
            "name": name,
            "keyword_passed": not missing,
            "keyword_detail": "ok" if not missing else f"missing: {missing}",
            "judge_question": case.get("judge_question", ""),
            "expected_in_transcript": expected,
            "from_number": call.get("from_number"),
            "status": call.get("status"),
            "duration_seconds": call.get("duration_seconds"),
            "transcript": text,
        }
    finally:
        # Restore numbers to their prior assignment, delete the two test agents.
        api.req("PATCH", f"/phone-numbers/{Cfg.num_user_pid}", {"agent_id": Cfg.num_user_restore or None})
        api.req("PATCH", f"/phone-numbers/{Cfg.num_under_pid}", {"agent_id": Cfg.num_under_restore or None})
        for aid in (under_id, user_id):
            if aid:
                api.req("DELETE", f"/agents/{aid}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--verify-contract", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--only")
    p.add_argument("--user-number-id", default=os.environ.get("LEADLOCK_NUM_USER_PID", ""),
                   help="phone_numbers.id of the number the user-sim agent calls FROM")
    p.add_argument("--under-number-id", default=os.environ.get("LEADLOCK_NUM_UNDER_PID", ""),
                   help="phone_numbers.id of the number the agent-under-test receives ON")
    p.add_argument("--sub-account-id", default=Cfg.sub_id,
                   help="X-Sub-Account-Id for an agency key acting on a sub-account")
    p.add_argument(
        "--out",
        default="/tmp/agent_loop_results.json",
        help="Where to write the results JSON the Claude session reads to judge.",
    )
    args = p.parse_args()

    require_api_key()
    if args.sub_account_id:
        Cfg.sub_id = args.sub_account_id

    api = Api()

    problems = verify_contract(api)
    if problems:
        print("CONTRACT DRIFT - refusing to run:")
        for x in problems:
            print("  -", x)
        return 2
    print("Contract check: OK")
    if args.verify_contract:
        return 0

    if not (args.user_number_id and args.under_number_id):
        sys.exit("Need --user-number-id and --under-number-id (two phone_numbers.id values).")
    load_numbers(api, args.user_number_id, args.under_number_id)

    cases = [c for c in TEST_CASES if not c.get("skip") and (not args.only or c["name"] == args.only)]
    if not cases:
        print(f"No active case matches --only {args.only!r}")
        return 1

    results = []
    for case in cases:
        print(f"\n=== {case['name']} ===")
        res = run_case(api, case, args.dry_run)
        results.append(res)
        kw = res.get("keyword_passed")
        print(f"  keyword pre-signal: {'pass' if kw else 'FAIL'} - {res.get('keyword_detail', '')}")
        if res.get("from_number"):
            print(f"  inbound from_number: {res['from_number']}")
        if res.get("judge_question"):
            print(f"  judge_question: {res['judge_question']}")
        if res.get("transcript"):
            print("  --- transcript ---")
            print("\n".join("  " + ln for ln in res["transcript"].splitlines()))

    # Write the full results so the Claude Code session can judge each transcript
    # against its judge_question. The harness does NOT call any LLM — the running
    # Claude session is the judge.
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {args.out}")
    print(
        "NEXT: the Claude session must read that file and render the real verdict "
        "per case (judge_question vs transcript). keyword_passed is only a pre-signal."
    )

    kw_passed = sum(1 for r in results if r.get("keyword_passed"))
    print(f"keyword pre-signal: {kw_passed}/{len(results)} (NOT the final verdict)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
