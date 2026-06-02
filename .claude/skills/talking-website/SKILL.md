---
name: talking-website
description: Turn any website into a talking website — a voice agent the visitor clicks and speaks to, that controls the page (navigates, scrolls, jumps to a section, spotlights an element), books appointments on the account's calendar, captures the lead into the CRM, and logs every conversation in Leadlock. Routes through Leadlock so the minutes bill to the account. Ships a drop-in browser engine (vanilla JS, any framework) plus a provisioning helper. Triggers on /talking-website, talking website, voice website, website voice agent, add voice to my site, make my website talk, voice agent on my website, surf the site by voice, web voice agent, embed a voice agent.
---

# Talking Website

Build a voice agent that lives on a website. The visitor clicks a button and talks; the agent answers, **drives the page** (navigate / scroll / jump to a section / spotlight an element / fill a form / click), **books on the calendar**, **captures the lead to the CRM**, and the whole call logs in Leadlock and bills to the account.

This is different from `prospect-demo` (which makes shareable orb demo URLs you send to a prospect). This skill puts a controllable agent **on the customer's own live website**, in their own UI.

## How it works (so you can explain it)

- The browser opens a WebSocket to Leadlock; Leadlock runs the voice provider. **Minutes route through Leadlock**, so they bill to the account that owns the demo slug.
- The agent's page-control tools are **client-executed**: Leadlock declares them to the model, relays the call to the browser over the voice WebSocket, and the page's JS performs the action. The browser engine (`voice-agent.js`) ships those handlers.
- The agent is a normal Leadlock agent — it shows in the dashboard and every call logs as a **Website** conversation.

## When to invoke

- "I want a voice agent on my website that can show people around"
- "Make my site talk / add voice to my site"
- "A talking website like [that Grok demo] but on Leadlock"
- "Embed a voice agent that books appointments on my site"

## Setup check

Confirm `.env` has `LEADLOCK_API_KEY` + `LEADLOCK_API_URL` (default `https://leadlock-app.onrender.com`). Probe `GET /tenants/me`; on 401 fire `setup-check`. Mask the key in output.

## Hard rules

1. **Provider support: `xai` (Grok) or `openai` ONLY.** The client-tool dispatch is wired in the xAI/OpenAI voice path. **Gemini and ElevenLabs do NOT execute web tools** — an agent on those providers would declare the tools but return "Unknown function" when the model calls them. Default to `xai`. If the user insists on Gemini/ElevenLabs, tell them page control won't work yet.
2. **Never name the platform in the agent's prompt/greeting.** Use "our team", "the assistant". Platform name is fine in operator-facing output.
3. **Scrub.** Never hardcode a slug, calendar ID, integration ID, or token into shipped files. Everything is per-account, discovered at build time.
4. **Look up endpoint shapes in `LEADLOCKDOCS.json`** before calling (`/agents` POST/PATCH, `/demos/` POST, `/integrations/ghl/integrations`, `/integrations/ghl/calendars`). The `web_*` tool names below are not REST endpoints — they're values for the agent's `tools_enabled`.

## The page-control tools (set in the agent's `tools_enabled`)

| Tool | Browser action |
|---|---|
| `web_navigate` | go to a path on the site (`{path}`) |
| `web_scroll` | scroll `{direction: down/up/top/bottom}` |
| `web_scroll_to` | smooth-scroll to a section by its visible `{text}` |
| `web_highlight` / `web_clear_highlight` | cinematic spotlight on an element by `{text}` |
| `web_fill` | type into a form field by label/placeholder (`{field, value}`) |
| `web_click` | click a button/link by visible `{text}` |
| `web_remember` | save `{name, interest}` in the visitor's browser → returning-visitor greeting |

Add booking + CRM with the normal built-ins: `book_appointment`, `check_availability`, `get_appointments`, `update_contact`.

## Steps

1. **Gather inputs.** Site URL, the business, the voice (`xai` default), and the site's **page map** — a list of `path → what's there` (e.g. `/pricing → plans`, `/contact → contact form`). Scrape the site or ask. Ask whether to enable booking (needs a calendar) and CRM capture (needs GHL connected).

2. **Attach a calendar (if booking).** `GET /integrations/ghl/integrations` → pick the integration; `GET /integrations/ghl/calendars?integration_id=...` → pick a calendar (ask the user which; never hardcode). You'll set `calendar_provider="gohighlevel"`, `calendar_integration_id`, `calendar_id` on the agent. Without this, `check_availability`/`book_appointment` fail "No calendar integration configured."

3. **Create the agent** (`POST /agents`): `voice_provider` (`xai`), a `greeting`, `ai_speaks_first: true`, `tools_enabled` = the `web_*` tools you want + `book_appointment`/`check_availability`/`update_contact`, and the calendar fields. Write the **system prompt** with: a short identity, the page map, a "call the tool immediately, don't just describe" instruction, a discovery→show→value→book sales sequence, and (if relevant) a service-area / qualification step. See `provision.py` for a working prompt scaffold.

4. **Create the web demo / slug** (`POST /demos/`): `{agent_id, channel: "web", name, config: {session_mode: "web", max_duration_seconds: 1800}}`. **`session_mode: "web"` is what makes the session bill as a real `call` minute and log as a `"web"` conversation** (not a free demo). The response gives you `slug`.

5. **Drop the engine into the site.** Copy `voice-agent.js` into the customer's site and add:
   ```html
   <script src="/voice-agent.js"
           data-leadlock-ws="wss://leadlock-app.onrender.com"
           data-leadlock-slug="THE_SLUG_FROM_STEP_4"></script>
   ```
   The engine renders a restyleable button and handles mic/audio + all the page-control tools. For a custom UI, use headless mode (`data-leadlock-headless="true"`) and drive `window.LeadlockVoice.start()/stop()` yourself. See the header comment in `voice-agent.js`.

6. **Verify.** Load the site, click the button, say "take me to the [page]" → it should navigate; describe a problem → it guides; ask to book → it books on the calendar; give name + phone → a GHL contact appears. The call shows in the Leadlock dashboard as a Website conversation.

`provision.py` does steps 2-4 in one shot (stdlib only). Run:
```
LEADLOCK_API_KEY=sk_live_... python3 provision.py --name "Acme Website Assistant" --voice xai
```
It prints the slug + the exact `<script>` tag to paste.

## Limitations to tell the user

- **Can't fill third-party iframes.** If the site's form/scheduler is an embedded vendor iframe (ServiceTitan, Calendly, a GHL form iframe), `web_fill`/`web_click` **cannot touch it** (browser cross-origin security). Book through the Leadlock calendar by voice instead. `web_fill` works on the site's own native (same-origin) forms.
- **Multi-page sites drop the call on hard navigation.** On a single-page app (React/Vue/Astro view-transitions) the engine keeps the call alive across page changes. On a classic multi-page site, `web_navigate` does a full reload that ends the call. The engine handles SPA persistence if you wire `window.__llNavigate` (see the file); full multi-page call-resume is a future enhancement.
- **It bills.** A web session meters real `call` minutes to the account. The engine ends the call after ~2.5 min of visitor silence (Leadlock's web silence watchdog), but it's still live voice — set expectations on usage.
