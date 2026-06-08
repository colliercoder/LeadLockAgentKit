# Consent, Opt-In, and Call-to-Action (CTA) Requirements

> Source: https://www.twilio.com/en-us/blog/insights/compliance/opt-in-opt-out-text-messages | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc | https://www.twilio.com/docs/api/errors/30909 | https://www.twilio.com/docs/api/errors/30896 | https://www.twilio.com/docs/api/errors/30924 | https://www.twilio.com/docs/api/errors/30925 | https://www.twilio.com/en-us/blog/insights/best-practices/improving-your-chances-of-a2p10dlc-registration-approval | https://api.ctia.org/wp-content/uploads/2023/05/230523-CTIA-Messaging-Principles-and-Best-Practices-FINAL.pdf - scraped 2026-06-07

Consent is the single most common reason A2P 10DLC campaigns get rejected. A campaign is reviewed by The Campaign Registry (TCR) and the carriers, and the reviewer's core job is to confirm that the people who will receive your messages actually agreed to receive them, and that the way you collected that agreement meets TCPA + CTIA + carrier standards. If the reviewer cannot see and verify your opt-in, the campaign is rejected - regardless of how legitimate your business is.

This document covers what consent means, what you must disclose at opt-in, how each opt-in channel works, what reviewers actually check, and how to write a `message_flow` / Call-to-Action that passes.

---

## 1. The Consent Principle

Per the CTIA Messaging Principles and Best Practices (May 2023, §5.1), and aligned with the TCPA and FCC regulations, every non-consumer message sender is expected to:

- **Obtain a consumer's consent to receive messages generally** (before any non-conversational message).
- **Obtain a consumer's express written consent to specifically receive marketing/promotional messages.**
- **Ensure consumers can revoke consent** at any time.

Three rules sit on top of this:

| Rule | Source | What it means |
|---|---|---|
| Consent must be direct from the consumer | CTIA §5.1 | You collect it yourself from the person whose number it is. |
| Consent **cannot be bought, sold, rented, or shared** | CTIA §5.1.4 | "Message Senders should not use opt-in lists that have been rented, sold, or shared. Message Senders should create and vet their own opt-in lists." |
| Consent is **not transferable or assignable** | CTIA §5.1.2.2 | One opt-in applies only to the specific campaign(s) and the specific message sender it was obtained for. You cannot reuse consent across brands, campaigns, or channels. |

**Consent for one channel does not carry to SMS.** If a consumer agreed to be emailed or called, that is not consent to be texted - even if they gave you their mobile number for that other purpose. SMS consent is its own affirmative act.

### Consent levels by message type (CTIA Exhibit II)

| Content type | Consent required | Definition |
|---|---|---|
| **Conversational** | Implied | A back-and-forth that the consumer initiates. If the consumer texts first and you respond, no extra permission is expected. |
| **Informational** | Express | The consumer gives you their number and asks to be contacted (appointment reminders, welcome texts, alerts). They must agree to receive texts for that specific purpose. |
| **Promotional / Marketing** | Express **written** | Any sales or marketing message. Adding a CTA like a coupon code can push a message into this category. The consumer must agree **in writing** (check a box online, sign a form, etc.) before you send promotional texts. |

---

## 2. Required Disclosures at the Point of Opt-In

The CTIA defines the Call-to-Action (§5.1.1) as *"an invitation to a Consumer to opt-in to a messaging campaign."* The disclosures exist so the consumer understands the nature and purpose of the program before consenting. Carriers reject campaigns (Twilio errors 30909, 30924) when these are missing.

A compliant opt-in / Call-to-Action must make the consumer aware of all of the following:

| # | Disclosure | Required by |
|---|---|---|
| 1 | **Program / brand name** - the specific identity of the organization sending messages | CTIA §5.1.1; Twilio 30896 |
| 2 | **Program or product description** - what the messages are about | CTIA §5.1.1 |
| 3 | **Phone number(s) or short code(s)** the messages originate from | CTIA §5.1.1 |
| 4 | **Message frequency** - e.g. "message frequency varies" or "Up to 5 msgs/month" | CTIA §5.1.2.1; Twilio 30924 |
| 5 | **"Message and data rates may apply"** - verbatim rate disclosure | Twilio 30909/30924; CTIA §5.1.1 (fees/charges) |
| 6 | **Opt-out instructions** - e.g. "Reply STOP to unsubscribe" | CTIA §5.1.1/§5.1.3; Twilio 30924 |
| 7 | **HELP instructions** - how to reach support (HELP keyword, toll-free / 10-digit number) | CTIA §5.1.1 |
| 8 | **Link to Terms & Conditions** | Twilio 30909/30934 |
| 9 | **Link to Privacy Policy** | Twilio 30908/30909/30933 |

