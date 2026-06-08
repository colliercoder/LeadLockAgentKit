> Source: https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US , https://www.twilio.com/docs/messaging/compliance/a2p-10dlc , https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/direct-standard-onboarding , https://www.twilio.com/en-us/changelog/increased-mms-rate-limits-for-a2p-10dlc-phone-numbers-in-the-u-s0 , https://www.twilio.com/docs/api/errors/30022 , https://www.twilio.com/docs/api/errors/30023 , https://www.twilio.com/docs/api/errors/30025 , https://www.twilio.com/docs/api/errors/30026 , https://support.twilio.com/hc/en-us/articles/1260804800549-T-Mobile-daily-message-limits-for-long-code-messaging-with-A2P-10DLC - scraped 2026-06-07

# A2P 10DLC: Throughput, Trust Scores & Daily Caps

A reference for understanding how fast you can send US application-to-person (A2P) SMS/MMS over 10-digit long codes (10DLC), how many messages you can send per day, and what controls those numbers.

> [!WARNING]
> **Values change - verify live.**
> Throughput tiers, daily caps, and the formulas that map Trust Score to limits are **set and changed by the US mobile carriers (AT&T, T-Mobile, Verizon) and The Campaign Registry (TCR)** - not by Twilio. The carriers adjust these numbers periodically and without much notice. Treat every specific number in this document as **indicative, not authoritative**. Before relying on any figure for capacity planning, confirm the current value against:
> - The live Twilio article: [Message throughput (MPS) and Trust Scores for A2P 10DLC in the US](https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US)
> - Your own brand's numbers in **Twilio Console → Trust Hub → A2P Messaging** (select your US A2P brand and view its Trust Score and daily limit)
> - The Twilio Console brands view: `console.twilio.com/us1/develop/sms/regulatory-compliance/brands`

---

## 1. Key terms

### Throughput (MPS / TPS)

"Throughput" is how fast you are allowed to push messages into the carrier network. It is most often expressed as **MPS (messages per second)**, sometimes called TPS (transactions per second). Some legacy carrier programs (and Sole Proprietor campaigns) express limits **per minute** instead.

Throughput is enforced **per carrier** (AT&T, T-Mobile, Verizon, etc.) and is allocated to a **campaign**, not to an individual phone number. All phone numbers attached to the same campaign **share** that campaign's throughput allocation.

### Daily cap (daily message limit)

A "daily cap" is the **maximum number of messages your brand can send to a given carrier in a single day**. The most prominent daily cap is **T-Mobile's**, which is applied at the **brand level (per EIN)** and **shared across every campaign and every messaging platform registered under that brand**. The day resets at **00:00 Pacific Time (US)** (which shifts with US Daylight Saving / Standard Time).

> Throughput limits *how fast*. Daily caps limit *how much total per day*. You can hit either one independently.

### Trust Score

A **Trust Score** is a number from **0 to 100** assigned by **The Campaign Registry (TCR)** to a **Standard Brand** during registration, based on the quality and completeness of the business information submitted. **Higher Trust Score → higher throughput and higher daily caps.** (See Section 3.)

---

## 2. How throughput is determined

Per Twilio, A2P 10DLC message throughput in the US is determined by three things:

1. **Brand type** - Sole Proprietor, Low-Volume Standard, or Standard.
2. **Campaign type / use case** - e.g. Marketing, Low Volume Mixed, and various special use cases.
3. **Trust Score** - applies to Standard Brands (which go through secondary vetting). Low-Volume Standard Brands and Sole Proprietor Brands **do not** receive a Trust Score, because they skip secondary vetting.

### Brand types at a glance

| | Sole Proprietor Brand | Low-Volume Standard Brand | Standard Brand |
|---|---|---|---|
| EIN / Tax ID required | No | Yes | Yes |
| Trust Score? | No | No (skips secondary vetting) | **Yes (0–100)** |
| Campaigns per brand | 1 campaign per brand | Up to 5 (more with valid business reason) | Up to 5 (more with valid business reason) |
| Daily volume to T-Mobile | ~1,000 SMS segments + MMS/day (≈3,000/day across all US carriers) | Up to ~2,000 SMS segments + MMS/day (≈6,000/day across all US carriers); Russell 3000 companies up to 200,000/day | Determined by Trust Score (highest tier available) |
| Throughput | Fixed, low (per number) | Fixed, modest | Scales with Trust Score (highest available) |

*Source: Twilio "Programmable Messaging and A2P 10DLC" overview. These volume figures are carrier-set and subject to change.*

> **Takeaway:** If you need meaningful volume or speed, you want a **Standard Brand with a high Trust Score**. Sole Proprietor and Low-Volume Standard are capped well below that ceiling by design.

---

## 3. Brand Trust Score - what it is and how to raise it

