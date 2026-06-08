# Leadlock Agent Kit

A growing library of Claude Code skills for Leadlock agency owners. Run them with one command, no UI clicks, no SQL access required — just your Leadlock API key.

## What's in the kit

| Skill | What it does |
|---|---|
| `build-agent` | Guided end-to-end builder for a single voice agent. Discovers your phones + GHL calendars on the account, asks the ~10 questions that actually matter, picks smart defaults for the rest, generates a Trejon-style prompt, creates the agent, optionally assigns a phone, and offers a test call. |
| `prospect-demo` | Build voice agent demos for a prospect from a URL or a filled intake form. Scrapes the site, writes the prompt, creates 1-to-N agents across voice models (Gemini, OpenAI, Grok, ElevenLabs) for A/B, returns live shareable URLs that embed in any GoHighLevel site. Ships with 12 intake email templates (generic + 11 verticals) you can send to prospects. |
| `prompt-tuner` | Tune an agent's system prompt based on real call performance. Pulls recent calls, runs AI analysis, surfaces failure patterns, proposes revisions, and applies them on confirmation. The iteration loop after demos go live. |
| `call-audit` | Score recent calls, identify patterns, generate a coaching plan. Read-only weekly review. Outputs a Markdown scorecard you can share with the team. |
| `knowledge-base-builder` | Build a searchable KB for an agent from URLs (auto-crawled), FAQ documents (auto-generated into Q&A), CSVs (parsed into rows), or markdown. Attaches to agents and enables the `search_knowledge_base` tool. |
| `subaccount-onboarding` | **Agency-tier only.** Onboard a new client end-to-end: create the sub-account, set pricing economics, assign integrations, copy a template agent, send the welcome invite. Collapses the 30-minute UI workflow into one command. |
| `agent-from-recording` | Clone a real salesperson into a voice AI. Paste a call transcript, the skill extracts the call flow, objection responses, and closing patterns, then writes a Trejon-style prompt and creates 1-to-N A/B agents. |
| `agent-to-agent-call-testing` | Verify your agents on a **real call** — two of your agents call each other over Twilio so call-time features (the caller's-phone-number variable, greetings, end-call, agent-team transfers) are proven against the true production path, not faked by a simulator. Guided wizard: pick two numbers, pick a test, place the call, get a PASS/FAIL with the transcript as proof. Also benchmarks voice latency per provider. |
| `retell-to-leadlock` | Port a Retell AI agent into Leadlock. Pulls the Retell LLM definitions, consolidates an orchestrator + its `agent_swap` sub-agents into ONE Leadlock prompt (Leadlock has no agent-to-agent transfer yet), recreates every custom HTTP tool as a Leadlock custom function (bridging the webhook-envelope difference when needed), maps phone transfers + end-call, and verifies booking/transfer/end-call live. Needs `RETELL_API_KEY` in `.env` alongside your Leadlock key. |
| `talking-website` | Turn any website into a talking website. Creates a voice agent the visitor clicks and speaks to that **controls the page** (navigate, scroll, jump to a section, spotlight, fill, click), **books on the calendar**, **captures the lead to the CRM**, and logs every call in Leadlock — minutes bill to the account. Ships a drop-in `voice-agent.js` (vanilla, works on WordPress / GHL / any framework) + a `provision.py` helper. Grok/OpenAI only for page control. |
| `a2p-registration` | Get your business registered for **A2P 10DLC** so US carriers deliver your SMS instead of silently filtering it. Walks all three layers in order (Customer Profile, Brand, Campaign) and fills every field for a **one-shot approval** using templates from a campaign that passed after three real rejections (30896, then 30886, then 30891). Ships the full Twilio reference library (use cases, every error code, consent rules, throughput, prohibited content) plus a stdlib generator that turns your brand details into a copy-paste answer sheet. Triggers when texts aren't delivering or a campaign/brand gets rejected. |
| `sales-presentation` | Build a branded, client-facing **sales deck** that pitches an AI voice-agent system to any business in any industry. One standalone dark-themed HTML page (single-scroll, not a slideshow) built from a reusable component library: hero, lead-journey flowcharts, stat grids, capability and compliance cards, unit economics, CTA. Give a logo, two brand colors, the client name, and the use-case; the deck rebrands in one place (the `:root` block) and the copy is rewritten for that industry. Ships a fill-in template plus a worked HVAC example. |
| `ghl-workflow-api` | Read and write **GoHighLevel workflows** through GHL's private backend API with a captured browser session token, no clicking through the builder. List workflows, dump any workflow node-by-node, audit every workflow for broken references (bad pipeline/stage, dead sub-workflow links, empty webhook samples, missing email templates), and bulk-edit action-node attributes then publish. Stdlib-only Python. Ships the token-capture guide, endpoint + JSON-anatomy reference, and four scripts (core helper, writer, auditor, tracer). Unofficial API: tokens expire hourly and triggers stay UI-only. |

**Setup helpers** (auto-fire when needed):

| Skill | What it does |
|---|---|
| `welcome` | Lists what the kit can do. Fires on "help", "what can you do", "I'm new", or any ambiguous first prompt. |
| `setup-check` | Verifies `.env`, tests your API key, identifies your tenant tier, reports which skills are available. Auto-fires when another skill hits a 401/403. |
| `add-to-learnings` | Captures bugs, platform gaps, and working recipes from a session into `learnings/` so the kit gets smarter over time. Run it at the end of a non-trivial session. |
| `kit-audit` | Maintainer self-check. Points the kit at itself: every skill structurally sound, every endpoint real (vs `LEADLOCKDOCS.json`), every skill registered, no hard-rule violations or leaked secrets, learnings healthy. Static lint + read-only live probes, auto-fixes safe drift, writes a scored health report to `./output/`. Run it now and then. |

More skills land here over time. Drop a new folder under `.claude/skills/<name>/SKILL.md` and Claude Code picks it up.

## Marketing showcase

`.claude/skills/prospect-demo/showcase.html` is a Leadlock × Claude Code branded slide deck that walks through what the `prospect-demo` skill does — built for YouTube recordings, demo calls, or any time you want to explain the workflow visually.

Open it in a browser. Arrow keys / spacebar to navigate. Six slides:
1. Partnership hero (Leadlock × Claude Code)
2. Today's prospect
3. How it's done (one command, six steps)
4. The result (three demo URLs + iframe embed)
5. White-label partner pitch
6. CTA

## Install

```bash
git clone <this-repo> ~/Projects/LeadLockAgentKit
cd ~/Projects/LeadLockAgentKit
cp .env.example .env
```

Open `.env`, paste in your Leadlock API key. That's it.

## Use

From inside `~/Projects/LeadLockAgentKit`:

```bash
claude
```

Then prompt Claude with what you want. The kit listens for natural language — you don't need to memorize commands.

### First time? Try these

```
help                                        → lists all available skills
check my setup                              → verifies your API key works
```

### Common phrases that fire each skill

```
"Build me an agent for Acme Plumbing"
"Create an inbound receptionist agent"
    → build-agent

"Build a demo for https://acmeplumbing.com"
"Make a voice agent demo for [business name]"
    → prospect-demo

"Tune my Sparky agent based on the last 20 calls"
"Why is my agent not booking?"
    → prompt-tuner

"Audit the last 30 calls on [agent]"
"How is my agent doing this week?"
    → call-audit

"Build a KB for [agent] from https://acme.com"
"Attach these FAQs to my agent"
    → knowledge-base-builder

"Clone my best salesperson — here's the transcript: ..."
"Build an agent from this call recording"
    → agent-from-recording

"Onboard a new client [Name] at [domain]"
"Spin up a new sub-account for [Client]"
    → subaccount-onboarding  (agency-tier keys only)

"Port my Retell agent into Leadlock"
"Consolidate my Retell orchestrator + sub-agents into one agent"
    → retell-to-leadlock  (needs RETELL_API_KEY in .env)

"Test my agent on a real call"
"Benchmark voice latency across providers"
    → agent-to-agent-call-testing
```

Claude picks up the matching skill, reads your `.env`, hits the Leadlock API, and hands you back the result.

## How it works

- Each skill is a folder under `.claude/skills/`. Claude Code auto-discovers them when you run `claude` from this directory.
- Skills authenticate to the Leadlock API using the `LEADLOCK_API_KEY` in your `.env`. Your tenant is inferred from the key.
- No Supabase access required. No backend running. Pure HTTP against `https://leadlock-app.onrender.com`.
- `LEADLOCKDOCS.json` at the kit root is the canonical API reference (275+ endpoints, request/response shapes, full component schemas) that Claude consults when building or revising skills. Parsed as structured OpenAPI 3.1 JSON.
- `CLAUDE.md` at the kit root tells Claude how to operate inside this project. You don't need to read it as a user, but it's the load-bearing config for adding new skills.

## Get a key

Generate an API key from your Leadlock account: Settings → API Keys → Create.

If you're on the Agency plan, the key has access to all your sub-accounts. If you're a sub-account user, the key is scoped to your tenant.

## Adding your own skills

Drop a new folder under `.claude/skills/<your-skill-name>/` with a `SKILL.md` file. Frontmatter format:

```yaml
---
name: your-skill-name
description: Short trigger description. List the phrases a user might say to invoke this.
---
```

Then write the skill body the way you'd brief a colleague. Claude reads it on invocation.

## Troubleshooting

- **`401 Unauthorized`** — Your `LEADLOCK_API_KEY` is wrong or expired. Regenerate it in the dashboard.
- **`Connection refused`** — Check `LEADLOCK_API_URL` matches the host in `.env.example`.
- **Skill doesn't trigger** — Make sure you ran `claude` from inside the kit directory so `.claude/skills/` is in scope.
