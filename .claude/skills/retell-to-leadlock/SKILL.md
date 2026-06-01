---
name: retell-to-leadlock
description: Port a Retell AI agent (or a Retell orchestrator + its transfer/sub-agents) into an equivalent Leadlock agent. Pulls the Retell LLM definitions, maps the prompt + every tool, consolidates a multi-agent transfer tree into ONE Leadlock prompt (Leadlock has no agent-to-agent transfer yet), recreates custom HTTP tools as Leadlock custom functions, and verifies the whole thing live. Triggers on /retell-to-leadlock, port a retell agent, port retell to leadlock, convert retell agent, migrate my retell agent, recreate my retell agent in leadlock, build a leadlock agent from retell, clone retell agent into leadlock, move retell agent to leadlock, retell to leadlock, port my retell sub agents, consolidate retell agents into one.
---

# Retell → Leadlock agent porter

Recreate a Retell agent as a working Leadlock agent. Handles the common Retell pattern — an orchestrator that `agent_swap`s to specialist sub-agents — by **collapsing it into a single Leadlock prompt** (Leadlock has no agent-to-agent transfer), preserving every tool's functionality, and verifying booking/transfer/end-call end to end. All work is HTTP: Retell read-only, Leadlock create/patch.

**Offline Retell reference:** a full copy of Retell's API docs ships in this skill folder as `retelldocs.md`. Consult it for any Retell endpoint, tool `type`, or field you don't recognize (`agent_swap`, `extract_dynamic_variable`, `args_at_root`, etc.). The live Retell API (Steps 1-2) remains the source of truth for the user's actual config; the file is for understanding shapes. For Leadlock shapes, use `LEADLOCKDOCS.json` at the kit root.

## When to invoke

- "Port my Retell agent into Leadlock" / "recreate this Retell agent in Leadlock"
- "Consolidate my Retell orchestrator + sub-agents into one Leadlock agent"
- User pastes a Retell `agent_id` or `llm_id`, or just says "migrate my Retell setup"
- After building a Retell demo and wanting the Leadlock equivalent

## Setup check

Before anything, confirm `./.env` has:
- `LEADLOCK_API_KEY` + `LEADLOCK_API_URL` (required — the target)
- `RETELL_API_KEY` (required — the source)
- **Optional, only if the Retell agent has custom HTTP tools that hit your own backend** (e.g. a Modal/cal.com wrapper): `MODAL_TOKEN_ID` + `MODAL_TOKEN_SECRET` (to deploy the bridge adapter) and any backend keys.

If `LEADLOCK_API_KEY` or `RETELL_API_KEY` is missing, stop and fire `setup-check`. Auth headers: Leadlock `X-API-Key: <key>`; Retell `Authorization: Bearer <key>`. **Never print full keys** — mask as `sk_live_***…last4`.

## Rules

