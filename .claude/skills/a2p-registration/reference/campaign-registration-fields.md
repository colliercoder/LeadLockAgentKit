> Source: https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/collect-business-info • https://www.twilio.com/docs/messaging/api/usapptoperson-resource • https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/quickstart • https://www.twilio.com/docs/trust-hub/registrations/a2p-10dlc-campaign • https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/direct-standard-onboarding • https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/troubleshooting-a2p-brands/troubleshooting-and-rectifying-a2p-campaigns • https://help.twilio.com/articles/11847054539547 (A2P 10DLC Campaign Approval Requirements) • https://help.twilio.com/articles/26149060902555 (Campaign Registration Recommendations) • Campaign vetting error pages: 30886, 30892, 30895, 30909, 30933, 30934 - scraped 2026-06-07

# A2P 10DLC Campaign Registration: Fields & Requirements

This is the field-by-field reference for everything Twilio and The Campaign Registry (TCR) ask when you register an A2P 10DLC **campaign** (the messaging use case attached to an already-approved Brand). It covers what each field means, its rules, its character limits, when it becomes required, and the most common reasons campaigns get rejected during vetting.

A **campaign** represents a single messaging use case (e.g., marketing promotions, order confirmations, 2FA). It is created against an approved Brand and, in the API, is the `UsAppToPerson` (a.k.a. `Usa2p`, SID prefix `QE...`) resource on a Messaging Service. Once approved, the campaign is what authorizes your phone numbers (attached to that Messaging Service) to send A2P traffic to US carriers.

> **Critical compliance framing:** Every free-text field on a campaign is read by human and automated reviewers at TCR and the carriers. These fields are a **compliance document**, not a marketing pitch. Write them to prove how you obtain consent and what you send - not to sell the reviewer on your product. Vague, promotional, or mismatched descriptions are the #1 cause of rejection.

---

## Field Overview

Two surfaces register the same underlying campaign:

- **Console (self-serve / manual flow):** form fields labeled Campaign description, Sample messages, Message contents (checkboxes), Opt-in process, etc.
- **API (`UsAppToPerson` resource):** parameters `Description`, `MessageSamples`, `MessageFlow`, `UsAppToPersonUsecase`, `HasEmbeddedLinks`, etc.

The table below maps the Console concept to the API parameter, whether it is required, and its limits. Detailed rules for each follow in the sections below.

| Console field | API parameter | Required? | Character limits |
|---|---|---|---|
| Use case | `UsAppToPersonUsecase` | Yes | enum value (e.g. `MARKETING`, `2FA`) |
| Campaign description | `Description` | Yes | 40 min / 4096 max |
| Sample messages | `MessageSamples` (array) | Yes | 2–5 messages; each 20 min / 1024 max |
| Opt-in process / Message Flow / Call-to-Action | `MessageFlow` | Yes | 40 min / 2048 max |
| Embedded links checkbox | `HasEmbeddedLinks` | Yes (boolean) | true/false |
| Embedded phone numbers checkbox | `HasEmbeddedPhone` | Yes (boolean) | true/false |
| Age-gated content checkbox | `AgeGated` | Optional (boolean) | true/false |
| Direct lending / loan arrangement checkbox | `DirectLending` | Optional (boolean) | true/false |
| Subscriber opt-in checkbox | `SubscriberOptIn` | Optional (boolean) | true/false |
| Opt-in keywords | `OptInKeywords` (array) | Conditional | 255 max; alphanumeric |
| Opt-in confirmation message | `OptInMessage` | Conditional | 20 min / 320 max |
| Opt-out keywords | `OptOutKeywords` (array) | Conditional | 255 max; alphanumeric |
| Opt-out confirmation message | `OptOutMessage` | Conditional | 20 min / 320 max |
| Help keywords | `HelpKeywords` (array) | Conditional | 255 max; alphanumeric |
| Help response message | `HelpMessage` | Conditional | 20 min / 320 max |
| Privacy Policy URL | `PrivacyPolicyUrl` | Yes (as of 2026-06-30) | valid HTTPS URL |
| Terms & Conditions URL | `TermsAndConditionsUrl` | Yes (as of 2026-06-30) | valid HTTPS URL |

> **Note on limits:** Twilio's `MessageFlow` is documented as "40 character minimum, 2048 character maximum" in the API reference. The Console-side business-info guide states the same field "must be between 40 and 2049 characters." Treat 2048 as the safe maximum.

---

## Campaign Use Case Selection (`UsAppToPersonUsecase`)

**Required.** A campaign maps to exactly one use case, which describes the *type* of messages you send (marketing promotions, order confirmations, OTP/2FA, account notifications, etc.). The use case drives the per-campaign carrier fees and throughput, and it must be internally consistent with the campaign description and sample messages.

