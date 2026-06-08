> Source: https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/troubleshooting-a2p-brands/troubleshooting-and-rectifying-a2p-campaigns, https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/troubleshooting-a2p-brands/troubleshooting-and-rectifying-a2p-standardlvs-brands, https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/troubleshooting-a2p-brands/troubleshooting-sole-proprietor-brand-registration-failures, https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/collect-business-info, and the individual Twilio error pages at https://www.twilio.com/docs/api/errors/<code> (30886, 30887, 30888, 30889, 30890, 30891, 30892, 30893, 30894, 30895, 30896, 30897, 30898, 30899, 30909, 30910, plus brand codes 30703, 30795, 18011) - scraped 2026-06-07

# A2P 10DLC Brand & Campaign Rejection Error Codes - The Troubleshooting Bible

This is the field manual for diagnosing and fixing US A2P 10DLC registration rejections. When a Brand or Campaign comes back rejected, you get an error code. This doc maps every code to **what it means**, the **usual root cause**, and the **concrete fix**.

> **Scope:** US A2P 10DLC only. The `3088x`–`3091x` series are **campaign-level** vetting rejections introduced/expanded in Twilio's March 2026 "more actionable error codes" rollout. The `307xx` / `18xxx` series are **brand-level** registration failures. Treat the two layers separately - a brand problem will not be fixed by editing campaign fields, and vice versa.

> **Verification note:** All entries below are taken from current official Twilio error pages and troubleshooting docs. Where a code's exact behavior is described only in Twilio's own words, it is quoted/paraphrased "per Twilio" with the page linked. Nothing here is invented.

---

## How to read this doc

