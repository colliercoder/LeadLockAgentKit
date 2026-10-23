---
name: install-addon
description: Install a paid Leadlock add-on (the Leadlock GHL Connector - GHL CLI with its Claude skill plus the Chrome extension; also in the Launch Bundle) that the user dropped into ./addons/. Installs it, links its Claude skill into the kit, reuses the GHL keys already in .env, and walks through loading the Chrome extension. Triggers on /install-addon, install my add-on, install the GHL connector, install the launch bundle, set up the GHL CLI, I bought the bundle, install the GHL extension, add-ons.
---

# Install a Leadlock add-on

The Agent Kit is free and public. Paid add-ons are not: the buyer unzips them into
`./addons/`, which is gitignored, and this skill wires them into the kit on their machine.
Nothing from `./addons/` is ever committed or pushed.

Today there is one add-on, the **Leadlock GHL Connector** (sold on its own and inside the
Leadlock Launch Bundle). Its zip unzips to `addons/leadlock-ghl-connector/`:

- `ghl-cli/`: the Leadlock GHL CLI plus its Claude skill, so Claude can read and change the
  user's GoHighLevel account (contacts, opportunities, calendars and bookings,
  conversations, workflows, documents, payments, forms, social, tags, custom values).
- `extension/`: the Leadlock GHL Connector Chrome extension, which copies the user's own
  GoHighLevel login token so Claude can build workflows (the public GHL API can only read
  them).

## When to invoke

- "Install my add-on" / "I bought the GHL Connector" / "I bought the Launch Bundle" / "set up
  the GHL CLI"
- The user asks Claude to work in GoHighLevel and `addons/leadlock-ghl-connector/` exists but
  `.claude/skills/addon-ghl-cli/` does not
- The user asks about the add-on and does not have it: point them to
  https://www.leadlock.ai/store and stop. Never recreate the add-on's code in this repo.

## Setup check

Needs Python 3.9 or newer (`python3 --version`; a Mac has it after `xcode-select --install`).
GHL keys are read from the kit's `.env` (`GHL_PIT`, `GHL_LOCATION_ID`); if they are blank,
ask for them in Step 3.

## Rules

1. **Nothing from `./addons/` is ever committed.** Before finishing, run
   `git status --porcelain` and confirm no path under `addons/` (other than
   `addons/README.md`) or `.claude/skills/addon-*` is listed. If one is, stop and fix
   `.gitignore` first.
2. **Never copy add-on code into a tracked path.** The linked skill folder is named
   `addon-*`, which is gitignored.
3. **Never print a token.** Mask keys as the first 6 and last 4 characters.
4. **The GoHighLevel login token from the extension is a password.** It goes only into
   `addons/leadlock-ghl-connector/ghl-cli/.env` as `GHL_FIREBASE_REFRESH_TOKEN`. It stops
   working when the user logs out of GoHighLevel.
5. **The installer makes its own `.venv` inside the add-on.** Never `pip install` into the
   user's global Python.
6. If the folder layout does not match Step 1, stop and ask. Do not guess paths.

## Required inputs

- The unzipped add-on at `addons/leadlock-ghl-connector/`
- GHL **Private Integration Token** (`pit-...`): GoHighLevel > Settings > Private
  Integrations > Create New, with the scopes the user wants Claude to use
- GHL **Location ID**: the long ID in the sub-account's URL

## Execution

### Step 1: Find the add-on

```bash
ls addons/leadlock-ghl-connector/
```

Expect `README.md`, `ghl-cli/` and `extension/`. If they unzipped it to
`addons/leadlock-ghl-connector/leadlock-ghl-connector/` or somewhere else, ask them to move
the folder so the path above is right.

### Step 2: Install the GHL CLI

```bash
addons/leadlock-ghl-connector/ghl-cli/install.sh
```

It picks the newest Python 3.9+ on the machine, creates `.venv/` and copies `.env.example` to
`.env` inside the add-on folder.

### Step 3: Reuse the kit's GHL keys

Read `GHL_PIT` and `GHL_LOCATION_ID` from the kit's `.env`. Write them into
`addons/leadlock-ghl-connector/ghl-cli/.env` as `GHL_API_KEY=<GHL_PIT>` and
`GHL_LOCATION_ID=<GHL_LOCATION_ID>`. If either is blank in the kit `.env`, ask the user for
it and write it to both files.

Smoke test:

```bash
addons/leadlock-ghl-connector/ghl-cli/ghl --json contacts list --limit 5
```

A list (or an empty list) is a pass. A 401 means the token is wrong or missing scopes.

### Step 4: Link the add-on's Claude skill into the kit

```bash
mkdir -p .claude/skills/addon-ghl-cli
cp addons/leadlock-ghl-connector/ghl-cli/cli_anything/gohighlevel/skills/SKILL.md .claude/skills/addon-ghl-cli/SKILL.md
```

Copy, never symlink (some tools skip symlinked skill folders). Re-run this step after the
user drops in a newer version of the add-on.

### Step 5: Load the Chrome extension

Walk the user through it, one step at a time:

1. In Chrome open `chrome://extensions` and turn on **Developer mode** (top right).
2. Click **Load unpacked** and pick `addons/leadlock-ghl-connector/extension`.
3. Click the puzzle icon and pin the Leadlock icon.
4. Open any GoHighLevel page while logged in, click the icon, press **Grab token**, then
   **Copy token**, and paste it here. Write it to the add-on `.env` as
   `GHL_FIREBASE_REFRESH_TOKEN` without echoing it.

This step is only needed to build workflows; everything else works without it.

### Step 6: Verify and report

```bash
git status --porcelain
```

Confirm Rule 1, then tell the user to restart Claude Code (new skills load at start) and
report:

```
GHL Connector installed.
  GHL CLI: working (contacts list returned N)
  Claude skill: addon-ghl-cli linked (restart Claude Code to load it)
  Chrome extension: loaded, workflow token saved (masked)
Try: "List my GHL workflows" or "Build a follow-up workflow for new leads"
```

## Templates

Nothing to send. The report block above is the output.

## Gotchas

- The workflow token expires when the user logs out of GoHighLevel. A sudden auth error on
  workflow commands means: grab a fresh token with the extension.
- Workflows are created as drafts. The user reviews and publishes them in GoHighLevel.
- An older download of the connector was the Chrome extension alone (no `ghl-cli/`). If
  `ghl-cli/` is missing, the user should re-download from the link in their purchase email.

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