### What it is

- A score from **0 to 100** assigned by **TCR** during **Standard Brand** registration.
- Derived from the **quality, accuracy, and completeness** of your registered business information (legal business name, EIN/Tax ID, address, website, etc.) cross-checked against authoritative records.
- For Standard Brands, Twilio submits the brand for **secondary vetting**, which produces (or raises) the Trust Score and unlocks higher default throughput and higher carrier daily limits.
- **Low-Volume Standard** and **Sole Proprietor** brands **do not** get a Trust Score - they skip secondary vetting, and their limits are set by fixed brand-type rules instead.

### Vetted vs. unvetted

- **Vetted (Standard Brand, secondary-vetted):** receives a 0–100 Trust Score → mapped to throughput tiers and the highest carrier daily caps.
- **Unvetted (Low-Volume Standard, Sole Proprietor):** no Trust Score; subject to the fixed lower limits in the brand-type table above.

### How to raise your Trust Score

1. **Register accurately.** Provide precise, current business details that **exactly match** how you registered with your country's tax agency. Mismatches (legal name, EIN, address) lower the score. This is the single biggest lever.
2. **Complete every field.** Completeness contributes directly to the score - include a working website, correct business type, and valid contact info.
3. **Request external/secondary vetting.** If your automatically assigned Trust Score is too low for your volume needs, you can submit the brand for additional (paid) **external vetting** through an approved vetting provider via TCR. A higher vetting score raises your throughput tier and daily caps.
4. **Follow Twilio's [A2P 10DLC Brand Approval Best Practices](https://help.twilio.com/hc/en-us/articles/4405758341659-A2P-10DLC-Brand-Approval-Best-Practices).**

> Where to read your score: **Twilio Console → Trust Hub → A2P Messaging** → select your brand → view TCR Trust Score and daily limit.

---

## 4. SMS throughput by Trust Score / use case (AT&T and others)

Each carrier sets its own throughput formula, and **the exact SMS MPS numbers per Trust Score band are carrier-controlled and change over time.** Twilio publishes the current tables in the live article - always confirm there.

**General pattern (verify current numbers live):**

- **Sole Proprietor campaigns** are capped at a low fixed rate. Twilio documents Sole Proprietor campaigns at roughly **15 messages/minute on AT&T per campaign**, and a fixed **0.5 MPS per number** allocation for MMS (see Section 5). Use this as an order-of-magnitude indicator only.
- **Standard Brand campaigns** scale their throughput with the Trust Score: the higher the score, the higher the AT&T (and other carrier) MPS allocation per campaign.
- **AT&T** historically publishes throughput as **TPM/MPS tiers keyed to the Trust Score band** and the registered use case. T-Mobile, by contrast, leans on the **daily brand cap** model (Section 6) rather than fine-grained per-second tiers.

> [!NOTE]
> Twilio does not freeze a single canonical SMS-MPS-by-Trust-Score table in its docs because the carriers revise it. For your brand's actual current AT&T/Verizon/T-Mobile MPS, read the live throughput article and your Console Trust Hub entry. **Do not hard-code SMS MPS tier numbers into capacity plans from memory.**

---

## 5. MMS throughput by Trust Score (verified, effective ~March 18, 2026)

Twilio's changelog documents the **MMS** rate-limit model that replaced the old fixed account-level cap of 1 MPS. **MMS MPS now scales with Brand Trust Score and campaign use case.**

For most registered campaign types (**Declared** and **Mixed / Marketing**):

| Brand Trust Score | MMS throughput (per major carrier: AT&T, T-Mobile, Verizon) |
|---|---|
| **75 or above** | up to **40 MPS** per carrier |
| **50 – 74** | up to **20 MPS** per carrier |
| **below 50** | up to **5 MPS** per carrier |

Additional rules:

- **Special use cases** (e.g. certain regulated/exempt categories) have **their own fixed MPS allocations that are NOT affected by Trust Score.**
- **Sole Proprietor Brands** have a fixed allocation of **0.5 MPS per number**, regardless of Trust Score or campaign type.
- Rollout note: Twilio described this as a **gradual rollout** that could take 5–6 weeks to reach all customers.

