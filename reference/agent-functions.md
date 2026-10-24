# Built-in agent functions (tools)

Every Leadlock agent can use these built-in functions during a call or text conversation. They are already on the platform: you never build them, you switch them on. Generated from the platform's tool definitions (leadlock-app `backend/app/voice/tool_schemas.py`, origin/main 6f57ef67) on 2026-10-24.

## How to switch them on

- The agent field `tools_enabled` is the list of function names the agent may call, for example `["end_call", "check_availability", "book_appointment", "update_contact", "add_note"]`. A name that isn't on this page is silently ignored.
- Several functions read their options from other agent fields (table below). The options are written into the function's description, so the model only uses the exact tags, workflows, pipelines, templates or transfer targets you configured.
- `tool_instructions` adds your own usage rule to any function: `{"update_contact": "Save the email as soon as the caller spells it."}`.
- Your own webhooks are a separate feature: custom functions (`/functions` endpoints in `LEADLOCKDOCS.json`). A custom function can't reuse a built-in name.

| Agent field | Feeds | Shape |
|---|---|---|
| `transfer_targets` | `transfer_call` | `[{name, number, reason}]` |
| `transfer_to_agents` | `transfer_to_agent` (dropped if empty) | `[{name, agent_id}]` |
| `ghl_tags` | `add_tag` | `[{name}]` |
| `ghl_remove_tags` | `remove_tag` | `[{name, condition?}]` |
| `ghl_custom_fields` | `update_custom_fields` | the fields the agent may write |
| `ghl_workflows` | `trigger_workflow` | `[{id, name, description?}]` |
| `ghl_pipelines` | `create_opportunity`, `update_opportunity_stage` | `[{id, name, stages: [{id, name}]}]` |
| `sms_templates` | `send_sms` | `[{name, content}]` |
| `sms_phone_number_id` | `send_sms` | which number texts go from (defaults to the agent's number) |
| `calendar_id`, `calendar_configs`, `multi_calendar_behavior` | calendar functions | one calendar, or several with `ask_user` / `auto_first` |
| `whisper_enabled` | `transfer_call` | an AI summary is whispered to the person receiving the transfer |

## What needs what

- **Works on every account:** `end_call`, `schedule_callback`, `transfer_call`, `transfer_to_agent`, `send_sms`, `search_knowledge_base` (needs a knowledge base attached), `trigger_outbound_call`, `schedule_text_back`.
- **Needs a connected calendar:** `check_availability`, `book_appointment`, `reschedule_appointment`, `get_appointments`, `cancel_appointment`.
- **Needs a connected CRM (GoHighLevel today):** `add_tag`, `remove_tag`, `update_contact`, `update_custom_fields`, `add_note`, `trigger_workflow`, `create_opportunity`, `update_opportunity_stage`. Without one they return a "CRM not connected" result and the call carries on. For any other CRM, use a custom function or the post-call webhook.

## Call control

| Function | What it does | Arguments (* required) |
|---|---|---|
| `end_call` | Hangs up. Only after the caller is clearly done and any open task is resolved. | `reason`* |
| `schedule_callback` | Books an automatic call back to this caller ("call me back in 5 minutes"). | `time`* (relative like "in 2 hours" or ISO), `phone_number` (defaults to the caller) |
| `transfer_call` | Transfers to a phone number from `transfer_targets`. | `phone_number`* (E.164), `reason` |
| `transfer_to_agent` | Hands the conversation to another AI agent, with the full history. | `agent_id`*, `reason` |
| `trigger_outbound_call` | Starts a call right now: to the contact when they ask "call me", or to a third party they name. | `reason`*, `phone_number` (only for a third party) |

## Calendar

| Function | What it does | Arguments (* required) |
|---|---|---|
| `check_availability` | Open slots for a date. Called as soon as the caller names a day. | `date`* (YYYY-MM-DD), `timezone`* (IANA) |
| `book_appointment` | Books a slot after checking availability and getting name and email. | `date`*, `time`* (HH:MM, 24h), `name`*, `email`*, `timezone`*, `phone`, `calendar_id` (when several calendars) |
| `reschedule_appointment` | Moves an existing appointment. | `date`*, `time`*, `timezone`*, `appointment_id` (auto-detected from the caller) |
| `get_appointments` | Looks up the caller's upcoming and recent appointments, with ids. | none |
| `cancel_appointment` | Cancels an appointment. | `appointment_id` (auto-detected), `reason` |

The timezone default is the agent's own timezone; if the agent has none, the model asks the caller.

## Contact and CRM

| Function | What it does | Arguments (* required) |
|---|---|---|
| `update_contact` | Saves what the caller told you onto their contact record. Finds or creates the contact from the phone for web and anonymous sessions. | any of `first_name`, `last_name`, `email`, `phone`, `company`, `timezone`, `address`, `city`, `state`, `postal_code`, `country` |
| `update_custom_fields` | Writes custom fields on the contact. | `fields`* (object of field name to value) |
| `add_tag` | Adds tags from `ghl_tags`. | `tags`* (list) |
| `remove_tag` | Removes tags from `ghl_remove_tags`. | `tags`* (list) |
| `add_note` | Adds a note to the contact (summary, objections, details). | `note`* |
| `trigger_workflow` | Starts a CRM workflow from `ghl_workflows` for this contact. | `workflow_name`* |
| `create_opportunity` | Creates a deal in a pipeline from `ghl_pipelines`; creates the contact if needed. | `pipeline_name`*, `stage_name` (defaults to the first stage), `name`, `value`, `phone`, `first_name`, `last_name` |
| `update_opportunity_stage` | Moves the caller's deal to another stage. | `stage_name`*, `status` |

`update_contact` only fills fields that are empty. A phone match isn't proof of identity (shared lines, recycled numbers, people calling for someone else), so an existing name or email is kept and reported back as skipped rather than overwritten. The result lists `updated` and `skipped`, and the agent should only say "saved" for fields in `updated`.

## Messaging and knowledge

| Function | What it does | Arguments (* required) |
|---|---|---|
| `send_sms` | Texts the caller a custom message or a template from `sms_templates`. Respects the account's texting on/off and pause. | `message` or `template_name` |
| `schedule_text_back` | Schedules a text for later; the message is written at send time. | `time`*, `context` |
| `search_knowledge_base` | Searches the agent's knowledge base. | `query`*, `limit` (default 5, max 20) |

## Example: an agent that books and keeps the CRM clean

```json
{
  "tools_enabled": ["check_availability", "book_appointment", "update_contact", "add_tag", "add_note", "end_call"],
  "ghl_tags": [{"name": "booked-by-ai"}, {"name": "hot-lead"}],
  "tool_instructions": {
    "update_contact": "Call it as soon as you have the caller's name and email, before booking.",
    "add_note": "At the end of the call, note the job, the address and any objection."
  }
}
```
