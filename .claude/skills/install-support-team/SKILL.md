---
name: install-support-team
description: Installs the advanced course's AI support team for "Granite Peak Equipment Rental" into the user's own accounts, end to end - n8n data tables seeded from the kit's CSVs, four n8n workflows (Verify Caller, Rentals, Maintenance, Billing) behind a shared-secret header, three Leadlock agents (Joanne on rentals, Doug Jim Bob McGee on maintenance, Miss Hattie Mae on billing) with their custom functions, handoffs and Contact Intelligence. Runs pre-flight checks (Leadlock key, GoHighLevel, n8n, email credential, A2P number, MY_PHONE_NUMBER) and tells the user exactly what to fix, asks only what it needs, verifies with real function tests and one real verification code, and can uninstall cleanly. Can install one piece at a time for the course videos. Triggers on /install-support-team, install the support team, install granite peak, install it (in the support-team course flow), install the support team tables, install the Verify Caller step, install Joanne, install Jim Bob, install Miss Hattie Mae, wire the handoffs, test the support team, uninstall the support team, reinstall the support team.
---

# Install the support team

The advanced course builds a three-desk AI support team for a fictional heavy equipment rental company, Granite Peak Equipment Rental. This skill installs all of it into the user's own Leadlock account and their own n8n, so they can follow the videos with a working system: callers verify with a code sent to the email or phone on file (bank style), then Joanne handles rentals, Jim Bob walks them through a breakdown safely and opens a ticket, and Miss Hattie Mae handles the balance and sends a payment link.

The work is done by `install.py` next to this file (standard library only). This file tells you how to drive it: what to check, what to ask, and how to report.

## When to invoke

- "Install the support team", "install granite peak", or "install it" while the user is following the support-team course videos.
- One piece for one video: "install the support team tables", "install the Verify Caller step", "install Joanne", "install Jim Bob", "install Miss Hattie Mae", "wire the handoffs".
- "Test the support team" (re-run the checks only), "reinstall" (update in place), "uninstall the support team".

## Setup check

Everything reads `./.env` at the kit root: `LEADLOCK_API_KEY`, `LEADLOCK_API_URL`, `N8N_API_URL`, `N8N_API_KEY`, `MY_PHONE_NUMBER`. The installer adds `SUPPORT_TEAM_WEBHOOK_SECRET` itself. If the Leadlock key fails, fire `setup-check`. If n8n isn't set up at all, fire `connect-n8n` first.

## Rules

1. **Run the script, don't rewrite it.** Every step below is a subcommand of `python3 .claude/skills/install-support-team/install.py`, run from the kit root. It is idempotent: re-running updates what exists (matched by name and prefix) instead of duplicating.
2. **Never print a secret.** The script masks the Leadlock key, phone numbers and never prints the webhook secret or the pepper. Don't `cat .env`. Show phone numbers as area code plus the last two digits, the way the script does.
3. **Only the user's own data goes out.** The one verification code goes to the email the user gave for themselves. Texts go only to the user's own number. Never send to a demo customer's example address.
4. **Confirm before anything the user can't take back:** the install itself (it creates agents, workflows and tables), the real verification email, a test call, and uninstall. Show what will happen, then wait for a yes.
5. **Ask questions in plain text, one short list at a time.** Use the lettered options below. Pick the safe default when the user says "you pick".
6. **Stop on a failed check, skip on a warning.** A `fail` means the install can't work: give the fix and stop. A `warn` means a reduced mode: say what's reduced and carry on.
7. **Each piece needs the ones before it.** Tables, then Verify Caller, then any desk. The script builds a missing dependency automatically and leaves existing ones alone.
8. **Use a prefix when testing next to a live install.** `--prefix "GP Test - "` names everything "GP Test - ..." and namespaces the function names (`gp_test_...`), so nothing collides. Without `--prefix` the names are the course defaults.

## Required inputs

After pre-flight, ask only what's still unknown:

1. **Company name.** (A) Keep "Granite Peak Equipment Rental" (recommended, matches the videos). (B) Rename it: the prompts, messages and the name prefix follow.
2. **You on file as the demo customer.** First name, last name and the email the verification code should reach. This goes onto customer C-1001 (Ridgeline Aggregates) in n8n only, with `MY_PHONE_NUMBER` as the phone. It never goes into the kit's files.
3. **How codes and payment links travel.** (A) Email (default; needs a Gmail or SMTP credential in n8n; ask which one if there are several). (B) Text (needs an A2P-registered number from the pre-flight list).
4. **Which number**, only when one is A2P-ready: it's the number texts come from. The installer never moves a number off another agent.

## Execution

Shorthand: `INSTALL = python3 .claude/skills/install-support-team/install.py` (add `--prefix "..."` to every command if the user picked one).

### Step 0: Pre-flight

```
INSTALL preflight
```

It returns one JSON entry per check: `status` is `ok`, `warn` or `fail`, with `detail` and `fix`. Turn it into a short checklist for the user:

| Check | fail / warn means | Say |
|---|---|---|
| `leadlock_key` | fail: key missing, wrong, or an agency key with no sub-account | the `fix`, then fire `setup-check` |
| `crm` | warn: no GoHighLevel | "Installing in calls-only memory mode: no Contact Intelligence, no update_contact / notes / tags. Connect GoHighLevel and re-run to switch them on." |
| `n8n` | fail: URL/key missing, unreachable, localhost, or no data tables | the `fix`; for "no n8n yet", fire `connect-n8n` |
| `n8n_mcp` | warn: MCP not connected in Claude Code | "Not needed for the install. Say 'connect n8n' afterwards so you can change these workflows by asking." |
| `email` | warn: no Gmail/SMTP credential in n8n | the `fix`; codes go by text only if a number is A2P-ready, otherwise stop until one exists |
| `phone` | warn: no number, numbers not A2P, or can't read numbers | not registered: "Carriers block business texts from unregistered numbers. A2P 10DLC registration fixes that; say 'register A2P' to run the a2p-registration skill. Installing with email codes for now." No number: "The agents still work in the web playground and test calls. Buy or import a number in Leadlock to take real calls." |
| `my_phone` | warn: MY_PHONE_NUMBER missing | ask them to add it to `.env`; it's the demo customer's phone and the test-call target |

Stop on any `fail`. Otherwise carry on with the warnings noted.

### Step 1: Ask