**The opt-in details must not be obscured.** CTIA §5.1.1: *"opt-in details should not be obscured in terms and conditions (especially terms related to other services)"* and the CTA must not contain deceptive language.

### Privacy policy content requirements

The privacy policy you link is itself inspected. It must state:

- Mobile numbers / opt-in data are **not shared or sold to third parties, affiliates, or lead generators** for marketing or promotional purposes.
- Message frequency.
- "Message and data rates may apply."

A privacy policy that omits the non-sharing statement is a documented rejection cause (Twilio 30896, 30908).

---

## 3. Web Form Opt-In Rules (the most-scrutinized path)

Website opt-in is the most common and most-rejected path because reviewers can directly inspect it. The rules below are strict and individually enforced by carrier rejection codes.

| Rule | Detail | Rejection code if violated |
|---|---|---|
| **Checkbox unchecked by default** | The consent control cannot be pre-selected. The consumer must actively check it. | Twilio **30925** |
| **Consent must be a separate, standalone control** | A dedicated checkbox/toggle for *messaging* consent - not bundled into a general "I accept Terms / Privacy Policy" checkbox. | Twilio **30925** |
| **Messaging consent ≠ Terms acceptance** | Accepting general Terms of Service or Privacy Policy does **not** count as messaging consent. They must be kept separate. | Twilio **30925** |
| **Marketing vs. transactional consent are separate** | Promotional/marketing consent (express written) is distinct from transactional/informational consent. Use a separate checkbox for marketing. | CTIA Exhibit II; Twilio 30924 |
| **Consent language must be standalone, not buried** | The consent disclosure cannot be hidden inside the T&C body. | CTIA §5.1.1 |
| **Opt-in should be optional** | Consent to receive marketing texts should not be a forced precondition of completing the form/purchase. The checkbox is a choice the consumer makes, not a gate. | CTIA §5.1 (express, affirmative consent) - Twilio: opt-in must show *active* choice |
| **All required disclosures present on/near the form** | Frequency, "message and data rates may apply," STOP/HELP, Terms link, Privacy link. | Twilio 30924 |

> Note on "optional / unchecked": Twilio error 30925 is explicit that the box must be **unchecked by default** and require **active consent**. The CTIA framework requires consent to be **express and affirmative**, which a default-required checkbox does not satisfy. Together these mean: a default-checked box, or a box the user must check just to submit, will not pass review as valid affirmative consent. Keep marketing-message consent genuinely optional.

---

## 4. Other Opt-In Channels

CTIA §5.1.2 explicitly recognizes multiple opt-in mechanisms; messages may only be sent **after** the consumer has opted in. Twilio supports verbal, web/online, paper, mobile QR code, and text/keyword-based consent.

| Channel | What it is | What you must capture / submit |
|---|---|---|
| **Web / online** | Standalone consent form on your site or app. | Public URL, unchecked consent checkbox, all disclosures, Terms + Privacy links. (See §3.) |
| **Keyword / text-to-join** | Consumer texts an advertising keyword (e.g. `JOIN`) to your number. | The keyword, the originating number, and a compliant auto-reply confirmation. You must populate `opt_in_keywords` and `opt_in_message` (and `help_message`/`opt_out_message` if you manage those yourself). |
| **Verbal / IVR** | Consent captured on a phone call or via interactive voice response. | A detailed script showing exactly how consent was requested and captured, in enough detail for a reviewer to verify. |
| **Point of sale (POS) / on-site** | Consumer signs up in person at a physical location. | Describe the in-store flow and provide verifiable evidence (e.g. hosted photo/screenshot of the sign-up form). |
| **Paper form** | Signed physical document indicating consent. | A signed document clearly indicating messaging consent (e.g. "Sign here to opt in to promotional messages from [Company]"), with the required disclosures on the form, plus a publicly hosted photo of the form. |
| **Mobile QR code** | Consumer scans a QR code. | The QR must lead either to a web opt-in form (phone number + consent) or to a templated opt-in message in the user's SMS app. Describe the destination and its disclosures. |

