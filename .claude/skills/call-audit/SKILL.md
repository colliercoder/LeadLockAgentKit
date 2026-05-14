---
name: call-audit
description: Pull recent calls for an agent, score each one with AI, surface failure patterns, and generate a coaching plan. Like prompt-tuner but read-only — produces a report without touching the prompt. Triggers on /call-audit, audit my calls, audit recent calls, review the calls, review my agent's calls, weekly call review, monthly call review, how is my agent doing, how is my agent performing, agent performance report, agent scorecard, score the last N calls, performance breakdown.
---

# Call Audit

Run a structured review of an agent's recent call performance. No prompt changes — just a clear scorecard, pattern detection, and a coaching plan. The natural weekly habit for any operator running real voice agents.

For prompt revisions, use the `prompt-tuner` skill instead.

## When to invoke

- "How's my agent doing this week?"
- "Audit the last 20 calls on [agent_name]"
- "Generate a scorecard / call review / performance report"
- Recurring weekly or monthly review

## Setup check

Confirm `./.env` has `LEADLOCK_API_KEY` and `LEADLOCK_API_URL`.

## Rules

1. **Read-only.** This skill never modifies an agent or prompt. If the user wants to apply changes, point them at `prompt-tuner`.
2. **Exclude test/demo traffic by default.** Score real calls only. Use `direction=inbound` or `direction=outbound`.
3. **Minimum sample size of 5.** Below that, the report is anecdote, not data. Tell the user and stop.
4. **Time window defaults to last 7 days.** Override if the user specifies.
5. **Surface specific transcript snippets**, not just abstract patterns. The user needs to see what actually happened.
6. **Branch discipline: stay on main.** No `git checkout -b`.

## Required inputs

- **Agent identifier**: name, id, or "my [provider] agent".
- **Window**: "last 7 days", "this month", "last 50 calls". Default: 7 days, capped at 50 calls.
- **Direction**: inbound, outbound, or both. Default: both.

## Execution

### Step 1 — Resolve the agent

```
GET /agents?search=<name>
```

Save `agent_id`, `name`, `voice_provider`, `system_prompt` length, `tools_enabled`.

### Step 2 — Pull recent calls

```
GET /calls?agent_id=<id>&limit=50&direction=inbound
GET /calls?agent_id=<id>&limit=50&direction=outbound
```

(Two requests, merge results.) Filter:
- Keep `status=completed`
- Keep `duration_seconds > 30` (drop instant hangups)
- Apply the time window
- Drop `direction=test`, `direction=demo`

If under 5 calls qualify, stop and report: "Only X calls in window. Need at least 5 for a real audit."

### Step 3 — Get scoring criteria

Use suggested criteria for this agent:

```
GET /testing/agents/<agent_id>/suggested-criteria
```

If empty, fall back to a sensible default set:
```python
DEFAULT_CRITERIA = [
    "booked_appointment",
    "asked_qualifying_questions",
    "handled_top_objection",
    "ended_call_cleanly",
    "one_question_at_a_time",
    "stayed_on_brand",
]
```

### Step 4 — Run analysis

```
POST /testing/agents/<agent_id>/analyze-calls
{
  "call_ids": [...],
  "criteria": [...],
  "model": "claude-sonnet-4-6"
}
```

Returns per-call analysis. Save the response.

For real-time feedback, use the `-stream` variant:
```
POST /testing/agents/<agent_id>/analyze-calls-stream
```

### Step 5 — Generate the coaching plan

```
POST /testing/agents/<agent_id>/coaching-plan
```

Returns a structured plan: strengths, weaknesses, suggested experiments. Save it.

### Step 6 — Build the scorecard

Render a clean Markdown report. Output to `./output/call-audit-<agent_slug>-<YYYY-MM-DD>.md`:

```markdown
# Call Audit — <Agent Name>

**Window:** <start> to <end>
**Calls scored:** <N>
**Direction:** <inbound | outbound | both>
**Voice provider:** <provider>

## Headline numbers

| Metric | Value |
|---|---|
| Pass rate (overall) | XX% |
| Booked appointment | X/N (XX%) |
| Asked all qualifiers | X/N (XX%) |
| Handled objections cleanly | X/N (XX%) |
| Ended cleanly | X/N (XX%) |
| Avg call duration | X:XX |
| Avg sentiment | X.X / 5 |

## Top failure patterns

### 1. <criterion> failed in X/N calls

**What happens:** <plain-English description>

**Example transcript:**
> Caller: "<...>"
> Agent: "<problematic line>"

**Suggested fix:** <one-sentence remediation>

### 2. ...

## Wins to keep

- <pattern the agent does well> (X/N calls)
- ...

## Coaching plan (from platform AI)

<paste platform-generated coaching plan>

## Suggested next actions

1. Run `/prompt-tuner` with these top failures as priorities
2. <vertical-specific tip>
3. After 20 more calls, re-run `/call-audit` to measure improvement
```

### Step 7 — Print a 5-line summary

Even though the full report is in the file, print a tight summary inline:

```
✓ Audited <N> calls for <agent_name>
  Pass rate: XX% (was YY% last week if available)
  Top issue: <one line>
  Top win: <one line>
  Full report: ./output/call-audit-<agent_slug>-<date>.md
```

## Comparing across audits

Multi-week comparisons:

```
GET /testing/agents/<agent_id>/analysis-history
```

Returns prior analyses with timestamps and pass rates. If the user asks "did we improve?", compute the delta and surface it.

## Gotchas

- **Pass rate can lie if criteria differ between audits.** Always note which criteria were used.
- **Outbound and inbound have very different baselines.** Don't combine them in a single pass rate without noting the split.
- **The analyzer model affects scoring.** Sticking with `claude-sonnet-4-6` keeps results comparable run-to-run. If you change models, restart your baseline.
- **Recording must be enabled for full analysis.** If `recording_enabled=false` on the agent (as it is for demos), the analyzer only has transcripts. Note this in the report header.
- **Demo calls are noise.** They use canned scenarios and don't represent real performance. Exclude unless explicitly asked.

## Rule capture

<!-- Append new rules here. -->
