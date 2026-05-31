# Agent-to-agent call testing — learnings

Hard facts learned building and validating the `agent-to-agent-call-testing`
harness (two real agents call each other over Twilio). Skim before changing the
harness or authoring new test cases.

Each entry: date, tags, evidence, rule, why, how to apply.

---

### Agent-to-agent outbound passes a real caller-id to the inbound leg

Date: 2026-05-30
Tags: skill:agent-to-agent-call-testing, type:best-practice, surface:call-metadata
Evidence: user-sim `+14129101786` called agent-under-test `+14024486711`; the inbound call_log recorded `from_number = +14129101786` and the agent spoke it: "Hi there! I can see you're calling from (412) 910-1786." Confirmed in the transcript via `GET /calls/{id}`.

**Rule:** A real agent-to-agent call DOES produce an inbound `call_log` with a real
`from_number`, so `{{caller_phone}}` (and contact intelligence / outbound context)
can be validated with no real human phone in the loop.

**Why:** The simulator and the browser playground never create a `call_log` with a
real `from_number`, so they FALSE-PASS anything that reads call metadata. Only a
real Twilio call exercises that path. The whole reason this harness exists is to
close that gap.

**How to apply:** For any feature that depends on call metadata, use this harness,
not the simulator. The proof is always the transcript from `GET /calls/{id}` plus
the `from_number` on the call_log — cite both.

---

### Create-time agent validation traps for the two test agents

Date: 2026-05-30
Tags: skill:agent-to-agent-call-testing, type:best-practice, surface:agent-config
Evidence: `POST /agents` rejected the outbound user-sim until `ai_speaks_first` was set false with a dummy `greeting`; two AI agents also ran to the duration cap until `end_call` + a low cap were added.

**Rule:**
- `POST /agents` rejects `ai_speaks_first=True` when `greeting` is empty. The
  OUTBOUND user-sim must set `ai_speaks_first:false` + a dummy `greeting:"Hello."`
  plus `ai_speaks_first_outbound:true` + a real `greeting_outbound`.
- Put `end_call` in `tools_enabled` on BOTH agents and give the user-sim a clear
  goal ("ask X, hear the answer, say bye, end the call"), or two AI agents chat
  until the duration cap.
- Set `max_call_duration_minutes` to 2 (single) / 3 (team) — a hard cost bound for
  when the agents don't hang up cleanly.

**Why:** Without these, create fails, or the call burns provider minutes until the
cap. The optional Twilio backstop (`LEADLOCK_TWILIO_SID/AUTH`) force-ends a runaway
call, but the agents' own `end_call` + the cap are the primary mechanism.

**How to apply:** These defaults are baked into `UNDER_BASE` / `USER_BASE` in
`harness.py`. Keep them when authoring new cases; only override the prompt,
greeting, tools, and variables.

---

### Agent-team transfer: wiring, voice limits, and the verdict signal

Date: 2026-05-31
Tags: skill:agent-to-agent-call-testing, type:best-practice, surface:agent-teams, feature:transfer_to_agent
Evidence: front-desk + billing/sales/support team; the front desk transferred to the asked-for department and the department's agent_id appeared in `call_logs.agent_transitions` while `call_logs.agent_id` stayed the front desk.

**Rule:**
- `transfer_to_agents = [{agent_id, name, when}]`. The `when` text is what the
  model matches the caller's intent against — make it specific per department.
- The front desk needs BOTH `transfer_to_agent` in `tools_enabled` AND a non-empty
  `transfer_to_agents`. The tool-schema builder only emits a tool whose name is in
  `tools_enabled`, then drops `transfer_to_agent` if there are no targets — both
  conditions are required.
- Department agents need NO phone number — transfer swaps the live session brain on
  the existing call, so a team still uses only the two borrowed numbers.
- Transfer only works on `xai` / `openai` voices. Gemini and ElevenLabs decline the
  mid-call session swap. Hop cap is 3.
- **Verdict signal:** the asked-for department's `agent_id` appears in
  `call_logs.agent_transitions` (a jsonb list of `{agent_id, agent_name,
  started_at}`); `call_logs.agent_id` stays the ORIGINATOR (front desk).

**Why:** A team that "looks" wired can still never offer transfer if either
condition is missing, and you'd waste a paid call discovering it. `team_harness.py`
verifies `transfer_to_agents` persisted (create → PATCH → re-GET) BEFORE placing
the call, and aborts with a clear message if it won't stick.

**How to apply:** Use `team_harness.py --team`. Judge the transcript (front desk
says "connecting you" → the department speaks) in addition to the transition
timeline pre-signal.

---

### Borrow numbers safely; restore them no matter what

Date: 2026-05-31
Tags: skill:agent-to-agent-call-testing, type:best-practice, surface:phone-numbers, safety
Evidence: harness resolves each number's current `agent_id` before reassigning and restores it in a `finally` block.

**Rule:** Prefer UNASSIGNED voice numbers for the test. If a number currently on a
production agent must be borrowed, warn the user: for the ~1–2 min test the number
points at the test agent, so a real inbound call in that window would reach it. The
harness records the prior `agent_id` and restores it (or leaves it unassigned) in a
`finally` block even if the run crashes; numbers are never released from Twilio.

**Why:** This is the one place the harness touches production config. The restore is
unconditional, but borrowing a live number still has a brief real-world window —
unassigned numbers avoid it entirely.

**How to apply:** In Step 1 of the wizard, sort `GET /phone-numbers` and offer
unassigned voice numbers first; only fall back to assigned ones with an explicit
warning.
