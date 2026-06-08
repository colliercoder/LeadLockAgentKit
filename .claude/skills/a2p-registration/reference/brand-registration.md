> Source: https://www.twilio.com/docs/messaging/compliance/a2p-10dlc | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/collect-business-info | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/direct-standard-onboarding | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/direct-sole-proprietor-registration-overview | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/transition-sole-proprietor-to-standard-brand | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/troubleshooting-a2p-brands/troubleshooting-and-rectifying-a2p-standardlvs-brands | https://www.twilio.com/docs/messaging/api/brand-registration-resource | https://www.twilio.com/docs/messaging/api/brand-vetting-resource | https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US | https://help.twilio.com/articles/4403988619163-What-is-Secondary-Vetting-for-A2P-10DLC | https://www.twilio.com/en-us/changelog/a2p-registration-now-automatically-includes-secondary-vetting | https://www.twilio.com/en-us/changelog/increased-mms-rate-limits-for-a2p-10dlc-phone-numbers-in-the-u-s0 - scraped 2026-06-07

# A2P 10DLC Brand Registration & Business Identity

This is the comprehensive reference for the **Brand** half of A2P 10DLC registration: establishing your business identity in Twilio Trust Hub (Customer Profile), submitting that identity to The Campaign Registry (TCR) as a **Brand**, and understanding Brand types, the Trust Score, vetting, and registration failures.

A2P 10DLC has two halves. This doc covers the first; the **Campaign** is registered separately after the Brand is approved.

1. **Brand** - *who* is sending the messages (business identity, verified against tax records). ← this doc
2. **Campaign** - *what* messages are sent and *how* recipients opt in/out.

---

## How the pieces fit together

When you register, the business information you supply creates several linked objects:

| Object | What it is |
|---|---|
| **Primary Customer Profile** (Primary Profile) | Your foundational business identity with Twilio. Created first; stores core business information. Lives in **Twilio Trust Hub**. |
| **TrustProduct** (compliance container / Trust Bundle) | A compliance-specific container holding the A2P 10DLC verification data. The EndUser resources attached to it are populated with the same business information. |
| **BrandRegistration** (the "Brand") | The resource (SID prefix `BN`) representing your business as registered with TCR. Created from the Customer Profile + TrustProduct. After success it receives a TCR Brand ID (`tcr_id`). |

> The same business information serves both the Primary Profile (identity) and the TrustProduct (compliance). They have different roles, but you enter the data once.

**The critical thing to understand for fixing failures:** when a Brand fails, you do **not** edit the Brand directly. The data that needs correcting lives **upstream** in the Customer Profile / TrustProduct. You fix it there, then resubmit (Console) or call brand update (API).

---

## Customer Profile - required business identity fields