1. **Leadlock has no agent-to-agent transfer.** A Retell orchestrator + `agent_swap` sub-agents MUST be consolidated into ONE Leadlock agent with internal "modes." Do not attempt to recreate the swap tree. The only live transfer Leadlock supports is a phone `transfer_call` to a number.
2. **Drop the state-passing machinery when consolidating.** Retell `extract_dynamic_variable` tools (e.g. `record_requests`, `record_appointment_details`) and `{{pending_requests}}`-style dynamic variables exist only to pass state across `agent_swap`. In one agent they're dead weight — remove them and use an internal "SILENT STATE TRACKING" section instead.
3. **Remove redundancy, preserve functionality.** Each Retell sub-agent repeats the same persona/disclosure/pronunciation boilerplate. Write it ONCE at the top of the consolidated prompt, then per-mode sections. Every *capability* (booking flow, FAQ KB, spam filter, callback intake, emergency, wrap-up) must survive.
4. **Default voice to OpenAI Realtime v2** unless the user says otherwise: `voice_provider:"openai"`, `openai_voice_model:"gpt-realtime-2"`, `openai_voice:"marin"` (or `cedar`), `openai_vad_type:"semantic_vad"`, `openai_vad_eagerness:"low"`, `openai_noise_reduction:"far_field"`, `openai_reasoning_effort:"low"`. Don't try to map the Retell `voice_id` 1:1 — Leadlock has its own voices.
5. **`POST /agents` silently drops `openai_voice_model` and `transfer_targets`.** It returns defaults for them. ALWAYS `PATCH /agents/{id}` with those two fields right after create, then GET to confirm they stuck. (See Gotchas.)
6. **Reserved tool names can't be custom functions.** `book_appointment`, `check_availability`, `end_call`, `schedule_callback`, `transfer_call` are built-ins — creating a custom function with those names returns 422. Rename the ported HTTP tool (e.g. `book_appointment` → `book_cal_appointment`) and update the prompt to match.
7. **Leadlock wraps custom-function webhook bodies.** It POSTs `{"function":..,"arguments":{..},"call_context":{..}}`, NOT the args at the root. Retell custom tools used `args_at_root:true`. If the Retell tool pointed at YOUR backend expecting root args, that backend will 500. Bridge it (Step 7) — don't claim done until a live function test returns 200.
8. **Confirmation gate before any create/mutation.** Creating the agent, attaching functions, deploying an adapter, and any test that books/sends SMS/transfers are outward-facing — show the plan and get a yes first. Test bookings/SMS create real side effects.
9. **Check the agent limit before building.** `GET /billing/limits` AND `GET /tenants/me` (they can disagree — see Gotchas). If `agents.limit` is 1 and one exists, a 1:1 multi-agent port is impossible; only the consolidated single agent fits. Tell the user.
10. **Never name the Leadlock platform in agent-output content.** Generated prompts/greetings say "our system"/"the platform we use." Never the word "closer" — use "specialist"/"team member".
11. **Branch discipline: stay on `main`.** No new branches. Don't modify the parent `leadlock-app` repo.
12. **Don't rebuild the user's backend from a stack trace.** If a custom HTTP tool's source isn't available, bridge with an adapter (Step 7) — never reconstruct a live booking/SMS service by guessing.
13. **Consult `learnings/` first.** Skim `learnings/index.md` for `type:platform-gap` and `retell`/`leadlock` entries before building; capture new ones with `/add-to-learnings` after.

## Required inputs

Ask the user (lettered) if not already clear:

- **(a)** A single Retell `agent_id` to port, OR
- **(b)** An orchestrator `agent_id` whose sub-agents should be consolidated into one Leadlock agent (the common case), OR
- **(c)** "All my Retell agents" — then list them and confirm which form the system (orchestrator + subs) vs. standalone agents.

Also confirm:
- **Port style:** consolidated single agent (default/recommended), 1:1 mirror of each agent, or both. (1:1 needs `agents.limit` headroom — Rule 9.)
- **Booking/tools backend:** reuse the existing custom-HTTP backend (bridge it) vs. switch to Leadlock-native `book_appointment`/`check_availability` (GoHighLevel calendar). If the Retell tools hit cal.com/Modal and the user wants cal.com kept, that's "reuse + bridge."
- **Live transfer target** for any Retell `transfer_call` (the phone number).

## Execution

### Step 0 — Probe both platforms

```bash
# Leadlock identity + limits (run BOTH — they can report different plan/limit)
curl -s -H "X-API-Key: $LEADLOCK_API_KEY" "$LEADLOCK_API_URL/tenants/me"
curl -s -H "X-API-Key: $LEADLOCK_API_KEY" "$LEADLOCK_API_URL/billing/limits"
```
Note `tenant_type` (agency vs sub_account → affects `X-Sub-Account-Id` header and `/agency/*` access) and `agents.current`/`agents.limit`. If a key 401s, fire `setup-check`.

### Step 1 — Inventory the Retell agents

```bash
curl -s -H "Authorization: Bearer $RETELL_API_KEY" https://api.retellai.com/list-agents
```
`list-agents` returns every **version** — dedupe by `agent_id`, keep the latest/published per agent. Map each `agent_id → agent_name → response_engine.llm_id`. Identify the orchestrator (the one whose tools are mostly `agent_swap`) vs. specialists vs. any standalone agents.