Ask the Required inputs above in one message, skipping anything pre-flight already answered (for example, no A2P number means email is the only option, so don't ask).

### Step 2: Confirm and build

Show the plan and wait for a yes:

```
Ready to install (prefix "Granite Peak - "):
  n8n:      6 tables, 4 workflows, webhook key credential
  Leadlock: 12 custom functions, 3 agents (Grok Voice 3.0: Joanne eve, Jim Bob rex, Miss Hattie Mae ara)
  You on file: Dan Example, d***@example.com, (555) ***-**23
  Codes by: email (Gmail: <credential name>)    Contact Intelligence: on
Go ahead?
```

Then:

```
INSTALL install --first-name <first> --last-name <last> --email <email> --email-cred <n8n credential id> \
  [--company "<name>"] [--codes sms --sms-number-id <id>] [--only tables|verify|rentals|maintenance|billing|handoffs]
```

The script prints one line per object (created / updated) and stops with `STOPPED: <reason>` on any failure, keeping what it already built. Fix the cause and re-run the same command. Answers are remembered in `output/support-team/<prefix>.json`, so later piece-by-piece runs don't need them again.

What it builds, in order:

1. **Tables** from `course/support-team/data/*.csv`: Customers, Fleet, Rentals, Service, Troubleshooting, Verifications. Dates shift so the CSVs' 2026-10-24 becomes today. Existing tables keep their rows; `--reseed` resets them to the CSVs.
2. **Webhook key**: an n8n Header Auth credential (`X-Support-Key`) holding `SUPPORT_TEAM_WEBHOOK_SECRET`, plus a Leadlock API key credential only when texting is on.
3. **Workflows** from `course/support-team/workflows/*.json`: table ids, credentials, company name, email or text mode and a fresh random pepper go in; each is published and checked (no key gets 403, the key gets 200).
4. **Functions** in the Leadlock library, each pointing at its workflow's production URL with the secret header.
5. **Agents** with the prompts in `prompts/`, the built-ins (`transfer_to_agent`, `end_call`, `schedule_callback`, and with a CRM `update_contact`, `add_note`, `add_tag`), handoffs to whichever desks exist, Contact Intelligence, then a read-back check of voice, tools and handoffs.

### Step 3: Verify

1. Function tests, which send nothing:
   ```
   INSTALL test
   ```
   Open functions return data; gated ones must return `verify_first`; `verify_code` must return `no_code_sent`. Anything else is a FAIL to fix before going on.
2. One real code. Confirm first ("I'll send one verification code to d***@example.com"), then:
   ```
   INSTALL send-code
   ```
   It shows the gate is closed (`verify_first`), then sends the code through Leadlock's function test, matching the user by first name and the last four of `MY_PHONE_NUMBER`. Ask the user to read you the six digits.
3. ```
   INSTALL check-code --code <digits>
   ```
   It submits a wrong code first (expect `attempts_left: 2`), then theirs (expect `verified: true`), shows the gate open (their rentals), and clears the test row so nothing stays verified.
4. Offer a test call. With a yes:
   ```
   INSTALL call-me --yes [--number-id <id of a number to call from>]
   ```
   Joanne calls `MY_PHONE_NUMBER`. If the account has no usable number, point them to the web playground on Joanne in the Leadlock dashboard instead.

### Step 4: Report

Use the template below. Include every `warn` from pre-flight under "Skipped or reduced", with its fix.

### Uninstall

Confirm with the list of what goes, then `INSTALL uninstall --yes`. It removes the three agents, the twelve functions, the four workflows, the credentials, the six tables, the install record, and the `.env` secret when no other install is left. It only touches objects whose names (and, for functions, webhook URLs) match this install's prefix.

## Templates

Report:

```
Support team installed (prefix "Granite Peak - ")

  Joanne (Rentals)               <agent id>   answers first
  Doug Jim Bob McGee (Maint.)    <agent id>
  Miss Hattie Mae (Billing)      <agent id>
  n8n: 4 workflows live at <n8n host>/webhook/granite-peak-*, 6 tables
  Tests: 10/10 functions pass; real code sent to d***@example.com and verified; gate closed before, open after
  Codes by: email     Contact Intelligence: on

Skipped or reduced:
  - Texting: your number isn't A2P registered. Say "register A2P", then re-run to switch it on.

Next: the next support-team video, or call Joanne from the web playground and ask about a 777.
```

What the caller can do, for explaining it:

| Desk | Open to anyone | Needs a verified caller |
|---|---|---|
| Joanne | fleet_availability, rental_quote | rental_status, extend_rental, call_off_rent |
| Jim Bob | troubleshoot_machine | create_service_ticket, service_ticket_status |
| Miss Hattie Mae | none | account_balance, send_payment_link |

## Gotchas

- **The n8n Code sandbox blocks `require('crypto')`.** Random bytes come from the Crypto node and SHA-256 is plain JS in the Verify Caller workflow. Don't "fix" it with `crypto`.
- **n8n expressions can't read a field named `arguments`.** Every workflow starts with an Unwrap Code node for that reason.
- **Leadlock's function test always uses call_sid `test-call-sid` and no caller phone.** That's why the test matches on first name + last four, and why `check-code` deletes the test row afterwards (otherwise the next test would start verified).
- **Verification belongs to the call.** It's stored per call_sid for 60 minutes, so a caller verified by Joanne stays verified after a handoff to Jim Bob or Miss Hattie Mae on the same call.
- **Execution saving is off on Verify Caller**, so n8n keeps no copy of a code. The other workflows keep only failed runs, for debugging.
- **The pepper lives only inside the Verify Caller workflow.** Re-runs keep it; a reinstall after uninstall makes a new one, which only invalidates codes in flight.
- **Function names are unique per Leadlock account.** If a same-named function from somewhere else exists, the script stops instead of taking it over; re-run with `--prefix`.
- **Handoffs need the same voice provider on every desk** (xAI or OpenAI). All three are Grok Voice 3.0; if the user changes one desk's provider, change all three.
- **Agent and prompt changes apply to the next call**, not one in progress.
- **Texting needs an A2P-registered number** and a Leadlock API key stored as an n8n credential (only created in text mode). Without A2P, `/outbound/sms` refuses to send.

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
