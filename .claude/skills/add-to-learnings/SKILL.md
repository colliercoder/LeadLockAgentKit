---
name: add-to-learnings
description: Capture session learnings into the kit's `learnings/` folder so the entire ecosystem gets smarter over time. Reviews what happened in the current session, surfaces what went wrong, what worked, and what to avoid, then routes each entry into the right category file (bugs, best practices, anti-patterns, platform gaps, prospect-demo, etc.) and links it from `learnings/index.md`. Triggers on /add-to-learnings, /learn, save this learning, remember this for next time, add to learnings, capture this learning, log this lesson, write this down, file a learning, retro on this session, end-of-session retro, what did we learn.
---

# Add to Learnings

The kit gets smarter when we write down what we learned. This skill is the discipline. Invoke it whenever a session surfaces something worth keeping: a bug we worked around, a pattern that worked, an anti-pattern we want to avoid next time, a platform gap that blocked us, a config knob that wasn't documented.

## When to invoke

- **End of any non-trivial session** — even short ones. If anything went sideways or anything went unexpectedly right, capture it.
- **The moment a platform gap surfaces.** Don't wait until the end and forget half of it.
- **When the user says "remember this", "next time we should...", "let's not do that again", "we learned something here".**
- **After resolving a bug** that another future session would benefit from knowing about.
- **After a successful run of an unfamiliar workflow** — bank the working recipe.

## Setup check

`learnings/` lives at the kit root. If it doesn't exist, create it with `index.md` as the index file. The folder is part of the repo (committed), not local-only.

## Rules

1. **Each learning lives in a category file, not in `index.md`.** `index.md` is an index of one-line pointers, never the body of any learning.
2. **One learning per entry.** Don't bundle "and also". If a session has three lessons, write three entries.
3. **Lead with the rule, then the why.** A reader scanning the file should know what to do in the first sentence. Reasons go in the second.
4. **Include a date and a tag set.** `Date: YYYY-MM-DD` and `Tags: skill:prospect-demo, type:platform-gap` or similar. Tags drive search.
5. **Link to evidence.** Tenant id, demo slug, commit, screenshot path in `./output/`, GitHub issue. Without evidence the entry is hearsay.
6. **Never copy secrets, API keys, or full call transcripts into a learning.** Mask keys, summarize transcripts.
7. **Confirm with the user before writing.** Read back the proposed entries and let them edit / drop / re-route.
8. **Append, don't rewrite.** New entries go at the bottom of the category file with a `---` separator above. Don't reflow old entries.
9. **Keep the index lean.** Each `index.md` line is `- [<date> — <one-liner>](<file>#<anchor>)`. Under 120 chars per line.
10. **Branch discipline: stay on `main`.** Same as the rest of the kit.

## Category files

Default routing. Create the file the first time a category gets used.

