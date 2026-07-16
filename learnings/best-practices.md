# Best practices

Patterns that worked well and are worth repeating. Concrete, not generic.

Each entry includes: date, tags, evidence link, rule, why, how to apply.

---

### A skill isn't shipped until it's in README + welcome + setup-check + .env.example

Date: 2026-05-31
Tags: type:pattern, area:skill-integration, discoverability

Evidence: `build-agent` and `agent-to-agent-call-testing` shipped with only a README skills-table row. Both were missing from the README "common phrases" block, the `welcome` menu, and the `setup-check` available-skills list, so a new user typing "help" would never be routed to them. `retell-to-leadlock` had the same gap before it was wired in.

**Rule:** Adding `.claude/skills/<name>/SKILL.md` makes a skill auto-discoverable by Claude, but NOT by a human reading the kit. A new skill is only "done" when it appears in all five surfaces: (1) README skills table, (2) README "Common phrases that fire each skill" block, (3) `welcome/SKILL.md` menu, (4) `setup-check/SKILL.md` "Skills available" list, and (5) any required env var documented in `.env.example`.

**Why:** CLAUDE.md promises the welcome skill will "either route them to the right tool or show them the menu." A skill absent from the menu silently breaks that promise, and setup-check (the auto-fired "what can I run" diagnostic) under-reports the kit on a user's first authenticated turn.

**How to apply:** Make this the closing checklist of "Adding a new skill." Grep all five surfaces for the new name before calling it shipped: `grep -c <skill-name> README.md .claude/skills/welcome/SKILL.md .claude/skills/setup-check/SKILL.md .env.example`.

---

### Helper-script artifacts go to ./output/, never /tmp/

Date: 2026-05-31
Tags: type:pattern, area:helper-scripts, hard-rule-10

Evidence: `agent-to-agent-call-testing/harness.py` + `team_harness.py` defaulted `--out` to `/tmp/agent_loop_results.json`, and the Claude session is told to read that file to judge transcripts. Hard rule 10 says output artifacts live in `./output/` (gitignored). Fixed both defaults to `./output/agent_loop_results.json` with `os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)`.

