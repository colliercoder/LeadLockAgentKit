# Platform gaps

Missing API knobs, undocumented behaviors, things that need a `leadlock-app` change. Each entry should reference the platform feature request if one was filed.

Each entry includes: date, tags, evidence link, rule, why, how to apply.

---

### ~~Demo page avatar cannot be overridden via API~~ — INCORRECT, retracted 2026-05-13

Date: 2026-05-13 (retracted same day)
Tags: skill:prospect-demo, type:retraction
Evidence: deployed bundle `https://app.leadlock.ai/assets/_slug_-DnMHePt3.js` reads `(t.config)?.phone_caller_image` and passes it as `callerImage` to PhoneDemoView

**Retraction:** This entry was wrong. The deployed `/d/<slug>` page DOES read a per-demo avatar from `demo.config.phone_caller_image` and renders it in the call-screen avatar circle. The original probing checked the wrong keys (`avatar_url`, `logo_url`, etc.) and never tried the real one (`phone_caller_image`). It also searched the main JS bundle and a couple of obvious chunks, but missed `_slug_-DnMHePt3.js` (the actual route-page component) which is where the wiring lives.

**Working recipe:** see `best-practices.md` → "Phone demo per-prospect branding".

---

### ~~Demo page theme cannot be overridden cross-origin~~ — INCORRECT, retracted 2026-05-13

Date: 2026-05-13 (retracted same day)
Tags: skill:prospect-demo, type:retraction
Evidence: deployed bundle `_slug_-DnMHePt3.js` contains: `z=h.get("embed")==="true"; A=window.self!==window.top; if(z||w||A){ document.documentElement.style.background="transparent"; document.body.style.background="transparent"; #root.style.background="transparent"; }`

**Retraction:** This entry was wrong. The deployed page makes html/body/#root transparent in three cases: (1) `?embed=true` query param, (2) `?mode=phone` query param, (3) the page is loaded inside an iframe at all (auto-detect via `window.self !== window.top`). The localStorage `leadlock_theme` is a SEPARATE bootstrap script for the surrounding chrome and doesn't gate the per-page transparency.

**Working recipe:** see `best-practices.md` → "Transparent iframe surround for demo embeds".

---

### ~~`PublicDemoResponse.branding` is agency-scope, not per-demo~~ — half-right, refined 2026-05-13

Date: 2026-05-13 (refined same day)
Tags: skill:prospect-demo, type:refinement, schema:PublicDemoResponse

**Refinement:** The `branding` field on `PublicDemoResponse` IS populated from agency-level `BrandingSettings` (still true — that part holds). But this does NOT mean per-demo customization is impossible — `demo.config` carries per-demo overrides for the call-screen avatar (`phone_caller_image`) and the accent color (`phone_accent_color`). Those keys live on `config`, not `branding`. The lesson: don't read the spec as the complete contract — the renderer reads keys that aren't in any documented schema (because `demo.config` is `additionalProperties: true`).

**How to apply:** When a customization "doesn't seem possible per the spec", read the deployed JS chunk that owns the rendering surface, not just the openapi schema. Look at the chunk list referenced from the main bundle for any route lazy-loads (e.g. `_slug_-DnMHePt3.js` for `/d/[slug]`). The component prop names (camelCase) often map directly to snake_case config keys.

---

### Two OpenAPI files at kit root — use them together

Date: 2026-05-13
Tags: type:docs-meta, file:openapi-spec.json, file:LEADLOCKDOCS.json
Evidence: `openapi-spec.json` (492KB, 283 paths) and `LEADLOCKDOCS.json` (910KB, 275 paths) on disk 2026-05-13

**Rule:** When auditing the API, check both `openapi-spec.json` AND `LEADLOCKDOCS.json` at the kit root. Neither is a strict superset. AND remember: `demo.config` is `additionalProperties: true` — the renderer reads keys that aren't in any documented schema. Verify customization knobs against the deployed JS chunks (`/assets/_slug_-*.js` for the demo route), not just the openapi spec.

