# The trigger-bucket limitation

This is the one hard boundary of the inline-JSON workflow API: **you cannot
set or edit triggers through it.**

## What happened

GHL migrated workflow TRIGGERS out of the inline workflow JSON into a separate
"trigger bucket". On a migrated workflow you will see `isTriggerBucketMigrated`
set to `true`, and the legacy `newTriggers` / `oldTriggers` fields come back
`null` even on a perfectly healthy, running workflow. That null is not a bug in
your fetch; it is the expected state post-migration. The triggers genuinely are
not in the JSON anymore.

## What this means in practice

- You **can** read, edit, and publish ACTION NODES (waits, fields, GPT
  prompts, webhook bodies, tags, opportunity pipeline/stage, branch
  conditions) via the auto-save / publish PUT. That path is reliable.
- You **cannot** add, remove, or change a workflow's TRIGGER through the API.
- You **cannot** create or change an inbound-webhook TRIGGER URL through the
  API (the inbound-webhook trigger is a trigger, not an action node).

## The workflow for trigger changes

Do the trigger part in the builder UI by hand:

1. Open the workflow in the GHL builder.
2. Add or edit the trigger (including grabbing an inbound-webhook trigger URL)
   in the UI.
3. Save in the builder.

Then use the API for everything downstream of the trigger: the action nodes.
A common pattern is "set up the trigger once by hand, then bulk-edit the action
nodes across many workflows by script."

## Do not try to force it

Do not attempt to reconstruct `newTriggers` / `oldTriggers` and PUT them back.
On a migrated workflow the server ignores or rejects that; the trigger bucket
is the source of truth and it is not exposed on this inline endpoint. Editing
action nodes still works regardless.
