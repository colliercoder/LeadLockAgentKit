---
name: agent-to-agent-call-testing
description: Functional test harness where two of YOUR Leadlock agents call each other over real Twilio, so call-time features are verified end-to-end against the true production call path (not faked by a simulator or the browser playground). One agent (the "user-sim") dials another (the "agent-under-test"); the harness pulls the transcript and proves the feature fired. Tests the caller's-phone-number variable, greetings, end-call, agent-team transfers, and benchmarks voice latency. Runs as a guided wizard. Triggers on /agent-to-agent-call-testing, test my agent on a real call, agent vs agent call test, functional call test, test the caller phone number on a call, test agent teams, test a transfer, benchmark voice latency, loop test my agents.
---

# Agent-to-Agent Call Testing

Two of the user's own Leadlock agents call each other over **real Twilio** so
call-time behavior is verified against the true production path. This is a guided
wizard: walk the user through it question by question, place the test call(s),
then judge the transcript and report PASS/FAIL with the proof.

For any Leadlock field or endpoint shape you need to confirm, consult `LEADLOCKDOCS.json` at the kit root (the canonical API reference). The harness also self-checks its required paths against the live `/openapi.json` before placing any paid call (Step 4).

## Why this exists (say this if the user asks "why not just use the simulator?")

The bot-vs-bot simulator and the browser voice playground **do not create a
call_log with a real `from_number`**, so they give a FALSE PASS for anything that
depends on real call metadata — the caller's-phone-number variable
(`{{caller_phone}}`), contact intelligence, outbound context. The only path that
exercises those is a real Twilio call. This harness places one.

```
[user-sim agent +1AAA] --real outbound call--> [agent-under-test +1BBB]
        |                                                |
        |  From=+1AAA, To=+1BBB (real Twilio)            v
        |                          inbound call_log.from_number = +1AAA
        |                          {{caller_phone}} resolves to +1AAA
        v
   transcript pulled via GET /calls/{id}  -->  verify the feature fired
```

## What it costs (tell the user up front)

Each test is **one real phone call** — roughly **$0.02–0.05 of Twilio** plus the
voice provider's per-minute charge, billed to the user's own account like any
other call. The latency benchmark places one call per voice model (up to 5). Get
an explicit yes before placing any call.

---

## Wizard flow

Run these steps in order. Use `AskUserQuestion` for the structured choices. Do not
place a paid call until Step 5's confirmation.

### Step 0 — Setup check

Confirm `./.env` (kit root) has `LEADLOCK_API_KEY` and `LEADLOCK_API_URL`. If
missing, stop: tell the user to `cp .env.example .env` and paste their key
(Leadlock dashboard → Settings → API Keys). Then `GET /tenants/me` with
`X-API-Key` to confirm the key works and capture the tenant name/type. Print
`Using key sk_live...XXXX on tenant <name>.` Mask the key everywhere.

If the user is on an **agency** key and wants to test a specific sub-account's
agents, ask for the sub-account id and pass it as `--sub-account-id` (the harness
sends it as `X-Sub-Account-Id`).

### Step 1 — Find two voice numbers to use

The test needs **two voice-capable phone numbers** on the account: one for the
caller (user-sim) and one for the agent-under-test.

```
GET /phone-numbers
```

Sort the items:
- **Voice-capable + unassigned** (`agent_id` is null) → PREFERRED. Use these.
- **Voice-capable + already on an agent** → usable but WARN: during the ~1–2 min
  test the number is temporarily pointed at the test agent, so a real inbound
  call to it in that window would reach the test agent. The harness restores the
  original agent afterward (even if it crashes), but prefer unassigned numbers.
- **GHL-only numbers** (`provider = gohighlevel`) → exclude, they're SMS-only.

If fewer than two voice-capable numbers exist, tell the user and stop — they need
to provision/import a second voice number first. Present the candidates as
lettered options and have the user pick two (or auto-pick two unassigned ones and
confirm). Capture each one's `id`.

### Step 2 — What to test

