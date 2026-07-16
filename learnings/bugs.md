# Bugs

Things that broke unexpectedly. Includes symptom, root cause if known, workaround.

Each entry includes: date, tags, evidence link, rule, why, how to apply.

---

### `PATCH /demos/{id}/` (trailing slash) silently drops the body via 307 redirect

Date: 2026-05-13
Tags: api:demos, http:redirect, type:bug
Evidence: `PATCH https://leadlock-app.onrender.com/demos/{id}/` returned 307; followed by GET that showed config keys not persisted. `PATCH /demos/{id}` (no slash) returned 200 with config stored correctly.

**Rule:** Use `PATCH /demos/{demo_id}` WITHOUT a trailing slash. The trailing-slash form returns 307 and urllib's default `urlopen` follows it but drops the request body in the redirected request, so the PATCH appears to succeed but the data never lands.

**Why:** FastAPI/Starlette typically configures route trailing-slash redirects via `redirect_slashes=True` (the default). The redirect uses HTTP 307 (preserve method), but most HTTP clients re-issue the request without preserving the body when they auto-follow. The result: 200-looking outcome with no state change. The `POST /demos/` endpoint (note the trailing slash) is fine because the route is defined that way — but `PATCH /demos/{id}` is defined WITHOUT trailing slash, and adding one triggers the redirect.

**How to apply:** In any new script hitting Leadlock endpoints, default to NO trailing slash on `PATCH` and `DELETE` routes. If a PATCH appears successful but the GET right after shows no change, the trailing-slash redirect is the most likely culprit. Also worth re-verifying with `urlopen(req).status` — a 307 sometimes leaks through if `MaxRedirects` is set to 0.

---

### `POST /agents` silently ignores `openai_voice_model` and defaults to `gpt-realtime-1.5`

Date: 2026-05-19
Tags: api:agents, skill:build-agent, type:bug, model:openai-realtime
Evidence: agent `baef6000-6707-40c6-91d4-45086c7514cf` — POSTed with `"openai_voice_model": "gpt-realtime-2"`; response returned `"gpt-realtime-1.5"`. Subsequent `PATCH /agents/{id}` with the same field returned `"gpt-realtime-2"` and a follow-up GET confirmed it stuck. Verified twice in one session.

**Rule:** When creating an agent that needs `openai_voice_model=gpt-realtime-2`, POST the agent first and then immediately PATCH `openai_voice_model` (and `openai_reasoning_effort` if non-default) in a second call. Do NOT trust the POST response — verify with a follow-up GET.

**Why:** The schema in `LEADLOCKDOCS.json` explicitly accepts `^(gpt-realtime-1\.5|gpt-realtime-2)$` for `openai_voice_model`, but `POST /agents` ignores the submitted value and writes the default (`gpt-realtime-1.5`) regardless. `PATCH /agents/{id}` honors the field correctly. Most likely a backend mismatch where the agent-creation path doesn't read `openai_voice_model` from the create-body even though the OpenAPI schema lists it. Cost: a user thinks they're on V2 (reasoning + better expressiveness) but the agent is actually running V1.5 — silent capability regression.

**How to apply:** In `build-agent` (and any future skill that creates an agent with the OpenAI provider): always follow `POST /agents` with a `PATCH` that re-asserts `openai_voice_model` and `openai_reasoning_effort`. After the PATCH, GET the agent and confirm `openai_voice_model` matches what was requested. If it doesn't, stop and surface the error — don't proceed to a test call on the wrong model. Track until the platform fix lands; remove the workaround when POST honors the field. Same defensive pattern likely applies to any future provider-version field that has a fallback default.

---

### `POST /agents` ignores `max_call_duration_minutes` and forces the plan default (30 min)

Date: 2026-07-16
Tags: api:agents, skill:build-agent, skill:prospect-demo, type:bug
Evidence: agent `a2136520-df7f-4276-8dc9-a02388cda11e` (Northern Mister Sparky demo, Self Selling tenant). `POST /agents` sent `"max_call_duration_minutes": 10`; the create response AND a follow-up GET both returned `30`. `PATCH /agents/{id}` with `max_call_duration_minutes=10` returned 10 and a GET confirmed it stuck. Verified before/after in one session.

**Rule:** When you need a `max_call_duration_minutes` other than the plan default, POST the agent, then immediately PATCH `max_call_duration_minutes`. Do NOT trust the create response, GET-verify. This is the exact twin of the `openai_voice_model` bug above: `POST /agents` writes a default and silently ignores the create-body value, while `PATCH` honors it.

**Why:** The create path applies a plan/tenant default of 30 minutes and drops the submitted value, with no error (the field is accepted). A demo agent then runs to a 30-minute cap when the operator asked for 10, visible only on a GET.

**How to apply:** In any skill or script that creates an agent (build-agent, prospect-demo, and Big Dawg's `bin/bd-make-demo`), add a post-create PATCH that re-asserts `max_call_duration_minutes` whenever the created value differs from intended, then GET to confirm. Fold it into the same "re-PATCH after create" step already used for `openai_voice_model`. Track until POST honors the field.