*Source: [Increased MMS rate limits for A2P 10DLC Phone Numbers in the U.S.](https://www.twilio.com/en-us/changelog/increased-mms-rate-limits-for-a2p-10dlc-phone-numbers-in-the-u-s0) (Twilio changelog). These figures are carrier-controlled - verify live.*

---

## 6. T-Mobile daily brand cap (per EIN, shared across campaigns)

T-Mobile (including **Sprint** and **MetroPCS**) imposes a **daily message limit** rather than only a per-second throughput tier. Key facts (all from Twilio docs):

- The cap is **per Brand (per EIN)**, derived from your **Trust Score** (secondary vetting score).
- It counts the **total outbound SMS segments + MMS messages** sent to T-Mobile **across all campaigns and across any messaging platform** where you've registered the brand.
- The day **resets at 00:00 Pacific Time (US)**.
- Since ~September 14, 2021, Twilio includes **automatic secondary vetting** at brand registration so a brand receives the **highest daily T-Mobile cap it qualifies for**.

### Documented baseline caps by brand type

| Brand type | T-Mobile daily cap (SMS segments + MMS) | Approx. across all US carriers |
|---|---|---|
| Sole Proprietor | ~**1,000**/day | ~3,000/day |
| Low-Volume Standard | up to ~**2,000**/day | ~6,000/day |
| **Russell 3000 Index companies** | **200,000**/day (by default) | - |
| Standard Brand (vetted) | **Tiered by Trust Score** - higher score → higher cap | - |

> [!IMPORTANT]
> **The exact Standard-Brand daily-cap value for each Trust Score band is carrier-controlled and changes.** Twilio shows your brand's specific T-Mobile daily limit in **Console → Trust Hub → A2P Messaging** and in the live [T-Mobile daily message limits article](https://support.twilio.com/hc/en-us/articles/1260804800549-T-Mobile-daily-message-limits-for-long-code-messaging-with-A2P-10DLC). Read it there - do not assume a fixed tier table.

### Removing the cap (Special Business Review)

By default, even high-Trust-Score brands sit under a T-Mobile daily ceiling. To **remove** the cap (beyond the default Russell-3000 200,000/day allowance), a business must complete T-Mobile's **Special Business Review (SBR)** process. SBR is for high-volume legitimate senders who need to exceed the standard daily limits.

---

## 7. Verizon's approach

Verizon does **not** publish per-Trust-Score daily-cap tiers the way T-Mobile does. Verizon's model is primarily **per-campaign throughput plus content/quality filtering**:

- Throughput is allocated **per registered campaign** (and shared across the numbers in that campaign).
- Verizon applies **aggressive content filtering** at the network level - messages can be **filtered/blocked** even when you are within your throughput and have no explicit "cap reached" error, if content trips spam/abuse heuristics (e.g., prohibited content, URL reputation, unexpected volume spikes).
- For MMS, Verizon follows the same Trust-Score-scaled MPS tiers shown in Section 5 (40 / 20 / 5 MPS by Trust Score band).

> Practical implication: with Verizon, **clean, consent-based, well-formatted content matters as much as your throughput tier.** Filtering is silent and is not surfaced as a daily-cap error.

---

## 8. How use case (campaign type) affects throughput

The registered **use case** changes your throughput and how it's calculated:

- **Marketing / Mixed (Declared, Mixed/Marketing):** standard campaign types whose MPS **scales with Trust Score** (per the Section 5 model for MMS, and the carrier tables for SMS).
- **Low Volume:** intended for low-throughput senders; lower fixed ceilings.
- **Special use cases** (e.g. certain regulated, charitable, emergency, or carrier-exempt categories): have **fixed MPS allocations independent of Trust Score** - they neither benefit from a high score nor suffer from a low one.
- **Sole Proprietor** campaigns: fixed, low limits regardless of use case (≈15 msg/min on AT&T per campaign; 0.5 MPS/number for MMS).

Pick the **most accurate use case** for your traffic. Misregistering (e.g., calling marketing traffic "low volume") will not raise your limits and can trigger filtering or campaign rejection.

---

## 9. Number pooling - how multiple numbers share throughput

You attach numbers to a campaign via a Twilio **Messaging Service** (the Messaging Service is the container that links your sender pool to the registered campaign).

Key behavior:

- **Throughput is per campaign, not per number.** Adding more phone numbers to a campaign **does not increase the campaign's total throughput** - all numbers in the campaign **share** the single campaign allocation. More numbers spread the *same* throughput across more senders (useful for sender reputation / per-number rate distribution, not for raw capacity).
- The **T-Mobile daily cap is per brand**, shared across **all** campaigns and platforms under that EIN - so spreading volume across many campaigns or numbers does **not** raise the brand's daily T-Mobile ceiling.
- A Messaging Service supports **Sticky Sender** (a given recipient keeps receiving from the same number) and pool-based number selection. These help with deliverability and consistency, **not** with raising the allocation.

> To genuinely raise capacity you must **raise the Trust Score / vet the brand** or **register additional brands/campaigns where legitimate** - not just add numbers.

---

## 10. What happens when you exceed a limit

| Situation | What you see | Behavior |
|---|---|---|
| Sending faster than the carrier allows for your campaign (per-second throughput exceeded) | **Error 30022 - US A2P 10DLC Rate Limits Exceeded** | The downstream carrier **rejects** the message. Causes: app sending faster than allowed, combined traffic across numbers in the same campaign exceeding the campaign throughput, or too many messages to the same number in a short window. |
| Brand hit its T-Mobile daily message cap | **Error 30023 - US A2P 10DLC Daily Message Cap Reached** | Further messages to T-Mobile are blocked **until the next calendar day (resets 00:00 Pacific Time)**. The cap is per brand (per EIN) across all platforms. |
| Approaching the T-Mobile daily cap (50% / 70% consumed) | **Errors 30025 / 30026 (and 30027) - DEPRECATED** | These "daily traffic used" warnings are **no longer generated.** Monitor usage via **Messaging Insights** instead. |
| Content trips carrier spam/abuse filtering (esp. Verizon, T-Mobile) | Often **no explicit cap error** | Messages can be **silently filtered/blocked** for content reasons even within throughput. |

### Handling 30022 (rate limit) properly

- **Throttle / queue** your sends so they stay under the campaign's allowed MPS, then **retry** rejected messages with backoff. (A burst over the limit gets rejected, not auto-queued indefinitely - you must control the send rate or implement retry.)
- Remember throughput is **shared across all numbers in the campaign** - adding numbers won't fix 30022; **slowing the aggregate send rate** will.

### Handling 30023 (daily cap)

- **Wait** for the next calendar day (00:00 PT reset).
- **Monitor** daily T-Mobile usage with **Twilio Messaging Insights** so you throttle before hitting the cap.
- **Raise the cap** by improving your Trust Score (vet/secondary-vet the brand) or, for high-volume needs, completing T-Mobile **Special Business Review**.

---

## 11. How to increase throughput and daily caps - checklist

1. **Register as a Standard Brand** (not Sole Proprietor / Low-Volume Standard) so you become eligible for Trust-Score-based tiers.
2. **Maximize your Trust Score:** submit accurate, complete business info matching your tax-agency records; fix any mismatches.
3. **Pursue secondary / external vetting** through TCR if your auto-assigned score is below the tier you need.
4. **Register the correct use case** for your traffic (don't under-declare marketing as low-volume).
5. **For very high T-Mobile volume**, complete **T-Mobile Special Business Review** to lift the daily cap.
6. **Don't rely on adding numbers** - throughput is per campaign and the T-Mobile cap is per brand; more numbers won't raise either ceiling.
7. **Keep content clean and consent-based** to avoid silent carrier filtering (especially Verizon and T-Mobile), which no amount of throughput allocation overrides.
8. **Monitor** with **Messaging Insights** and check your live numbers in **Trust Hub → A2P Messaging**.

---

## 12. Carrier-controlled disclaimer (read this)

> The specific throughput tiers, MPS-per-Trust-Score mappings, and daily-cap values in this document are **defined and revised by AT&T, T-Mobile, Verizon, and TCR** - not by Twilio and not by this skill. They **change without broad notice.** Always confirm current values against the **live Twilio article** ([Message throughput (MPS) and Trust Scores for A2P 10DLC in the US](https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US)) and your **own brand's entry in Twilio Console → Trust Hub → A2P Messaging** before making capacity commitments.

---

## Sources

- [Message throughput (MPS) and Trust Scores for A2P 10DLC in the US](https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US) - Twilio Help Center
- [Programmable Messaging and A2P 10DLC (overview)](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc) - Twilio Docs
- [Direct Standard and Low-Volume Standard Registration Guide](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/direct-standard-onboarding) - Twilio Docs
- [Increased MMS rate limits for A2P 10DLC Phone Numbers in the U.S. (effective ~Mar 18, 2026)](https://www.twilio.com/en-us/changelog/increased-mms-rate-limits-for-a2p-10dlc-phone-numbers-in-the-u-s0) - Twilio Changelog
- [T-Mobile daily message limits for long code messaging with A2P 10DLC](https://support.twilio.com/hc/en-us/articles/1260804800549-T-Mobile-daily-message-limits-for-long-code-messaging-with-A2P-10DLC) - Twilio Support
- [Error 30022 - Rate Limits Exceeded](https://www.twilio.com/docs/api/errors/30022) - Twilio Docs
- [Error 30023 - Daily Message Cap Reached](https://www.twilio.com/docs/api/errors/30023) - Twilio Docs
- [Error 30025 - 50% T-Mobile Daily Limit Consumed (deprecated)](https://www.twilio.com/docs/api/errors/30025) / [Error 30026 - 70% (deprecated)](https://www.twilio.com/docs/api/errors/30026) - Twilio Docs
- [A2P 10DLC Brand Approval Best Practices](https://help.twilio.com/hc/en-us/articles/4405758341659-A2P-10DLC-Brand-Approval-Best-Practices) - Twilio Support