`AskUserQuestion`:
- **A single feature** → pick from the registry in `test_cases.py`. The ready one
  is `caller_phone` (agent reads back the caller's number). The others
  (`greeting_verbatim`, `end_call`, `recording_disclosure`, …) are stubs marked
  `skip` — un-skip or author a new case to run them. To author one, copy the
  `caller_phone` shape: a prompt/greeting for the under-test agent, a prompt that
  drives the scenario for the user-sim, and a `judge_question`.
- **Agent-team transfer** → a front desk wired to billing/sales/support
  departments; the user-sim asks for one and we verify the handoff. Uses
  `team_harness.py --team`.
- **Voice latency benchmark** → one call per voice model, prints a TTFA / connect
  / avg-latency table. Uses `team_harness.py --latency`.

### Step 3 — Pick the voice

`AskUserQuestion` for the voice on both agents (or just the under-test agent if
only its behavior matters):
- **xAI Grok** (`xai`, voice ara/eve/rex/sal/leo) — default.
- **OpenAI** (`openai-1.5` or `openai-2`).
- **Gemini** (`gemini`).
- **ElevenLabs** (`elevenlabs`).

For **agent-team transfer**, restrict to `xai` / `openai-1.5` / `openai-2` —
gemini and elevenlabs decline the mid-call session swap, so transfers don't fire
on them.

### Step 4 — Contract self-check (no call, free)

Run this first — it verifies the API still matches what the harness sends, so a
drifted endpoint stops here instead of mid-test:

```bash
cd .claude/skills/agent-to-agent-call-testing
python3 harness.py --verify-contract
```

Optionally show the user a **dry run** (creates + configures the agents, assigns
the numbers, then deletes them — no call placed, no charge):

```bash
python3 harness.py --user-number-id <USER_ID> --under-number-id <UNDER_ID> --dry-run
```

### Step 5 — Confirm, then place the real call

Show the full plan: which two numbers, which voice, which test, and the cost note.
Require an explicit **yes**. Then run:

```bash
# Single feature:
python3 harness.py --user-number-id <USER_ID> --under-number-id <UNDER_ID> --only caller_phone

# Agent-team transfer:
python3 team_harness.py --team --ask-for billing --voice xai \
    --user-number-id <USER_ID> --under-number-id <UNDER_ID>

# Latency benchmark (one call per voice):
python3 team_harness.py --latency --voices xai,openai-2 \
    --user-number-id <USER_ID> --under-number-id <UNDER_ID>
```

`<USER_ID>` is the number the caller dials FROM; `<UNDER_ID>` is the number the
agent-under-test (or front desk) receives ON.

### Step 6 — Judge and report

The harness writes the full result (transcript, status, signals) to
`./output/agent_loop_results.json` and does NOT call an LLM itself. **You are the
judge.** Read that file and for each case:

1. Read the `transcript` against the `judge_question`.
2. Confirm the pre-signal: `keyword_passed` / `from_number` (single feature),
   `agent_transitions` containing the asked-for department (team), or the metrics
   table (latency).
3. Render **PASS** or **FAIL** with a one- or two-line transcript excerpt as proof.

Example proof for `caller_phone`:
> assistant: "Hi there! I can see you're calling from (412) 910-1786…"
> user: "what phone number am I calling from?"
> assistant: "You're calling from (412) 910-1786." → **PASS**

---

## Safety rails (already enforced by the harness)

- Test agents are always named with a `LOOPTEST-` prefix.
- Cleanup deletes only the agents THIS run created, tracked by id — never by
  name-match, so it can never delete a real agent.
- Borrowed numbers are **restored** to their prior agent (or left unassigned) in a
  `finally` block, even if the run crashes. Numbers are never released from Twilio.
- `--dry-run` exercises everything except the paid call.
- The harness never touches Supabase or any production data directly — it only
  uses the same HTTP API the user already has a key for.

## Configuration the harness reads

From `./.env` in the kit root (same as every other skill):
- `LEADLOCK_API_KEY` — required.
- `LEADLOCK_API_URL` (or `LEADLOCK_API_BASE`) — the API host.
- `LEADLOCK_SUB_ACCOUNT_ID` — optional; or pass `--sub-account-id`.
- `LEADLOCK_TWILIO_SID` / `LEADLOCK_TWILIO_AUTH` — optional. Only used as a
  runaway backstop to force-end a call if two AI agents fail to hang up on their
  own. Without them the agents' own `end_call` tool plus the per-agent
  `max_call_duration_minutes` cap (set to 2–3 min) bound the cost.

## Hard facts learned building this (see learnings/agent-to-agent-call-testing.md)

- Agent-to-agent outbound **does** pass a real caller-id to the inbound leg, so
  this harness can validate `{{caller_phone}}` with no real human phone.
- `POST /agents` rejects `ai_speaks_first=True` when `greeting` is empty. The
  outbound user-sim sets `ai_speaks_first:false` + a dummy `greeting`, and
  `ai_speaks_first_outbound:true` + `greeting_outbound`.
- Set `max_call_duration_minutes` low (2–3) on every agent — two AI agents won't
  always hang up cleanly, and the cap bounds cost.
- For teams: `transfer_to_agents = [{agent_id, name, when}]`; `when` is what the
  model matches caller intent against. The front desk needs BOTH
  `transfer_to_agent` in `tools_enabled` AND a non-empty `transfer_to_agents`.
  Department agents need NO phone number — transfer swaps the live session brain.
- Verdict signal for transfers: `call_logs.agent_transitions` (the department's
  agent_id appears in the timeline); `call_logs.agent_id` stays the front desk.

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
