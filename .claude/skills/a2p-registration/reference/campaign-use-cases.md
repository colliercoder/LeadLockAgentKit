> Source: https://help.twilio.com/articles/1260801844470-List-of-Campaign-Types-and-Use-Case-Types-for-A2P-10DLC-registration ; https://www.twilio.com/docs/messaging/api/usapptopersonusecase-resource ; https://help.twilio.com/articles/4402972441243-Special-Use-Cases-for-A2P-10DLC ; https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US ; https://help.twilio.com/articles/4407882914971-Comparison-between-Starter-Low-Volume-Standard-and-Standard-registration-for-A2P-10DLC ; https://www.twilio.com/docs/messaging/compliance/a2p-10dlc - scraped 2026-06-07

# A2P 10DLC Campaign Use Cases

A practical, verified reference for choosing and registering the correct A2P 10DLC **campaign use case** in the United States. Every fact here is drawn from current Twilio documentation (see Source line above). Where Twilio does not publish a precise number, this doc says so rather than guessing.

---

## What a "Use Case" Is

In A2P 10DLC, a **Brand** represents the business sending messages, and a **Campaign** represents a specific messaging program under that Brand. Every Campaign must declare a **use case** - the registered purpose of the messages, such as marketing, account verification, or customer care.

The use case is not a label you pick for convenience. It is a declaration to the carriers (via The Campaign Registry) about what kind of content you will send. Carriers and the registry use the declared use case to:

- Assign **message throughput** (messages per second, MPS) and daily volume caps.
- Apply **content filtering** rules appropriate to that traffic type.
- Set **carrier fees** (some use cases carry different fees).
- Determine whether the Campaign needs **extra manual review/approval** before it can send.

### Why Messages MUST Match the Registered Use Case

Carriers filter and audit live traffic against the registered use case. If your sent messages do not match what you registered:

- Messages can be **filtered or blocked** by the carrier.
- The Campaign can be **flagged or rejected** during manual Campaign Vetting.
- In persistent cases, the Brand/Campaign can lose its registered (lower-filtering, higher-throughput) status.

Twilio's own guidance is blunt: registering correctly results in **lower message filtering and higher throughput**, while mismatched or unregistered traffic gets additional carrier fees and heavier filtering. The registered use case is effectively a contract about your content - honor it.

---

## Standard vs. Special Use Cases

Twilio's API exposes a `post_approval_required` boolean on every use case. This boolean is the dividing line:

- **Standard use cases** (`post_approval_required: false`) - Available through the normal registration flow. No additional manual approval step beyond standard Campaign Vetting.
- **Special use cases** (`post_approval_required: true`) - Unique or sensitive in nature. They get carve-outs for throughput and carrier fees, **require an additional approval/vetting process**, and in some cases carry different fees. Twilio calls these "Special Use Cases."

You select exactly **one** use case per Campaign. The "Mixed," "Marketing," and "Low Volume Mixed" options exist specifically so a single Campaign can carry more than one content type without misregistering (see the Marketing-Only Rule below).

---

## Standard Use Cases (No Extra Approval)

These all have `post_approval_required: false`. Definitions and example content are taken verbatim/paraphrased from Twilio's UsAppToPersonUsecase API resource.

