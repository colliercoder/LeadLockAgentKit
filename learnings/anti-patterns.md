# Anti-patterns

Things we tried (or were tempted to try) that don't work. Don't redo without new evidence.

Each entry includes: date, tags, evidence link, rule, why, how to apply.

---

### Agent timezone must match prospect, not operator

Date: 2026-05-13
Tags: skill:prospect-demo, type:anti-pattern, surface:agent-config, integration:gohighlevel
Evidence: Northern Mister Sparky build (Twin Cities, set correctly to `America/Chicago`); user surfaced the gotcha while testing a 1:30 booking

**Rule:** When building or editing an agent for a prospect, set `agent.timezone` to the **prospect's** local timezone, not the operator's. Infer it from the scrape (the city/state on the contact page). When ambiguous, stop and ask.

**Why:** The agent reasons about times — "today", "tomorrow at 1:30", "first available this afternoon" — in its configured timezone. If the agent is on Eastern but the prospect is in Central, the agent's "1:30" lands an hour later than the caller intended, and the booking confirmation email shows a mismatched local time. The platform's GoHighLevel calendar has its OWN timezone setting inside GHL, separate from `agent.timezone` — so even if you set the agent right, the wired calendar can still book into a different timezone. Verify both before sending a demo out.

**How to apply:**
- In `prospect-demo`, infer timezone from the scrape's city/state. Twin Cities → `America/Chicago`. Phoenix → `America/Phoenix`. NYC/Miami → `America/New_York`. Denver → `America/Denver`. LA/Seattle → `America/Los_Angeles`. National / ambiguous businesses → stop and ask.
- After build, also check the wired GHL calendar's timezone in the GHL admin matches the prospect. The API doesn't expose this; check manually before sending.
- When a user reports "the agent booked the wrong time", look at three places: `agent.timezone`, the GHL calendar's tz, and the booker's browser tz on the confirmation email.

---

### Never write a tool name into scripted dialogue lines

Date: 2026-05-19
Tags: skill:build-agent, type:anti-pattern, model:gpt-realtime-2, surface:system-prompt
Evidence: agent `baef6000-6707-40c6-91d4-45086c7514cf`, call `74f62ec4-4982-4b66-a703-f14a07ced784` — transcript shows `end_call({"reason":"completed"})` fired at 24.45s, ~1.5s after a one-word misheard user utterance ("Biosite"). The prompt's scripted reaction was `"Thank you, I'll be here all week — well, until end_call fires."` and the greeting punchline ended `"AI ends call. Greatest exit of all time."` Both contained the literal tool name. After rewriting to remove all spoken references to tool names, the next test call held the line.

**Rule:** Never write the literal name of any tool (`end_call`, `transfer_call`, `book_appointment`, `search_knowledge_base`, `send_sms`, etc.) into ANY line of scripted dialogue in a system prompt — greetings, scripted responses, example reactions, closing lines, the lot. Tool names belong only in the `## Tools` section and in the policy/guardrail clauses, never in anything the agent is expected to say out loud.

**Why:** Reasoning-capable voice models (notably `gpt-realtime-2` with `openai_reasoning_effort` enabled) parse spoken tool names as invocation cues. If a scripted line says "until end_call fires" the model is primed to actually fire `end_call`. If the joke punchline says "AI ends call", same effect. Cheaper voice models tolerate this; V2 with reasoning does not. The failure mode is silent: the model says the line, fires the tool, and the call drops with no error.

**How to apply:**
- When drafting a system prompt, do a final scan for any tool name appearing inside quoted scripted dialogue, examples, or copy that the agent is expected to read out. Strip or rephrase.
- Tool-policy lines belong in `## Tools` and `## Guardrails` ("Invoke `end_call` only after Dan clearly wraps") — those are instructions the model reads but does not speak, so they're safe.
- When writing a closing line, describe it indirectly: "say one short goodbye, then invoke the hangup tool" rather than "say 'I'll end_call now'".
- Cross-reference: anti-patterns "Greeting punchlines with call-control verbs" (related but distinct — that one is about narrative phrasing, this one is about literal tool names).

---

### Greeting punchlines with call-control verbs prime tool firing

Date: 2026-05-19
Tags: skill:build-agent, type:anti-pattern, model:gpt-realtime-2, surface:greeting
Evidence: same call as above (`74f62ec4-4982-4b66-a703-f14a07ced784`). The greeting was the "AI walks into a bar / AI ends call / greatest exit of all time" bit. Even rephrased away from the literal `end_call` tool name, the narrative verb "ends call" sits dangerously close to the tool invocation surface for V2 reasoning models. Subsequent rewrite changed the punchline to `"AI leaves. Greatest exit of all time."` — same comedic shape, no call-control verb.

**Rule:** Greetings and other scripted dialogue should avoid narrative phrasing that names call-control actions ("ends the call", "hangs up", "transfers you", "books the appointment"), even when phrased as story content rather than instruction. Use neutral synonyms ("walks out", "leaves", "wraps", "handing off") that don't map onto a tool the agent has.

**Why:** Distinct from the literal tool-name anti-pattern, this one fires when the model recognizes the *intent* of a tool ("end the call") even without the exact tool name. Reasoning models pattern-match meaning, not just lexicon. Cute punchlines that reference call actions ("and then the AI just hangs up") read funny on the page but read as instructions to the model.

