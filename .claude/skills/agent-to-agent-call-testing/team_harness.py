#!/usr/bin/env python3
"""Agent Teams + Latency harness — extends agent-to-agent-call-testing.

TEAM MODE (--team): a user-sim calls a FRONT-DESK agent wired to department
agents (billing, sales, support) via `transfer_to_agents`. The user-sim asks for
one department; we verify the front desk actually hands off by reading
`call_logs.agent_transitions`. Department agents need NO phone number — transfer
swaps the live session brain on the existing call, so a team still uses only the
two borrowed numbers (user-sim + front-desk).

LATENCY MODE (--latency): place one real call per voice model and read
`metadata.performance_metrics` (time_to_first_audio, connect duration, avg/min/max
turn latency) from each completed call_log — a cross-provider table.

The harness is mechanical. The running Claude Code session is the judge (reads the
dumped JSON). No LLM API key is used here.

Verified config:
- transfer_to_agents = [{agent_id, name, when}]; `when` is the routing key.
- Do NOT add "transfer_to_agent" to tools_enabled by itself — the front desk must
  list BOTH it AND have non-empty transfer_to_agents (see comment below).
- Same voice_provider + same tenant for every team member; hop cap 3.
- agent_transitions: jsonb column [{agent_id, agent_name, started_at}];
  call_logs.agent_id stays the ORIGINATOR (front desk).
- transfer only works on xai / openai voices (gemini/elevenlabs decline the swap).

Usage:
    python team_harness.py --team --user-number-id A --under-number-id B
    python team_harness.py --latency --user-number-id A --under-number-id B
    python team_harness.py --latency --voices xai,openai-2 --user-number-id A --under-number-id B
Auth + numbers work exactly like harness.py (API key in .env, two phone ids).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from harness import (
    Api,
    Cfg,
    _poll_until_complete,
    load_numbers,
    require_api_key,
    transcript_text,
)

MAX_DURATION_MIN = 3  # teams need more than 2 min: greet -> ask -> transfer -> dept


# ---------------------------------------------------------------------------
# Voice model resolution
# ---------------------------------------------------------------------------

VOICE_CONFIGS: dict[str, dict] = {
    "xai": {"voice_provider": "xai", "voice": "ara"},
    "openai-1.5": {"voice_provider": "openai", "openai_voice_model": "gpt-realtime-1.5"},
    "openai-2": {"voice_provider": "openai", "openai_voice_model": "gpt-realtime-2"},
    "gemini": {"voice_provider": "gemini"},
    "elevenlabs": {"voice_provider": "elevenlabs"},
}
# transfer_to_agent only works on xai/openai (mid-call session.update); gemini /
# elevenlabs decline the swap. Teams must use an xai or openai voice.
TRANSFER_CAPABLE = {"xai", "openai-1.5", "openai-2"}


# ---------------------------------------------------------------------------
# Default support team — front desk + 3 departments
# ---------------------------------------------------------------------------

DEPARTMENTS = [
    {
        "key": "billing",
        "name": "Billing Department",
        "when": "when the caller asks about invoices, payments, refunds, or their bill",
        "greeting": "Billing department, how can I help with your account?",
        "system_prompt": (
            "You are the BILLING department. When connected, say 'This is billing' "
            "and help with their payment or invoice question briefly. When the "
            "caller says they're done, use the end_call tool to hang up."
        ),
    },
    {
        "key": "sales",
        "name": "Sales Department",
        "when": "when the caller is interested in buying, pricing, upgrades, or new service",
        "greeting": "Sales here, what are you looking to get set up?",
        "system_prompt": (
            "You are the SALES department. When connected, say 'This is sales' and "
            "help with their purchase interest briefly. When the caller says "
            "they're done, use the end_call tool to hang up."
        ),
    },
    {
        "key": "support",
        "name": "Technical Support",
        "when": "when the caller has a technical problem or something is broken",
        "greeting": "Tech support, what seems to be the trouble?",
        "system_prompt": (
            "You are TECHNICAL SUPPORT. When connected, say 'This is tech support' "
            "and help with their issue briefly. When the caller says they're done, "
            "use the end_call tool to hang up."
        ),
    },
]

FRONT_DESK_PROMPT = (
    "You are the front desk receptionist. Greet the caller, find out which "
    "department they need, and use transfer_to_agent to hand them off. Tell them "
    "you're connecting them before you transfer. Do not try to answer billing, "
    "sales, or technical questions yourself — route them."
)


def voice_overrides(voice: str) -> dict:
    cfg = VOICE_CONFIGS.get(voice)
    if cfg is None:
        sys.exit(f"Unknown voice '{voice}'. Options: {', '.join(VOICE_CONFIGS)}")
    return cfg


# ---------------------------------------------------------------------------
# TEAM MODE
# ---------------------------------------------------------------------------


def run_team(api: Api, voice: str, ask_for: str, dry_run: bool) -> dict:
    """Create a front-desk + department team, have user-sim ask for one dept,
    verify the transfer happened via agent_transitions."""
    if voice not in TRANSFER_CAPABLE:
        sys.exit(
            f"Voice '{voice}' can't transfer (gemini/elevenlabs decline mid-call "
            f"swap). Use one of: {', '.join(sorted(TRANSFER_CAPABLE))}"
        )
    vo = voice_overrides(voice)
    dept = next((d for d in DEPARTMENTS if d["key"] == ask_for), None)
    if not dept:
        sys.exit(f"Unknown department '{ask_for}'. Options: {[d['key'] for d in DEPARTMENTS]}")

    created: list[str] = []  # track every agent id we create, for cleanup
    try:
        # 1. Department agents — NO phone number needed (transfer swaps the brain).
        dept_ids: dict[str, str] = {}
        for d in DEPARTMENTS:
            r = api.req(
                "POST",
                "/agents",
                {
                    "name": f"LOOPTEST-dept-{d['key']}",
                    "agent_mode": "inbound",
                    "ai_speaks_first": True,
                    "greeting": d["greeting"],
                    "system_prompt": d["system_prompt"],
                    "tools_enabled": ["end_call"],
                    "max_call_duration_minutes": MAX_DURATION_MIN,
                    **vo,
                },
            )
            r.raise_for_status()
            aid = r.json()["id"]
            dept_ids[d["key"]] = aid
            created.append(aid)

        # 2. Front desk — wired to all departments via transfer_to_agents.
        transfer_to_agents = [
            {"agent_id": dept_ids[d["key"]], "name": d["name"], "when": d["when"]}
            for d in DEPARTMENTS
        ]
        r = api.req(
            "POST",
            "/agents",
            {
                "name": "LOOPTEST-frontdesk",
                "agent_mode": "inbound",
                "ai_speaks_first": True,
                "greeting": "Thanks for calling! Which department do you need?",
                "system_prompt": FRONT_DESK_PROMPT,
                "transfer_to_agents": transfer_to_agents,
                # transfer_to_agent must be in tools_enabled AND transfer_to_agents
                # must be non-empty: the tool-schema builder only emits a tool whose
                # name is in tools_enabled, then drops transfer_to_agent if there are
                # no targets. Both conditions are required.
                "tools_enabled": ["end_call", "transfer_to_agent"],
                "max_call_duration_minutes": MAX_DURATION_MIN,
                **vo,
            },
        )
        r.raise_for_status()
        front_resp = r.json()
        front_id = front_resp["id"]
        created.append(front_id)

        # VERIFY the team wired up before spending a call. The front desk's
        # transfer_to_agents must be non-empty or transfer_to_agent is never
        # offered to the model. If create didn't persist it, PATCH then re-GET;
        # abort (no call placed) if it still won't stick.
        def _targets(agent_obj: dict) -> list:
            return agent_obj.get("transfer_to_agents") or []

        if not _targets(front_resp):
            api.req("PATCH", f"/agents/{front_id}", {"transfer_to_agents": transfer_to_agents})
            front_resp = api.req("GET", f"/agents/{front_id}").json()
        if not _targets(front_resp):
            return {
                "mode": "team",
                "voice": voice,
                "ask_for": ask_for,
                "keyword_passed": False,
                "keyword_detail": (
                    "ABORTED before call: front desk transfer_to_agents did not "
                    "persist (create + PATCH both returned empty). Likely the "
                    "department targets failed same-tenant/same-provider validation. "
                    f"Sent targets: {transfer_to_agents}"
                ),
            }
        print(f"  team wired: {len(_targets(front_resp))} transfer targets on front desk")

        # 3. User-sim — outbound, asks for the chosen department.
        r = api.req(
            "POST",
            "/agents",
            {
                "name": "LOOPTEST-user",
                "agent_mode": "outbound",
                "ai_speaks_first": False,
                "ai_speaks_first_outbound": True,
                "greeting": "Hello.",
                "greeting_outbound": f"Hi, I need the {ask_for} department please.",
                "system_prompt": (
                    f"You are a caller who needs the {ask_for} department. Ask for "
                    f"{ask_for}. Once connected to that department, say 'great, "
                    f"thanks, that's all' and end the call. Keep it short."
                ),
                "max_call_duration_minutes": MAX_DURATION_MIN,
                **vo,
            },
        )
        r.raise_for_status()
        user_id = r.json()["id"]
        created.append(user_id)

        # 4. Assign the 2 borrowed numbers: front desk receives, user-sim calls.
        api.req("PATCH", f"/phone-numbers/{Cfg.num_under_pid}", {"agent_id": front_id}).raise_for_status()
        api.req("PATCH", f"/phone-numbers/{Cfg.num_user_pid}", {"agent_id": user_id}).raise_for_status()

        if dry_run:
            return {
                "mode": "team",
                "voice": voice,
                "ask_for": ask_for,
                "keyword_passed": True,
                "keyword_detail": "dry-run: team configured, call skipped",
                "dept_ids": dept_ids,
                "front_id": front_id,
            }

        # 5. Place the call: user-sim -> front desk number.
        api.req(
            "POST",
            f"/outbound/agents/{user_id}/call",
            {"to_number": Cfg.num_under_e164, "from_phone_number_id": Cfg.num_user_pid},
        ).raise_for_status()

        # 6. Poll the FRONT-DESK call_log (agent_id stays the originator).
        call = _poll_until_complete(api, front_id)
        if not call:
            return {
                "mode": "team",
                "voice": voice,
                "ask_for": ask_for,
                "keyword_passed": False,
                "keyword_detail": "no completed call within timeout",
            }

        transitions = call.get("agent_transitions") or []
        target_id = dept_ids[ask_for]
        transferred = any(t.get("agent_id") == target_id for t in transitions)
        names = [t.get("agent_name") for t in transitions]
        return {
            "mode": "team",
            "voice": voice,
            "ask_for": ask_for,
            "keyword_passed": transferred,
            "keyword_detail": (
                f"transition timeline: {names}"
                if transferred
                else f"expected {ask_for} dept in transitions, got: {names}"
            ),
            "judge_question": (
                f"Did the front desk correctly transfer the caller to the "
                f"{ask_for} department? The transition timeline should include the "
                f"{ask_for} department, and the transcript should show the handoff "
                f"(front desk says it's connecting, then the {ask_for} department speaks)."
            ),
            "agent_transitions": transitions,
            "agent_id_stays_originator": call.get("agent_id"),
            "from_number": call.get("from_number"),
            "status": call.get("status"),
            "duration_seconds": call.get("duration_seconds"),
            "transcript": transcript_text(call),
        }
    finally:
        _restore_numbers(api)
        for aid in created:
            api.req("DELETE", f"/agents/{aid}")


# ---------------------------------------------------------------------------
# LATENCY MODE
# ---------------------------------------------------------------------------


def run_latency(api: Api, voices: list[str]) -> list[dict]:
    """One real call per voice model; read performance_metrics from each call_log."""
    rows = []
    for voice in voices:
        vo = voice_overrides(voice)
        created = []
        try:
            r = api.req(
                "POST",
                "/agents",
                {
                    "name": f"LOOPTEST-lat-under-{voice}",
                    "agent_mode": "inbound",
                    "ai_speaks_first": True,
                    "greeting": "Hello! Thanks for calling, how can I help you today?",
                    "system_prompt": (
                        "You are a receptionist. Answer briefly and warmly. When the "
                        "caller says goodbye, use the end_call tool to hang up."
                    ),
                    "tools_enabled": ["end_call"],
                    "max_call_duration_minutes": 2,
                    **vo,
                },
            )
            r.raise_for_status()
            under_id = r.json()["id"]
            created.append(under_id)

            r = api.req(
                "POST",
                "/agents",
                {
                    "name": f"LOOPTEST-lat-user-{voice}",
                    "agent_mode": "outbound",
                    "ai_speaks_first": False,
                    "ai_speaks_first_outbound": True,
                    "greeting": "Hello.",
                    "greeting_outbound": "Hi, I have a quick question about your hours.",
                    "system_prompt": (
                        "Your GOAL: ask what the business hours are. Listen to the "
                        "answer, say 'perfect, thanks, bye', then use the end_call "
                        "tool to hang up. Keep it short; don't linger after the answer."
                    ),
                    "tools_enabled": ["end_call"],
                    "max_call_duration_minutes": 2,
                    **vo,
                },
            )
            r.raise_for_status()
            user_id = r.json()["id"]
            created.append(user_id)

            api.req("PATCH", f"/phone-numbers/{Cfg.num_under_pid}", {"agent_id": under_id}).raise_for_status()
            api.req("PATCH", f"/phone-numbers/{Cfg.num_user_pid}", {"agent_id": user_id}).raise_for_status()

            api.req(
                "POST",
                f"/outbound/agents/{user_id}/call",
                {"to_number": Cfg.num_under_e164, "from_phone_number_id": Cfg.num_user_pid},
            ).raise_for_status()

            call = _poll_until_complete(api, under_id)
            pm = ((call or {}).get("metadata") or {}).get("performance_metrics") or {}
            rows.append(
                {
                    "voice": voice,
                    "status": (call or {}).get("status"),
                    "duration_seconds": (call or {}).get("duration_seconds"),
                    "time_to_first_audio_seconds": pm.get("time_to_first_audio_seconds"),
                    "connect_duration_ms": pm.get("xai_connect_duration_ms"),
                    "avg_response_latency_ms": pm.get("avg_response_latency_ms"),
                    "min_response_latency_ms": pm.get("min_response_latency_ms"),
                    "max_response_latency_ms": pm.get("max_response_latency_ms"),
                    "turn_count": pm.get("turn_count"),
                    "turn_response_times_ms": pm.get("turn_response_times_ms"),
                }
            )
        finally:
            _restore_numbers(api)
            for aid in created:
                api.req("DELETE", f"/agents/{aid}")
    return rows


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------


def _restore_numbers(api: Api) -> None:
    api.req("PATCH", f"/phone-numbers/{Cfg.num_user_pid}", {"agent_id": Cfg.num_user_restore or None})
    api.req("PATCH", f"/phone-numbers/{Cfg.num_under_pid}", {"agent_id": Cfg.num_under_restore or None})


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--team", action="store_true", help="run the agent-teams transfer test")
    p.add_argument("--ask-for", default="billing", help="department to ask for (billing/sales/support)")
    p.add_argument("--latency", action="store_true", help="run latency benchmark per voice")
    p.add_argument("--voice", default="xai", help="voice for team mode (xai/openai-1.5/openai-2)")
    p.add_argument("--voices", default="xai,openai-1.5,openai-2,gemini,elevenlabs",
                   help="comma list of voices for latency mode")
    p.add_argument("--user-number-id", default=os.environ.get("LEADLOCK_NUM_USER_PID", ""),
                   help="phone_numbers.id of the number the user-sim agent calls FROM")
    p.add_argument("--under-number-id", default=os.environ.get("LEADLOCK_NUM_UNDER_PID", ""),
                   help="phone_numbers.id the front-desk / under-test agent receives ON")
    p.add_argument("--sub-account-id", default=Cfg.sub_id,
                   help="X-Sub-Account-Id for an agency key acting on a sub-account")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--out", default="/tmp/agent_loop_results.json")
    args = p.parse_args()

    require_api_key()
    if args.sub_account_id:
        Cfg.sub_id = args.sub_account_id
    if not (args.user_number_id and args.under_number_id):
        sys.exit("Need --user-number-id and --under-number-id (two phone_numbers.id values).")

    api = Api()
    load_numbers(api, args.user_number_id, args.under_number_id)

    if args.team:
        res = run_team(api, args.voice, args.ask_for, args.dry_run)
        with open(args.out, "w") as f:
            json.dump([res], f, indent=2)
        print(f"\nTeam result written to {args.out}")
        print(f"  transfer pre-signal: {'fired' if res.get('keyword_passed') else 'NOT fired'}")
        print(f"  {res.get('keyword_detail', '')}")
        if res.get("transcript"):
            print("  --- transcript ---")
            print("\n".join("  " + ln for ln in res["transcript"].splitlines()))
        print("\nNEXT: Claude session judges judge_question vs transcript + agent_transitions.")
        return 0

    if args.latency:
        voices = [v.strip() for v in args.voices.split(",") if v.strip()]
        rows = run_latency(api, voices)
        with open(args.out, "w") as f:
            json.dump(rows, f, indent=2)
        print(f"\nLatency results written to {args.out}")
        print(f"{'voice':<12} {'TTFA(s)':>8} {'connect(ms)':>12} {'avg(ms)':>9} {'turns':>6}")
        for r in rows:
            print(
                f"{r['voice']:<12} "
                f"{str(r.get('time_to_first_audio_seconds')):>8} "
                f"{str(r.get('connect_duration_ms')):>12} "
                f"{str(r.get('avg_response_latency_ms')):>9} "
                f"{str(r.get('turn_count')):>6}"
            )
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