### Step 2 — Pull each unique LLM definition

For each unique `llm_id`:
```bash
curl -s -H "Authorization: Bearer $RETELL_API_KEY" https://api.retellai.com/get-retell-llm/$LLM_ID
```
Save each to `./output/retell-export/<role>.json`. From each, extract:
- `general_prompt` (the system prompt) and `begin_message` (greeting), `model`, `start_speaker`
- `general_tools[]` — **classify every tool**:
  - `type:"agent_swap"` → a sub-agent handoff → **collapse into a mode** (drop the tool)
  - `type:"transfer_call"` → phone transfer → map to `transfer_targets` + native `transfer_call`
  - `type:"end_call"` → native `end_call`
  - `type:"extract_dynamic_variable"` → state passing → **drop** (Rule 2)
  - `type:"custom"` → an HTTP webhook tool → becomes a Leadlock **custom function** (note `url`, `method`, `parameters`, `args_at_root`, `timeout_ms`, `speak_during_execution`)

### Step 3 — Map architecture & confirm the plan

Build a table: orchestrator + each specialist + its real (non-swap) tools. Then decide with the user:
- **Consolidated (default):** one prompt, modes for each former specialist (triage → spam → faq → booking → callback → emergency → wrap-up), shared boilerplate once, swaps + state tools removed.
- **1:1 (only if limit allows):** one Leadlock agent per Retell agent; leave `agent_swap`s as documented `transfer_targets` placeholders until Leadlock ships agent transfer.

Show the plan and the gap analysis (what maps cleanly, what needs a bridge, the agent-limit reality). Get a yes.

### Step 4 — Map tools to Leadlock

| Retell tool | Leadlock equivalent |
|---|---|
| `end_call` | `tools_enabled: ["end_call"]` |
| `transfer_call` (phone) | `tools_enabled: [..., "transfer_call"]` + `transfer_targets:[{name,number,reason}]` |
| `agent_swap` | **removed** — folded into a prompt mode |
| `extract_dynamic_variable` | **removed** — internal state tracking in prompt |
| `custom` HTTP tool | Leadlock **custom function** (Step 7), renamed if it collides with a reserved name (Rule 6) |

Native booking option (only if user chose it): `book_appointment` + `check_availability` (GoHighLevel calendar) instead of a custom function — mirror an existing agent's `calendar_id`/`calendar_integration_id`/`calendar_provider`.

### Step 5 — Write the consolidated prompt

Use the skeleton in `## Templates`. Merge the orchestrator's routing + each specialist's flow into mode sections. Lift shared boilerplate (persona, AI disclosure, pronunciation, tone, one-question-at-a-time) to the top, written once. Preserve scripted lines verbatim where the Retell prompt quoted exact phrasing (consent scripts, summaries). Save to `./output/consolidated-prompt.md`.

### Step 6 — Create the agent (then PATCH the dropped fields)

```bash
# Create. Build the JSON from a file to avoid shell-escaping the long prompt.
curl -s -X POST "$LEADLOCK_API_URL/agents" -H "X-API-Key: $LEADLOCK_API_KEY" \
  -H "Content-Type: application/json" -d @output/agent-create.json
```
`agent-create.json` includes: `name`, `system_prompt`, `greeting`, `business_name`, `industry`, `timezone` (match the BUSINESS, infer from KB/address), `ai_speaks_first:true`, the OpenAI v2 voice block (Rule 4), `tools_enabled`, `transfer_targets`, `max_call_duration_minutes`, `enable_recording_disclosure:false` (if the greeting already discloses recording).

Then — because create drops them (Rule 5):
```bash
curl -s -X PATCH "$LEADLOCK_API_URL/agents/$AGENT_ID" -H "X-API-Key: $LEADLOCK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"openai_voice_model":"gpt-realtime-2","transfer_targets":[{"name":"Emergency Line","number":"+1XXXXXXXXXX","reason":"..."}]}'
```
GET the agent and confirm `openai_voice_model` and `transfer_targets` actually stuck.