**How to apply:**
- Before locking a greeting, scan it for any phrase that semantically matches a tool the agent has enabled. "Hangs up", "ends the call", "transfers", "books", "sends a text". Replace with neutral verbs.
- For demo / creative copy, prefer absurdist or unrelated subject matter (fridges, weather, traffic) over jokes about phone calls themselves — fewer trap phrases, more comedy mileage.
- This applies to all voice models but matters most for `gpt-realtime-2` and any future reasoning-capable provider tier.

---

### Framing a system prompt as "performing to a room" for an outbound demo

Date: 2026-05-23
Tags: skill:build-agent, type:anti-pattern, surface:system-prompt, context:live-demo
Evidence: Big Dawg agent `cbdfa5b7-dfc6-4b50-b958-ff8eb0fed22e` built live during a Medellin meetup. First prompt draft told the agent "You are NOT on a phone call with one person, you are PERFORMING FOR A ROOM." Operator corrected: the agent is on an outbound 1:1 call, the room only hears it because the human picker-upper is on speakerphone. Rewrote with hybrid framing (1:1 conversation that's also being broadcast to a live audience) and operator approved.

**Rule:** When building a voice agent for a live demo, do not write the system prompt as if the agent is addressing a room. Most live demos are outbound calls played on speaker. The agent IS in a 1:1 conversation; the audience is ambient. Use hybrid framing: "you're on a call with one person, but that phone is on speaker in front of an audience — engage the human directly, throw the occasional line to the room."

**Why:** Prompting an agent to "perform to a room" makes it talk at the audience instead of with the human who picked up. That breaks the dynamic that makes the demo charming — the human is the agent's scene partner. The audience laughs because they're eavesdropping on a real-feeling exchange, not watching a monologue. The "perform to a room" framing also confuses the agent about who it should ask questions to.

**How to apply:**
- Always confirm with the operator: "is this a 1:1 call that an audience will hear (speaker-phoned), or is the agent genuinely addressing a crowd directly?" 1:1-on-speaker is the common case.
- Default prompt framing: agent is on a call with one human, knows the call is being played live for an audience, plays both — engages the human as the scene partner, throws the occasional line to the room.
- Avoid lines like "you are PERFORMING FOR A ROOM" or "address the crowd directly." Replace with "engage the human directly, every few exchanges throw a line over them to the room."

---

### `agent_mode` not inferred from operator intent — must be set explicitly at create

Date: 2026-05-23
Tags: skill:build-agent, type:anti-pattern, surface:agent-create, field:agent_mode
Evidence: Built Big Dawg with operator saying "this will be outbound" up front. `POST /agents` payload omitted `agent_mode` (schema default: `inbound`). Resulting agent had `agent_mode: inbound` even though `greeting_outbound` and `ai_speaks_first_outbound` were populated. Operator caught it. Required a follow-up `PATCH /agents/{id}` with `agent_mode: outbound`.

**Rule:** When the operator says the agent is for outbound (or both), set `agent_mode` explicitly in the `POST /agents` payload. Valid values: `inbound`, `outbound`, `both`. The default is `inbound` — the platform does NOT infer the mode from other fields (greeting_outbound, ai_speaks_first_outbound) or from natural-language intent in the conversation.

**Why:** `agent_mode` is a hard switch that gates which call flows the agent participates in. Setting outbound-flavored fields (greeting_outbound, etc.) without flipping `agent_mode` leaves the agent in inbound-only mode — outbound calls from it may not behave as expected. The operator noticing requires a round-trip PATCH that should have been part of the initial create.

**How to apply:**
- Build-agent flows: when operator's first message includes "outbound", "outbound demo", "outbound call", or similar, set `agent_mode: "outbound"` in the create payload. When unclear, ask before creating.
- For agents that need to serve both directions (rare in this kit's workflows): `agent_mode: "both"` plus populate both greeting fields.
- Verify with `GET /agents/{id}` after create — confirm `agent_mode` matches operator intent.

---

### Building a new agent without consulting `learnings/` first

Date: 2026-05-23
Tags: kit-rule, type:anti-pattern, meta
Evidence: During the Big Dawg live build, the initial `POST /agents` payload set `openai_voice_model: "gpt-realtime-2"` but the response came back with `gpt-realtime-1.5`. This exact bug was already documented in `learnings/bugs.md` (2026-05-19: "POST /agents silently ignores openai_voice_model; defaults to gpt-realtime-1.5. PATCH works"). I had to discover it live and PATCH around it — wasting demo time. Operator was already running a presentation.

**Rule:** Before any non-trivial agent build, skim `learnings/index.md` and at minimum read `learnings/bugs.md` end-to-end. CLAUDE.md mandates this and it's load-bearing — the kit's bug-recovery time depends on it.

**Why:** The bugs file is short. Reading it costs seconds. Re-discovering a documented bug live during a demo costs minutes and operator confidence. Same applies to anti-patterns and best-practices — there are recipes in there that prevent doing the wrong thing.

**How to apply:**
- First action in a build-agent / prospect-demo / any agent-mutation session: `cat learnings/index.md learnings/bugs.md` (or read both via the Read tool). Skim for entries tagged with the surfaces you're about to touch (agent-create, voice config, system prompt, phone assignment).
- Apply known workarounds proactively. Example: when creating an agent with `openai_voice_model: "gpt-realtime-2"`, plan for a follow-up PATCH to actually pin it. Don't be surprised by it mid-build.
- When a learning contradicts a SKILL.md rule, the learning wins until the skill is updated (CLAUDE.md rule).
