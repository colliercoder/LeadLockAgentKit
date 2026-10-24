# Learnings — index

Pointers into the category files. Newest at top within each section. Skim this before starting any non-trivial task.

Content lives in the category files, not here. To add a new entry, invoke `/add-to-learnings`.

## Platform gaps

- 2026-05-19 — ~~RESOLVED same day~~: `openai_voice` docs updated to list cedar/marin (V2-only) — [platform-gaps.md](platform-gaps.md)
- 2026-05-13 — Two OpenAPI files at kit root — use them together (and remember `demo.config` is open-ended) — [platform-gaps.md#two-openapi-files-at-kit-root-use-them-together](platform-gaps.md#two-openapi-files-at-kit-root-use-them-together)
- 2026-05-13 — ~~RETRACTED~~: avatar/theme/branding gap entries were probing errors; see retractions at top of platform-gaps.md

## Anti-patterns

- 2026-10-24 - Letting the agent guess a last name (update_contact writes it into empty fields) - [anti-patterns.md](anti-patterns.md)
- 2026-07-16 - `collect_contact` is not a functional tool; do not enable it or name it in a prompt - [anti-patterns.md](anti-patterns.md)
- 2026-05-23 — Building a new agent without skimming `learnings/index.md` + `bugs.md` first — [anti-patterns.md](anti-patterns.md)
- 2026-05-23 — `agent_mode` not inferred from intent; must set `outbound` explicitly at create — [anti-patterns.md](anti-patterns.md)
- 2026-05-23 — Framing system prompt as "performing to a room" for an outbound demo (it's a 1:1 on speaker) — [anti-patterns.md](anti-patterns.md)
- 2026-05-19 — Never write a tool name into scripted dialogue lines (V2 reasoning models fire it) — [anti-patterns.md](anti-patterns.md)
- 2026-05-19 — Greeting punchlines with call-control verbs prime tool firing on gpt-realtime-2 — [anti-patterns.md](anti-patterns.md)
- 2026-05-13 — Agent timezone set to operator's tz instead of prospect's causes booking confusion — [anti-patterns.md#agent-timezone-must-match-prospect-not-operator](anti-patterns.md#agent-timezone-must-match-prospect-not-operator)
- 2026-05-13 — Concluding "platform-gap" from openapi alone when the field is `additionalProperties: true` — [best-practices.md#read-deployed-js-chunks-to-find-undocumented-config-keys](best-practices.md#read-deployed-js-chunks-to-find-undocumented-config-keys) (cross-referenced as a debug pattern, not a true anti-pattern entry)

## Best practices

- 2026-10-24 - n8n public API recipes: data tables, row delete path, credentials, publish + webhook probe - [best-practices.md](best-practices.md)
- 2026-10-24 - Leadlock function names are unique per library; test endpoint shape and `test-call-sid` - [best-practices.md](best-practices.md)
- 2026-10-24 - `update_contact` can't correct an email already on file; check updated/skipped - [best-practices.md](best-practices.md)
- 2026-10-24 - Default `openai_vad_eagerness` is `medium` (platform default), not `low` - [best-practices.md](best-practices.md)
- 2026-10-23 - Voice model lineup (Grok Voice 3.0, gpt-realtime-2.1 / 2.1-mini, GPT-Live, Gemini 3.8); supersedes older model names - [best-practices.md](best-practices.md)
- 2026-10-24 - Tool set is fixed at call connect; prompt must describe every enabled tool - [best-practices.md](best-practices.md)
- 2026-10-24 - Describe `reschedule_appointment` as a one-step move or the agent cancels + rebooks - [best-practices.md](best-practices.md)
- 2026-10-24 - Contact intelligence: both flags + Caller Intelligence section, name on turn two - [best-practices.md](best-practices.md)
- 2026-10-24 - GPT-Live voices carry built-in accents; pick the voice for the accent - [best-practices.md](best-practices.md)
- 2026-10-24 - Phone demo caller name is `config.display_name`; keep it short - [best-practices.md](best-practices.md)
- 2026-10-24 - Phone-channel demos run in-browser; no phone number needed on the agent - [best-practices.md](best-practices.md)
- 2026-10-24 - GHL API from Python needs a browser User-Agent (Cloudflare 1010) - [best-practices.md](best-practices.md)
- 2026-10-24 - Local-service prompts state business timezone, service area, only-claim-what-you-know - [best-practices.md](best-practices.md)
- 2026-07-16 - `POST /demos/import-from-url` is slow (Jina + AI extraction); use a 120s timeout - [best-practices.md](best-practices.md)
- 2026-05-31 — Dogfood a new lint/audit skill on the real repo; first-run false positives are the suppression-list spec — [best-practices.md](best-practices.md)
- 2026-05-31 — Content rules (no "closer", no platform name) apply to prompt TEMPLATES, not just runtime output — [best-practices.md](best-practices.md)
- 2026-05-31 — LEADLOCK_API_URL is canonical; _BASE is a deliberate fallback alias, not drift — [best-practices.md](best-practices.md)
- 2026-05-31 — Optional-integration skills carry their own key inline (RETELL_API_KEY), not in base .env — [best-practices.md](best-practices.md)
- 2026-05-31 - A skill isn't shipped until it's in README + welcome + setup-check + .env.example - [best-practices.md](best-practices.md)
- 2026-05-31 - Helper-script artifacts go to ./output/, never /tmp/ - [best-practices.md](best-practices.md)
- 2026-05-23 — `openai_vad_eagerness: high` for outbound 1:1 demo agents (refines the earlier `auto` rule) — [best-practices.md](best-practices.md)
- 2026-05-19 — `LEADLOCKDOCS.json` is the canonical doc source; openapi-spec.json + leadlock-docs.md are stale — [best-practices.md](best-practices.md)
- 2026-05-19 — `GET /calls/{id}` transcript field is the primary diagnostic for unexpected call endings — [best-practices.md](best-practices.md)
- 2026-05-19 — Default to V2-native voices (cedar, marin) when `openai_voice_model=gpt-realtime-2` — [best-practices.md](best-practices.md)
- 2026-05-19 — `openai_vad_eagerness=auto` for conversational/demo agents (not `low`) — [best-practices.md](best-practices.md)
- 2026-05-13 — Read deployed JS chunks to find undocumented config keys — [best-practices.md#read-deployed-js-chunks-to-find-undocumented-config-keys](best-practices.md#read-deployed-js-chunks-to-find-undocumented-config-keys)
- 2026-05-13 — Phone demo per-prospect branding works today (`phone_caller_image` + `phone_accent_color`) — [best-practices.md#phone-demo-per-prospect-branding-works-today](best-practices.md#phone-demo-per-prospect-branding-works-today)
- 2026-05-13 — Transparent iframe surround via `?embed=true` or auto-detect — [best-practices.md#transparent-iframe-surround-for-demo-embeds](best-practices.md#transparent-iframe-surround-for-demo-embeds)
- 2026-05-13 — Use `find_logo.py` to pull a prospect's logo with browser headers — [best-practices.md#use-find_logopy-to-pull-a-prospects-logo-with-browser-headers](best-practices.md#use-find_logopy-to-pull-a-prospects-logo-with-browser-headers)

## Bugs

- 2026-10-24 - `book_appointment` files the booking under whichever contact owns the email - [bugs.md](bugs.md)
- 2026-07-16 - `POST /agents` ignores `max_call_duration_minutes`, forces plan default (30); PATCH works - [bugs.md](bugs.md)
- 2026-05-19 - ~~FIXED on the platform (2026-10-23)~~: `POST /agents` silently ignored `openai_voice_model`; defaults to gpt-realtime-1.5. PATCH works - [bugs.md](bugs.md)
- 2026-05-13 — `PATCH /demos/{id}/` (trailing slash) drops body via 307 redirect — [bugs.md#patch-demosid-trailing-slash-silently-drops-the-body-via-307-redirect](bugs.md#patch-demosid-trailing-slash-silently-drops-the-body-via-307-redirect)

## Skill-specific

- 2026-10-24 - How to word SKILL.md files for current Claude models (Opus 5.5): 10 rules with Anthropic sources. Read before writing or rewording a skill - [skill-authoring.md](skill-authoring.md)
- 2026-05-31 — Agent-team transfer wiring (`transfer_to_agent` in tools_enabled AND non-empty `transfer_to_agents`), voice limits (xai/openai only), verdict via `agent_transitions` — [agent-to-agent-call-testing.md](agent-to-agent-call-testing.md)
- 2026-05-30 — Agent-to-agent outbound passes a real caller-id to the inbound leg, so `{{caller_phone}}` is testable with no human phone — [agent-to-agent-call-testing.md](agent-to-agent-call-testing.md)
- 2026-05-30 — Two-AI-agent calls need `end_call` + a goal-driven user-sim + a low `max_call_duration_minutes`, or they run to the cap — [agent-to-agent-call-testing.md](agent-to-agent-call-testing.md)

## Vertical / industry

(none yet)