| Category | File | What goes here |
|---|---|---|
| Bugs | `learnings/bugs.md` | Something broke unexpectedly. Includes the symptom, the root cause if known, the workaround. |
| Best practices | `learnings/best-practices.md` | Patterns that worked well and are worth repeating. Concrete, not generic ("KISS" isn't a learning). |
| Anti-patterns | `learnings/anti-patterns.md` | Things we tried that didn't work, and shouldn't be tried again without new evidence. |
| Platform gaps | `learnings/platform-gaps.md` | Missing API knobs, undocumented behavior, things that need a `leadlock-app` change. Each entry should reference the platform feature request if one was filed. |
| Skill-specific | `learnings/skill-<name>.md` (e.g. `learnings/skill-prospect-demo.md`) | Lessons that only apply inside one skill. Create when there are 2+ entries that would otherwise clutter a generic file. |
| Vertical / industry | `learnings/vertical-<name>.md` (e.g. `learnings/vertical-electrical.md`) | Industry-specific lore: typical objections, timezone defaults, FAQs that recur for that vertical. |

If a learning fits two files, pick one (prefer the more specific one) and cross-reference it in the other with a one-line "see also".

## Required inputs

None — the skill reads the session context and proposes. The user confirms.

If invoked with no session context (fresh terminal), ask: "What do you want to capture? Describe the situation and I'll route it."

## Execution

### Step 1 — Read what already exists

```bash
ls learnings/
cat learnings/index.md
```

Skim each category file's titles so you know what's already covered and don't write a duplicate.

### Step 2 — Mine the current session

Identify candidate learnings:
- Anything the user reacted to with "yeah, we should remember that" / "huh, that's a gotcha" / "next time" / "interesting"
- Bugs caught and fixed
- Workarounds applied
- API endpoints/keys discovered the hard way
- Confirmations / clarifications the user had to ask for that should have been automatic
- Platform gaps surfaced
- Decisions that worked out

Skip:
- Things already documented in CLAUDE.md, SKILL.md files, or `leadlock-docs.md`
- One-off context that doesn't generalize (the prospect's name, today's specific calendar id)
- Vague generalities ("be careful with edge cases")

### Step 3 — Draft each entry

For each candidate, draft:

```markdown
---

### <one-line title — imperative or fact, not a question>

Date: YYYY-MM-DD
Tags: skill:<slug>, vertical:<slug>, type:<bug|gap|pattern|anti-pattern>
Evidence: <tenant id, demo slug, commit sha, link, or path>

**Rule:** <the actionable rule in one sentence>

**Why:** <the reason — what happened, what would happen again without the rule>

**How to apply:** <when this rule kicks in, what to do, what to check>
```

`---` above each entry separates it from the previous one.

### Step 4 — Confirm with the user

Show the proposed entries and ask:
- Keep / drop / merge?
- Route to a different file?
- Edit the title or wording?

Don't write until the user confirms. Use lettered options (a/b/c/d) if there are multiple proposed entries so they can answer compactly.

### Step 5 — Write the entries

Append each confirmed entry to its target file. If the file doesn't exist, create it with this header:

```markdown
# <Category name>

<One-line description of what goes in this file.>

```

Then leave a blank line and start appending entries (each preceded by `---`).

### Step 6 — Update the index

Append a line to `learnings/index.md` for each entry, under the right section:

```markdown
- 2026-05-13 — <one-liner> — [bugs.md#anchor](bugs.md#anchor)
```

Group lines under category headings (`## Bugs`, `## Best practices`, etc.). Sort newest at top within each section.

### Step 7 — Report

Summarize what was written:
- "Added N entries: bugs (M), platform-gaps (P), …"
- "Index updated"
- Skip the file paths if the user clearly knows them.

## Index file shape

`learnings/index.md` is the table of contents the rest of the kit consults. It looks like:

```markdown
# Learnings — index

Pointers into the category files. Newest at top within each section. Skim before starting a non-trivial task.

## Bugs
- 2026-05-13 — short one-liner — [bugs.md#anchor-slug](bugs.md#anchor-slug)

## Best practices
- 2026-05-13 — short one-liner — [best-practices.md#anchor-slug](best-practices.md#anchor-slug)

## Anti-patterns
- 2026-05-13 — short one-liner — [anti-patterns.md#anchor-slug](anti-patterns.md#anchor-slug)

## Platform gaps
- 2026-05-13 — short one-liner — [platform-gaps.md#anchor-slug](platform-gaps.md#anchor-slug)

## Skill-specific
- 2026-05-13 — short one-liner — [skill-prospect-demo.md#anchor-slug](skill-prospect-demo.md#anchor-slug)
```

No content lives in `index.md`. Only one-line pointers.

## Gotchas

- **Don't paste tenant API keys or unmasked secrets into a learning, even in an evidence link.** Mask: `sk_live_***...***last4`.
- **Don't write a learning for things that are already a SKILL.md rule.** If the rule should live in a skill, edit the skill instead and skip the learning.
- **Don't make the learnings folder a dumping ground.** If a category file grows past ~50 entries, split it (by date range, by sub-topic) and update the index.
- **Don't write speculation as fact.** "We think this might be because…" → "Hypothesis: …. Verify with X." Mark uncertain entries with `Tags: type:hypothesis`.
- **Don't bury the action.** A learning that doesn't change behavior is just journaling. Each entry should change what the next session does.

## Rule capture

<!-- Append new rules here as the maintainer learns from real /add-to-learnings runs. -->
