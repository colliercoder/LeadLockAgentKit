# Self-Selling Snapshot - Setup Checklist (get it 100% live)

Assumes the GHL snapshot is already imported into your sub-account. Work top to bottom.
Items marked **[script]** are auto-done by `setup_values.py`; the rest are GHL UI (a few minutes each).
The order matters - later steps depend on IDs/links produced by earlier ones.

## 1. Prereqs
- [ ] Snapshot imported into the sub-account (workflows, funnel pages, the cost/agreement come in with it)
- [ ] **Stripe connected** in GHL (Payments -> Integrations) - LIVE mode when you're ready
- [ ] A Leadlock account + API key for this client/sub-account
- [ ] Create a GHL **Private Integration Token** (Settings -> Private Integrations) with the customValues read+write scopes -> used by the scripts

## 2. Build the AI agents (Leadlock)
- [ ] Create your demo agent (runs the role-play + books), your follow-up/reminder agent, and the orb agent
- [ ] Point every agent's booking calendar at the calendar you'll use (note its calendar ID)
- [ ] Grab: demo agent ID -> `leadlock_agent_id`, follow-up agent ID -> `leadlock_reminder_agent_id`, orb page link -> `orb_link`

## 3. Build the intake survey (GHL Surveys)
- [ ] Build the Client Intake survey (business basics, services, hours, call-handling, booking, FAQs, voice)
- [ ] Map standard fields to GHL standards (business name -> Company Name, phone/email -> standard); the rest are custom fields
- [ ] Publish -> copy the share link -> `intake_form_link`

## 4. Build the agreement (GHL Documents & Contracts)
- [ ] Create the service agreement (your terms; fill any bracketed placeholders)
- [ ] Add ONE Signature + a Date field (single client signer)
- [ ] **Attach ONLY the $1,000 Setup product** to the contract's payment (not the monthly) - so it bills the setup, not setup+monthly
- [ ] Payment settings: Invoice Type = One Time, "Generate invoice on signing" = ON, "Send Invoice" = ON
- [ ] **Publish the contract** (this is easy to miss - an unpublished contract = a dead sign link)
- [ ] Copy the doc-form link -> `agreement_link`

## 5. Products + recurring billing (GHL Payments)
- [ ] Create 2 products: `Setup / Build Fee` (one-time) and `AI Receptionist - Monthly` (recurring) with your prices
- [ ] Create the recurring invoice template for the monthly (sent/started at go-live, not at signing)

## 6. Fill the custom values  **[script]**
- [ ] Run `setup_values.py values.json` (fills business name, sender, fees, FAQ, and the links/IDs from steps 2-4)

## 7. Wire the triggers (GHL workflow builder - triggers are UI-only)
- [ ] **C1 Onboarding**: trigger on Opportunity Status = Won (and/or Pipeline Stage = Won). Confirm re-entry OFF.
- [ ] **C1b Agreement Signed**: Documents & Contracts trigger, Status = Signed/Accepted, Template = your agreement.
- [ ] **C2 Payment Received**: Payment received, Source=Invoice, Sub-Source=One-time invoice, Payment status=Success. Re-entry OFF.
- [ ] **C2 Dunning**: Payment received, Source=Invoice, Payment status=Failed. **Re-entry ON** (dun every failure, not just the first).
- [ ] **C3 Fulfillment**: Contact tag added = `onboarded`.
- [ ] **C3 Go Live**: Contact tag added = `qa-passed`. Add a paid-gate (If/Else "has tag paid" as the first step, or rely on the sequence) so an unpaid client can't be flipped live.
- [ ] **Scheduled (reminders)**: Appointment Status trigger -> set Calendar = your booking calendar.

## 8. Publish everything
- [ ] Publish all the workflows (Draft -> Publish)
- [ ] Confirm the agents' calendars + the Scheduled trigger calendar all point to the same calendar

## 9. Verify + test  **[script]**
- [ ] Run `verify.py values.json` -> confirms every custom value is filled + 2 products exist
- [ ] **Test-buyer run** with a test contact + a number you control: mark Won -> sign -> pay (Stripe test mode) -> onboarded -> add `qa-passed` -> live. Confirm each field/tag/stage flips.

## Gotchas we learned
- The contract **must be published**, or its link is dead.
- Dunning re-entry must be **ON**; everything else **OFF**.
- Attach **only the setup product** to the contract (signing bills setup; monthly starts at go-live).
- Triggers are **UI-only** - they don't import/edit via API.
- After switching calendars later, update all agents **and** the Scheduled trigger's calendar.
