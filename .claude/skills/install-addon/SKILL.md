---
name: install-addon
description: Install a paid Leadlock add-on (the Leadlock Launch Bundle - GHL CLI with its Claude skill plus the Leadlock GHL Connector Chrome extension) that the user dropped into ./addons/. Installs it, links its Claude skill into the kit, reuses the GHL keys already in .env, and walks through loading the Chrome extension. Triggers on /install-addon, install my add-on, install the launch bundle, set up the GHL CLI, I bought the bundle, install the GHL extension, add-ons.
---

# Install a Leadlock add-on

The Agent Kit is free and public. Paid add-ons are not: the buyer unzips them into
`./addons/`, which is gitignored, and this skill wires them into the kit on their machine.
Nothing from `./addons/` is ever committed or pushed.

Today there is one add-on, the **Leadlock Launch Bundle**:

- `ghl-cli/`: a GoHighLevel command-line tool plus a Claude skill, so Claude can read and
  change the user's GHL account (contacts, opportunities, calendars, workflows,
  conversations, emails, payments, forms, social, locations, documents).
- `extension/` (or `leadlock-ghl-connector.zip`): the Leadlock GHL Connector Chrome
  extension, which copies the user's own GHL login token so Claude can create and edit
  workflows (the public GHL API can only read them).

## When to invoke

- "Install my add-on" / "I bought the Launch Bundle" / "set up the GHL CLI"
- The user asks Claude to build a GHL workflow and `addons/leadlock-launch-bundle/` exists but
  `.claude/skills/addon-ghl-cli/` does not
- The user asks about the bundle and does not have it: point them to
  https://www.leadlock.ai/store and stop. Never recreate the add-on's code in this repo.

## Setup check

Needs Python 3.10+ (`python3 --version`). GHL keys are read from the kit's `.env`
(`GHL_PIT`, `GHL_LOCATION_ID`); if they are blank, ask for them in Step 3.

## Rules

1. **Nothing from `./addons/` is ever committed.** Before finishing, run
   `git status --porcelain` and confirm no path under `addons/` (other than
   `addons/README.md`) or `.claude/skills/addon-*` is listed. If one is, stop and fix
   `.gitignore` first.
2. **Never copy add-on code into `.claude/skills/` or anywhere tracked.** The linked skill
   folder is named `addon-*`, which is gitignored.
3. **Never print a token.** Mask keys as the first 6 and last 4 characters.
4. **The GHL login token from the extension is a password.** It goes only into
   `addons/leadlock-launch-bundle/ghl-cli/.env` as `GHL_FIREBASE_REFRESH_TOKEN`. It stops
   working when the user logs out of GoHighLevel.
5. **Run commands from the add-on's own folder**, never `pip install` into the user's global
   Python. The installer makes its own `.venv`.
6. If the folder layout does not match Step 1, stop and ask. Do not guess paths.

## Required inputs

- The unzipped bundle at `addons/leadlock-launch-bundle/`
- GHL **Private Integration Token** (`pit-...`): GHL > Settings > Private Integrations >
  Create New, with the scopes the user wants Claude to use
- GHL **Location ID**: the long ID in the sub-account's URL

## Execution

### Step 1: Find the add-on

```bash
ls addons/
ls addons/leadlock-launch-bundle/
```

Expect `ghl-cli/` and `extension/` (or `leadlock-ghl-connector.zip`). If the user unzipped
it somewhere else, ask them to move it into `addons/` rather than pointing at another path.

### Step 2: Install the GHL CLI

```bash
cd addons/leadlock-launch-bundle/ghl-cli && ./install.sh
```

It creates `.venv/` and copies `.env.example` to `.env` inside the add-on folder.

### Step 3: Reuse the kit's GHL keys

Read `GHL_PIT` and `GHL_LOCATION_ID` from the kit's `.env`. Write them into
`addons/leadlock-launch-bundle/ghl-cli/.env` as `GHL_API_KEY=<GHL_PIT>` and
`GHL_LOCATION_ID=<GHL_LOCATION_ID>`. If either is blank in the kit `.env`, ask the user for
it and write it to both files.

Smoke test:

```bash
addons/leadlock-launch-bundle/ghl-cli/ghl contacts list --limit 5
```

A list (or an empty list) is a pass. A 401 means the token is wrong or missing scopes.

### Step 4: Link the add-on's Claude skill into the kit

Create `.claude/skills/addon-ghl-cli/SKILL.md` (gitignored) with:

```markdown
---
name: addon-ghl-cli
description: Drive the user's GoHighLevel account from the terminal with the Leadlock GHL CLI (paid add-on) - contacts, opportunities, calendars, workflows, conversations, emails, payments, forms, social, locations, documents. Triggers on ghl, gohighlevel, ghl contacts, ghl workflows, ghl calendars, build a GHL workflow, update my GHL.
---

# GHL CLI (Leadlock Launch Bundle add-on)

Run every command through the wrapper, which loads the add-on's own .venv and .env:

    addons/leadlock-launch-bundle/ghl-cli/ghl <group> <command> [--json]

Full command reference: addons/leadlock-launch-bundle/ghl-cli/README.md and
addons/leadlock-launch-bundle/ghl-cli/cli_anything/gohighlevel/skills/SKILL.md.
Ignore any install path or default location ID in that file; this kit's .env values win.

Creating or editing workflows needs GHL_FIREBASE_REFRESH_TOKEN in the add-on's .env,
captured with the Leadlock GHL Connector extension. If it is missing or expired, ask the
user to click the Leadlock icon on a logged-in GoHighLevel page, press "Copy token" and
paste it. Never print it.

Always show the user what will change in GHL before running a create, update or delete.
```

### Step 5: Load the Chrome extension

Walk the user through it, one step at a time:

1. If there is only a zip, unzip `leadlock-ghl-connector.zip`.
2. In Chrome open `chrome://extensions` and turn on **Developer mode** (top right).
3. Click **Load unpacked** and pick the extension folder.
4. Pin the Leadlock icon.
5. Open any GoHighLevel page while logged in, click the icon, press **Copy token**, and paste
   it here. Write it to the add-on `.env` as `GHL_FIREBASE_REFRESH_TOKEN`.

### Step 6: Verify and report

```bash
git status --porcelain
```

Confirm Rule 1, then report:

```
Launch Bundle installed.
  GHL CLI: working (contacts list returned N)
  Claude skill: addon-ghl-cli linked
  Chrome extension: loaded, workflow token saved (masked)
Try: "List my GHL workflows" or "Build a GHL workflow that texts new leads"
```

## Templates

Nothing to send. The report block above is the output.

## Gotchas

- Claude Code picks up a new skill when it starts, so restart `claude` after Step 4.
- The workflow token expires when the user logs out of GoHighLevel. A sudden 401 on
  workflow commands means: capture a fresh token with the extension.
- The bundle's own docs mention a `chrome-extension/` folder and a "Grab Refresh Token"
  button from an older build. The current extension is `extension/` and the button is
  "Copy token".

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
