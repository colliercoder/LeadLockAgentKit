---
name: prompt-tuner
description: Tune an agent's system prompt based on real call performance. Pulls recent calls, runs AI analysis, surfaces failure patterns, proposes prompt revisions, and applies them on confirmation. Triggers on /prompt-tuner, tune my agent, improve the prompt, fix my agent, agent is failing, agent is broken, the prompt isn't working, rewrite the prompt, update the prompt, make my agent better, agent says weird things, my agent missed bookings, agent talks too much, why is my agent not booking, audit and rewrite the prompt, prompt revision.
---

# Prompt Tuner

Close the loop between real call performance and agent prompt quality. Pulls N recent calls for an agent, runs the platform's analysis pipeline, gets prompt-revision suggestions back, lets you review them, and saves the new prompt — all from one command.

## When to invoke

- "My [Agent] isn't booking" / "calls are dropping" / "agent talks too much"
- "Run a tune on [agent_name]"
- After a fresh batch of real calls (5-50) has accumulated
- After a customer complaint about an agent's behavior

## Setup check

Confirm `./.env` has `LEADLOCK_API_KEY` and `LEADLOCK_API_URL`. If missing, stop and tell the user to copy `.env.example` to `.env`.

## Rules

1. **Never apply a rewrite without user review.** Always show the diff/summary and get explicit confirmation.
2. **Minimum sample size.** Don't tune on fewer than 5 real calls. Less than that, suggest running `/prompt-tuner` again after more volume.
3. **Exclude test calls by default.** Use `direction=inbound` or `direction=outbound` — skip `test` and `demo` unless the user explicitly asks.
4. **Preserve hard rules.** Never let a suggested rewrite remove eligibility gates, the AI-disclosure handler, end-call discipline, or "speak numbers as words" guardrails. If a suggestion removes these, flag it and ask.
5. **Single agent per run.** If the user mentions multiple agents, ask which to start with.
6. **Branch discipline: stay on main.** No `git checkout -b`.

## Required inputs

