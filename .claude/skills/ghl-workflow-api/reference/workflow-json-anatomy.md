# Workflow JSON anatomy

A workflow's flow is a flat list of nodes at `workflowData.templates` (or
`templates` on older shapes). Each node is one step in the automation.

## Node shape

Every node has roughly:

```json
{
  "type": "custom_webhook",
  "name": "Send to backend",
  "order": 3,
  "attributes": { ... type-specific ... },
  "next": "<id or pointer to the next node>"
}
```

| Field | Meaning |
|---|---|
| `type` | The node kind (see table below). Determines what `attributes` holds. |
| `name` | The label shown in the builder. |
| `order` | Position in the flow. |
| `attributes` | The editable payload. This is what you mutate on writes. |
| `next` | Pointer to the following node. |
| `parentKey` / `goto` | Present on branching (which branch a node sits in, jump targets). |
| `incompleteData` | If `true`, the builder flagged the node as broken. The audit checks for this. |

When you edit a node, keep `type`, `order`, and `next` intact. Only change
`attributes` (and only on action nodes; triggers are not here).

## Common node types and their key attributes

### `create_opportunity`
- `pipeline_id` - the pipeline the opportunity goes into
- `pipeline_stage_id` - a stage id that must belong to that pipeline
- A stray legacy `stage` key is a bug; it should not be present.

### `custom_webhook`
- `url`, `method`
- `body` - the request body sent to the webhook
- `saveResponse` - whether to capture the response
- `webhookResponse` - the sample response shape. If `saveResponse` is true but
  this is `{}`, mapping downstream will fail (the audit flags this).

### `email`
- `template_id` - id of a template in the email library, OR
- `html` - inline content. A node with neither has no content (audit flags it).

### `if_else`
- `conditionName`
- `branches[]` -> `segments[]` -> `conditions[]`, each condition having
  `conditionType`, `conditionSubType`, `conditionOperator`, `conditionValue`.
- A `conditionType` of `workflow_contact` whose `conditionValue` is a
  no-longer-existing workflow id is a dead reference (audit flags it).

### `wait`
- `window` - allowed send window, e.g. `{ "start": "09:00", "end": "19:00" }`
- `startAfter` - delay, e.g. `{ "value": 24, "type": "hours" }`
- `type: "condition"` - a conditional wait, with a `condition` block holding
  `branches -> segments -> conditions` plus a timeout in `startAfter`.

### `chatgpt`
- `model`
- `promptText` - the prompt sent to the model

### `add_contact_tag` / `remove_contact_tag`
- `tags` - list of tag strings to add or remove

### `add_to_workflow` / `remove_from_workflow`
- `workflow_id` - target workflow id (string or list). A target not in the
  location's live workflow ids is a dead reference (audit flags it).

### `goto`
- A jump to another node. Attributes carry the jump target.

### `math_operation`
- An arithmetic step on contact fields. Attributes carry operands and target.

## How to explore a real workflow

Run `trace.py <location_id> "Workflow Name"` to print every node with a
one-line summary of its attributes and its `next` pointer. Add `--json` to also
dump the raw `templates` list so you can see the exact attribute keys before
you write to them.