| Use Case (code) | Name | Definition | Typical Examples |
| --- | --- | --- | --- |
| `2FA` | Two-Factor Authentication (2FA) | Two-factor authentication, one-time-use password, password reset. | OTP login codes, password-reset codes, verification codes. |
| `ACCOUNT_NOTIFICATION` | Account Notification | All reminders, alerts, and notifications. | Flight delayed, hotel booked, appointment reminders. |
| `CUSTOMER_CARE` | Customer Care | All customer care messaging, including account management and support. | Support replies, account-management messages, service follow-ups. |
| `DELIVERY_NOTIFICATION` | Delivery Notification | Information about the status of the delivery of a product or service. | "Your order shipped," "out for delivery," tracking updates. |
| `FRAUD_ALERT` | Fraud Alert Messaging | Fraud alert notification. | "Did you authorize this charge?", suspicious-activity alerts. |
| `HIGHER_EDUCATION` | Higher Education | For campaigns on behalf of Colleges or Universities, and School Districts etc. that fall outside any "free to the consumer" messaging model. | University/college notifications, district announcements (post-secondary). |
| `MARKETING` | Marketing | Any communication with marketing and/or promotional content. | Promotions, sales, offers, newsletters, drip campaigns. |
| `MIXED` | Mixed | Mixed messaging reserved for a specific consumer service industry. | Combined transactional + promotional traffic for a consumer-service brand. |
| `LOW_VOLUME` | Low Volume Mixed | Low throughput, any combination of use cases. | Test accounts, demo accounts, small senders mixing content types. |
| `POLLING_VOTING` | Polling and Voting | Polling and voting. | Surveys, "reply A/B," vote-by-text. |
| `PUBLIC_SERVICE_ANNOUNCEMENT` | Public Service Announcement | An informational message meant to raise the audience's awareness about an important issue. | Awareness campaigns, public-interest notices. |
| `SECURITY_ALERT` | Security Alert | A notification that the security of a system (software or hardware) has been compromised and there is an action you need to take. | Breach notices, "reset your password now," security action prompts. |
| `CHARITY` | Charity | Includes 501(c)(3) charity. Does **not** include religious organizations. | Charity/501(c)(3) outreach (note: special handling applies - see Charity note below). |
| `POLITICAL` | Political | Part of an organized effort to influence the decision-making of a specific group. **All campaigns must be verified.** | Political outreach, campaign messaging (requires verification). |

> Note on `CHARITY` and `POLITICAL`: Twilio's API marks both as `post_approval_required: false`, but Twilio's Help Center separately documents Charity/501(c)(3) and Political as **Special Use Cases** with their own registration/verification processes and (for Political) mandatory verification of all campaigns. Treat these two as "standard flag, but special handling" - confirm the current vetting requirements in Twilio's Special Use Cases article before registering.

---

## Special Use Cases (Extra Approval Required)

These all have `post_approval_required: true`. They require an additional approval step and may have different throughput carve-outs and fees.

| Use Case (code) | Name | Definition | Notes / Examples |
| --- | --- | --- | --- |
| `EMERGENCY` | Emergency | Notification services designed to support public safety / health during natural disasters, armed conflicts, pandemics, and other national or regional emergencies. | Disaster, pandemic, and public-safety notifications. |
| `K12_EDUCATION` | K-12 Education | Campaigns for messaging platforms supporting schools from grades K-12 and distance-learning centers. **Not** for post-secondary schools. | K-12 school/district platforms only. |
| `AGENTS_FRANCHISES` | Agents and Franchises | For brands with multiple agents, franchises, or offices in the same brand vertical that require individual localized numbers per agent/location/office. | Multi-location franchises, real-estate agents, distributed offices. |
| `PROXY` | Proxy | Peer-to-peer, app-based group messaging with proxy/pooled numbers (e.g., GroupMe). Supports personalized services and non-exposure of personal numbers for enterprise/A2P communications. | Marketplaces masking personal numbers (e.g., Uber, Airbnb). |
| `SOCIAL` | Social | Communication within or between closed communities. | Influencer alerts, closed-community notifications. |
| `SWEEPSTAKE` | Sweepstake | Sweepstake. | Contest entries, sweepstakes notifications. |

> The Higher Education vs. K-12 split matters: **Higher Education is standard**, **K-12 Education is special** (extra approval). Pick the one that matches the school level you actually serve.

---

## The Marketing-Only Rule

This is the single most common cause of rejected campaigns and filtered traffic.

**If you register the `MARKETING` use case, every message you send under it must be promotional/marketing content.** You cannot mix transactional content into a Marketing campaign. Specifically, the following are **not** allowed under a Marketing use case:

- Appointment reminders
- Order/booking confirmations
- Delivery/shipping notifications
- Account alerts and notifications
- 2FA / one-time passwords
- Customer-care replies

Sending transactional messages under a Marketing registration causes the Campaign to be **rejected during vetting** and/or the **traffic to be filtered** by carriers, because the live content does not match the declared use case.

### What to register instead when you send a blend

If your program genuinely sends **both** promotional and transactional messages on the same Brand/number, do **not** force everything into Marketing. Choose a mixed-content use case:

