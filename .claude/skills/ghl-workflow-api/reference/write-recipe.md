# Write recipe (the hard-won part)

Writing back to a GHL workflow works, but only for **action-node attributes**,
and only if you pin the `version` correctly. Get the version wrong and the
server rejects the write with 422 "outdated".

> Unofficial API. Tokens expire ~hourly. Triggers cannot be set this way
> (see `trigger-bucket-limitation.md`).

## The read -> transform -> write loop

1. **Read current state.** `get_state(loc, wfid)` returns
   `(current_version, templates)`. It reads the live meta for `version` and
   round-trips the signed file for `templates`.
2. **Transform.** Mutate the `templates` list in place: change a wait window,
   a GPT `promptText`, a webhook `body`, a tag list, an opportunity
   `pipeline_id`/`pipeline_stage_id`, etc.
3. **Write.** Save a draft with `auto_save(...)`, or go live with
   `publish(...)`. Pass the SAME `version` you read in step 1.

Always re-read state immediately before writing. If anything else (you in the
UI, another script, an automation) saved in between, your version is stale.

## The version gotcha

The workflow carries an integer `version`. The server increments it on each
save. **You send the CURRENT version, not current+1.**

- Send `current` -> accepted, server bumps to `current+1`.
- Send `current+1` -> 422 "outdated" (the server thinks you are behind).

This is the single most common mistake. `ghl_write.py` detects the 422 and
tells you to re-read the version.

## Publish

```
PUT /workflow/{loc}/{workflowId}
body:
{
  "templates":  <the full node list>,
  "version":    <CURRENT version>,
  "status":     "published",
  "autoSaveSession": null
}
```

`autoSaveSession: null` clears any pending draft session so the publish is not
rejected as conflicting with an open auto-save. The server increments the
version; do not pre-increment.

## Draft save (auto-save)

```
PUT /workflow/{loc}/{workflowId}/auto-save
body:
{
  "templates": <the full node list>,
  "version":   <CURRENT version>
}
```

Use this to stage changes without publishing. Then `publish(...)` when ready.

## What is writable this way

Action-node attributes only:

- `wait` windows and `startAfter` timing
- field updates (`update_contact_field`)
- GPT prompts (`chatgpt` `promptText`, `model`)
- webhook bodies (`custom_webhook` `body`, `method`, `url`, `saveResponse`)
- tags (`add_contact_tag` / `remove_contact_tag` `tags[]`)
- opportunity pipeline / stage (`create_opportunity` `pipeline_id`,
  `pipeline_stage_id`)
- branch conditions on existing `if_else` nodes
- sub-workflow add/remove targets (`add_to_workflow` / `remove_from_workflow`)

## What is NOT writable this way

- **Triggers.** They live in the trigger bucket. Add them in the builder UI.
- **Inbound-webhook trigger URLs.** These are part of the trigger, not an
  action node. Builder UI only.
- Anything that requires creating a brand-new node type the builder would
  normally scaffold with extra server-side metadata. Editing existing nodes is
  reliable; hand-constructing exotic new nodes is not.

## Safe-write checklist

1. `get_state()` right before writing.
2. Edit `templates`; keep every node's `type`, `order`, and `next` intact.
3. `auto_save()` first if you want to eyeball it in the builder.
4. `publish()` with the version from step 1.
5. On 422 "outdated": re-read state and retry. On 401: re-capture the token.
6. Re-run `audit.py` to confirm you did not introduce a broken reference.