| Rule | Detail |
|---|---|
| One use case per campaign | A campaign is a single messaging use case. Mixed traffic needs a use case that explicitly permits it (e.g., a "Mixed" use case) or separate campaigns. |
| Must match description + samples | The selected use case has to align with your `Description` and `MessageSamples`. A mismatch (e.g., MARKETING use case but transactional-only samples, or vice versa) is a documented rejection cause (error 30886). |
| Some use cases require carrier review | Use cases flagged **"Requires Carrier Review"** need additional approval from carriers before they can send. Plan for extra lead time. |
| Sole Proprietor brands | If the Brand is a Sole Proprietorship, the use case value must be `SOLE_PROPRIETOR`. |
| Special-category use cases | Categories like sweepstakes (`SWEEPSTAKE`), charity, political, and others have their own eligibility and content rules. |

API examples of use case values include `2FA`, `EMERGENCY`, and `MARKETING`. The authoritative, current list of use case types and their fees is maintained at Twilio's "List of campaign use case types for A2P 10DLC registration" (help center article 1260801844470). Select the use case that most accurately reflects your traffic; do not pick a lower-fee use case if your actual content doesn't fit it.

---

## Campaign Description (`Description`)

**Required. 40 character minimum, 4096 character maximum.**

A clear, factual summary of what the SMS campaign does. This is a compliance document, not ad copy.

**It must answer all three of these:**

1. **Who is sending** the messages (the actual business / Brand name - not your platform or ISV name).
2. **Who receives** the messages (the recipients / audience).
3. **Why** the messages are being sent (the purpose of the messaging program).

**Rules and rejection causes (error 30886 - Invalid Campaign Description):**

| Requirement | Why it fails if missing |
|---|---|
| Be specific and complete | Vague or incomplete descriptions are rejected. |
| Name the sender, recipients, and purpose | Omitting any of the three causes rejection. |
| Align with the selected use case | A description that doesn't match the use case is rejected. |
| Match sample messages, Brand name, and website | The description must be consistent with the other registration fields and the registered brand details. |
| Identify the **actual business**, not your platform | If you're an ISV registering on behalf of customers, the description must describe the end business sending the messages - not your ISV/platform. |
| Use a general summary, not personal data | Do not put personally identifiable information in the description; describe the program generally. |
| Compliance tone, not marketing | Describe the messaging program; do not write a promotional pitch. |

**Good pattern:** "[Business name] sends [order confirmations / appointment reminders / promotional offers] to [customers who have purchased / leads who requested a quote]. Customers opt in by [method]. Messages include [examples]." Make every sentence verifiable against the brand website and sample messages.

---

## Sample Messages (`MessageSamples`)

**Required. Minimum 2, maximum 5 messages. Each message 20 character minimum, 1024 character maximum.**

Sample messages are representative examples of the actual messages this campaign will send. Reviewers compare them directly against the use case and description.

**Rules:**

| Requirement | Detail |
|---|---|
| 2–5 samples | At least two are required; up to five accepted. In the Console edit modal you may see five boxes, but only the first two are required. |
| Align with use case + description | Samples must clearly match the selected `UsAppToPersonUsecase` and the campaign `Description`. |
| Identify the Brand in each | The Brand must be identified by name and/or website **in each message**. At least one sample must include the business name. |
| Bracketed variables | Use square brackets `[]` to indicate templated/variable content (e.g., `[name]`, `[date]`, `[order #]`). |
| Include real links if you send links | If the campaign's messages will contain URLs, include them in the samples so they can be verified (and set `HasEmbeddedLinks=true`). |
| Include real phone numbers if you send them | If messages contain phone numbers, include them in the samples (and set `HasEmbeddedPhone=true`). |
| Show opt-out language | Where appropriate, include the opt-out instruction (e.g., "Reply STOP to opt out") so reviewers can see compliant messaging. |
| Mix sample types for mixed traffic | In the self-serve flow, Sample #1 is typically used for Promotional/Marketing content and Sample #2 for Transactional/Informational. For mixed messaging, include one of each type. |

**URL rules in samples (error 30892 - Public URL Shorteners):**

- **No public/shared URL shorteners.** Links such as `bit.ly`, `TinyURL`, and similar free shared shorteners cause rejection.
- Use a **direct, full business URL** or a **dedicated branded short domain that belongs to your business**.
- If you need short links, configure link shortening with your own branded domain through Twilio Messaging Services - do not use a free public shortener.
- Every URL in a sample must be **secure (HTTPS) and publicly accessible** so reviewers can open it.

