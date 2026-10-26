---
name: kit-rules
description: The Leadlock Agent Kit's operating rules. Load before any Leadlock task (building, tuning, testing or auditing a voice agent, sub-accounts, demos, phone numbers, the Leadlock connector) when the kit is installed as a Claude Code plugin, because a plugin does not load the kit's CLAUDE.md on its own.
---

# Leadlock Agent Kit rules

When the kit runs from a clone, its `CLAUDE.md` loads as project context. When it is installed as a plugin, it does not, so read it now:

1. Read `CLAUDE.md` at the kit root. As a plugin that is `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`; from this skill's folder it is `../../../CLAUDE.md`.
2. Follow it as the kit's rules for the rest of the session.

If the file cannot be found, say so and continue with the skill the user asked for.
