---
name: subaccount-onboarding
description: Onboard a new agency client end-to-end — create the sub-account, set pricing economics, wire integrations, copy a template agent, and send the welcome invite. Compresses the 30-minute UI workflow into one command. Requires an agency-tier API key. Triggers on /subaccount-onboarding, onboard a new client, set up a new client, set up a sub-account, create a sub-account, create a sub-account for [name], add a client, new client signup, provision a client, spin up a new client, new agency client, new sub-account for [name], we just signed [client].
---

# Sub-Account Onboarding

Stand up a new client under your agency: create the sub-account with the right pricing, assign integrations, optionally copy a template agent, and email the invite. All via API.

This is an agency-tier skill — your API key must belong to an agency tenant (not a sub-account itself). The skill checks this first.

## When to invoke

- "Onboard <Client Name> as a new sub-account"
- "Spin up a new client"
- "Create a sub-account for [Client]"
- New deal closed, ready to provision

## Setup check

Confirm `./.env` has `LEADLOCK_API_KEY` and `LEADLOCK_API_URL`. Then probe:

```
GET /tenants/me
```

Must return `tenant_type: "agency"`. If it's `sub_account` or anything else, stop and tell the user: "This skill requires an agency-tier API key. Your current key is for a sub-account."

## Rules

1. **Confirm pricing economics with the user before creating.** Per-minute rate, monthly platform fee, billing start day. The defaults below are starting points, not law.
2. **Slug is global and permanent.** Check availability first. Pick something short, brandable, and the client's domain stem (e.g. `acmeplumbing` for acmeplumbing.com).
3. **Don't auto-send the invite.** Always confirm with the user before firing `/invite` — that email goes to the client.
4. **Integrations are agency-level resources.** You can assign existing integrations (GHL, Twilio, calendars) to the sub-account. You cannot create a new GHL/Twilio connection for them from the kit — they OAuth themselves later.
5. **Branding is agency-level, not per sub-account.** All sub-accounts share the agency's white-label branding. To customize per-client, the client logs in and customizes from their own UI (or you do, from theirs).
6. **Branch discipline: stay on main.** No `git checkout -b`.

## Required inputs

