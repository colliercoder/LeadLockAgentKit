---
name: clarify-voice
description: Turn a rambling voice-to-text note into a short, clean summary of what you want, confirm it with you, and only then start the work (usually by handing off to the matching kit skill). For anyone who talks to Claude Code through dictation. Triggers on /clarify-voice, clarify voice note, clarify this, voice note, transcribed note, clean up this voice note, what did I mean, summarize what I said, I'm dictating, I just rambled.
---

# Clarify Voice

Dictation is the fastest way to tell Claude Code what you want, but the transcript comes out messy: filler words, half-finished sentences, mid-thought changes of direction, and technical names mangled by speech-to-text ("lead lock", "go high level", "eleven labs"). This skill turns that transcript into a short summary you confirm before anything gets built, so the confirmed summary becomes the spec.

No API calls. It reads what you said, asks you to confirm, and then routes to the right skill.

## When to invoke

- You paste a voice-to-text transcript that rambles, repeats itself, or changes direction.
- The transcript has garbled names: product names, file paths, voice model names, skill names.
- You drop a loose idea before a bigger build and want to agree on the plan before work starts.
- You say "clarify this" or "what did I mean" after a long dictated message.

## Setup check

None needed. This skill makes no API calls, so it works before `.env` is set up. The skill it hands off to will run its own setup check.

## Rules

1. **Confirm before any work.** No API calls that change anything, no file edits, no other skill invoked until you reply "yes" (or a correction that you then confirm). Voice notes change direction mid-recording; acting on the first half is the failure this skill exists to prevent.
2. **Restate, don't quote.** The summary is clean prose in your own intent, not a trimmed copy of the transcript. No raw rambling text in the output.
3. **Expand and audit, not just condense.** If the note implies steps you didn't say out loud (for example "build a demo" implies a prospect URL and a voice choice), list them under "My understanding" so you can confirm or correct them.
4. **Ask when it is ambiguous.** If a phrase could mean two different things ("the audit": a call audit or the kit audit?), offer the two or three real interpretations and ask. Never pick one silently.
5. **Fix obvious transcription errors, flag the rest.** Correct clear misspellings of known names (see the glossary below). If you are not sure what a word was meant to be, show your best guess with a question mark rather than guessing quietly.
6. **Keep it short.** The summary is 1-3 sentences. Every bullet under "My understanding" is filled in, or marked "n/a".
7. **Mask personal data.** If the note contains a phone number, email, or API key, refer to it generically ("your cell", "the key you mentioned") and never echo the full value.

## Required inputs

- The transcribed voice note: the text the user passed with the trigger, or their last message.

If there is no transcript, ask the user to paste it.

## Execution

### Step 1: Read the context

Read-only. Note anything that helps interpret the note:

- What the user has been doing this session (the last few messages).
- Which kit skills exist (`.claude/skills/*/SKILL.md` names and their trigger phrases), so a request like "make a demo for that roofing company" can map to `prospect-demo`.
- `git status` in the kit, only if the note talks about files or changes.

### Step 2: Clean the transcript

- Strip filler ("um", "uh", "like", "you know", "kind of", "basically") and collapse repetition.
- When the speaker corrects themselves ("no wait, actually..."), keep the later version.
- Stitch spoken paths and names: "dot claude slash skills" becomes `.claude/skills`, "dot env" becomes `.env`.
- Fix known names using the glossary below.

### Step 3: Extract the intent

Pull out:

- **Core intent**: what outcome the user wants.
- **Action type**: build / change / fix / check / question / plan.
- **Targets**: agents, prospects, URLs, files, skills, accounts named in the note.
- **Matching skill**: the kit skill whose triggers fit best, if any.
- **Missing inputs**: what that skill will need that the note didn't say.

### Step 4: Present the summary and wait

Use the format in Templates. Then stop and wait for the reply.

- **"Yes"**: proceed. If a kit skill matches, invoke it and pass the confirmed summary as its input. Otherwise do the work as confirmed.
- **"Close, but..."**: apply the correction, re-present the summary, wait again.
- **"No, I meant..."**: start over from Step 2 with the new explanation.

## Templates

### Summary format

```
## What you said (clarified)
<1-3 sentence summary in clean prose>

## My understanding
- **Action**: <what needs to be done>
- **Target**: <agent / prospect / file / account, or n/a>
- **Skill**: <matching kit skill, e.g. prospect-demo, or "none, I'll do it directly">
- **Still needed**: <inputs the note didn't include, or n/a>

## Possible interpretations
<only when genuinely ambiguous: 2-3 numbered options>

## Is this what you meant?
- Yes, that's right
- Close, but <correction>
- No, what I meant was <clarification>
```

### Glossary of common dictation errors

| Heard as | Meant |
|---|---|
| lead lock, lead-lock, led lock | Leadlock |
| go high level, go hi level, GHL | GoHighLevel |
| eleven labs, 11 labs | ElevenLabs |
| grok, groc, grock, X AI | Grok / xAI |
| GPT live, G P T live | GPT-Live |
| gemini three point eight | Gemini 3.8 |
| twillio, twilio | Twilio |
| a two p, A2P, ten DLC | A2P 10DLC |
| N eight N, nathan | n8n |
| prospect demo, build agent, call audit (etc.) | the kit skills `prospect-demo`, `build-agent`, `call-audit` |
| sub account | sub-account |
| dot env | `.env` |

## Example

The user runs:

```
/clarify-voice okay so um I want to like make a demo for that roofing guy, the website is uh summit roofing dot example, and maybe use the eleven labs voice or actually no let's do grok and gemini both so I can compare, and then text me the link I guess
```

The skill returns:

```
## What you said (clarified)
Build a prospect demo for Summit Roofing (summitroofing.example) on two voices, Grok and Gemini, so you can compare them, then send you the links.

## My understanding
- **Action**: build an A/B voice demo from the prospect's website
- **Target**: summitroofing.example
- **Skill**: prospect-demo
- **Still needed**: agent name and voice gender (prospect-demo will ask)

## Possible interpretations
1. "Text me the link": prospect-demo prints the demo links here; you forward them yourself.
2. "Text me the link": after the build, send the links by SMS to your cell (`MY_PHONE_NUMBER`), which needs an SMS-capable number on the account.

## Is this what you meant?
- Yes, that's right
- Close, but <correction>
- No, what I meant was <clarification>
```

Note how the ElevenLabs mention was dropped because the speaker changed their mind, and how the vague "text me the link" became a question instead of a guess.

## Gotchas

- **Mid-sentence reversals are the main trap.** "Use ElevenLabs, or actually no, Grok" means Grok. Re-read the whole note before summarising; the last word on a topic wins.
- **Don't over-correct.** A business or person name that looks like a typo may be real. Keep unusual proper nouns as spoken and ask if unsure.
- **One note can hold several requests.** List each as its own action and confirm the order before starting.
- **"Yes" confirms the summary, not every downstream step.** Skills that change things still run their own confirmation gates (sending invites, applying a prompt rewrite, placing a call).

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