### Step 7 — Recreate custom HTTP tools as custom functions

For each Retell `custom` tool, create a Leadlock custom function (rename if reserved — Rule 6):
```bash
curl -s -X POST "$LEADLOCK_API_URL/agents/$AGENT_ID/functions" -H "X-API-Key: $LEADLOCK_API_KEY" \
  -H "Content-Type: application/json" -d '{
    "name":"book_cal_appointment",
    "description":"...",
    "webhook_url":"<same URL as the Retell tool>",
    "webhook_method":"POST",
    "webhook_timeout_ms":30000,
    "speak_during_execution":true,
    "parameters":{ <copy the Retell tool parameters JSON Schema verbatim> }
  }'
```
Note: `webhook_timeout_ms` max is **30000** (Retell allowed 120000) — fine for fast endpoints, a risk for slow ones.

**The envelope bridge (Rule 7).** Leadlock POSTs `{"function","arguments":{..},"call_context":{..}}`. If the tool's backend expects args at the root (Retell `args_at_root:true`), it WILL fail. Capture the real outbound body once with a throwaway inspector to confirm, then bridge by EITHER:
- **(preferred, if you control the backend source):** add `args = body.get("arguments", body)` at the top of each handler and redeploy (stays Retell-compatible), OR
- **(no source needed):** deploy the thin adapter in `## Templates` to the backend's host and point the Leadlock function `webhook_url` at it. It unwraps `arguments`, forwards to the original endpoint untouched, and can coerce required constants (e.g. a fixed `event_type_id`) so a model slip or the test form's integer-default `0` can't break it.

For Modal backends on Windows: run `PYTHONUTF8=1 modal deploy …` (Rule/Gotcha).

### Step 8 — Verify end to end

```bash
# Fire each custom function through Leadlock's own webhook path:
curl -s -X POST "$LEADLOCK_API_URL/agents/$AGENT_ID/functions/$FUNC_ID/test" \
  -H "X-API-Key: $LEADLOCK_API_KEY" -H "Content-Type: application/json" \
  -d '{"arguments":{ ...real values... }}'
```
- Read-only first (availability/lookups). Expect `success:true`, HTTP 200.
- **The test form defaults integer params to `0`** — pass real values (e.g. the real event/calendar id), not the default, or the backend 404s.
- For booking/SMS/transfer (real side effects): get explicit OK, use clearly-marked test data, then **clean up** (e.g. cancel the test booking). Remember timestamps in API responses are usually **UTC** — convert to the business's local tz before judging "wrong time."
- Confirm the agent config one more time (voice = `gpt-realtime-2`, transfer target present, functions point at the bridge, tools_enabled correct).

### Step 9 — Report

