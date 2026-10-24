# Skill authoring: how to write SKILL.md files for current Claude models

How to write and edit the instructions in `.claude/skills/*/SKILL.md` so current Claude models (Opus 5.5 and its siblings) follow them well. Read this before writing a new skill or rewording an old one. CLAUDE.md's "Skill anatomy" section still sets the required sections and frontmatter; this file is about how to word what goes inside them.

Sources (checked 2026-10-24):

- Anthropic, "Skill authoring best practices": https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Anthropic, "Prompting best practices" (current models, with per-model pages including Opus 5.5): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, "Prompting Claude Opus 5.5": https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
- Anthropic, "Agent Skills overview": https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code skills docs: https://code.claude.com/docs/en/skills
- The prompt-audit guide bundled with Claude Code's `claude-api` skill (`/claude-api prompt-audit`), which turns the pages above into a checklist.

---

## The rules

### 1. The description says what the skill does and when to use it

The `description` is the only part of a skill Claude sees before deciding to load it. Write it in the third person ("Builds...", not "I can help you..."), name the concrete outcome, and list the phrases a user would actually type. This is the one place where firm wording is fine, because skills tend to under-trigger. Keep it under 1,024 characters.

### 2. Normal volume, with the reason attached

Current models follow instructions closely and literally. Text written in ALL CAPS, "CRITICAL", "you MUST" was needed by older models; on current ones it makes the model over-apply the rule and turns everything around it rigid. Write `Use X when...`, not `CRITICAL: you MUST use X`. Keep emphasis for the one or two rules a real run showed the model skipping, and put the reason next to it.

### 3. Explain why

A rule with its reason generalizes: "Callers hear the agent's text read aloud, so write numbers as words" covers cases the rule never listed. A bare "NEVER write digits" does not. Keep every "because" that is already in a skill; it is the most valuable text in the file.

### 4. Say what to do, and keep the real prohibitions

Describe the result you want rather than listing failures ("write flowing prose" beats "no bullets"). A prohibition can even anchor the model toward the thing it forbids. The exception: prohibitions that encode a real constraint stay as prohibitions: never name the platform in agent copy, never print an API key, never place a call or send an invite without confirmation. In this kit those are the hard rules, and they are load-bearing.

### 5. Only write what Claude doesn't already know

Claude already knows HTTP, JSON, Python and how to be thorough. What it can't know is the kit's context: the Leadlock API's quirks, the user's business, which settings were proven on live calls, and what burned us before. Spend the words there. Say each thing once, in the place it applies.

### 6. Match the strictness to how fragile the step is

Mutations, auth, billing, compliance and anything the user can't undo get exact steps, exact payloads and a confirmation gate. Judgment work (writing a prompt, scoring a call, picking a voice) gets the goal, the constraints and how to check the result, not a script.

### 7. State what done looks like, and verify it

End mutating steps with a check: GET the resource and compare the fields, run the linter, confirm the URL loads. "Verify `voice_provider` and the matching voice column after create" beats "make sure it worked".

### 8. Use examples that teach the shape

Examples steer output more than any description. Use them where the output format matters (a report, an email, a summary block), make them concrete, and label them as illustrative when they are only one possible answer. A single worked example tends to get copied word for word, so vary them or keep them short.

### 9. Progressive disclosure: keep SKILL.md under 500 lines

SKILL.md is loaded whole every time the skill runs. Long templates, reference tables and rarely used branches go into files next to it (`templates/`, `reference/`), linked one level deep from SKILL.md with a line saying when to read them. Scripts the skill runs are better than code Claude regenerates each time.

### 10. Write the current rule, not its history

Instructions say what to do now. Incident stories, "this used to be X", and dated conditionals belong in `learnings/`, not in the skill body. A short "Gotchas" bullet that keeps the evidence is fine, and the kit's `## Gotchas` section exists for exactly that.

---

## How to apply this to an existing skill

- **Rewording is wording only.** Keep every step, field, payload, default and gate. If the reworded skill would do something different on any input, it is not a rewording.
- **Diff one skill per commit**, so each change can be reviewed and reverted on its own.
- **Don't trim trigger phrases** in descriptions as part of a style pass: they change when the skill fires.
- **Leave format-pinning templates as they are** (`Output exactly this`, report and email templates). They pin a shape on purpose.
- After editing, run the kit-audit static checks (frontmatter, anatomy, length, registration) and re-read the hard rules section of the skill to confirm nothing was softened that should not be.