**Rule:** Any helper script that writes a results/output artifact must default to `./output/` under the kit root, and must `os.makedirs(..., exist_ok=True)` first (the dir is gitignored and won't exist on a fresh clone). Never default to `/tmp/`: users look in `./output/`, `/tmp/` isn't guaranteed writable/persistent cross-platform, and Hard rule 8 says don't write to `/tmp/` without flagging it.

**Why:** A new user following the kit convention looks in `./output/` and finds nothing if the artifact landed in `/tmp/`. One consistent location also means one place to find every run's output.

**How to apply:** When writing or reviewing a helper `.py`, check its output-path default. Mirror the pattern: `default="./output/<name>.json"` plus a mkdir at the top of `main()`.

---

### Use `find_logo.py` to pull a prospect's logo with browser headers

Date: 2026-05-13
Tags: skill:prospect-demo, type:pattern, helper-script
Evidence: `.claude/skills/prospect-demo/find_logo.py`; verified working against `northernmistersparky.com` (Cloudflare-protected) — picked the 192×192 apple-touch-icon as avatar

**Rule:** When you need a prospect's logo, run `python3 .claude/skills/prospect-demo/find_logo.py <url> --download ./output/<slug>` instead of hand-grepping the HTML. The helper handles Cloudflare's basic block (browser User-Agent), parses `<link rel="apple-touch-icon">`, `<link rel="icon">`, og:image, and `<img class="logo">`, dedupes by URL, and returns two best-fit candidates — `avatar` (square) and `header` (rectangular).

**Why:** Logo extraction repeats across most demo builds. The bare `curl` pattern fails on Cloudflare sites without the right headers. Selecting "the right logo" depends on the slot (avatar wants square icons, header wants og:image), and that prioritization is non-obvious. Centralizing it in a small helper means each new build does it the same way and the priorities can be improved in one place.

**How to apply:** Step 1.5 of `prospect-demo/SKILL.md` calls this helper. When building any future demo-creation skill, reuse the pattern (don't duplicate the helper — point at the file). Then upload the chosen avatar to the demo via `POST /demos/{demo_id}/upload-image` and wire it through `phone_caller_image` — see `[[best-practices#phone-demo-per-prospect-branding-works-today]]`.

---

### Phone demo per-prospect branding works today

Date: 2026-05-13
Tags: skill:prospect-demo, type:pattern, channel:phone, surface:public-demo-page
Evidence: deployed bundle `https://app.leadlock.ai/assets/_slug_-DnMHePt3.js` reads `(t.config)?.phone_caller_image` and `(t.config)?.phone_accent_color`; passes them as `callerImage` / `accentColor` to `PhoneDemoView`

**Rule:** Phone-channel demos accept two per-demo branding knobs in `demo.config`. Set them via `PATCH /demos/{demo_id}`:
- `phone_caller_image` — URL to the avatar image (PNG/JPG, square). Replaces the agent-initials fallback.
- `phone_accent_color` — hex color string (e.g. `"#FFC72C"`). Drives the call-arc ring color, the accept-button glow, and other accents. Defaults to `#3b82f6` (blue) when absent.

Recipe (Northern Mister Sparky example):
```bash
# 1. Find and download the logo
python3 .claude/skills/prospect-demo/find_logo.py https://prospect.com --download ./output/<slug>

# 2. Upload to the demo, get back a Supabase URL
curl -X POST $API_URL/demos/$DEMO_ID/upload-image \
  -H "X-API-Key: $KEY" \
  -F "file=@./output/<slug>/<avatar>.png"
# → { "url": "https://<project>.supabase.co/storage/v1/object/public/.../avatar.png" }

# 3. Wire it into the demo config (plus accent color)
curl -X PATCH $API_URL/demos/$DEMO_ID \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"config": {
        "phone_caller_image": "<url from step 2>",
        "phone_accent_color": "#FFC72C",
        "display_name": "Northern Mister Sparky",
        "landing_heading": "Talk to Maya — Northern Mister Sparky",
        "landing_subheading": "Tap to call: ...",
        "landing_instructions": "..."
      }}'
```

**Why:** These keys are undocumented — they don't appear in `openapi-spec.json`/`LEADLOCKDOCS.json` because `demo.config` is `additionalProperties: true`. Found them by reading the deployed `/d/<slug>` route chunk (`_slug_-DnMHePt3.js`), which destructures the keys directly from `t.config`. The prior "platform-gap" entry was a probing error — see `[[platform-gaps#demo-page-avatar-cannot-be-overridden-via-api]]` (retracted).

**How to apply:** Add this to every phone-channel demo build by default. The logo-finder already stages the right image. The accent color should match the prospect's brand (pull from `og:image` ambient color, or pick from the brand palette manually). If the prospect doesn't have an obvious brand color, leave `phone_accent_color` off and accept the blue default. Verify after PATCH by re-fetching the demo and confirming both keys are stored — then load the page and confirm the avatar circle shows the image, not initials.

---

### Transparent iframe surround for demo embeds

Date: 2026-05-13
Tags: skill:prospect-demo, type:pattern, surface:iframe-embed
Evidence: deployed bundle `_slug_-DnMHePt3.js` lines (post-mount useEffect): `if(z||w||A){ document.documentElement.style.background="transparent"; document.body.style.background="transparent"; #root.style.background="transparent"; }` where `z=h.get("embed")==="true"`, `w=h.get("mode")==="phone"`, `A=window.self!==window.top`

**Rule:** Embedded demo iframes get transparent backgrounds automatically when ANY of these conditions hit:
1. The iframe URL includes `?embed=true`
2. The iframe URL includes `?mode=phone`
3. The page is loaded inside an iframe at all (`window.self !== window.top` — auto-detect)

This means: the parent page's background bleeds through. White GHL page → white surround. Whatever color the user puts behind the iframe wins.

**Why:** The surround color is controlled by the parent, not the demo. Old approach was to file a feature request for a per-demo theme override — unnecessary. Just embed the iframe on the GHL section with the right background.

**How to apply:** Always include `?embed=true` on iframe sources for safety (it's idempotent with the iframe auto-detect, but explicit is better). The iframe template in `prospect-demo/SKILL.md` should look like:

```html
<iframe
  src="https://app.leadlock.ai/d/<slug>?embed=true"
  width="100%"
  height="780"
  style="border:0; border-radius:12px; max-width:480px; background:transparent;"
  allow="microphone; autoplay"
  loading="lazy"
  title="<Business> — <Agent> (Phone Demo)"
></iframe>
```

Tell the prospect to drop it on whatever GHL section color they want. If they want white surround, the section background needs to be white. Note: the *phone mockup itself* keeps its dark bezel — that's the iPhone-style frame design, not the page background. Only the area around the bezel inherits from the parent.

---

### Read deployed JS chunks to find undocumented config keys

Date: 2026-05-13
Tags: type:debug-pattern, source:deployed-bundle
Evidence: discovered `phone_caller_image`, `phone_accent_color`, `embed=true` query handling by reading `_slug_-DnMHePt3.js`; none of these strings appear in openapi-spec or LEADLOCKDOCS

**Rule:** When the openapi spec marks a field as `additionalProperties: true` (typical for `demo.config`, `agent.tool_instructions`, etc.) and a user claims undocumented behavior, don't argue from the spec — read the deployed JS chunk that renders the relevant surface.

Recipe:
```bash
# 1. Get the HTML for the surface in question
curl -s -H "User-Agent: Mozilla/5.0" https://app.leadlock.ai/d/<some-existing-slug> > /tmp/page.html

# 2. Find the JS bundles referenced
grep -oE '/assets/[A-Za-z0-9_\-]+\.js' /tmp/page.html

# 3. Grab the main bundle, find route lazy-loads
curl -s https://app.leadlock.ai/assets/index-<hash>.js | grep -oE '[A-Za-z]+(_[A-Za-z]+)*-[A-Za-z0-9]{8,}\.js' | sort -u
# Look for chunk names matching the surface (e.g. _slug_-*.js for /d/[slug], PhoneDemoView-*.js)

# 4. Grep that chunk for snake_case property accesses (config keys are usually snake_case)
curl -s https://app.leadlock.ai/assets/_slug_-<hash>.js | grep -oE '\.[a-z][a-z_]{4,30}' | sort -u | grep _

# 5. For each key, find the usage context to understand what it controls
```

**Why:** The platform's openapi schema is the formal contract for typed fields. For `additionalProperties: true` fields like `demo.config`, the schema doesn't enumerate accepted keys — they're discoverable only from the renderer. Doing this discovery in 60 seconds saves a feature-request round-trip and prevents publishing wrong "platform gap" entries.

**How to apply:** Whenever you're about to write "the API doesn't support X" for a feature that lives in a free-form config object, run this audit first. If the JS chunk contains the snake_case key, the feature exists — try it. If it doesn't, then it's a real gap. Document the audit result either way.

---

### Default V2-native voices when using `openai_voice_model=gpt-realtime-2`

Date: 2026-05-19
Tags: skill:build-agent, type:pattern, model:gpt-realtime-2, provider:openai
Evidence: live YouTube demo agent `baef6000-6707-40c6-91d4-45086c7514cf` — switched from `ash` (legacy v1 voice) to `cedar` (V2-native voice) once the user pointed it out; the V2-native voice noticeably improved prosody and expressiveness on the test call.

**Rule:** When creating an agent with `voice_provider=openai` and `openai_voice_model=gpt-realtime-2`, default to a V2-native voice (currently `cedar` or `marin`) rather than the legacy v1 voices (`alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`). Only fall back to a legacy voice if the user explicitly requests one or if voice continuity with an existing V1.5 agent matters.

**Why:** Legacy v1 voices technically render on V2 but were tuned for V1.5 and don't take advantage of V2's improved expressiveness. V2-native voices were introduced alongside the V2 model. For demos and customer-facing agents where voice quality matters, the V2-native voices are the better default. See `[[platform-gaps#openai_voice-description-lists-only-legacy-voices-cedar-marin-v2-only-accepted-but-undocumented]]` for why this isn't obvious from the docs.

**How to apply:**
- Update `build-agent`'s curated voice menu so the top picks for `voice_provider=openai` lead with V2-native voices (cedar, marin, …) when the user is picking V2 mode.
- Group the legacy voices into a "legacy / v1.5" sub-section in the picker so users see them but understand they're not the recommended path for V2.
- When the user explicitly requests V1.5 (e.g. for cost reasons — V2 is premium-priced), revert to the legacy v1 voices as the default.

---

### `openai_vad_eagerness=auto` for conversational demo agents

Date: 2026-05-19
Tags: skill:build-agent, type:pattern, model:gpt-realtime-2, surface:vad
Evidence: live YouTube demo agent `baef6000-6707-40c6-91d4-45086c7514cf` — the user manually changed `openai_vad_eagerness` from `low` (the kit's default) to `auto` after the first test call felt awkwardly paced. The follow-up call held conversational rhythm better.

**Rule:** For conversational demo or receptionist agents where the human user may pause, laugh, react slowly, or talk to someone off-mic mid-call, set `openai_vad_eagerness=auto` rather than the kit's `low` default. `low` is meant for production qualifying agents where being extra patient is safer; `auto` lets the model decide based on context.

**Why:** `low` eagerness instructs the OpenAI realtime VAD to wait longer before deciding the user has finished talking. For qualifying calls where the agent must not interrupt the prospect's objection mid-sentence, `low` is correct. For demo or banter-style calls where the human may finish their turn quickly with a one-word reaction ("nice", "yeah", a laugh), `low` holds the turn open too long and creates an awkward gap. `auto` adapts based on speech patterns and tends to feel more natural in those contexts. `high` (the other end) is fine for fast-paced calls but risks talking over the user.

**How to apply:**
- In `build-agent`, when the agent's purpose is a demo, a receptionist with light conversational intent, or any "feels like a friend" use case — default to `openai_vad_eagerness=auto`.
- Keep `low` as the default for outbound prospecting / qualifying agents where being patient is critical.
- Make this a question in the build-agent interview if the agent's primary purpose isn't obvious from context.
- This applies to `voice_provider=openai`. Other providers have their own analogues (`gemini_end_sensitivity`, etc.) — different tuning rules.

---

### `GET /calls/{id}` transcript field is the primary diagnostic for "the call ended weird"

Date: 2026-05-19
Tags: skill:build-agent, skill:call-audit, skill:prompt-tuner, type:debug-pattern, surface:transcript
Evidence: call `74f62ec4-4982-4b66-a703-f14a07ced784` — `transcript` field contained an ordered list of `{role, content, timestamp}` entries (plus `tool_args`/`tool_result` for tool roles), which pinpointed `end_call` firing at 24.45s, ~1.5s after a one-word misheard user utterance. Without the transcript, we'd have been guessing at AMD vs silence vs prompt issue. With it, the root cause was immediate.

**Rule:** Whenever a call ends unexpectedly (too soon, too late, dropped, weird tool firing, missed booking), the FIRST diagnostic step is `GET /calls/{id}` and read the `transcript` array. The transcript shows role (`assistant` / `user` / `tool` / `tool_result`), content, timestamp (seconds from start), and for tool roles also `tool_name`, `tool_args`, and `tool_result`. Scan for the exact moment things went wrong and the immediate preceding turn — that's almost always the cause.

**Why:** The call detail also has `amd_status`, `amd_detection_ms`, `duration_seconds`, and `ended_at` — useful framing but not diagnostic. The transcript is where the actual sequence is. Reasoning models can fire tools based on a single misheard utterance, a scripted dialogue line, or a punchline phrase — none of those are visible from status fields, only from the transcript. The `tool_args` field is especially useful: e.g. `end_call({"reason":"completed"})` vs `end_call({"reason":"no_response"})` tells you whether the model thought the call was wrapped up or thought the user was unreachable.

**How to apply:**
- `build-agent` and `prompt-tuner` should both include "fetch call transcript via `GET /calls/{id}` after test call" as a standard step.
- `call-audit` should make the transcript the centerpiece of every per-call analysis.
- When PATCH'ing an agent's prompt after a bad call, quote the offending transcript line(s) in the change rationale so the next maintainer can see what triggered the rewrite.
- Useful one-liner: list the last 5 calls for an agent, then pull the transcript of the most recent one:
  ```python
  calls = GET(f"{API}/calls?agent_id={aid}&limit=5")
  last = calls['calls'][0]
  detail = GET(f"{API}/calls/{last['id']}")
  for turn in detail['transcript']:
      print(f"{turn['timestamp']:6.2f}s  {turn['role']:12s}  {turn.get('content','')[:140]}")
  ```

---

### `LEADLOCKDOCS.json` is the canonical doc source; `openapi-spec.json` and `leadlock-docs.md` are stale exports

Date: 2026-05-19
Tags: type:docs-meta, file:LEADLOCKDOCS.json, kit-rule
Evidence: User explicitly designated `LEADLOCKDOCS.json` as the canonical reference (2026-05-19). During this session, the file was updated twice mid-session by the user (adding `openai_voice_model`, then updating `openai_voice` description to enumerate cedar/marin) — both updates landed in `LEADLOCKDOCS.json`, neither in `openapi-spec.json` or `leadlock-docs.md`. The latter two files at the kit root were not refreshed and are now drifted.

**Rule:** When referencing the Leadlock API docs from any skill, helper script, or new code in this kit, point at `/Users/danielgauerke/Projects/LeadLockAgentKit/LEADLOCKDOCS.json` (or just `LEADLOCKDOCS.json` if working from the kit root). Do not reference `leadlock-docs.md` or `openapi-spec.json` in new content. The latter two are kept on disk for now but are slightly older snapshots — drift will accumulate.

**Why:** The user maintains `LEADLOCKDOCS.json` as the live export from the platform. The other two files were earlier exports and don't get updated when fields are added or descriptions are corrected. Skills that reference the stale files will give wrong answers about new fields (e.g. `openai_voice_model`, `openai_reasoning_effort`, V2-only voices). The user has also stated they will refresh `LEADLOCKDOCS.json` as the platform changes — so it's the live contract.

**How to apply:**
- New skill SKILL.md files should reference `LEADLOCKDOCS.json` in their endpoint-lookup steps. Pattern: `python3 -c "import json; s=json.load(open('LEADLOCKDOCS.json')); print(s['paths']['/agents']['post'])"`.
- Existing skills (prospect-demo, add-to-learnings) had references to the old filenames — those were updated 2026-05-19 (this session).
- CLAUDE.md and README.md were also updated to reflect this 2026-05-19.
- When the user says "the docs were updated," re-read `LEADLOCKDOCS.json` (not the other two). The pattern of "user updates docs mid-session" happens — assume it could happen again.

---

### `openai_vad_eagerness: high` for outbound 1:1 demo agents (not `auto` or `low`)

Date: 2026-05-23
Tags: skill:build-agent, type:pattern, model:gpt-realtime-2, surface:vad
Evidence: Big Dawg outbound demo (agent `cbdfa5b7-dfc6-4b50-b958-ff8eb0fed22e`). Initial config set `openai_vad_eagerness: "low"` (under the false assumption the agent would be "performing to a room" and need to ride audience laughter). Operator changed to `high` for the live outbound call to a single picker-upper. Existing learning (2026-05-19) said "use `auto` for conversational/demo agents" — that was for inbound web-widget demos with potentially ambient noise. Outbound 1:1 is different.

**Rule:** For outbound voice agents on `gpt-realtime-2` calling a single human (including live demos played on speaker), set `openai_vad_eagerness: "high"`. The agent needs snappy turn-taking with one person on a phone line. Reserve `auto` for inbound conversational demos and `low` only when the agent genuinely needs to ride extended pauses (long-form storytelling, multi-party crowd interaction directly).

**Why:** Outbound 1:1 calls have one clear conversation partner. High eagerness means the agent picks up turns quickly, which feels lively and natural. Low/auto eagerness makes the agent feel slow on the phone, with awkward gaps after the human stops speaking. Crowd noise from a room hearing the call on speaker is not a real ambient-noise concern for the agent's mic — the agent only hears the picker-upper's phone, not the room.

**How to apply:**
- Build-agent flow: if `agent_mode` is `outbound`, default to `openai_vad_eagerness: "high"`. If `inbound` and the demo is web-widget / quiet-room, use `auto`. If `inbound` and used in a noisy retail/restaurant phone line, consider `medium` or `low`.
- Cross-reference: the 2026-05-19 best-practice entry "openai_vad_eagerness=auto for conversational/demo agents" applies to inbound conversational demos, not outbound. Both rules coexist — pick based on direction and use case.
- Verify after create/PATCH with `GET /agents/{id}` — confirm `openai_vad_eagerness` matches intent.
- If a skill genuinely needs prose for grepping (the old `leadlock-docs.md` use case), generate it on demand from `LEADLOCKDOCS.json` rather than reading the stale file.

---

### Dogfood a new lint/audit skill on the real repo before trusting its output

Date: 2026-05-31
Tags: skill:kit-audit, type:pattern
Evidence: commit 9b383ec (kit-audit), output/kit-audit-2026-05-31.md

**Rule:** Run any new audit/lint skill against the actual kit on its first build, treat the first run's false positives as the design spec for a suppression list, and bake that list into the SKILL.md before relying on the skill.

**Why:** kit-audit's first run threw 8 FAILs + 41 WARNs against the repo — nearly all false positives from a naive regex pass (forbidden strings used to forbid them, placeholder secrets, slash-commands/website-routes mistaken for API paths, utility skills held to execution-skill anatomy). A regex can't tell "names a file to prohibit it" from "instructs reading it." Endpoint correctness and content-rule checks need Claude's judgment, not grep.

**How to apply:** On a new lint/audit skill, do a first real run, sort findings into real vs false-positive, and write the false-positive classes into a "Suppress these" block in the SKILL.md so future runs (and other Claudes) don't repeat them. The script is only a first-pass net; the SKILL.md drives the judgment.

---

### Content rules apply to prompt TEMPLATES, not just runtime output

Date: 2026-05-31
Tags: skill:prospect-demo, type:pattern
Evidence: commit ef9fb46

**Rule:** Apply the kit's content rules (no "closer", never name the platform in agent copy) to generated-prompt skeletons and placeholder examples, not only to live runtime output.

**Why:** prospect-demo carried the word "closer" inside its generated system-prompt template — in a `<ROLE_BOUNDARIES — e.g. "...not a closer.">` placeholder. It's still generated copy, so it still violated CLAUDE.md hard rule 4 and the skill's own rule 3, even framed as a negative example. kit-audit caught it; it had shipped unnoticed.

**How to apply:** When auditing or writing a skill, grep its prompt-template blocks (the skeleton the skill emits) for "closer" and the platform name the same way you'd check runtime copy. Placeholder examples count.

---

### LEADLOCK_API_URL is canonical; LEADLOCK_API_BASE is a deliberate alias, not drift

Date: 2026-05-31
Tags: type:pattern
Evidence: this session (.env standardized; a2a harness.py L86, build-agent SKILL.md L99)

**Rule:** Standardize `.env` and new skills on `LEADLOCK_API_URL`. The a2a harness and build-agent additionally accept `LEADLOCK_API_BASE` as a fallback — that's defensive, not an inconsistency. Don't flag it as drift.

**Why:** The kit's `.env` shipped with the minority name `LEADLOCK_API_BASE` while 11 skills read `LEADLOCK_API_URL`; it only worked because both fall back to the same default host. Two skills read `_BASE` first then `_URL`, which is exactly what kept a stale `.env` from breaking them. Standardizing on `_URL` (the name CLAUDE.md documents) while keeping the alias is the robust resolution.

**How to apply:** New skills read `env.get("LEADLOCK_API_URL", env.get("LEADLOCK_API_BASE", "<default-host>"))`. A bare `.env` missing the key, or a skill reading ONLY a non-standard name, is a real finding; `_BASE` present as a fallback is not.

---

### Optional-integration skills carry their own key inline, not in the base .env

Date: 2026-05-31
Tags: skill:retell-to-leadlock, type:pattern
Evidence: commit 194c229

**Rule:** A skill that needs a third-party key most kit users will never have (e.g. retell-to-leadlock → RETELL_API_KEY) should fail fast at its own setup step with an inline "add this key" one-liner, not force the key into everyone's base `.env` or bounce to setup-check.

**Why:** Retell is a niche skill. Putting RETELL_API_KEY in the base `.env`/setup-check as if it were required would confuse the majority who never port from Retell. The skill owns its dependency: on a missing key it now hands the user `echo 'RETELL_API_KEY=...' >> ./.env` plus where to find it. A missing Leadlock (base) key still routes to setup-check — that's a different problem.

**How to apply:** For any future optional-integration skill, keep its key out of the base config, mark it optional in setup-check/welcome, and have the skill's own setup step give the add-it-now instruction inline.

---

### `POST /demos/import-from-url` is slow, give it a 120s timeout

Date: 2026-07-16
Tags: api:demos, skill:prospect-demo, type:pattern, http:timeout
Evidence: `POST /demos/import-from-url` for `northernmistersparky.com` timed out at a 30s HTTP client timeout twice, then succeeded at ~150s. The endpoint runs the Jina Reader scrape plus an xAI extraction pass across multiple pages (homepage + /about + several /areas-we-serve/*), so wall-clock routinely exceeds 30s.

**Rule:** When calling `POST /demos/import-from-url` (or `/agents/wizard/import-website`), set the HTTP client timeout to at least 120s. The common 30s default times out on real multi-page sites, and a naive retry just times out again.

**Why:** The scrape endpoint fans out to several pages then runs an LLM extraction, so it takes tens of seconds to two minutes depending on the site. A 30s timeout fails on anything non-trivial and the operator sees "read operation timed out", which reads like the site is unreachable when it is really just slow.

**How to apply:** In new code, do the scrape POST with an explicit long timeout (Big Dawg's `bin/bd-make-demo scrape` uses `--timeout 120` via a direct `urlopen` rather than the shared 30s client). If the scrape still fails, fall back to reading the homepage plus key pages directly to author the prompt, rather than blocking the whole demo on the extraction endpoint.