For every offline/non-public channel (verbal, paper, POS, gated page), the disclosures are the same - what changes is that you must **provide hosted, publicly accessible evidence** (screenshots, a photo of the form, the IVR script) because the reviewer cannot reach the flow directly.

---

## 5. Double Opt-In (Confirmed Opt-In)

**What it is:** After the consumer opts in, you send a single confirmation SMS that the consumer must (or can) acknowledge, confirming they want recurring messages, before any further messaging begins.

**Why it's recommended:** It reduces unwanted messages and protects against wrong-number opt-ins - a consumer who mistakenly or deliberately enters a number that isn't theirs gets caught at the confirmation step (CTIA §5.1.2). It is the cleanest way to prove enrollment.

**The CTIA flow (§5.1.2.1 - required for recurring campaigns):** After confirming a consumer has opted in, send an opt-in confirmation message **before any additional messaging is sent.** That confirmation message must include:

1. Program name or product description.
2. Customer care contact info (toll-free number, 10-digit number, or HELP instructions).
3. How to opt out.
4. A disclosure that messages are **recurring**, plus the message frequency.
5. Clear language about any fees/charges and how they will be billed.

**Worked confirmation message (from Twilio's accepted keyword example):**

```
Acme Sandwich Co: You are now subscribed to weekly deals.
Msg frequency varies. Msg & data rates may apply.
Reply HELP for help, STOP to cancel.
```

When you offer keyword opt-in, this text is what goes in the `opt_in_message` field (20–320 characters), and it must name the brand and include opt-out instructions.

---

## 6. What Reviewers Actually Check

TCR reviewers verify each of these before approving (Twilio 30909). This is the practical rejection checklist:

| Check | What it means | Fails when… |
|---|---|---|
| **Collection mechanism** | `message_flow` describes every way users give consent (web form, keyword, paper, QR, verbal). | "End users opt in on our website." - names no URL, mechanism, or disclosures. |
| **Required disclosures** | Privacy link, Terms link, message frequency, and "message and data rates may apply" all present. | Any one is missing. |
| **Public verifiability** | The reviewer can actually reach and confirm the opt-in experience. | URL is behind a login, incomplete, or the form doesn't exist at the stated URL - **and** no hosted screenshots were provided. |
| **All paths listed** | If the campaign has multiple opt-in methods, every one is in the **same** `message_flow` field. | Submission describes only one of several active paths. |
| **Checkbox state** | Web consent control is unchecked by default and separate from Terms acceptance. | Pre-checked, or bundled into the general Terms checkbox (30925). |
| **Sample messages** | Match the declared use case, identify the brand by name, and include opt-out language. | Generic samples, no brand name, no STOP language. |

**The opt-in URL must be publicly accessible - not behind a login.** If your real opt-in page is gated (members area, app behind auth) or the flow is offline, you must host screenshots of the complete consent flow (the form, the consent language, the disclosures) at a public URL and submit that. Twilio error 30921 is dedicated to "Website requires authentication and cannot be reviewed." Screenshots of the full consent experience are explicitly recommended as supporting evidence.

### Related granular rejection codes

| Code | Meaning |
|---|---|
| 30896 | General opt-in error - `message_flow` doesn't adequately show consent. |
| 30907 | Website URL validation issue. |
| 30908 / 30933 | Compliant Privacy Policy / Privacy Policy URL required. |
| 30917 | All opt-in methods must include complete workflow descriptions. |
| 30919 | Website lacks sufficient business or messaging use-case info. |
| 30921 | Website requires authentication and cannot be reviewed. |
| 30924 | Missing or non-compliant consent agreement language in opt-in flow. |
| 30925 | Opt-in must be unchecked by default; active consent required. |
| 30934 | Terms and Conditions URL required. |

---

## 7. Consent Recordkeeping

CTIA §5.1.2 directs message senders to **document and retain** opt-in consent. Keep, where applicable:

- **Timestamp** of consent acquisition.
- **Consent acquisition medium** (web form, physical sign-up form, SMS keyword, etc.).
- **Capture of the experience** - the exact language and action used to secure consent (i.e. what the consumer actually saw and did).
- **The specific campaign** the opt-in was provided for.
- **IP address** used to grant consent.
- **The consumer phone number** consent was granted for.
- **Identity of the individual** who consented (name or other identifier - online username, session ID, etc.).

Additional retention duties (CTIA §5.1.5): retain **all** opt-in and opt-out requests so future messages are not sent to opted-out numbers, and process telephone-number deactivation files regularly (e.g. daily) to remove deactivated numbers from opt-in lists.

---

## 8. The CTA / `message_flow` Field

In Twilio's A2P registration, the Call-to-Action is submitted as the `message_flow` field (40–2049 characters). It must describe, end-to-end, where and how opt-in occurs, and link to your Privacy Policy and Terms.

| Field | Purpose | Length | When required |
|---|---|---|---|
| `message_flow` | End-to-end description of every opt-in path + links to Privacy Policy and Terms. | 40–2049 chars | Always. |
| `opt_in_message` | Auto-reply confirming enrollment, including brand name + opt-out instructions. | 20–320 chars | When keyword opt-in is offered. |
| `help_message` | Auto-reply with support options when a user sends a HELP keyword. | 20–320 chars | When you manage HELP replies yourself. |
| `opt_out_message` | Acknowledges opt-out and confirms no further messages. | 20–320 chars | When you manage opt-out yourself. |

If a campaign uses more than one opt-in method, **describe every path in the same `message_flow` field.** Reviewers reject campaigns that account for only one of several active paths.

### Acceptable vs. unacceptable `message_flow` examples (Twilio 30909)

**Website - unacceptable:**
> `End users opt in on our website.`
> (No URL, no Privacy/Terms link, no consent mechanism described.)

**Website - acceptable:**
> `End users opt in by visiting www.acmesandwich.com/sms-signup and entering their phone number. They check a box agreeing to receive recurring promotional text messages from Acme Sandwich Company. Message frequency varies. Message and data rates may apply. Terms and Conditions: www.acmesandwich.com/terms. Privacy Policy: www.acmesandwich.com/privacy (states mobile numbers are not shared with third parties).`

**Keyword - acceptable:**
> `End users opt in by texting JOIN to (555) 123-4567. They receive an auto-reply: "Acme Sandwich Co: You are now subscribed to weekly deals. Msg frequency varies. Msg & data rates may apply. Reply HELP for help, STOP to cancel." Terms: www.acmesandwich.com/terms. Privacy: www.acmesandwich.com/privacy.`

**Paper / offline - acceptable:**
> `End users opt in by filling out a paper form at Acme Sandwich Company retail locations. The form collects the customer's mobile number and includes checkboxes for consent to receive recurring promotional messages from Acme Sandwich Company. The form text states message frequency varies and message and data rates may apply, and provides links to www.acmesandwich.com/terms and www.acmesandwich.com/privacy. A photo of the form is hosted at www.acmesandwich.com/opt-in-evidence.`

**Multiple paths in one campaign - acceptable:**
> `End users opt in by (1) visiting www.acmesandwich.com/sms-signup and entering their phone number, checking a box agreeing to receive recurring promotional text messages, or (2) texting JOIN to (555) 123-4567 and receiving a confirmation auto-reply. Message frequency varies. Msg & data rates may apply. Terms: www.acmesandwich.com/terms. Privacy: www.acmesandwich.com/privacy.`

---

## 9. Cold Outreach Is Prohibited

A2P 10DLC exists to ensure that SMS traffic to US end users is *"verified and consensual"* (Twilio A2P 10DLC docs). Messaging requires **prior consent** before the first message - you cannot text people who have not opted in. The CTIA framework is the same: messages should be sent **only after** the consumer has opted in (§5.1.2), and the only no-prior-permission case is purely **conversational** messaging that the consumer initiates first.

There is no compliant path for sending unsolicited marketing or informational SMS to a list of numbers you did not collect consent from. Purchased, rented, or shared lists are explicitly disallowed (CTIA §5.1.4). Cold SMS outreach gets campaigns rejected and traffic blocked/filtered.

---

## 10. Opt-Out and HELP Handling Obligations

Honoring opt-out and HELP is mandatory and is part of what makes consent valid (the consumer must be able to revoke). CTIA §5.1.3:

**Opt-out:**
- Consumers must be able to opt out **at any time**.
- Support **multiple** opt-out mechanisms (phone, email, text).
- On a valid opt-out, send **one final opt-out confirmation message** per campaign and then **no further messages**.
- State in messages how to opt out. Use standardized **STOP** wording, but you must also read and honor normal-language variants: **STOP, END, UNSUBSCRIBE, CANCEL, QUIT,** and phrases like "please opt me out" - except where a specific word could cause an unintentional opt-out.
- Opt-out validity is **not** affected by de minimis variance - capitalization, punctuation, or letter-case do not invalidate a STOP request.

**HELP:**
- The **HELP** keyword must return support/contact information (e.g. a toll-free number, a 10-digit number, or care instructions).

**Confirmation replies:**
- Opt-out: send exactly one confirmation, then stop.
- HELP: respond with support contact info.
- Opt-in (recurring): send the confirmation message before any additional messaging (see §5).

> Twilio offers default and Advanced Opt-Out handling. If you let Twilio manage STOP/HELP/UNSTOP, you don't supply `opt_out_message`/`help_message` yourself. If you manage these flows independently, you **must** populate `opt_out_message`, `opt_out_keywords`, `help_message`, and `help_keywords` in registration.

---

## Quick Pre-Submission Checklist

- [ ] `message_flow` names the exact URL, keyword, paper form, or mechanism where consent is collected - every path, in one field.
- [ ] `message_flow` includes a link to the Privacy Policy **and** a link to Terms & Conditions.
- [ ] Privacy Policy states mobile numbers are not shared with third parties, includes message frequency, and includes "message and data rates may apply."
- [ ] Web consent checkbox is **unchecked by default**, separate from Terms acceptance, and optional (not a forced gate for marketing consent).
- [ ] Marketing consent is a separate checkbox from transactional/informational consent.
- [ ] Opt-in URL is publicly accessible; if gated or offline, hosted screenshots of the full consent flow are provided.
- [ ] The opt-in flow actually exists at the stated URL.
- [ ] For keyword opt-in: `opt_in_message`, `opt_in_keywords`, `help_message`, `help_keywords`, `opt_out_message`, `opt_out_keywords` populated (if not using Twilio defaults).
- [ ] Sample messages match the use case, name the brand, and include STOP/opt-out language.
- [ ] Consent records retained: timestamp, medium, exact language shown, campaign, IP, phone number, consenter identity.
- [ ] No purchased/rented/shared lists; no cold outreach.

---

## Worked Opt-In Checkbox Example

A compliant web-form consent block. The checkbox is **unchecked by default**, is **separate** from any "I accept the Terms" checkbox, is **optional** (the form submits without it; only marketing texts depend on it), and the consent language is **standalone** (not buried in the Terms).

```html
<form action="/signup" method="post">
  <label for="phone">Mobile number</label>
  <input type="tel" id="phone" name="phone" required>

  <!-- Separate, REQUIRED: general account terms (this is NOT messaging consent) -->
  <label>
    <input type="checkbox" name="accept_terms" required>
    I agree to the
    <a href="https://acmesandwich.com/terms" target="_blank">Terms &amp; Conditions</a>
    and
    <a href="https://acmesandwich.com/privacy" target="_blank">Privacy Policy</a>.
  </label>

  <!-- Separate, OPTIONAL, UNCHECKED BY DEFAULT: marketing SMS consent -->
  <label>
    <input type="checkbox" name="sms_marketing_consent">
    <!-- no "checked", no "required" -->
    By checking this box, I agree to receive recurring automated promotional
    text messages from Acme Sandwich Company at the number provided. Consent is
    not a condition of purchase. Message frequency varies. Message and data
    rates may apply. Reply HELP for help, STOP to cancel. See our
    <a href="https://acmesandwich.com/terms" target="_blank">Terms</a> and
    <a href="https://acmesandwich.com/privacy" target="_blank">Privacy Policy</a>.
  </label>

  <button type="submit">Sign up</button>
</form>
```

Why this passes:

- **Unchecked by default** - no `checked` attribute on the SMS box (avoids error 30925).
- **Separate control** - messaging consent is its own checkbox, not folded into the Terms checkbox (avoids 30925).
- **Optional** - the SMS box has no `required`; only `accept_terms` is required. "Consent is not a condition of purchase" is stated explicitly.
- **Standalone consent language** - the disclosure lives next to the checkbox, not inside the Terms document (CTIA §5.1.1).
- **All disclosures present** - brand name, recurring + automated, frequency, "message and data rates may apply," STOP/HELP, Terms + Privacy links (avoids 30924).

After building this, host the page at a **publicly accessible** URL, put that URL in `message_flow`, and - if the page is ever gated - capture screenshots of the full flow and host them publicly for the reviewer.
