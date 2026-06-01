---
name: welcome
description: Show the user what skills are available in this kit and example phrases that invoke each one. Use proactively when a user is new to the kit, asks "what can this do", "help", "what's available", "I'm new", "where do I start", "list skills", "show me what you can do", "/help", "how do I use this", or types anything ambiguous that doesn't match a specific skill's triggers.
---

# Welcome to the Leadlock Agent Kit

When the user is new, lost, or asks "what can this do", surface the kit's full skill list with concrete example phrases they can type next.

## When to invoke

- "Hi, what can you help me with?"
- "I'm new — where do I start?"
- "List the skills" / "What's available?"
- "/help" / "/welcome"
- "How do I use this?"
- ANY first-turn prompt in this kit that doesn't clearly map to a specific skill

## What to show the user

Output exactly this (substitute the user's name if known):

```
Welcome to the Leadlock Agent Kit. Every skill is driven from natural language.
You don't need to memorize commands — just describe what you want.

  prospect-demo
    "Build a demo for https://acmeplumbing.com"
    "Make a voice demo for [business name]"
    "Spin up A/B agents across Gemini, OpenAI, and Grok for this prospect"
    "Take this filled intake form and build a demo"

  prompt-tuner
    "Tune my Sparky agent based on the last 20 calls"
    "Improve the prompt on [agent name]"
    "Why is my agent not booking?"
    "Run a rewrite on [agent]"

  call-audit
    "Audit the last 30 calls on [agent]"
    "How is my agent doing this week?"
    "Generate a scorecard for [agent]"
    "Weekly call review"

  knowledge-base-builder
    "Build a KB for [agent] from https://acme.com"
    "Attach these FAQs to my agent"
    "Import this CSV as a pricing knowledge base"
    "Crawl [URL] into a knowledge base"

  agent-from-recording
    "Clone my best closer — here's the transcript: ..."
    "Build an agent from this call recording"
    "Mimic this salesperson's style"

  subaccount-onboarding   (agency-tier API keys only)
    "Onboard a new client [Name] at [domain]"
    "Spin up a new sub-account for [Client]"
    "Create a sub-account: name=Acme, slug=acme, admin=email@..."

  retell-to-leadlock   (needs RETELL_API_KEY in .env)
    "Port my Retell agent into Leadlock"
    "Consolidate my Retell orchestrator + sub-agents into one agent"
    "Migrate my Retell setup to Leadlock"

  add-to-learnings
    "/add-to-learnings"
    "Save this learning"
    "Remember this for next time"
    "What did we learn from this session?"
    Run this at the end of any non-trivial session to capture bugs,
    platform gaps, and patterns into ./learnings/ so the kit gets
    smarter over time.

Setup helpers:
  setup-check
    "Check my setup" / "Is my API key working?" / "Diagnose"

The ./learnings/ folder is the kit's persistent memory. Before starting
non-trivial work, Claude skims learnings/index.md for prior lessons.

Need to add your own skill? Drop a folder under .claude/skills/<name>/SKILL.md
and Claude picks it up next time.
```

## Then ask what they want to do

After listing, follow up with a tight question:

```
What do you want to do first?
  (A) Build a demo for a prospect
  (B) Tune or audit an existing agent
  (C) Build a knowledge base
  (D) Onboard a new client (agency tier)
  (E) Something else — just describe it
```

Let them pick a letter, or describe in their own words, and route to the right skill.

## Rules

- **Don't lecture.** Show the list, ask one follow-up, stop. The user is here to do work, not read documentation.
- **Don't quote dollar amounts or pricing.** Pricing changes; the README and platform handle that.
- **Don't claim a skill does something it doesn't.** Match the description on each skill folder.
- **If the user asks something the kit can't do**, say so plainly and suggest they file a feature request rather than improvising.