- **Client business name** (display)
- **Client slug** (URL-safe, lowercase, hyphens)
- **Admin email** (the person who'll log in)
- **Admin name**
- **Per-minute rate cents** (what you charge them per voice minute; default 12 = $0.12/min)
- **Monthly platform fee cents** (default 9700 = $97/mo)
- **Billing start day** (1-28; default 1)
- **Integrations to assign** (optional list of integration_ids)
- **Template agent to copy** (optional — your "starter agent" you reuse for new clients)

If the user hasn't supplied economics, ask with lettered options. If they have a template agent, ask whether to copy.

## Execution

### Step 1 — Slug availability

```
POST /agency/sub-accounts/check-slug
{ "slug": "<proposed-slug>" }
```

Returns `{available: true|false, slug, message}`. If unavailable, propose 2-3 variations and ask the user to pick.

### Step 2 — List existing integrations (for assignment)

```
GET /agency/my-integrations
```

Returns the agency's integrations (GHL, Twilio, Google Calendar, etc.). Save the IDs.

If the user wants to wire integrations during onboarding, pick which to assign:
- Default: assign the primary GHL integration if there's one
- Calendar integrations (GHL calendar or Google) — assign if the client will book
- Twilio — assign if the client needs phone numbers

Ask the user with lettered options if more than one of each type exists.

### Step 3 — Create the sub-account

```
POST /agency/sub-accounts
{
  "name": "<Display name>",
  "slug": "<verified slug>",
  "admin_email": "<email>",
  "admin_name": "<name>",
  "per_minute_rate_cents": <int>,
  "monthly_platform_fee_cents": <int>,
  "billing_start_day": <1-28>,
  "upcharge_by_provider": null,
  "test_demo_upcharge_by_provider": null,
  "text_upcharge_by_type": null
}
```

Optional `upcharge_by_provider` lets you set different markups per voice provider (e.g. higher for ElevenLabs). Skip unless the user specifies.

Returns the created sub-account with `id`. Save `sub_account_id`.

### Step 4 — Assign integrations

```
POST /agency/sub-accounts/<sub_account_id>/integrations
{ "integration_ids": ["<id1>", "<id2>", ...] }
```

Returns `{success, sub_account_id, assigned, errors}`. If `errors` is non-empty, surface them to the user and continue.

### Step 5 — Copy a template agent (optional)

If the user has a "starter agent" they want every new client to begin with:

```
POST /agents/<template_agent_id>/copy-to/<sub_account_id>
```

The copy carries over the prompt, voice, tools, calendar config (where compatible). The new agent lives in the sub-account.

You can repeat this for multiple template agents.

### Step 6 — Send the invite (with confirmation)

ALWAYS ask before this step. Once fired, the email goes out.

```
POST /agency/sub-accounts/<sub_account_id>/invite
```

This sends the admin a magic-link email to set their password and access the dashboard.

### Step 7 — Verify

```
GET /agency/sub-accounts/<sub_account_id>
```

Check that the sub-account is active, integrations are visible, and any copied agents appear.

### Step 8 — Report back

```
✓ Sub-account "<Client Name>" provisioned
  Slug: <slug>
  Sub-account ID: <id>
  Pricing: $<rate>/min, $<fee>/mo platform fee
  Integrations assigned: <count> (<names>)
  Template agents copied: <count> (<names>)
  Invite sent to: <email>

  Client dashboard:
    https://app.leadlock.ai/<your-agency-slug>/dashboard
  (Or your white-label domain if you've set one.)
```

## Default pricing presets

When the user doesn't specify, propose these defaults with the option to override:

| Preset | Per-minute | Monthly fee | Notes |
|---|---|---|---|
| **Standard** (default) | $0.12 (12¢) | $97 | Healthy margin on top of platform costs |
| **Reseller** | $0.18 (18¢) | $197 | Higher markup for full-service deals |
| **High-volume** | $0.08 (8¢) | $297 | Lower per-minute, higher fixed |
| **Trial** | $0.10 (10¢) | $0 | First month no fee, evaluate before commit |

Pricing is in cents in the API. Always confirm the dollar amount back to the user before posting.

## Post-onboarding next steps (suggest to user)

After the skill completes, tell the user:

1. **The client will get the invite email shortly.** They click the link, set a password, log in.
2. **Their first task: connect their GHL or calendar** (if not pre-assigned) and set up their first agent.
3. **Recommended next**: schedule a 15-minute orientation call with the client to walk them through the platform.
4. **If they need help building their first agent**, the `prospect-demo` skill can spin one up from their site URL.
5. **For branding**: their portal already inherits your agency's white-label. If they want their OWN logo for their team's view, they can change it from their UI.

## Gotchas

- **Slug uniqueness is global across all agencies on the platform.** "acme" is already taken. Pick something distinctive.
- **You can't change the slug after creation.** Treat it like a domain.
- **Billing starts immediately on the billing start day of the current or next month.** If you create on the 15th with `billing_start_day=1`, the first invoice covers a partial period.
- **Assigning a GHL integration doesn't connect their GHL account** — it just gives the sub-account permission to USE your agency's GHL connection. If they want their own GHL, they OAuth from inside their dashboard.
- **Twilio numbers don't auto-transfer.** Numbers must be purchased or imported per sub-account after creation.
- **Invite emails can land in spam.** If the client says they didn't get it, you can re-send via the same endpoint.
- **`upcharge_by_provider` defaults to none, meaning the same per-minute rate across all voice providers.** ElevenLabs costs you more than xAI, so consider an upcharge for ElevenLabs in high-volume accounts.

## Rule capture

<!-- Append new rules here. -->