**Example sample message (from Twilio docs):**

> `This is a message from the Acme Sandwich Company. Your order for [sandwich type, other item] will be delivered by [time] on [date]. If you have questions or would like to change your order schedule, call 333-444-1212. If you would like to opt out of future notifications like this, text STOP in reply to this message.`

This sample is compliant because it: names the brand, uses `[]` for variables, includes a real phone number, and shows opt-out language.

---

## Message Flow / Call-to-Action / Opt-In Process (`MessageFlow`)

**Required. 40 character minimum, 2048 character maximum.** (Console business-info guide states 40–2049; use 2048 as the safe ceiling.)

This is the single most scrutinized field. It must describe **how end users opt in (consent)** to receive the campaign's messages - the "call to action." If there are multiple opt-in paths, **every** path must be described.

**What the field must contain (errors 30909, 30917, 30924, 30925):**

| Element | Requirement |
|---|---|
| Every opt-in path | List and fully describe **all** methods by which users can opt in (website form, text-to-join keyword, point of sale, paper form, verbal/IVR, etc.). |
| The consent action | Describe the explicit action the user takes to consent (e.g., checks a box, submits a form, texts a keyword). |
| Active, unchecked consent | The opt-in must be **unchecked by default** - active consent is required. A pre-checked box is non-compliant (error 30925). |
| Compliant consent language | The opt-in flow must include compliant consent agreement language (error 30924 if missing or non-compliant). |
| Message frequency disclosure | State that message frequency varies (or the expected frequency). |
| "Message and data rates may apply" | Include this disclosure. |
| Link to the opt-in website | If opt-in occurs on a website, provide the **direct link** to the page where opt-in happens. The site must be publicly accessible (not behind login) and must describe the business/use case. |
| Link to Privacy Policy and Terms | Reference the Privacy Policy and Terms & Conditions (the website used for opt-in must have both). |
| Hosted screenshots if not public | If the opt-in mechanism (or any required info) is **not** publicly accessible at the business URL - e.g., it's behind a login or on a paper form - provide a URL hosting **screenshots/images** of the relevant opt-in pages. |

**Website opt-in checklist** - when the opt-in happens on a website you must:
- Provide a link to the website.
- Ensure the website has both a privacy policy and terms of service.
- Provide a link to the privacy policy.
- The privacy policy must include: a statement that mobile numbers are **not shared** (non-sharing for mobile numbers), the **message frequency**, and a **"message and data rates may apply"** disclosure.

**Acceptable `MessageFlow` example (from Twilio error 30909 guidance):**

> `End users opt in by visiting www.acmesandwich.com/sms-signup and entering their phone number. They check a box agreeing to receive recurring promotional text messages from Acme Sandwich Company. Message frequency varies. Message and data rates may apply. Terms and Conditions: www.acmesandwich.com/terms. Privacy Policy: www.acmesandwich.com/privacy (states mobile numbers are not shared with third parties).`

It passes because it names the URL, describes the consent action, discloses frequency and rates, and links to both required legal pages.

**Multiple-method example (from Twilio docs):**

> `End users opt-in by visiting www.example.com and adding their phone number. They then check a box agreeing to receive text messages from Acme, Inc. Additionally, end users can also opt-in by texting START to (111) 555-3333 to opt in. Terms and Conditions at www.example.com/tc. Privacy Policy at www.example.com/privacy`

**Related rejection codes:** 30896 (opt-in error), 30907 (website URL validation issue), 30908 (compliant privacy policy required), 30919 (website lacks sufficient business/use-case info), 30921 (website requires authentication and cannot be reviewed).

---

## Message Content Attributes (Checkboxes / Booleans)

In the Console these appear as "Message contents" checkboxes; in the API they are booleans. They tell carriers what kinds of content your messages contain. Mismatches between these flags and your actual samples/description cause rejection.

| Attribute | API parameter | Required? | Rule |
|---|---|---|---|
| Embedded links | `HasEmbeddedLinks` | Yes (boolean) | Set `true` if any message contains a URL. When `true`, include example links in `MessageSamples` so they can be verified. Don't claim `false` while a sample contains a link. |
| Embedded phone numbers | `HasEmbeddedPhone` | Yes (boolean) | Set `true` if any message contains a phone number. When `true`, include the phone number(s) in `MessageSamples` for verification. |
| Age-gated content | `AgeGated` | Optional (boolean) | Set `true` if the content is age-gated (e.g., alcohol, gambling, or other age-restricted material). Age-gated campaigns must enforce age verification at opt-in. |
| Direct lending / loan arrangement | `DirectLending` | Optional (boolean) | Set `true` if the business engages in direct, first-party lending or loan arrangement. **Must be disclosed even for OTP/2FA** campaigns of a lending business. Failing to flag it when the brand/description/samples indicate lending causes rejection (error 30895). |
| Subscriber opt-in | `SubscriberOptIn` | Optional (boolean) | Indicates whether the campaign uses subscriber opt-in. |