Below are the fields TCR requires for **Standard** and **Low-Volume Standard** Brands (i.e., any business that is *not* a Sole Proprietor). Parameter names (e.g. `business_name`) are the API field names; in the Console you enter the same information in form fields. Sole Proprietor requirements differ - see [Sole Proprietor section](#sole-proprietor-brands-no-ein-path).

### Business details

| Field | Required | Description / rules |
|---|---|---|
| `business_name` | Yes | **Exact legal business name** as registered with the EIN. See [exact-match rule](#the-exact-match-rule-1-cause-of-brand-failure). |
| `business_type` | Yes | Legal structure. Allowed: `Co-operative`, `Corporation`, `Limited Liability Corporation`, `Non-profit Corporation`, `Partnership`. **Government orgs must use `Non-profit Corporation`.** |
| `business_industry` | Yes | Closest-matching industry. Government → `GOVERNMENT`; non-profit → `NOT_FOR_PROFIT`. (Full list: AGRICULTURE, AUTOMOTIVE, BANKING, CONSTRUCTION, CONSUMER, EDUCATION, ELECTRONICS, ENGINEERING, ENERGY, FAST_MOVING_CONSUMER_GOODS, FINANCIAL, FINTECH, FOOD_AND_BEVERAGE, GOVERNMENT, HEALTHCARE, HOSPITALITY, INSURANCE, JEWELRY, LEGAL, MANUFACTURING, MEDIA, NOT_FOR_PROFIT, OIL_AND_GAS, ONLINE, PROFESSIONAL_SERVICES, RAW_MATERIALS, REAL_ESTATE, RELIGION, RETAIL, TECHNOLOGY, TELECOMMUNICATIONS, TRANSPORTATION, TRAVEL.) |
| `business_registration_identifier` | Yes | The *type* of tax ID. For US entities use `EIN`. **Do not use a DUNS number.** Other allowed: `DUNS` (US), `CBN` (Canada), `CN` (Great Britain), `ACN` (Australia), `CIN` (India), `VAT` (Estonia), `VATRN` (Romania), `RN` (Israel), `Other`. |
| `business_registration_number` | Yes | The actual tax ID number, formatted for the identifier. EIN format: `00-0000000`. For Canadian `CBN`, provide the first nine digits only. |
| `website_url` | Yes | Must be **functional** and bear a relationship to `business_name`. The URL is auto-verified: Twilio captures a screenshot and evaluates it against A2P compliance rules. This compliance check is **mandatory**. |
| `social_media_profile_urls` | Optional | URL(s) of business social accounts (LinkedIn, Facebook, X/Twitter). Helps verification. |
| `business_identity` | Yes | `direct_customer`, `isv_reseller_or_partner`, or `unknown`. If you are not an ISV, use `direct_customer`. |
| `business_regions_of_operation` | Yes | One or more of: `AFRICA`, `ASIA`, `EUROPE`, `LATIN_AMERICA`, `USA_AND_CANADA`. |
| `stock_exchange` | If public | Exchange where stock trades (e.g. `NASDAQ`, `NYSE`, `NONE`, `OTHER`, and many international codes). |
| `stock_ticker` | If public | Ticker symbol, e.g. `TWLO`. |
| `company_type` | Yes | `government`, `non-profit`, `private`, or `public`. |
| `brand_contact_email` | Yes (public, for-profit) | Email of a Brand representative who completes 2FA / Authentication+. See [Brand identity verification](#brand-identity-verification-2fa--authentication). **Must be a business domain** - personal/free addresses (gmail.com) and distribution addresses cause failure. |
| `skip_automatic_sec_vet` | Optional | Boolean, default `false`. Set `true` **only** to register as Low-Volume Standard, for 527 political orgs, or those holding a Campaign Verify token. See [Brand types](#brand-types). |

### Authorized representative (business contact)

The authorized representative is a real person at the business who attests to the registration.

| Field | Description |
|---|---|
| `first_name` | First name of the authorized representative. |
| `last_name` | Last name of the authorized representative. |
| `business_title` | Exact job title of the representative. |
| `job_position` | Position. Allowed: `Director`, `GM`, `VP`, `CEO`, `CFO`, `General Counsel`, `Other`. |
| `phone_number` | Representative's phone in E.164 format. |
| `email` | Representative's email. Must be well-formatted, valid domain, **not disposable**. Usable a **maximum of 10 times** across all TCR A2P registrations (registrations with other vendors count toward the limit). |

### Business mailing address

| Field | Description |
|---|---|
| `customer_name` | The name of the business (for the mailing address). |
| `street` | Number and street, e.g. `23 Main Street`. Usable a **maximum of 10 times** across all TCR A2P registrations (other vendors count). |
| `street_secondary` | Optional - suite/attention line. |
| `city` | City, e.g. `San Francisco`. |
| `region` | Two-letter state/province abbreviation, e.g. `CA`. |
| `postal_code` | ZIP/postal code, e.g. `90210`. |
| `iso_country` | ISO country code, e.g. `US`. |

---

## The exact-match rule (#1 cause of Brand failure)

> **The single most common reason a Standard / LVS Brand fails is a mismatch between the business information you submitted (exact legal business name, EIN, exact address) and that information as registered with the government tax authority.**

For US entities, `business_name` must be the **exact legal business name as registered with the EIN**, found on the **IRS CP 575 EIN Confirmation Letter**.

Rules:

- **Use the CP 575 (or 147c) name, not the W-2 or W-9 name** - those may differ from the CP 575.
- If you've lost the CP 575, request a **147c letter** from the IRS and use the information on it.
- If the business name spans multiple lines on the CP 575 / 147c, **input all lines above the address line.** (Example: on a letter showing "ACME INC" the business name is `ACME INC`.)
- An **exact match** between the legal company name and the EIN as displayed on the CP 575 is required for the Brand to register successfully. Punctuation, suffixes ("INC", "LLC"), and spacing all matter.

### If your EIN is new

Newly issued EINs (or equivalent tax IDs) can take **30–90 days** to propagate across the database validation systems Twilio and its ecosystem partners use. If your Brand failed on a tax-ID mismatch and you recently registered for the tax ID, **wait a few weeks and resubmit.** The same applies to newly registered 501(c)(3) / non-profit organizations.

### Urgent / appeal path (manual re-vetting)

If the submitted information **exactly matches** your tax registration but the Brand still fails (common with brand-new EINs or non-profits not yet in the databases), you can **appeal** to Twilio Support:

- Share the complete EIN documentation (**CP 575 notice or 147c letter**) with Twilio Support.
- Documentation must be at the **federal level, not state level.**
- This triggers a **manual identity-status appeal / re-vetting** by the ecosystem partner, which usually takes **5–7 business days.**
- The appeal-based manual re-vetting entails a **$10 fee**, over and above the normal Brand submission fees. (This is distinct from the free self-service resubmissions described below.)

---

## Brand registration with TCR - what is submitted and verified

When you click **Register**, Twilio submits your Secondary/Customer Profile and Brand to **The Campaign Registry (TCR)**.

**What is submitted:** the business identity (legal name, tax ID, address, website, industry, business type), the authorized representative, and the brand contact email.

**What TCR verifies:**

- The **legal business name matches the EIN / tax ID** in publicly available tax records (the exact-match check above).
- The **address** and other identity fields are consistent with registered records.
- The **website** passes the automated screenshot/compliance check.
- For public, for-profit brands, the **brand contact email domain** is verified via 2FA / Authentication+ (see below).

Based on this, TCR attempts to **verify the identity** of the brand and (for Standard Brands) assigns a **Trust Score**.

---

## Brand status and verification outcomes

The `BrandRegistration` resource has a `status`:

| `status` | Meaning |
|---|---|
| `PENDING` | Registration not yet complete. Most complete within minutes; a few take >7 days. |
| `IN_REVIEW` | Under manual third-party review (≥7 business days). No action needed from you. |
| `APPROVED` | Completed and verified. You can now register Campaigns. **May still carry feedback** (in `errors[]`) suggesting ways to raise the Trust Score. |
| `FAILED` | Information couldn't be verified. Review the `errors[]` fields. |
| `SUSPENDED` | Brand is deemed to have violated A2P ecosystem rules. Requires Twilio Support to resolve. |
| `DELETION_PENDING` / `DELETION_FAILED` | Brand deletion in progress / failed. |

### Identity status (`identity_status`)

Separately from `status`, TCR records how confidently it verified the business identity:

| `identity_status` | Meaning |
|---|---|
| `SELF_DECLARED` | Identity asserted by the registrant, not independently confirmed. |
| `UNVERIFIED` | TCR could not verify the identity (a failed/unverified state). |
| `VERIFIED` | Identity verified against records. |
| `VETTED_VERIFIED` | Identity verified **and** an external/secondary vetting score is on file - the strongest standing. |

### Feedback fields

- `errors[]` - the consolidated, actionable field. Populated **either** when the Brand is `APPROVED` but the Trust Score could be improved, **or** when the Brand `FAILED` (describing what to fix for resubmission).
- `brand_feedback` (*DEPRECATED*, now folded into `errors[]`) - a list of Feedback IDs, each a recommendation to improve the score. Possible IDs: `TAX_ID`, `STOCK_SYMBOL`, `NONPROFIT`, `GOVERNMENT_ENTITY`, `OTHERS`.
- `failure_reason` (*DEPRECATED*, now folded into `errors[]`) - why a `FAILED` Brand failed.
- `tcr_id` - the TCR Brand ID, assigned **only after successful registration**.
- `russell_3000`, `government_entity`, `tax_exempt_status` (`501c3`, etc.) - flags that affect throughput/limits.

---

## The Brand Trust Score

The **Trust Score** is a reputation score TCR assigns to **Standard Brands** during registration. It is the single biggest lever on your messaging throughput and daily limits.

| Property | Detail |
|---|---|
| **Range** | **0–100.** |
| **Who gets one** | **Standard Brands only.** **Low-Volume Standard** Brands do **not** get a Trust Score (they skip secondary vetting). **Sole Proprietor** Brands do **not** get a Trust Score (fixed throughput). |
| **How it's set** | A reputation algorithm reviews your company information; **secondary vetting** (Aegis) maximizes/confirms the score. The API field is `brand_score` - "the secondary vetting score if it was done; otherwise the brand score returned from TCR; may be `null` if no score is available." |
| **Why it matters** | The higher the score, the higher your **messages-per-second (MPS) throughput** and **daily message limits** to US carriers. |
| **How to raise it** | Provide **precise, current information that matches your tax-agency registration**; complete **secondary vetting**; resolve any `errors[]` / feedback IDs (e.g. supply stock symbol for public companies, confirm non-profit/government status). |
| **What lowers it** | Incomplete, inaccurate, or mismatched business information; missing vetting. |

### Trust Score → throughput tiers

Per the official Twilio changelog, for most registered campaign types (Declared and Mixed/Marketing), throughput scales with Trust Score:

| Trust Score | Throughput (per major carrier: AT&T, T-Mobile, Verizon) |
|---|---|
| **75 or above** | up to **40 MPS** |
| **50–74** | up to **20 MPS** |
| **below 50** | up to **5 MPS** |

Notes:
- [Special use cases](https://help.twilio.com/articles/4402972441243-Special-Use-Cases-for-A2P-10DLC) have their own fixed MPS allocations not affected by Trust Score.
- **Sole Proprietor** Brands have a fixed allocation of **0.5 MPS per number**, regardless of Trust Score or campaign type.
- Throughput is also gated by **T-Mobile daily message limits**, which scale with Brand type and vetting. Customers needing more than 200,000 daily messages to T-Mobile must submit a **T-Mobile Special Business Review (SBR)**.

> The numeric MPS tiers above come from Twilio's March 2026 MMS rate-limit changelog. Always confirm current SMS/MMS tiers against [Message throughput (MPS) and Trust Scores for A2P 10DLC in the US](https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US) before quoting hard numbers, as carrier allocations change.

---

## Brand types

Twilio offers three Brand types. Your choice depends on whether you have a tax ID and your expected volume.

### Decision rule

- **No business tax ID** (no US EIN, no Canadian Business Number), US/Canada only → **Sole Proprietor Brand.**
- **Have a tax ID**, lower volume / want to skip vetting → **Low-Volume Standard Brand.**
- **Have a tax ID**, higher volume → **Standard Brand.**

> A sole proprietorship that **does** have an EIN must register as **Low-Volume Standard or Standard** - **not** Sole Proprietor. Registering it as Sole Proprietor incurs fees and limits its ability to send.

### Comparison

| | **Sole Proprietor** | **Low-Volume Standard** | **Standard** |
|---|---|---|---|
| **Tax ID required?** | No (US/Canada, no EIN/CBN) | Yes | Yes |
| **Brand type value (API)** | `SOLE_PROPRIETOR` | `STANDARD` (with `skip_automatic_sec_vet = true`) | `STANDARD` |
| **Trust Score?** | No (fixed throughput) | No (skips secondary vetting) | **Yes (0–100)** |
| **Secondary vetting?** | No | No (skipped) | Yes (automatic, Aegis) |
| **Campaigns per Brand** | **1** | Up to **5** (more needs a valid business reason) | Up to **5** (more needs a valid business reason) |
| **Phone numbers** | **1 number per Campaign** | Multiple numbers per Campaign | Multiple numbers per Campaign |
| **Throughput** | Fixed, **0.5 MPS per number** | Lower / fixed (lowest tier; lower than Standard) | Scales with Trust Score (5 / 20 / 40 MPS tiers) |
| **Daily volume to T-Mobile** | ~1,000 SMS segments + MMS/day (≈3,000/day across US carriers) | Up to ~2,000 SMS segments + MMS/day (≈6,000/day across carriers); Russell 3000 companies up to 200,000/day to T-Mobile | From 2,000 up to **unlimited** to T-Mobile, depending on Trust Score |
| **Best for** | Students, hobbyists, individuals, first-time testers without a registered business | Small businesses with a tax ID and modest, mixed messaging | Businesses needing higher throughput and volume |

### Per-tax-ID Brand limits

Each tax ID may register **up to five** Standard / Low-Volume Standard Brands. Beyond that, additional Brands may register successfully but their **Campaigns may be rejected** during manual vetting unless a clear, valid business reason is presented.

### Low-Volume Standard vs Standard

Both require a tax ID and both allow up to five Campaigns and multiple numbers per Campaign. The difference:

- **Standard** goes through **secondary vetting** and gets a **Trust Score**, unlocking the higher throughput tiers (up to unlimited daily to T-Mobile depending on score).
- **Low-Volume Standard** sets `skip_automatic_sec_vet = true`, **skips secondary vetting**, gets **no Trust Score**, and is fixed at the lowest throughput tier with a lower monthly fee. Good when you want a real (tax-ID-backed) Brand without paying for vetting or needing high volume.

---

## Secondary / external Brand vetting

**Secondary vetting** is an additional, independent review of your Brand by a third-party vetting partner that confirms the accuracy of your business information and **maximizes your Trust Score**, unlocking higher throughput and higher T-Mobile daily limits.

| Aspect | Detail |
|---|---|
| **Provider** | **Aegis** (in the API, `vetting_provider = aegis`, `vetting_class = STANDARD`). A separate provider, **Campaign Verify** (`vetting_provider = campaign-verify`, `vetting_class = POLITICAL`), handles political-organization tokens. |
| **Automatic?** | Yes - since 2021, **all Standard Brand registrations automatically include secondary vetting.** No special action is needed; it triggers for all standard brands registering for US A2P. |
| **Cost** | A **one-time vetting fee** (introduced as **$40**; current pricing is on the order of **~$41.50**, on top of the base Brand registration fee). Confirm current fees on the [A2P 10DLC pricing page](https://help.twilio.com/articles/1260803965530-What-pricing-and-fees-are-associated-with-the-A2P-10DLC-service). |
| **Timeline** | Typically **no additional approval time**; if a score can't be retrieved at registration, the review can take **up to 7 business days** (`IN_REVIEW`). |
| **Benefits** | Higher T-Mobile daily message limits; maximized throughput per Campaign via a maximized TCR/Trust Score; `identity_status` of `VETTED_VERIFIED`. |
| **When to skip** | Low-Volume Standard registrations, 527 political organizations, and Campaign Verify token holders set `skip_automatic_sec_vet = true`. |

### External vetting via the Vettings API

You can submit a third-party vetting record to a Brand via the **Vettings subresource** (`POST /v1/a2p/BrandRegistrations/{BrandSid}/Vettings`):

| Field | Detail |
|---|---|
| `vetting_provider` | `aegis` (Secondary Vetting) or `campaign-verify` (Campaign Verify political tokens). |
| `vetting_class` | `STANDARD` (Aegis) or `POLITICAL` (Campaign Verify). |
| `vetting_id` | The unique vetting ID from the third-party provider (e.g. a Campaign Verify token). |
| `vetting_status` | `PENDING`, `SUCCESS` / `IN_PROGRESS`, or `FAILED`. |
| `brand_vetting_sid` | Twilio SID of the vetting record (prefix `VT`). |

> Note: the Vettings API is primarily for **government/non-profit and political** flows (importing a Campaign Verify token) - do not call it ad hoc without following the relevant onboarding guide, or you may incur delays and unintended fees. For ordinary commercial Standard Brands, secondary vetting is automatic.

**When external vetting is worth it:** for ordinary Standard Brands it's automatic and bundled - there's no separate decision. It's worth proactively engaging when you need to **raise a low Trust Score** to reach a higher throughput tier, or when a political/non-profit org needs the specialized vetting path.

---

## EIN vs Sole Proprietor (no-EIN) path

The fork in the road is the **business tax ID**:

- **You have a US EIN or Canadian Business Number** → register as **Standard** or **Low-Volume Standard**. (A sole proprietorship *with* an EIN must take this path - not the Sole Proprietor path.)
- **You have no tax ID**, and you're in the **US or Canada** → register as **Sole Proprietor**.
- **You're outside the US/Canada** → you must register as **Standard or Low-Volume Standard** (Sole Proprietor is US/Canada-only).
- **OTP / 2FA only?** Consider **Twilio Verify** instead - it avoids A2P Brand and Campaign registration entirely.

---

## Sole Proprietor Brands (no-EIN path)

For US/Canada registrants without a business tax ID (students, hobbyists, individuals, first-time testers).

### Required information

The Sole Proprietor profile collects a reduced set of fields:

| Field | Notes |
|---|---|
| `brand_name` | The business name - usually the proprietor's **first and last name**, or a DBA. For hobbyists/students, use their first and last name. |
| `first_name` / `last_name` | **The sole proprietor's own** name (the proprietor *is* the authorized representative). |
| `email` | The sole proprietor's email. Usable a **maximum of 10 times** across all TCR A2P registrations. |
| `mobile_phone_number` | Receives the **OTP** verification (see below). |
| `customer_name`, `street`, `street_secondary`, `city`, `region`, `postal_code`, `iso_country` | Business mailing address. The street address is usable a **maximum of 10 times** across all TCR registrations. |
| `vertical` | Optional industry (different allowed list from Standard: AGRICULTURE, COMMUNICATION, ENERGY, ENTERTAINMENT, FINANCIAL, GAMBLING, GOVERNMENT, HEALTHCARE, HOSPITALITY, HUMAN_RESOURCES, INSURANCE, LEGAL, MANUFACTURING, NGO, POLITICAL, POSTAL, PROFESSIONAL, REAL_ESTATE, RETAIL, TECHNOLOGY, TRANSPORTATION). |

### OTP mobile-number verification

Sole Proprietor registration uses a **one-time passcode (OTP)** sent by SMS to the supplied mobile number, which the proprietor must respond to before the Brand is fully approved.

- Must be a **valid US or Canadian mobile** device.
- **Cannot** be acquired from a CPaaS provider such as Twilio.
- Usable **no more than three times** across all Sole Proprietor Brand registrations with TCR (registrations with other vendors using the same number count toward this limit).
- The same number may serve both the Profile phone field and the Mobile OTP field if it meets all requirements.

### Sole Proprietor constraints

- **Brand type** is fixed to `Sole Proprietor` (the only permitted value).
- **One Campaign per Brand**; the Campaign use case must be `SOLE_PROPRIETOR`.
- **One 10DLC phone number per Campaign.**
- **Fixed throughput: 0.5 MPS per number; ~1,000 SMS segments + MMS/day to T-Mobile** (≈3,000/day across US carriers).
- **No Trust Score** and **no secondary vetting.**
- You agree to a **one-time Brand registration fee** before submitting. Approval typically occurs within a few minutes.

---

## Brand identity verification (2FA / Authentication+)

Since **October 17, 2024**, public, for-profit Brands require **Brand identity verification** (Authentication+ 2FA) for new and existing Brand registrations when creating new Campaigns. TCR uses this to validate the identity and domain ownership of the brand submitter.

- You must supply a **`brand_contact_email`** - the email of a Brand representative who completes the 2FA.
- The email **domain must be tied to the brand** (listed on the official website, matching WHOIS / DNS TXT). **Free / consumer domains (gmail.com) and distribution addresses fail.**
- In the Console, add the Brand Contact Email during registration (or to an existing Brand) and complete 2FA before creating new Campaigns. Via API, set `brand_contact_email` in the `us_a2p_messaging_profile_information` bundle.

### 2FA / Authentication+ failure codes

| Error | Message | Fix |
|---|---|---|
| `21736` | Domain Ownership Could Not Be Verified | Use an email domain clearly tied to your brand (on the website, matching WHOIS / DNS TXT). |
| `21737` | 2FA Verification Expired | Submit a new 2FA request and complete it within the window. |
| `21738` | 2FA Email Undeliverable | Ensure the email is correct, active, and can receive external mail; update if needed. |
| `21739` | 2FA Verification Failed or Timed Out | Re-initiate and have the contact complete promptly. |
| `21740` | Invalid Brand Contact Email Domain | Use a business/organizational domain - not a free provider. |
| `21741` | 2FA Code Expired | Re-initiate and complete in time. |

You can **resend the 2FA email** from the Console: **Messaging → Regulatory Compliance → Brands → select brand → resend verification email.**

---

## Common Brand registration failures and how to fix them

| Failure | Root cause | Fix |
|---|---|---|
| **Name / EIN mismatch** (most common) | `business_name` doesn't exactly match the legal name on the CP 575 for that EIN. | Pull the **CP 575 / 147c**, correct the legal name (include all name lines above the address line, exact punctuation/suffixes), update the **Customer Profile**, resubmit. |
| **Address mismatch** | Submitted address differs from registered records. | Correct the address in the Customer Profile to match tax-registration records, resubmit. |
| **New EIN not yet in databases** | A brand-new EIN (or 501(c)(3)) hasn't propagated (30–90 days). | Wait a few weeks and resubmit. If urgent, **appeal** with CP 575 / 147c to Twilio Support (federal docs only) - manual re-vetting, 5–7 business days, **$10 fee**. |
| **Website fails verification** | `website_url` is non-functional, unrelated to the business, or fails the compliance screenshot check. | Provide a live business website tied to the legal name; ensure it meets A2P compliance content rules. |
| **Bad brand contact email** | Free/personal/distribution email, or domain ownership can't be verified. | Use a **business-domain** email tied to the brand; complete 2FA (see error codes above). |
| **Wrong Brand type for a sole prop with EIN** | Registered as Sole Proprietor despite having an EIN. | Register as **Standard / Low-Volume Standard** instead (see [transition](#transitioning-sole-proprietor--standard)). |
| **SUSPENDED** | Ecosystem partners flagged a violation (traffic/campaign mismatch, spam, phishing, prohibited content, excessive complaints, etc.). | Requires **Twilio Support**. Do **not** spin up another Brand/Campaign to route the same traffic - that risks account termination. |

### Resubmitting a failed Brand

- Twilio supports **up to three free self-service resubmissions** of a Brand in the `unverified` / `FAILED` state, via Console or the Trust Hub API. After three, contact Twilio Support. (A 4th API attempt returns HTTP 400 with error `21724`.)
- **The data you fix lives in the Customer Profile / Trust Bundle, not the Brand itself.**
  - **Console:** click "Edit customer profile" on the error, correct and resubmit the **Profile**, then go to **Messaging → Regulatory Compliance → Brands**, **delete** the failed Brand, return to **Onboarding**, switch to the corrected Profile, and submit a new Brand.
  - **API:** update the upstream Customer Profile / EndUser resources via the [Trust Hub API](https://www.twilio.com/docs/trust-hub/trusthub-rest-api), then call `update()` on the existing `brand_registrations` resource (only the Brand SID is needed - all the corrected data is upstream). Newly updated info often requires **manual re-verification**, so allow time.
- The three free resubmissions are **distinct** from the appeal-based manual re-vetting (the **$10** path for new-EIN/non-profit cases that match but still fail).

---

## Transitioning Sole Proprietor → Standard

If you outgrow a Sole Proprietor Brand (more volume, more numbers, more campaigns) or obtain an EIN, you transition to a Standard (or Low-Volume Standard) Brand:

1. Create a **(Secondary) Customer Profile** with the full Standard business identity, submit it for review.
2. Submit a new **Standard** or **Low-Volume Standard** Brand, specifying the customer organization type (e.g. private), and agree to the registration fee.
3. On **Register**, Twilio submits the Secondary Profile + Brand to TCR. Once registered, the Standard Brand gets a **Trust Score** (Low-Volume Standard does not, as it skips secondary vetting).
4. Move your numbers and create new Campaigns under the new Brand.

Direct customers use the [Direct Standard / Low-Volume Standard guide](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/direct-standard-onboarding); ISVs use the [ISV API onboarding guide](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/onboarding-isv-api).

---

## Quick reference: which path am I on?

```
Do you have a business tax ID (US EIN / Canadian Business Number)?
├─ NO  → US/Canada?  ── YES → SOLE PROPRIETOR  (OTP verify, 1 campaign, 1 number, 0.5 MPS, no Trust Score)
│                     └─ NO  → must use STANDARD / LOW-VOLUME STANDARD
└─ YES → High volume / need throughput?
         ├─ YES → STANDARD            (auto secondary vetting → Trust Score 0–100 → 5/20/40 MPS tiers)
         └─ NO  → LOW-VOLUME STANDARD (skip secondary vetting, no Trust Score, lowest tier, lower fee)
```

Only sending OTP / 2FA? Consider **Twilio Verify** and skip A2P registration entirely.
