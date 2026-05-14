---
name: agent-from-recording
description: Clone a real salesperson's call patterns into a voice AI agent. Takes a transcript (or audio file you've already transcribed), extracts the call flow, objection responses, personality, and closing patterns, then writes a Trejon-style prompt and creates the agent(s). Triggers on /agent-from-recording, build an agent from this call, build an agent from this recording, build an agent from this transcript, clone my best closer, clone my best salesperson, clone my best setter, clone my top SDR, turn this recording into an agent, turn this call into an agent, agent from transcript, agent from recording, mimic this salesperson, copy this rep's style, model an agent after this human.
---

# Agent From Recording

"Take my best salesperson's call and make an AI that sounds like them." Input: a call transcript (or text you've already transcribed). Output: a Trejon-style system prompt + 1-to-N agents that mirror the human's patterns.

The kit doesn't do speech-to-text itself — bring a transcript. If you need to transcribe an audio file first, use a tool like ElevenLabs Scribe v2, OpenAI Whisper, or paste into your platform's STT and bring the text here.

## When to invoke

- User pastes a transcript: "build an agent from this call"
- "Clone my best closer / SDR / setter"
- "Mimic this call style"
- After listening to a great recording and wanting to capture the pattern

## Setup check

Confirm `./.env` has `LEADLOCK_API_KEY` and `LEADLOCK_API_URL`.

## Rules

1. **Never use the word "closer"** anywhere in the generated prompt or copy. Use "team member" / "specialist" / "funding specialist".
2. **Strip personally identifying details** from the transcript before reusing. Names, phone numbers, full addresses, specific dollar amounts the human quoted. Generalize them in the prompt.
3. **Don't mirror tactics the human shouldn't have done.** If the recording shows the salesperson dodging questions, using deceptive framing, or making unauthorized claims, do NOT bake those patterns in. Flag them to the user and ask before proceeding.
4. **Preserve hard rules.** The generated prompt MUST have: one-question-at-a-time, end-call discipline, speak-numbers-as-words, AI-disclosure handler. Even if the human did 5-question stacks, the agent doesn't.
5. **Trejon-style structure exactly.** Same skeleton as `prospect-demo`. No "CRITICAL RULES" header at the top. Guardrails section at the bottom only.
6. **Target 5K-9K chars.** Trim aggressive humor or context-specific banter that doesn't generalize.
7. **Never name the platform** in the generated prompt. Use "our system."
8. **Branch discipline: stay on main.** No `git checkout -b`.

## Required inputs

- **Transcript text** — the full call, ideally with speaker labels (Agent: / Caller:). If unlabeled, ask for clarification.
- **Business context** — what's the business, what's the offer, what's the conversion event? Often inferable from the transcript but confirm.
- **Agent name** — propose one or ask
- **Number of models** — single or A/B across 2-4 providers (default 3: Gemini, OpenAI, Grok)
- **Voice gender** — match the human's gender by default
- **Calendar** — discovered from existing agents (same as prospect-demo)

## Execution

### Step 1 — Triage the transcript

Read the full transcript. Note:

- **Who's speaking when.** If labels are missing, ask the user to clarify.
- **Length and stage count.** A 20-minute call has more material than a 2-minute one. A short call may not have enough patterns.
- **Conversion event.** Did the call book, capture contact, or end without action?
- **Any red flags** (see Rule 3). If present, surface to the user before continuing.

If the transcript is under ~500 words or doesn't show a meaningful sales pattern, stop and tell the user: "This transcript is too short / doesn't have enough sales pattern. Try a longer call or one where the human closes."

### Step 2 — Extract patterns

Read through and identify:

- **Greeting / opening line** — the human's first turn, verbatim (you'll quote it in the prompt's Call Flow Step 1 and use it as the agent's `greeting`)
- **Personality markers** — fillers ("yeah, totally", "got it"), tone, pacing
- **Top objections** the caller raised, plus the human's responses (verbatim, 2-3 sentences each)
- **Qualifying questions** the human asked, in order
- **Conversion ask** — how the human pitched the booking / next step
- **Closing line** — the human's actual sign-off
- **Any disqualifiers** the human surfaced (price, location, eligibility)
- **Tone of voice** — warm? direct? folksy? professional?

Make a structured note (in your reasoning or a temp file) of all of these.

### Step 3 — Confirm with the user

Show the user what you extracted in a tight format:

```
From the transcript, I'm seeing:

Style: <warm/direct/folksy/etc.>
Greeting: "<exact phrase>"
Top 3 objections handled: 1) ... 2) ... 3) ...
Qualifying questions: <list>
Conversion ask: "<phrase>"
Closing: "<phrase>"

Building an agent that mirrors this. Confirm or correct?
```

Wait for confirmation or corrections.

### Step 4 — Find calendar config to mirror

Same pattern as `prospect-demo`:

