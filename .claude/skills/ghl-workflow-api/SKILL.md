---
name: ghl-workflow-api
description: Read and write GoHighLevel (GHL) workflows and assets directly through GHL's private backend API using a captured browser session token, no clicking through the builder. List workflows, dump any workflow node-by-node, audit every workflow for broken references (bad pipeline/stage, dead sub-workflow links, empty webhook samples, missing email templates), and bulk-edit action-node attributes (waits, GPT prompts, webhook bodies, tags, opportunity pipeline/stage) then publish. Stdlib-only Python, no pip installs. Triggers on /ghl-workflow-api, edit a GHL workflow, bulk-edit GoHighLevel, read GHL workflow json, fix GHL workflow via api, audit GHL workflows, change GHL workflow without clicking, GHL private api, GoHighLevel backend api, dump a GHL workflow, trace a GHL workflow, publish a GHL workflow programmatically, leadconnectorhq api.
---

# GHL Workflow API

Read and write GoHighLevel workflows through the same private backend API the
GHL app itself uses, driven by a session token you capture from your browser.
No browser automation, no clicking through the builder for every change. List
and trace workflows, audit them for broken references, and bulk-edit action
nodes then publish.

> **Unofficial API. Use at your own risk.** This is GHL's internal backend, not
> a supported public API. Captured tokens expire about every hour (re-capture
> on a 401). **Triggers are UI-only** and cannot be set through this API (GHL
> moved them to a separate trigger bucket; see
> `reference/trigger-bucket-limitation.md`).

## What it does

- **Read** the workflow list, dump any workflow node-by-node, and read
  pipelines/stages and the email-template library.
- **Audit** every workflow for common breakage: builder errors, invalid
  opportunity pipeline/stage, dead sub-workflow references, webhooks that save
  a response with an empty sample, email nodes pointing at missing templates,
  and unpublished workflows.
- **Write** action-node attributes (waits, fields, GPT prompts, webhook
  bodies, tags, opportunity pipeline/stage, branch conditions) and publish or
  draft-save, with the version-pinning gotcha handled.

## Quickstart: capture a token

1. Open GoHighLevel in Chrome, go to the sub-account (location) you want.
2. DevTools (Cmd-Option-I) -> **Network** tab -> filter on
   `backend.leadconnectorhq.com`.
3. Click around the Automation/workflow builder so requests fire. Click any XHR
   to that host and copy the `authorization` and `token-id` **request headers**.
4. Copy `headers.example.json` to `headers.json` in this skill folder and paste
   your real values over the placeholders. `headers.json` is gitignored; never
   commit it.

Your **location id** is in the GHL URL while inside a sub-account
(`.../location/<your-location-id>/...`). You pass it to every script. Full
walkthrough in `reference/token-capture.md`.

## The read -> transform -> write loop

1. **Read** current state: version + node list (`ghl_write.get_state`).
2. **Transform** the node list in memory (change a wait, a prompt, a tag, a
   webhook body, etc.).
3. **Write**: draft-save (`auto_save`) or publish (`publish`), passing the
   SAME version you read. Sending version+1 returns 422 "outdated" - the server
   increments it for you. Re-read state right before writing. See
   `reference/write-recipe.md`.

## Hard rules

1. **Never commit a real token or location id.** `headers.json` is gitignored;
   the example file ships placeholders only. The scripts take the location id as
   an argument and never hardcode one.
2. **Triggers are UI-only.** Set triggers and inbound-webhook trigger URLs in
   the builder. The API edits action nodes only.
3. **Fetch the signed file URL without `content-type`.** The read helper does
   this for you; do not add `content-type` to GETs of the Firebase-signed
   `fileUrl` or the signature breaks.
4. **Stdlib only.** This kit has a zero-dependency rule: `urllib` only, no
   `requests`/`httpx`, no pip installs.

## Scripts

All scripts live in `scripts/` and read `headers.json` from the skill folder
(override with `--headers <path>` or `$GHL_HEADERS`). Run with `python3`.

### `ghl.py` - core read helper
```
python3 scripts/ghl.py list <location_id>                  # list workflows
python3 scripts/ghl.py load <location_id> <workflow_id>    # dump node JSON
python3 scripts/ghl.py pipelines <location_id>             # pipelines + stages
python3 scripts/ghl.py emails <location_id>                # email template ids
```
Also the importable helper: `load_headers`, `hdrs`, `get`, `get_json`,
`list_workflows`, `load_workflow` (does the meta -> fileUrl -> json round-trip
with the no-content-type fetch), `pipelines`, `email_library`.

### `trace.py` - dump a workflow node-by-node
```
python3 scripts/trace.py <location_id>                     # list names
python3 scripts/trace.py <location_id> "Workflow Name"     # trace one
python3 scripts/trace.py <location_id> "A" "B"             # trace several
python3 scripts/trace.py <location_id> --id <workflow_id>  # by id
python3 scripts/trace.py <location_id> --json "Name"       # + raw json
```

### `audit.py` - validate every workflow
```
python3 scripts/audit.py <location_id> \
    --expected-pipeline <pipeline_id> \
    --webhook-host <substring> \
    --require-published
```
All options are optional. With no `--expected-pipeline`, pipeline membership
is not enforced (only stage-within-its-own-pipeline). Exits non-zero if any
issue is found.

### `ghl_write.py` - edit and publish action nodes
```
python3 scripts/ghl_write.py state <location_id> <workflow_id>   # inspect first
```
Programmatic (the normal path):
```python
import ghl, ghl_write
h = ghl.load_headers()
version, templates = ghl_write.get_state(loc, wfid, h)
# ... mutate templates in place ...
ghl_write.auto_save(loc, wfid, templates, version, h)   # draft
ghl_write.publish(loc, wfid, templates, version, h)      # go live
```

## Reference

- `reference/token-capture.md` - capturing and refreshing the session token
- `reference/endpoints.md` - every read/write endpoint and required headers
- `reference/workflow-json-anatomy.md` - node types and their key attributes
- `reference/write-recipe.md` - the version-pinning rules, publish vs draft
- `reference/trigger-bucket-limitation.md` - why triggers are UI-only

## Conventions

Follows the LeadLockAgentKit conventions (see `talking-website/SKILL.md`):
stdlib-only Python, no hardcoded ids or tokens in shipped files, per-account
inputs discovered or passed at run time, secrets kept in a gitignored local
file. Unlike most kit skills this one talks to GoHighLevel's backend, not the
Leadlock API, so it uses a captured GHL session token instead of a Leadlock
API key.