1. **Get the code.** Find it in Console (**Messaging → Regulatory Compliance → Campaigns** / **Brands**) or via the API (`Usa2p` / `BrandRegistration` resource `errors` field).
2. **Identify the layer.** `3088x`–`3091x` = campaign. `307xx` / `18xxx` = brand.
3. **Look it up in the table** below for cause + fix.
4. **Read the expanded section** for the high-frequency codes (30886, 30891, 30892, 30896, 30897, 30909).
5. **Fix the field, then resubmit** following the [Resubmission Process](#resubmission-process--vetting-fees).

---

## Master lookup table - Campaign-level rejections (`3088x`–`3091x`)

| Code | Official short name | What it means (plain English) | Usual root cause | Concrete fix |
|---|---|---|---|---|
| **30886** | Invalid Campaign Description | The free-text campaign description is too vague, or it doesn't match the rest of your registration. | Description doesn't say who is sending, who receives, and why; or it contradicts the use case, sample messages, brand name, or website. | Rewrite the description to clearly state **sender, recipients, and purpose**. Make it match the use case and samples. Use the real registered business name (not your ISV/platform name). Remove personal info. Then edit + resubmit. |
| **30887** | Opt-out Error | The way users stop messages isn't clearly defined or is incomplete. | CTA/message flow doesn't explain opt-out; or you self-manage opt-outs but left `opt_out_keywords` / `opt_out_message` blank; or the opt-out reply doesn't confirm no further messages. | Describe opt-out in the CTA/flow. Provide every `opt_out_keywords` value (STOP, UNSUBSCRIBE, END, QUIT, HALT). Add an `opt_out_message` that names your brand and confirms messages will stop. Or use Twilio default/Advanced Opt-Out instead of custom fields. |
| **30888** | Age Gate Not Present / Not Acceptable | Age-restricted content lacks a proper age gate before opt-in/content access. | No age gate on the website or opt-in flow; or the method is too weak (a simple yes/no prompt). | Add a robust age gate (collect full date of birth or use a third-party age-verification service) **before** content/opt-in. Explain in the message flow where and how age verification happens. Resubmit. |
| **30889** | Embedded Phone Number | You flagged that messages contain phone numbers, but the samples don't show them (or vice versa). | `has_embedded_phone = true` (or the Console checkbox) but no sample message includes a phone number; samples aren't representative. | If you do send phone numbers, add representative numbers to 2–5 realistic samples (at least one naming your brand/website). If you don't, set `has_embedded_phone = false` / clear the checkbox. Make description, use case, and samples consistent. Resubmit. |
| **30890** | Subscriber Help | The HELP reply doesn't give users a real way to get support. | `help_message` is missing your brand name and/or a support phone/email; help response doesn't tell users who to contact. | Update `help_message` to include your **brand name + a valid support phone or email**. If you don't self-manage help, use Twilio default/Advanced Opt-Out instead of a custom help flow. Resubmit. |
| **30891** | Invalid Website URL | The website you submitted is broken, unreachable, or doesn't show the opt-in. | Bad/typo URL; site down or geo-restricted; opt-in flow not found on the page; pre-launch site not flagged as such. | Verify the URL works and is publicly accessible. If geo-specific or pre-launch, say so in the description and link a hosted **screenshot** of the SMS opt-in. Put the direct opt-in link in the **Message Flow** field. For login/paper opt-ins, host an image of the form. Resubmit. |
| **30892** | Invalid Sample Message - Public URL Shorteners | A sample message uses a shared public link shortener (e.g. bit.ly) or an unsecured URL. | Public/shared shortener instead of a business-owned branded domain; or a non-HTTPS URL; link doesn't identify your business. | Replace shared shorteners with a direct business URL or a **branded short URL you own**. Ensure all URLs are HTTPS and public. If you need shortening, use Messaging Services link shortening with your own branded domain. Resubmit. |
| **30893** | Inconsistency between Sample Message and Use-case | The sample messages don't match the use case you selected. | Samples missing/unclear, or their content doesn't reflect the declared use case; invalid content in samples. | Provide at least **2** accurate, representative samples. Bracket templated fields `[like this]`. At least one sample should include your business name + opt-out language. Align use case ↔ description ↔ samples. Resubmit. |
| **30894** | Invalid Brand Information | The campaign can't be tied to a valid brand behind it. | Registration isn't associated with the brand actually sending; an ISV registering a direct offering didn't say so in the description. | Verify the brand information is valid and that the campaign is associated with the correct brand. If you're an ISV with a direct offering, state that in the campaign description. Resubmit. |
| **30895** | Direct Lending - Campaign and Content Attribute Error | A lending-related campaign didn't disclose direct lending in its content attributes. | Financial/loan use case but "direct lending" not disclosed; the direct-lending setting not selected in Console / not set in the API; description or samples imply lending but attributes don't match. (Applies even to OTP/2FA for a lender.) | If the business does first-party (direct) lending, **declare Direct Lending** in the description and set the direct-lending content attribute. Make content attributes match the actual use case. Resubmit. |
| **30896** | Opt-in Error | The consent/opt-in flow isn't clearly explained or can't be verified. | `message_flow` doesn't show who/where/how consent is collected; multiple opt-in methods but not all listed; missing privacy policy / ToS / hosted screenshots; privacy policy lacks the mobile-number non-sharing statement, message frequency, or "msg & data rates may apply"; keyword opt-in declared without `opt_in_keywords` / `opt_in_message`; consent implied to be shared/transferred. | Rewrite `message_flow` to explain **who opts in, where, and how** - list every opt-in path. Supply website URL + privacy policy + ToS, or hosted screenshots for gated/paper flows. Add the required privacy-policy disclosures (non-sharing of mobile numbers, frequency, rates). For keyword opt-in, provide `opt_in_keywords` + a compliant `opt_in_message`. Resubmit. |
| **30897** | Disallowed Content | The campaign's content/business model falls into a forbidden messaging category. | High-risk financial (loan marketing, stock/crypto alerts), third-party debt collection / debt reduction / credit repair / lead-gen, gambling/sweepstakes, or federally illegal substances - i.e. a forbidden category. | **Do not resubmit the same campaign - it is ineligible for resubmission.** Review your use case against Twilio's Forbidden Message Categories + Messaging Policy and build a different, compliant campaign. If you believe it was rejected in error, contact Twilio Support. |
| **30898** | Excessive EIN | Too many brands registered under one EIN without a valid business reason. | Same EIN used for too many brand registrations; campaign on a brand that duplicates an existing identity under the same EIN; separate brands created for traffic that should sit under one approved brand. | Consolidate: review all brands on that EIN, remove duplicates, keep the minimum needed. Reuse an existing approved brand when the identity is the same, then resubmit the campaign under the correct brand. **Don't resubmit the rejected campaign until the brand structure is fixed.** If you genuinely need multiple brands, be ready to justify it; appeal via Support if rejected in error. |
| **30899** | Campaign registration failed due to carrier rejection(s) | A downstream carrier rejected the campaign during ecosystem review. | Inaccurate/inconsistent registration data across brand/website/samples/use case; message flow or CTA missing required disclosures; or the campaign appeared to carry prohibited/high-risk traffic. | Fetch the `Usa2p` resource and read `campaign_status` + `errors` to find the specific underlying code(s). Make brand, website, samples, use case, and message flow accurate, complete, and consistent; document opt-in + disclosures. Contact Support (campaign SID + Messaging Service SID) if not directly resubmittable. |
| **30909** | Campaign rejected: Message Flow or Call to Action incomplete/unverified | The opt-in evidence in your Message Flow can't be verified by a reviewer. | Message flow doesn't explain opt-in for offline flows (verbal, paper, in-store, QR); not every opt-in method listed; website opt-in missing ToS / privacy / frequency / "msg & data rates" disclosure; opt-in page private/behind a login with no public screenshots; keyword opt-in missing required `opt_in_message` / `opt_out_message` / `help_message` details. | Write a self-contained Message Flow describing **exactly how consent is collected** for every method. For offline/gated flows, host a publicly accessible screenshot or a publicly reachable page (e.g. the QR-code destination) containing the same disclosures a website opt-in needs. **Edit the rejected campaign** (don't delete/recreate) and resubmit. |
| **30910** | Campaign rejected: A2P 10DLC campaigns must be submitted in English | Registration fields contain non-English text without an English translation. | Description, `message_flow`, sample messages, or other fields are in another language (or mixed-language) without an English translation. | Rewrite all registration fields in English. If end-user disclosures/samples are in another language, include an **English translation** in the registration details and in `message_flow`. Keep samples consistent with the use case + brand. Resubmit. |

## Master lookup table - Brand-level registration failures (`307xx` / `18xxx`)

These are about your **business identity**, not your messaging program. Fix the Business Profile / Brand, not the campaign.

| Code | Official short name | What it means (plain English) | Usual root cause | Concrete fix |
|---|---|---|---|---|
| **30703** | Brand Registration Failure: Duplicate record detected | A unique field on your brand collides with an existing brand. | One of these is not unique: mobile phone number, business registration identifier (EIN), business legal name, authorized representative, email address, website address, or stock symbol. | Read the error to see which field(s) collided, then supply a **unique** value for each: unique US mobile number, unique EIN, unique legal name, unique authorized rep, unique email, unique website, unique stock symbol. Resubmit. |
| **30795** | Brand Registration: Tax ID data mismatch | The Tax ID (EIN) and your legal company name don't match authoritative records. | Invalid/unverifiable US EIN (or Canadian/foreign gov ID); legal company name doesn't match the name tied to the EIN; or an SSN was submitted instead of an EIN. | Use the **exact legal name as it appears on the IRS CP 575 (or 147c) letter** - all lines above the address line. Use the EIN, never an SSN. If the EIN is new (issued in the last 30–90 days), wait a few weeks for it to propagate before resubmitting. For urgent cases, send the CP 575 / 147c letter to Twilio Support for a manual identity-status appeal (typically 5–7 business days; federal docs only). |
| **18011** | Business name mismatch | The business name doesn't match the supporting registration document. | Business name + registration info don't align with the local/commercial company register excerpt. | Resubmit with the **accurate business name and the corresponding business registration number** that match the supporting document. |

> **Other brand-level codes you may see** (not individually fetched here, look them up at `twilio.com/docs/api/errors/<code>` if encountered): identity/address verification failures and "Brand not qualified to run Campaign for AT&T" gating. The same root principle applies - make the Business Profile match authoritative records exactly.

---

## Expanded notes - the codes you'll hit most often

### 30886 - Invalid Campaign Description

**What it means:** Your campaign's free-text description failed review. This is the single most common "soft" rejection because the description is the reviewer's first read on your whole program.

**Root causes (per Twilio):**
- Too vague or incomplete - doesn't explain **who** sends, **who** receives, and **why** they get messages.
- Doesn't align with the selected use case.
- Contradicts your sample messages, brand name, website, or other registration details.
- For ISVs/platforms: the description names your platform instead of the actual business sending the messages.
- Contains personal information instead of a general program summary.

**The fix:**
- Rewrite to state, in order: **sender → recipients → purpose**.
- Make it specific enough to describe the real messaging program (not boilerplate).
- Match it to the use case **and** the sample messages.
- Use the actual registered business/brand name. If you're an ISV with a direct offering, say so explicitly.
- Strip personal info.
- If the business does direct first-party lending, include "Direct Lending."
- **Edit the failed campaign and resubmit** - only create a brand-new campaign if the use case itself was wrong or the failure is tied to the brand rather than the campaign details.

---

### 30891 - Invalid Website URL

**What it means:** The reviewer couldn't load your site, or loaded it and couldn't find the opt-in. Without a verifiable site, consent can't be confirmed.

**Root causes (per Twilio):**
- An invalid URL was entered (typo, wrong protocol, dead link).
- The site is down, broken, or otherwise inaccessible (including geo-restricted sites the reviewer can't reach).
- The opt-in flow isn't present on the page provided.
- A pre-launch website wasn't flagged as pre-launch in the description.

**The fix:**
- Confirm the URL works and is publicly reachable. If it's geo-specific, say so in the description **and** link a hosted screenshot.
- If pre-launch, instead provide a publicly accessible URL to a **screenshot of the SMS opt-in flow** that will appear.
- If opt-in happens on the site, put the **direct link in the Message Flow field**.
- If opt-in is on paper or behind a login, host an **image of the opt-in form** and link it.
- Resubmit after fixing.

---

### 30892 - Invalid Sample Message (Public URL Shorteners)

**What it means:** A link in your sample messages uses a shared public shortener or an insecure URL. Carriers treat shared shorteners as a spam/phishing vector because the destination is opaque.

**Root causes (per Twilio):**
- A sample includes a link from a **shared public URL shortener** (e.g. bit.ly, tinyurl) instead of a business-owned branded short domain.
- A sample includes an **unsecured (non-HTTPS)** URL.
- The URL doesn't clearly identify your business.

**The fix:**
- Remove shared shortener links from samples; use a **direct business URL** or a **branded short URL you own**.
- Make every URL secure (HTTPS) and publicly accessible.
- If you need shortening, configure **link shortening with your own branded domain** via Messaging Services - never a free public shortener.
- Re-check all samples before resubmitting so every link maps to your business.

---

### 30896 - Opt-in Error

**What it means:** The consent flow is the heart of A2P compliance, and yours couldn't be verified. This is the most detailed rejection because there are many ways consent can be unclear.

**Root causes (per Twilio):**
- `message_flow` doesn't clearly explain **who** opts in, **where** opt-in happens, or **how** consent is collected.
- You use more than one opt-in method but didn't list every one.
- A website opt-in flow is missing a public website link, a privacy policy link, terms of service, or hosted screenshots for gated/paper/other flows the reviewer can't access.
- The **privacy policy** is missing the required **mobile-number non-sharing statement**, **message frequency**, or **"message and data rates may apply"** disclosure.
- You declared keyword opt-in but didn't provide `opt_in_keywords` or a compliant `opt_in_message`.
- The opt-in description implies consent is shared, transferred, or not collected specifically for this campaign.
- Verbal/offline opt-in described without enough detail to verify.

**The fix:**
- Rewrite `message_flow` to explain **who opts in, where, and how** - list **every** opt-in path.
- Website opt-in: provide the URL + a privacy-policy link + terms of service. Gated/paper opt-in: provide a hosted screenshot or document showing the exact opt-in language and form.
- Keyword opt-in: provide `opt_in_keywords` and an `opt_in_message` that includes the brand name, recurring-campaign confirmation, how to get help, and clear opt-out instructions.
- Update the **privacy policy** to state mobile numbers are **not shared with third parties/affiliates for marketing**, plus message frequency and the msg-&-data-rates disclosure.
- Make samples match the use case and name the brand; include opt-out language in at least one.
- Verbal opt-in: describe the exact script/flow in detail.
- Resubmit after updating.

> **Note:** 30896 (Opt-in) and 30909 (Message Flow / CTA incomplete) overlap heavily. Both are consent-verification failures. If you get one, audit for the other.

---

### 30897 - Disallowed Content

**What it means:** Your business model or content is in a **forbidden category** for US/Canada messaging. This is different from every other code on this page: **it is not a "fix the field" rejection.**

**Root causes (per Twilio):**
- High-risk financial services: loan marketing, stock alerts, cryptocurrency, other risky investment content.
- Third-party debt collection, debt reduction, credit repair, or third-party lead generation.
- Gambling, sweepstakes, or federally illegal substances.
- Anything else in Twilio's Forbidden Message Categories or that violates the Messaging Policy.

**The fix:**
- **Do NOT resubmit the same campaign.** Campaigns rejected for disallowed content are **ineligible for resubmission**.
- Review your use case, samples, and business model against the Forbidden Message Categories and Messaging Policy, then build a **different, compliant** campaign.
- If you genuinely believe the rejection was an error, contact Twilio Support - do not just retry.

> This is the one code where "edit and resubmit" is the wrong move. Map it correctly in any triage automation.

---

### 30909 - Message Flow or Call to Action incomplete/unverified

**What it means:** Your Message Flow (the CTA + consent narrative) doesn't give a reviewer enough verifiable evidence that users actually consented - especially for opt-ins that happen off a public website.

**Root causes (per Twilio):**
- Message Flow doesn't explain opt-in for **offline flows** (verbal, paper, in-store, QR, etc.).
- Not every opt-in method for the campaign is listed in `message_flow`.
- A website opt-in is missing required info: terms & conditions link, privacy policy, message frequency, or "message and data rates may apply."
- Opt-in evidence can't be verified - site is private, behind a login, incomplete, or has no publicly accessible screenshots of the consent flow.
- Keyword opt-in is incomplete: missing keyword details or the related `opt_in_message` / `opt_out_message` / `help_message` when you self-manage those flows.

**The fix:**
- Make the Message Flow **self-contained and verifiable**. Spell out exactly how consent is captured for every method.
- For QR / offline flows, point to a **publicly accessible** destination that carries the same disclosures a website opt-in needs.

  *Twilio's accepted example:* "End users scan a QR code displayed at Acme Sandwich Company locations, which opens www.acmesandwich.com/sms-signup in their mobile browser. On that page they enter their phone number and check a box agreeing to receive promotional messages. Message frequency varies. Message and data rates may apply. Terms: www.acmesandwich.com/terms. Privacy: www.acmesandwich.com/privacy." - passes because the QR destination is a public page with the required disclosures.
- For gated/paper flows, host public screenshots of the consent form.
- **Edit the rejected campaign rather than deleting and recreating it** - the vetting fee is assessed only once per campaign, so editing avoids a second fee.
  - **Console:** Messaging → Regulatory Compliance → Campaigns → click the failed campaign → **Edit Campaign** → correct fields → resubmit.
  - **API:** update the campaign resource with corrected field values.

---

## Brand-level vs campaign-level: how to tell them apart

| | Brand-level failures | Campaign-level rejections |
|---|---|---|
| **Codes** | `307xx`, `18xxx` (e.g. 30703, 30795, 18011) | `3088x`–`3091x` (e.g. 30886, 30896, 30909) |
| **What's wrong** | Your **business identity** - EIN, legal name, address, uniqueness | Your **messaging program** - description, opt-in, samples, content, flow |
| **Where to fix** | The **Business Profile / BrandRegistration** | The **Campaign** fields |
| **Authoritative source of truth** | IRS CP 575 / 147c letter, company register | Your real opt-in flow, website, and message content |
| **Key trap** | Legal name must match the EIN **exactly** (all CP 575 lines above the address); new EINs take 30–90 days to propagate | Disallowed-content (30897) cannot be resubmitted - everything else can |

**Most common brand failure (per Twilio):** a mismatch between the business info submitted in the Business Profile (exact legal name, exact address) and the same info as registered with the government tax authority. Standard/LVS US brands **must use an EIN** - a DUNS number is not acceptable for US Standard A2P brand registration, and an SSN is not an EIN.

**Remediation pattern for brand failures:** review your tax documentation, fix any discrepancy between it and the Business Profile, update the Business Profile, then resubmit the Brand. If the EIN is newly issued, wait for propagation. For urgent verification, send federal-level EIN documentation (CP 575 or 147c) to Twilio Support for a manual identity-status appeal (≈5–7 business days).

---

## Resubmission process & vetting fees

**The golden rule: edit and resubmit the *same* campaign - don't delete and recreate it.**

Per Twilio:
- Every new US A2P 10DLC **campaign registration is subject to manual vetting** and is charged a **campaign verification (vetting) fee at the time of external vetting**.
- The vetting **fee is assessed once per campaign.** Editing a rejected campaign and resubmitting it avoids a brand-new fee. Deleting and recreating it triggers a fresh fee.
- "If a Campaign is denied during external vetting, **additional charges might apply for resubmission**" (per Twilio) - so re-vetting can still cost. Get it right before you resubmit.
- A newly submitted campaign sits in **Pending** until manual vetting approves it. You can only send compliant A2P traffic **after full approval.** Due to volume, vetting can take **several weeks**.

**When to create a new campaign instead of editing** (per Twilio, from 30886 guidance): only when the **selected use case is wrong**, or the failure is tied to the **associated brand** rather than the campaign details. Otherwise, edit in place.

**Exception - 30897 (Disallowed Content):** do not resubmit at all. The campaign is ineligible; build a different compliant one or appeal via Support.

**Exception - 30898 (Excessive EIN):** fix the underlying **brand structure** first; don't resubmit the campaign until the EIN/brand duplication is resolved.

---

## General triage workflow

```
1. READ THE CODE
   Console: Messaging → Regulatory Compliance → Campaigns (or Brands)
   API:     fetch Usa2p / BrandRegistration resource → read `errors` field
            (for 30899, read campaign_status + errors for the underlying code)

2. CLASSIFY THE LAYER
   3088x–3091x → CAMPAIGN problem → fix campaign fields
   307xx / 18xxx → BRAND problem → fix Business Profile / BrandRegistration

3. MAP CODE → CAUSE → FIX
   Use the lookup tables above. For 30886 / 30891 / 30892 / 30896 / 30897 / 30909,
   read the expanded section - they have the most failure modes.

4. APPLY THE FIX
   - Edit the existing record (campaign or brand). Do NOT delete + recreate a campaign
     (avoids a second vetting fee).
   - Make description ↔ use case ↔ samples ↔ website ↔ message flow all CONSISTENT.
     Inconsistency is the root cause behind most rejections (30886, 30889, 30893, 30899).

5. SPECIAL CASES (don't just resubmit)
   - 30897 Disallowed Content → ineligible for resubmission. Build a different campaign
     or contact Support.
   - 30898 Excessive EIN → fix brand/EIN structure FIRST, then resubmit campaign.
   - 30795 / brand tax mismatch with a NEW EIN → wait 30–90 days for propagation, or
     send CP 575 / 147c to Support for a manual identity appeal.

6. RESUBMIT
   Campaign re-enters Pending → manual vetting (can take weeks). Send A2P traffic only
   after full approval.
```

**Consistency is the meta-fix.** Across almost every campaign code, the reviewer is checking that your **description, use case, sample messages, website, and message flow all tell the same story** and that **consent is verifiable**. Make those five agree and name your brand in the samples, and most of the `3088x` series resolves itself.