**Why:** `openapi-spec.json` has 10 endpoints that `LEADLOCKDOCS.json` doesn't. `LEADLOCKDOCS.json` has 2 endpoints openapi-spec doesn't. Demo-related schemas are functionally identical in both. The naming is misleading — `LEADLOCKDOCS.json` sounds canonical but is actually a slightly older export. Neither file documents `phone_caller_image`, `phone_accent_color`, `embed=true` etc., even though those are deployed and working.

**How to apply:** Default to `openapi-spec.json` for endpoint coverage. Cross-check `LEADLOCKDOCS.json` for trial/billing endpoints. For demo customization knobs specifically, ALWAYS verify against the deployed renderer chunk — see best-practices "Read deployed JS chunks to find undocumented config keys".

---

## Real platform gaps (not retracted)

---

### ~~`openai_voice` description lists only legacy voices; cedar/marin (V2-only) accepted but undocumented~~ — RESOLVED 2026-05-19

**Resolution (2026-05-19, same day):** Platform docs updated. `LEADLOCKDOCS.json` → `AgentCreate.properties.openai_voice.description` now reads: `"OpenAI voice ID. v1.5 voices: alloy, ash, ballad, coral, echo, sage, shimmer, verse. v2 adds: marin, cedar (only available when openai_voice_model='gpt-realtime-2')."` The description correctly enumerates both the legacy and V2-native voices and notes the model-compatibility constraint. The field is still `type: string` with no enum/pattern (so other voice names won't error at the schema layer), but the documented contract is now accurate. Leaving the entry below as a historical record; do not act on the original "gap" since it's been closed.

---

### Original entry (kept for history)

Date: 2026-05-19
Tags: skill:build-agent, type:platform-gap, file:LEADLOCKDOCS.json, model:gpt-realtime-2
Evidence: `LEADLOCKDOCS.json` → `AgentCreate.properties.openai_voice.description` reads `"OpenAI voice ID (alloy, ash, ballad, coral, echo, sage, shimmer, verse)"`. Field schema is `{"type": "string"}` with no pattern restriction. Setting `openai_voice: "cedar"` via PATCH on agent `baef6000-6707-40c6-91d4-45086c7514cf` returned 200 and the value persisted; a follow-up GET confirmed `openai_voice: "cedar"`. The user named `marin` as a second V2-only voice but it wasn't probed in this session.

**Rule:** When building an agent with `openai_voice_model=gpt-realtime-2`, prefer the V2-native voices (`cedar`, `marin`, and likely others) over the legacy v1 voices listed in the schema description. The schema description is wrong by omission; treat the documented list as a non-exhaustive sample, not a closed enum.

**Why:** The OpenAI realtime API ships with provider-version-specific voice rosters. The legacy v1 voices (alloy, ash, ballad, coral, echo, sage, shimmer, verse) technically render on V2 but don't take advantage of V2's improved prosody/expressiveness. The V2-native voices (cedar, marin, …) were introduced alongside the V2 model and are noticeably better for it. The platform's docs description hasn't been updated to reflect them, but the field is open-string so they accept anything; verification only happens at runtime against OpenAI's API.

**How to apply:**
- In `build-agent`'s voice picker, when the user selects `voice_provider=openai` AND the agent is being created with `openai_voice_model=gpt-realtime-2` (which should be the new default — see best-practices entry), surface cedar/marin as the primary recommendations and demote ash/alloy/etc. to a "legacy" sub-list.
- Don't restrict the picker to only the documented voice list. If a user pastes a voice name the docs don't mention, accept it and verify with a test call.
- Re-probe periodically — OpenAI ships new voices on the V2 line; update the curated list as they appear.
- Until the platform updates the field description, this gap stays open. A short feature request to Leadlock: "Update `openai_voice` description to reflect the V2 voice roster (cedar, marin, …) and add a `model_compatibility` tag if possible."