- **`MIXED`** - "Mixed messaging reserved for a specific consumer service industry." Use this when a consumer-service brand legitimately sends a blend of transactional + promotional traffic at normal volume.
- **`LOW_VOLUME` (Low Volume Mixed)** - "Low throughput, any combination of use cases." Use this when you mix content types **and** you are a small/low-volume sender (test/demo accounts, small businesses). It carries a lower monthly fee than a standard Campaign in exchange for lower throughput and a lower daily cap.

**Rule of thumb:** Marketing campaign → 100% promotional, no exceptions. Any blend → Mixed (normal volume) or Low Volume Mixed (small sender). If you are purely transactional, register the specific transactional use case that fits (`2FA`, `ACCOUNT_NOTIFICATION`, `CUSTOMER_CARE`, `DELIVERY_NOTIFICATION`, etc.) for the best throughput.

---

## Low Volume Mixed: Deep Dive

`LOW_VOLUME` (display name: **Low Volume Mixed**) is a standard use case designed for small senders who need to mix content types without paying full Campaign price.

**What it is:**
- Low throughput, **any combination of use cases** in one Campaign.
- Examples Twilio gives: test accounts, demo accounts.
- `post_approval_required: false` - no extra approval step.

**Daily volume cap:**
- Supports **up to 2,000 SMS segments and MMS per day toward T-Mobile** (approximately 6,000 SMS segments and MMS per day across all US carriers, per Twilio's Low-Volume Standard Brand guidance).

**Throughput (MPS):**
- Low Volume Mixed is given a **lower message throughput (MPS) than other use cases, regardless of Trust Score.** Even a high Trust Score will not raise a Low Volume Mixed campaign's MPS above this reduced tier.

**Cost trade-off:**
- It has a **lower monthly Campaign fee** than a standard Campaign. (Exact fees change over time and vary by registration path - confirm current pricing on Twilio's A2P pricing page.)

**When it's the right pick:**
- You are a small business / agency sub-account sending a modest volume.
- You send a **mix** of transactional and promotional content on the same number.
- You stay comfortably under ~2,000 T-Mobile segments/day.
- You want the lowest monthly Campaign fee and don't need high MPS.

**When to move up instead:**
- If you regularly exceed the daily cap or need higher throughput, register a **Standard Brand** with a full Campaign (`MIXED`, `MARKETING`, or a specific transactional use case) instead.

---

## Brand Type vs. Use Case (How They Interact)

The use case is chosen per Campaign, but daily volume is governed by the **Brand type** and Trust Score. From Twilio's brand-type comparison:

| | Sole Proprietor Brand | Low-Volume Standard Brand | Standard Brand |
| --- | --- | --- | --- |
| Campaigns per Brand | One Campaign per Brand | Up to 5 Campaigns (more only with a clear, valid business reason) | Up to 5 Campaigns (more only with a clear, valid business reason) |
| Daily message volume | ~1,000 SMS segments + MMS/day to T-Mobile (≈3,000/day across US carriers) | Up to 2,000 SMS segments + MMS/day to T-Mobile (≈6,000/day across US carriers) | Higher, set by Trust Score; Russell 3000 companies can reach 200,000 segments + MMS/day to T-Mobile by default |
| Tax ID required | No | Yes (EIN or equivalent) | Yes (EIN or equivalent) |

Notes:
- The **T-Mobile daily cap is applied at the Brand level and shared across all Campaign use cases** under that Brand.
- Each Tax ID may register **up to five** Standard / Low-Volume Standard Brands; beyond that, additional Brands register but their Campaigns may be rejected during manual vetting without a valid business reason.

---

## Throughput Differences by Use Case

Twilio determines US A2P 10DLC throughput from three inputs: **Brand type**, **Campaign type (use case)**, and **Trust Score** (for Standard Brands). Documented relationships:

- **Higher Trust Score → higher MPS** (for Standard Brands).
- **Specific / "Declared" use cases** (e.g., the dedicated transactional use cases) **may receive higher MPS for the same Trust Score** than a generic `MIXED` or `MARKETING` use case. In other words, declaring a precise use case can earn you more throughput than lumping traffic into Mixed/Marketing.
- **Low Volume Mixed** receives a **lower MPS than other use cases regardless of Trust Score** - it is intentionally throttled in exchange for its lower fee and simpler registration.
- **Special use cases** receive throughput **carve-outs** (and sometimes different carrier fees) handled through their separate approval process.

> Twilio does not publish a single fixed "MPS per use case" table independent of Trust Score and carrier - exact MPS values depend on your Brand's Trust Score and the carrier. Check Twilio's "Message throughput (MPS) and Trust Scores for A2P 10DLC in the US" article for the current Trust-Score-to-MPS mapping rather than hardcoding a number.

---

## How to Choose the Right Use Case (Decision Guidance)

Work top-down. The first matching row wins.

1. **Sending only login/verification codes?** → `2FA`. Highest-trust transactional category.
2. **Sending only fraud/security action alerts?** → `FRAUD_ALERT` or `SECURITY_ALERT`.
3. **Sending only delivery/shipping status?** → `DELIVERY_NOTIFICATION`.
4. **Sending only reminders/alerts/notifications (appointments, bookings)?** → `ACCOUNT_NOTIFICATION`.
5. **Sending only support / account-management messages?** → `CUSTOMER_CARE`.
6. **Sending only promotional content - and nothing else?** → `MARKETING`. (Remember: zero transactional content allowed.)
7. **Sending a blend of promotional + transactional on one number, at normal volume?** → `MIXED`.
8. **Same blend, but you're a small/low-volume sender (≤ ~2,000 T-Mobile segments/day) and want the lowest fee?** → `LOW_VOLUME` (Low Volume Mixed).
9. **Polls/surveys?** → `POLLING_VOTING`. **Public awareness?** → `PUBLIC_SERVICE_ANNOUNCEMENT`.
10. **College/university/district (post-secondary)?** → `HIGHER_EDUCATION`. **K-12 schools?** → `K12_EDUCATION` (special).
11. **Charity/501(c)(3)?** → `CHARITY` (special handling). **Political?** → `POLITICAL` (all campaigns verified).
12. **Multi-location agents/franchises, proxy/pooled numbers, closed-community social, sweepstakes, emergency services?** → the matching **special** use case (`AGENTS_FRANCHISES`, `PROXY`, `SOCIAL`, `SWEEPSTAKE`, `EMERGENCY`) - expect an extra approval step.

**Key principles:**
- **Prefer the most specific transactional use case** you qualify for - it usually earns higher throughput than Mixed/Marketing at the same Trust Score.
- **Never put transactional content under Marketing.** Use Mixed or Low Volume Mixed for blends.
- **Match live content to the declared use case** continuously, not just at registration - carriers audit ongoing traffic.

---

## Quick Reference: All Use Case Codes

| Code | Name | Class |
| --- | --- | --- |
| `2FA` | Two-Factor Authentication (2FA) | Standard |
| `ACCOUNT_NOTIFICATION` | Account Notification | Standard |
| `CUSTOMER_CARE` | Customer Care | Standard |
| `DELIVERY_NOTIFICATION` | Delivery Notification | Standard |
| `FRAUD_ALERT` | Fraud Alert Messaging | Standard |
| `HIGHER_EDUCATION` | Higher Education | Standard |
| `MARKETING` | Marketing | Standard |
| `MIXED` | Mixed | Standard |
| `LOW_VOLUME` | Low Volume Mixed | Standard |
| `POLLING_VOTING` | Polling and Voting | Standard |
| `PUBLIC_SERVICE_ANNOUNCEMENT` | Public Service Announcement | Standard |
| `SECURITY_ALERT` | Security Alert | Standard |
| `CHARITY` | Charity | Standard flag / special handling |
| `POLITICAL` | Political | Standard flag / special handling (all campaigns verified) |
| `EMERGENCY` | Emergency | Special (post-approval) |
| `K12_EDUCATION` | K-12 Education | Special (post-approval) |
| `AGENTS_FRANCHISES` | Agents and Franchises | Special (post-approval) |
| `PROXY` | Proxy | Special (post-approval) |
| `SOCIAL` | Social | Special (post-approval) |
| `SWEEPSTAKE` | Sweepstake | Special (post-approval) |

> "Class" reflects Twilio's `post_approval_required` flag from the UsAppToPersonUsecase API, plus Help Center special-handling notes for Charity and Political. Always confirm the current list and requirements against the live Twilio API/Help Center before registering, since carriers and Twilio update use cases and their requirements over time.