Tight summary: agent id + name, voice, tools_enabled, transfer target, each custom function + verified status, any bridge/adapter deployed, and the gap analysis (what's deferred — e.g. 1:1 port pending an agent-limit raise). Full artifacts in `./output/`.

## Templates

### Consolidated prompt skeleton
```
# 1. IDENTITY & PERSONA      (name, role: handles whole call, only live handoff = emergency phone transfer, tone)
# 2. VOICE & STYLE           (brevity, contractions, one-question-at-a-time, pronunciation, number/time reading)
# 3. AI DISCLOSURE           (honest one-liner; never name the platform; resume task)
# 4. SILENT STATE TRACKING   (CURRENT MODE / INTENT / COLLECTED / PENDING / LAST QUESTION) — replaces Retell dynamic vars
# 5. SCOPE & SAFETY/EMERGENCY (checked first every call; supersedes everything; emergency → transfer_call)
# 6. INTENT CLASSIFICATION & INTERNAL ROUTING (switch MODE silently — never say "transferring")
# 7..N MODES                 (one section per former sub-agent: SPAM / FAQ / BOOKING / CALLBACK / EMERGENCY / WRAP-UP)
#   - BOOKING MODE carries the full collect→constraints→get_slots→book→summary→consent→send flow
#   - FAQ MODE answers ONLY from an inline KNOWLEDGE BASE section
# KNOWLEDGE BASE             (facts only; do not improvise beyond)
# TOOLS                      (one line per tool: when to call, which fields, read `formatted` vs `start`, etc.)
# EDGE CASES                 (corrections, mis-hears, partial info, haggling, abuse)
# FINAL VALIDATION           (silent pre-send checklist: not re-asking, not re-entering a step, not announcing a "mode")
```

### Webhook envelope bridge (deploy to the backend's host; no source of the original app needed)
```python
import urllib.request, urllib.error, json, modal
app = modal.App("leadlock-<backend>-adapter")
image = modal.Image.debian_slim().pip_install("fastapi[standard]")
UPSTREAM = "https://<existing-backend-base-url>"
DEFAULT_CONST = {"event_type_id": 0}  # set required constants the model/test-form might omit or zero out

def _unwrap(body):  # Leadlock nests under "arguments"; Retell sent args at the root
    return body["arguments"] if isinstance(body, dict) and isinstance(body.get("arguments"), dict) else (body or {})

def _forward(path, args):
    req = urllib.request.Request(UPSTREAM+path, data=json.dumps(args).encode(),
                                 headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e: return {"success":False,"error":f"upstream {e.code}","detail":e.read().decode("utf-8","ignore")}

@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    from fastapi import FastAPI, Request
    web = FastAPI()
    @web.post("/v1/<endpoint>")
    async def ep(request: Request):
        args = _unwrap(await request.json())
        for k,v in DEFAULT_CONST.items():
            if not args.get(k): args[k] = v
        return _forward("/v1/<endpoint>", args)
    return web
# deploy:  PYTHONUTF8=1 modal deploy <file>.py
```

## Gotchas

- **`POST /agents` drops `openai_voice_model` + `transfer_targets`.** They come back as defaults (`gpt-realtime-1.5`, empty). PATCH after create and re-GET. (`type:bug`)
- **Leadlock custom-function webhook envelope** is `{"function","arguments","call_context"}` — no `args_at_root` knob exists. Backends built for Retell's root-args will 500 (manual-Pydantic handlers escape as 500, not 422). Bridge it. (`type:platform-gap`)
- **Reserved built-in names** (`book_appointment, check_availability, end_call, schedule_callback, transfer_call`) → 422 if used as a custom function name. Rename. (`type:platform-gap`)
- **`/tenants/me` and `/billing/limits` can disagree** on plan + agent limit for the same key. Read both; surface the mismatch to the user. (`type:bug`)
- **Test form defaults integers to `0`.** A `get_slots`/lookup test with `event_type_id:0` 404s at the backend even though it returns HTTP 200 with `success:false`. Pass real values; optionally force constants in the bridge. (`type:gotcha`)
- **Modal CLI on Windows crashes on output rendering** with a `charmap` codec error (the deploy still partially registers as *stopped*). Run with `PYTHONUTF8=1` (or `PYTHONIOENCODING=utf-8`). (`type:tooling`)
- **API timestamps are UTC.** Booking responses/records show UTC; convert to the business tz before judging the time. Don't trust PowerShell `Invoke-RestMethod` for date fields — it reparses ISO into local `[DateTime]` and shifts it; read raw response text and parse offset-aware. (`type:anti-pattern`)
- **cal.com / similar backends:** bookings are referenced by string `uid`, not the numeric `booking_id` the create call returns — to cancel a test booking, list bookings, match the numeric `id`, get its `uid`, cancel by `uid`. A single `GET /v2/event-types/{id}` 404 without a `cal-api-version` header is benign — slots/booking still work. (`type:reference`)
- **`webhook_timeout_ms` caps at 30000** (Retell allowed 120000). Fine for fast endpoints; watch slow ones.
- **Agent-swap depth is lost on purpose.** When consolidating, verify no capability was dropped — walk every former sub-agent's tools and flows against the merged prompt.

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