> **Affiliate marketing:** Twilio's campaign-vetting guidance treats affiliate-marketing / third-party "lead generation and marketing" content as high-risk and frequently disallowed for A2P 10DLC. There is no dedicated boolean for it the way there is for direct lending; instead, the use case, description, and samples must not present prohibited affiliate/third-party promotional content. If your messaging shares or monetizes consumer data with third parties, or markets on behalf of unrelated third parties, expect carrier rejection. Keep consent first-party and disclose data handling in the privacy policy. (Always verify against the current Twilio Messaging Policy and prohibited-message rules before registering affiliate-style traffic.)

---

## Opt-In Keywords & Confirmation Message

These configure the **text-to-join** flow. They become **required when end users can text a keyword to a campaign number to subscribe**.

### Opt-In Keywords (`OptInKeywords`)

| Rule | Detail |
|---|---|
| Format | Comma-delimited list (Console) / array of strings (API). |
| Characters | All characters must be **alphanumeric**. |
| Length | **255 character maximum** total. |
| When required | Required if end users can text a keyword to the campaign phone number to subscribe. |
| Example | `START` |

### Opt-In Confirmation Message (`OptInMessage`)

| Rule | Detail |
|---|---|
| Length | **20 character minimum, 320 character maximum.** |
| When required | Required if end users can text in a keyword to start receiving messages. |
| Must include | (1) the **Brand name**; (2) confirmation of **opt-in enrollment to a recurring message campaign**; (3) **how to get help**; (4) a **clear description of how to opt out**. |

---

## Opt-Out Keywords & Confirmation Message

These handle **unsubscribe**. They become required when you manage opt-out yourself instead of using Twilio's Default or Advanced Opt-Out features.

### Opt-Out Keywords (`OptOutKeywords`)

