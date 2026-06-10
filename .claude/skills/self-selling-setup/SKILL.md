---
name: self-selling-setup
description: Walk an agency step-by-step through standing up the Leadlock self-selling GHL snapshot for their own business - from imported snapshot to a live, paying, hands-off system. Claude runs an intake interview, auto-fills every GHL custom value via the public API, hands over an ordered checklist for the GHL-UI-only steps (Stripe, products, contract, triggers, publishing), and verifies there are no gaps. Ships the token-grabber Chrome extension and the API scripts. Triggers on /self-selling-setup, set up the self-selling snapshot, configure the snapshot, get the snapshot ready, stand up the self-selling system, set up the AI receptionist snapshot, onboard our agency onto the snapshot, configure the imported snapshot, finish setting up the snapshot.
---

# Self-Selling Snapshot Setup

Turn a freshly-imported self-selling GHL snapshot into a live, configured, paying system for your
agency. You answer a short interview; Claude fills in everything that's API-automatable and hands you
a tight checklist for the GHL-UI-only parts; then a verify pass confirms it's 100% ready.

**Assumes:** you've already imported the GHL snapshot into your sub-account. This skill *configures*
it - it doesn't create the snapshot.

## When to invoke
- "Set up the self-selling snapshot for [agency]"
- "Configure the imported snapshot"
- "Get the self-selling system live for my business"

## What you'll need
- The GHL sub-account **Location ID** (in the GHL URL)
- A GHL **Private Integration Token** (Settings -> Private Integrations -> Create, with the
  `customValues` read + write scopes) - lets the scripts fill your custom values via the public API
- A **Leadlock account + API key** for this sub-account
- Stripe connected in GHL

## The flow Claude runs

**1. Interview (the agency intake).** Claude walks you through `AGENCY-INTAKE.md` - your business name,
sender name/email, the AI's name, your setup + monthly prices, your demo FAQ. (Your Location ID + PIT go
in `.env`, not here.) Claude writes your answers to `scripts/values.json` (copy of `values.example.json`). A few values
(survey link, agreement link, agent IDs, orb link) are generated while you build - left blank for now.

**2. Auto-fill the custom values.** Run:
```bash
python3 scripts/setup_values.py scripts/values.json
```
This fills your GHL custom values via the public API. The not-yet-built ones show as "not filled yet."

**3. Build the pieces + complete the checklist.** Follow `setup-checklist.md` top to bottom: build the
agents, the intake survey, the agreement (publish it!), the products + recurring invoice, then wire the
triggers and publish the workflows. As you build, collect the survey link / agreement link / agent IDs /
orb link, drop them into `values.json`, and re-run `setup_values.py` so everything's filled.

**4. Verify.** Run:
```bash
python3 scripts/verify.py scripts/values.json
```
Confirms every required custom value is filled and the 2 products exist. The checklist covers the
UI-only checks (workflow publish status, triggers, contract published).

**5. Test-buyer run.** Push a test contact through Won -> sign -> pay (Stripe test) -> onboarded ->
qa-passed -> live, confirming each field/tag/stage flips. Then go live for real clients.

## What's bundled
- `AGENCY-INTAKE.md` - the interview questions and which custom value each fills
- `setup-checklist.md` - the full ordered GHL setup, with the gotchas we learned (publish the contract,
  dunning re-entry ON, attach only the setup product, triggers are UI-only, calendar sync)
- `scripts/setup_values.py` - auto-fills custom values (GHL public API + your PIT, non-expiring)
- `scripts/verify.py` - confirms no config gaps
- `scripts/values.example.json` - the config template
- `chrome-extension/` - a token-grabber for the **advanced** path: GHL's internal API (workflow edits)
  needs a Firebase refresh token, not a PIT. Load `chrome-extension/` as an unpacked Chrome extension,
  grab the token on an app.gohighlevel.com tab. For editing workflow nodes via that internal API, use
  the **`ghl-workflow-api`** skill - this setup skill only needs the PIT for the normal config.

## Notes
- The PIT + public API path is the reliable, documented, non-expiring way to fill custom values - use it
  for setup. The Chrome extension / internal API is only for advanced workflow-node edits (rarely needed
  on a fresh snapshot).
- Triggers and the contract's publish state are **UI-only** - the checklist flags every one, because a
  forgotten trigger or an unpublished contract silently breaks the flow.
- `values.json` holds your Leadlock API key - it's gitignored; never commit it. (Location ID + PIT live in `.env`.)
- Custom values in the snapshot are matched by their `fieldKey` (e.g. `custom_values.your_business_name`),
  not their display name - so the snapshot's mixed naming ('Your Business Name' vs 'setup_fee') all fills
  correctly. Don't rename the snapshot's custom values.