```
GET /agents?limit=50
```

Find one with `calendar_integration_id` set. Copy the calendar fields. If none, ask the user (A) wire a calendar first or (B) build without book_appointment.

### Step 5 — Write the Trejon-style prompt

Map the extracted patterns into the skeleton:

| Skeleton section | Source from transcript |
|---|---|
| `## Role` | Inferred business + conversion event |
| `## Personality` | Style + 3 filler examples from transcript |
| `## Context` | Business name, services, pricing (ranges only, not human's quoted figures) |
| `## Call Flow` | Step 1 = exact greeting. Steps 2-5 = qualifying questions in order. Step 6 = conversion ask. Step 7 = wrap. |
| `## Tools` | Default inbound set + `book_appointment` if conversion is booking |
| `## Handling Common Situations` | 10-20 entries, the top objections + human's actual responses (lightly cleaned) |
| `## Closing Line` | Exact closing phrase from transcript |
| `## Guardrails` | Hard rules — one question, 30-word cap with override, speak numbers as words, end-call discipline, AI disclosure |

Length target 5K-9K chars. If under 4K, you didn't extract enough — re-read the transcript. If over 10K, trim the objection list.

### Step 6 — Set the greeting

The agent's `greeting` field must EXACTLY match Call Flow Step 1. Single open-ended question. No contractions in the greeting (some voice models read them oddly).

If the human's transcript greeting was a compound question, simplify it. Example:
- Human said: "Hey, thanks for calling. Are you reaching out about the rate? What's the best way to get started?"
- Agent greeting becomes: "Hey, thanks for calling. How can I help you today?"

### Step 7 — Create agents

Same as `prospect-demo`. For each provider in the A/B set:

```
POST /agents
{
  "name": "<Agent name> (<Provider>)",
  "system_prompt": "<generated prompt>",
  "greeting": "<single open question>",
  "business_name": "<...>",
  "industry": "<...>",
  "timezone": "<...>",
  "agent_mode": "inbound",
  "temperature": 0.6,
  "ai_speaks_first": true,
  "enable_recording_disclosure": false,
  "recording_enabled": false,
  "max_call_duration_minutes": 10,
  "tools_enabled": ["end_call", "book_appointment", "check_availability", "collect_contact"],
  "calendar_provider": "<from step 4>",
  "calendar_id": "<from step 4>",
  "calendar_integration_id": "<from step 4>",
  "calendar_configs": [...from step 4],
  "voice_provider": "<gemini|openai|xai>",
  "<provider_voice_field>": "<voice>"
}
```

Voice picks (match the human's gender):

| Provider | Male | Female |
|---|---|---|
| Gemini | `Charon`, `Orus`, `Iapetus` | `Aoede`, `Kore`, `Leda` |
| OpenAI | `ballad`, `ash`, `verse`, `echo` | `shimmer`, `coral`, `sage` |
| xAI (Grok) | `rex`, `leo` | `ara` |

### Step 8 — Create demo configs

For each agent, create an orb demo so the user can hear it:

```
POST /demos/
{
  "agent_id": "<id>",
  "channel": "orb",
  "name": "<Display name> (<Provider>)",
  "config": {
    "max_duration_seconds": 600,
    "landing_heading": "<...>",
    "landing_subheading": "<...>",
    "landing_instructions": "Talk to <Agent Name> like you're a real caller. <one-line scenario hint>."
  }
}
```

### Step 9 — Verify and report

Check each agent with `GET /agents/<id>`. Confirm voice fields are right per provider (don't trust default values — see prospect-demo's gotchas).

Output:

```
✓ Cloned the recording into <count> agents

Style captured:
  Greeting: "<phrase>"
  Top objection handled: "<objection>" → "<response>"
  Closing: "<phrase>"

Live demos:
  Gemini: <demo_url>
  OpenAI: <demo_url>
  Grok:   <demo_url>

Open one and listen. If the voice or pacing is off, run /prompt-tuner after 20 real calls.
```

## Gotchas

- **Transcript quality matters.** Auto-transcripts with bad punctuation make the pattern extraction noisier. Spend 2 minutes cleaning the transcript first if it's rough.
- **The human's banter doesn't always generalize.** A reference to "the Vikings game" or "this rain" is great in context, terrible in a prompt. Strip context-specific lines.
- **Don't bake in the human's quoted prices.** Pricing changes. Use ranges and "the team confirms on the visit."
- **Match `temperature` to the source style.** Improvisational, warm humans → 0.7. Tight, scripted humans → 0.6. Avoid 0.8+ for cloned agents — drift kills the mirror.
- **A great human call doesn't always mean a great prompt.** If the human's success came from voice/inflection rather than words, the agent will fall flat. Set expectations: "We're cloning the structure. Voice tone needs A/B testing."

## Rule capture

<!-- Append new rules here. -->