| Rule | Detail |
|---|---|
| Format | Comma-delimited list (Console) / array of strings (API). |
| Characters | All characters must be **alphanumeric**. |
| Length | **255 character maximum** total. |
| When required | Required if you manage opt-out keywords yourself (not using Twilio's Default or Advanced Opt-Out). |
| Example | `STOP` |

### Opt-Out Confirmation Message (`OptOutMessage`)

| Rule | Detail |
|---|---|
| Length | **20 character minimum, 320 character maximum.** |
| When required | Required if the business manages opt-out messages itself. |
| Must include | (1) **acknowledgment of the opt-out request**; (2) **confirmation that no further messages will be sent**. The **Brand name** is recommended but not strictly required. |

---

## Help Keywords & Response Message

### Help Keywords (`HelpKeywords`)

| Rule | Detail |
|---|---|
| Format | Comma-delimited list (Console) / array of strings (API). |
| Characters | All characters must be **alphanumeric**. |
| Length | **255 character maximum** total. |
| When required | Required if you manage help keywords yourself (not using Twilio's Default or Advanced Opt-Out). |
| Example | `HELP` |

### Help Response Message (`HelpMessage`)

| Rule | Detail |
|---|---|
| Length | **20 character minimum, 320 character maximum.** |
| When required | Required if the business manages help messages itself. |
| Should include | The **Brand name** and additional **support options and/or contact information** (phone number, email, or support URL). |
| Example | `Acme Corporation: Please visit www.example.com to get support. To opt-out, reply STOP.` |

---

## Privacy Policy URL (`PrivacyPolicyUrl`)

**Required as of June 30, 2026.** Campaign registrations submitted without it return a hard `400` (rejection error **30933**).

| Rule | Detail |
|---|---|
| Must be present | Include `PrivacyPolicyUrl` in every campaign creation request. |
| Must be a valid HTTPS URL | Use `https://`. |
| Must be publicly accessible | Reachable **without authentication** - reviewers must be able to open it. |
| Must point to a real privacy policy | The page must contain an actual privacy policy relevant to the business. |
| ISVs | If registering on behalf of customers, collect each customer's privacy policy URL during onboarding before submitting. |

**Privacy policy content requirements** (from the opt-in/`MessageFlow` rules and error 30908): the privacy policy must include a statement that **mobile numbers are not shared** with third parties (non-sharing statement), the **message frequency**, and a **"message and data rates may apply"** disclosure.

---

## Terms & Conditions URL (`TermsAndConditionsUrl`)

**Required as of June 30, 2026.** Campaign registrations submitted without it return a hard `400` (rejection error **30934**).

| Rule | Detail |
|---|---|
| Must be present | Include `TermsAndConditionsUrl` in every campaign creation request. |
| Must be a valid HTTPS URL | Use `https://`. |
| Must be publicly accessible | Reachable without authentication. |
| Must point to real terms of service | The page must contain the business's actual terms and conditions covering the messaging program. |
| Consistency | The Terms & Conditions and Privacy Policy should be referenced/linked in the `MessageFlow` opt-in description as well. |

> The website used for opt-in must have **both** a privacy policy and terms of service. The 2026-06-30 change formalizes both as explicit, separately-required campaign fields rather than relying on them being mentioned only inside `MessageFlow`.

---

## CTIA-Required Keyword Handling (STOP / HELP / START)

Independent of what you register, US carriers and the CTIA require that **STOP**, **HELP** (and resubscribe keywords like **START/UNSTOP**) work on every campaign. Twilio supports this two ways:

| Option | What it does |
|---|---|
| **Twilio Default Opt-Out** | Twilio automatically handles the standard opt-out keywords (STOP and variants), HELP, and resubscribe keywords with default responses. With this enabled, you generally do **not** need to supply your own `OptOutKeywords`/`OptOutMessage`/`HelpKeywords`/`HelpMessage`. |
| **Advanced Opt-Out (Messaging Service)** | Lets you customize the keyword lists and the auto-reply text for opt-out, opt-in, and help at the Messaging Service level. |
| **Self-managed** | If you turn off Twilio's defaults and manage keywords yourself, the keyword fields and their response messages **become required** on the campaign, and the responses must meet the content rules in the sections above. |

**Rule of thumb:**
- If you use Twilio's **Default or Advanced Opt-Out**, the opt-out/help keyword and message fields are optional on the campaign (Twilio fulfills the CTIA obligation for you).
- If you **manage opt-out/help yourself**, you **must** provide `OptOutKeywords`, `OptOutMessage`, `HelpKeywords`, and `HelpMessage`, each meeting its content and length rules.
- Opt-in keyword/message fields are required whenever a **text-to-join** keyword exists for the campaign, regardless of opt-out configuration.

---

## Character-Limit Quick Reference

| Field | API parameter | Min | Max |
|---|---|---|---|
| Campaign description | `Description` | 40 | 4096 |
| Each sample message | `MessageSamples[]` | 20 | 1024 |
| Number of sample messages | `MessageSamples` | 2 | 5 |
| Message flow / opt-in | `MessageFlow` | 40 | 2048 (Console guide: 2049) |
| Opt-in keywords (total) | `OptInKeywords` | - | 255 (alphanumeric) |
| Opt-in confirmation message | `OptInMessage` | 20 | 320 |
| Opt-out keywords (total) | `OptOutKeywords` | - | 255 (alphanumeric) |
| Opt-out confirmation message | `OptOutMessage` | 20 | 320 |
| Help keywords (total) | `HelpKeywords` | - | 255 (alphanumeric) |
| Help response message | `HelpMessage` | 20 | 320 |

---

## Common Rejection Codes (Reference)

| Code | Meaning |
|---|---|
| 30886 | Invalid Campaign Description (vague, mismatched use case/samples, or identifies ISV instead of business). |
| 30892 | Invalid Sample Message - public URL shortener / unsecured URL. |
| 30895 | Direct Lending content/attribute error - lending not disclosed. |
| 30896 | Opt-in error. |
| 30907 | Website URL validation issue. |
| 30908 | Compliant privacy policy required. |
| 30909 | Message Flow / Call-to-Action incomplete or unverified. |
| 30917 | Not all opt-in methods include complete workflow descriptions. |
| 30919 | Website lacks sufficient business or messaging use-case info. |
| 30921 | Website requires authentication and cannot be reviewed. |
| 30924 | Missing or non-compliant consent agreement language in opt-in flow. |
| 30925 | Opt-in must be unchecked by default; active consent required. |
| 30933 | Privacy Policy URL is required. |
| 30934 | Terms and Conditions URL is required. |

---

## Editing a Campaign After Rejection

If a campaign fails review, the Console **Edit Campaign** modal re-exposes the text-entry fields from the original submission flow - Campaign description, Sample messages (five boxes shown, first two required), the Message contents checkboxes (embedded links, embedded phone numbers, direct lending/loan arrangement, age-gated), and the opt-in process description - all pre-populated with your prior values. Fix the flagged fields and resubmit. The same fields can be updated in place via the API by updating the `UsAppToPerson` resource.