- **Agent identifier**: the agent name, agent id, or "my [provider] agent" (you'll resolve via `GET /agents`).
- **Call sample size**: default 20. Smaller for fast iteration, larger for higher signal. Cap at 50.
- **Time window** (optional): "last 7 days" / "since the last tune". Default: most recent 20 calls.

If the user hasn't specified, use defaults and proceed — don't gate on every input.

## Execution

### Step 1 — Resolve the agent

```
GET /agents?search=<name>
```
Returns matches. Pick the one the user named. Save `agent_id`, current `system_prompt`, `voice_provider`.

### Step 2 — Pull recent calls

```
GET /calls?agent_id=<id>&limit=<N>&offset=0&direction=inbound
```

Filter out `direction=test` and `direction=demo`. Keep only calls where `status` is `completed` or has a `duration_seconds > 30` so you're scoring real conversations, not hangups.

If fewer than 5 qualifying calls returned, stop and tell the user: "Only X completed calls in window. Wait until you have at least 5 real conversations and re-run."

### Step 3 — Get suggested evaluation criteria

```
GET /testing/agents/<agent_id>/suggested-criteria
```

Returns recommended scoring criteria specific to this agent's purpose (qualifier vs booker vs receptionist). Save the list.

If no suggestions return, fall back to the criteria library:
```
GET /testing/criteria-library
```

Pick a default set: `["booked_appointment", "asked_qualifying_questions", "handled_objections", "ended_cleanly", "one_question_at_a_time"]`.

### Step 4 — Run analysis on the call sample

```
POST /testing/agents/<agent_id>/analyze-calls
{
  "call_ids": ["<id1>", "<id2>", ...],
  "criteria": [...from step 3],
  "model": "claude-sonnet-4-6"
}
```

Returns analysis results per call (pass/fail per criterion, failure reasons, transcript snippets). Save the `analysis_ids` from the response.

If the user wants real-time streaming feedback, use `POST /testing/agents/<agent_id>/analyze-calls-stream` instead.

### Step 5 — Get prompt suggestions

```
POST /testing/agents/<agent_id>/suggest-prompt
{
  "analysis_ids": ["<analysis_id1>", "<analysis_id2>", ...],
  "model": "claude-sonnet-4-6"
}
```

Returns a list of suggested changes. Each suggestion has:
- `area` — which section of the prompt
- `issue` — what's wrong (e.g. "agent skips eligibility gate on roof question")
- `suggestion` — specific text to change
- `rationale` — why this fixes it

### Step 6 — Show the user

Print a tight scorecard:

```
Agent: <name>  ·  Sample: <N> calls  ·  Pass rate: <X>%

Top failures:
  1. <criterion>: <fail_count>/<total> calls
     Pattern: "<snippet from one failing transcript>"
     Suggestion: <suggestion text>

  2. <criterion>: ...

Suggested rewrites: <count> changes proposed
```

Ask: "Apply all suggested changes? (yes / pick specific ones / skip)"

### Step 7 — Rewrite the prompt

If the user approves all (or picks a subset):

```
POST /testing/agents/<agent_id>/rewrite-prompt
{
  "suggestions": [<approved suggestion objects>],
  "model": "claude-sonnet-4-6"
}
```

Returns the rewritten prompt.

### Step 8 — Validate the rewrite

Check the rewritten prompt against the hard rules. Fail and ask the user before applying if:
- It removed any "speak numbers as words" guidance
- It removed end-call discipline ("after saying goodbye, end_call")
- It removed the AI-disclosure handler
- It removed eligibility gates from Guardrails
- It dropped below 80% of original length (probably nuked useful content)
- It exceeded 11,000 chars (bloat)

If any of these trip, show the user the issue and offer: (A) re-run with stricter instructions, (B) apply anyway, (C) cancel.

### Step 9 — Save and apply

```
POST /testing/agents/<agent_id>/save-rewritten-prompt
{
  "rewritten_prompt": "<full new prompt text>"
}
```

Then apply:

```
POST /testing/agents/<agent_id>/apply-prompt
{
  "original_text": "<old prompt>",
  "suggested_text": "<new prompt>"
}
```

Or directly:

```
PATCH /agents/<agent_id>
{ "system_prompt": "<new prompt>" }
```

### Step 10 — Generate a coaching plan (optional)

For ongoing improvement, generate a coaching plan that summarizes the patterns:

```
POST /testing/agents/<agent_id>/coaching-plan
```

Returns a plan: things the agent does well, things to improve, suggested next experiments. Save this to a file the user can read.

### Step 11 — Report back

```
✓ Tuned <agent_name>
  Sample: <N> calls, <date_range>
  Pass rate before: <X>%
  Changes applied: <count>
  New prompt: <char_count> chars (was <old_count>)

  Run again after the next 20 calls to keep tightening.
```

## Reading the analysis history

To see prior tunes:
```
GET /testing/agents/<agent_id>/analysis-history
```

Returns chronological analyses with pass rates. Useful for plotting improvement over time.

## Gotchas

- **Sample bias**: If all 20 calls are from the same hour or same caller demographic, suggestions may overfit. If possible, pull a wider window.
- **The model can hallucinate "issues"**. Always show suggestions to the user before applying. Don't trust the analyzer blindly — the user knows the business.
- **Greeting and Call Flow Step 1 must match**. If a rewrite changes the greeting field but not Call Flow Step 1 (or vice versa), the agent will append a second question on first turn. Catch this in Step 8 validation.
- **`temperature` matters but isn't in the rewrite scope**. If the agent paraphrases too much, that's a temperature issue, not a prompt issue. Suggest `PATCH /agents/<id> {"temperature": 0.6}` separately.
- **xAI agents need different tuning than OpenAI/Gemini**. xAI is more literal-prompt-following; OpenAI improvises more. The analyzer doesn't know this — be skeptical of "more explicit" suggestions on OpenAI agents.
- **Don't tune demos** (`channel=demo` or `direction=demo`). Those calls are warm/canned and don't reflect production behavior.

## Rule capture

<!-- Append new rules here as the maintainer learns from real tuning sessions. -->
