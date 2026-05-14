# Leadlock Agent Kit

A growing library of Claude Code skills for Leadlock agency owners. Run them with one command, no UI clicks, no SQL access required — just your Leadlock API key.

## What's in the kit

| Skill | What it does |
|---|---|
| `prospect-demo` | Build voice agent demos for a prospect from a URL or a filled intake form. Scrapes the site, writes the prompt, creates 1-to-N agents across voice models (Gemini, OpenAI, Grok, ElevenLabs) for A/B, returns live shareable URLs that embed in any GoHighLevel site. Ships with 12 intake email templates (generic + 11 verticals) you can send to prospects. |
| `prompt-tuner` | Tune an agent's system prompt based on real call performance. Pulls recent calls, runs AI analysis, surfaces failure patterns, proposes revisions, and applies them on confirmation. The iteration loop after demos go live. |
| `call-audit` | Score recent calls, identify patterns, generate a coaching plan. Read-only weekly review. Outputs a Markdown scorecard you can share with the team. |
| `knowledge-base-builder` | Build a searchable KB for an agent from URLs (auto-crawled), FAQ documents (auto-generated into Q&A), CSVs (parsed into rows), or markdown. Attaches to agents and enables the `search_knowledge_base` tool. |
| `subaccount-onboarding` | **Agency-tier only.** Onboard a new client end-to-end: create the sub-account, set pricing economics, assign integrations, copy a template agent, send the welcome invite. Collapses the 30-minute UI workflow into one command. |
| `agent-from-recording` | Clone a real salesperson into a voice AI. Paste a call transcript, the skill extracts the call flow, objection responses, and closing patterns, then writes a Trejon-style prompt and creates 1-to-N A/B agents. |

**Setup helpers** (auto-fire when needed):

| Skill | What it does |
|---|---|
| `welcome` | Lists what the kit can do. Fires on "help", "what can you do", "I'm new", or any ambiguous first prompt. |
| `setup-check` | Verifies `.env`, tests your API key, identifies your tenant tier, reports which skills are available. Auto-fires when another skill hits a 401/403. |

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
```

Claude picks up the matching skill, reads your `.env`, hits the Leadlock API, and hands you back the result.

## How it works

- Each skill is a folder under `.claude/skills/`. Claude Code auto-discovers them when you run `claude` from this directory.
- Skills authenticate to the Leadlock API using the `LEADLOCK_API_KEY` in your `.env`. Your tenant is inferred from the key.
- No Supabase access required. No backend running. Pure HTTP against `https://leadlock-app.onrender.com`.
- `leadlock-docs.md` at the kit root is the prose API reference (280+ endpoints, request/response shapes, schemas) Claude consults when building or revising skills.
- `openapi-spec.json` at the kit root is the same data in structured OpenAPI 3.1 form — Claude parses it when it needs exact field types or nested schemas.
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
