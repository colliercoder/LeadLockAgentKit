# Prohibited & Restricted Content: SHAFT and Carrier Filtering Rules

> Source: https://www.twilio.com/en-us/legal/messaging-policy | https://www.twilio.com/en-us/legal/aup | https://www.twilio.com/en-us/guidelines/sms | https://help.twilio.com/articles/360045004974-Forbidden-Message-Categories-in-the-US-and-Canada-Short-Code-Toll-Free-and-Long-Code | https://www.twilio.com/docs/api/errors/30883 | https://www.twilio.com/docs/api/errors/30897 | https://www.twilio.com/docs/api/errors/30457 | https://www.twilio.com/docs/api/errors/30525 | https://www.twilio.com/docs/api/errors/30892 | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/troubleshooting-a2p-brands/troubleshooting-and-rectifying-a2p-campaigns | https://help.twilio.com/articles/4410588996123-A2P-10DLC-Carrier-Penalties-for-Non-Compliant-Messaging | https://api.ctia.org/wp-content/uploads/2023/05/230523-CTIA-Messaging-Principles-and-Best-Practices-FINAL.pdf | https://www.infobip.com/docs/essentials/usa-and-canada-compliance/usa-messaging-content-requirements - scraped 2026-06-07

This reference covers what content and use cases are **prohibited or restricted** on US (and Canadian) messaging channels - application-to-person (A2P) SMS/MMS over long codes (10DLC), toll-free, and short codes. The rules come from two layers that stack on top of each other:

1. **The CTIA Messaging Principles and Best Practices** - the wireless-industry standard that the major carriers (AT&T, T-Mobile, Verizon) build their enforcement on.
2. **Twilio's Messaging Policy and Acceptable Use Policy (AUP)** - which incorporate the carrier rules and Twilio's own SMS Guidelines.

A message can be **legal** under federal/state law and still be **prohibited** on the carrier networks. Carrier policy is stricter than the law in several areas (cannabis is the clearest example). Compliance is judged on **both the message text and the underlying business type** - a campaign can be rejected purely because of what the business does, even if no individual sample message looks problematic.

---

## 1. SHAFT - The Core Prohibited Categories

**SHAFT** is the industry shorthand for the five content categories carriers scrutinize most heavily:

| Letter | Category | Treatment |
|---|---|---|
| **S** | **Sex / adult / sexual content** | Outright prohibited as explicit content. Limited sexual-wellness use cases may pass with **robust age gating** and carrier review. |
| **H** | **Hate** (hate speech, harassment, discrimination) | **Outright prohibited.** No age gate or carrier approval makes hate speech acceptable. |
| **A** | **Alcohol** | **Restricted, not banned.** Allowed with **robust age gating** (verified date-of-birth / age verification). |
| **F** | **Firearms** (and accessories, ammunition) | **Outright prohibited** on toll-free, short code, and long code - **regardless of age gating.** |
| **T** | **Tobacco** (including vaping/e-cigarettes/vape products) | Prohibited / heavily restricted. Carriers treat tobacco and vape as disallowed content. |

> Twilio's content-violation guidance lists the SHAFT triggers as: "sexual content, hate speech, firearms, tobacco or vape content, marijuana, or other disallowed material." (Twilio error 30883)

### How each is treated - age-gated vs. outright banned

- **Age-gateable (restricted):** Alcohol and certain sexual-wellness / adult-content programs *may* be approved if the sender implements a **robust age gate** and survives carrier review. A robust age gate means electronic confirmation of age and identity - e.g., "Reply with your birthdate xx/xx/xxxx" or a web opt-in form with a date-of-birth field. Asking a recipient to reply "YES" or "AGREE" to confirm they are over a certain age is **not** considered robust age verification.
- **Outright banned (no age gate helps):** **Hate** and **Firearms** are disallowed across all number types regardless of age gating. Per Twilio: "Firearms and accessories are not allowed on Toll Free, Short Code, or Long Code regardless of age gating."

---

## 2. Cannabis / CBD / Marijuana - Prohibited Even Where State-Legal

Cannabis is the single most important "legal but prohibited" trap.

- **Marijuana, cannabis, and CBD content is prohibited on US carrier networks** - even in states where cannabis is legal and even for hemp-derived CBD.
- Carriers (and Twilio) treat cannabis/CBD as a **content violation** independent of the SHAFT five. Twilio's content-violation error explicitly states: "Content violations include SHAFT-related material **and marijuana or CBD**."
- The underlying rule is federal: T-Mobile's "illegal content" tier requires that content be **legal federally and in all 50 states**. Because marijuana remains federally illegal (Schedule I), it fails this test nationwide regardless of local legalization.
- This applies to dispensaries, delivery services, cannabis marketing, CBD retailers, and adjacent businesses - the **business type itself** can trigger rejection, not just the words in a sample message.

---

## 3. Illegal Substances and Illegal / Illicit Content

- **Federally illegal substances** and **controlled substances** are prohibited. Campaign suspensions explicitly list "Controlled substance: including but not limited to messaging pertaining to controlled substances."
- **Illicit content** - "messages relating to illegal activity" - is grounds for immediate campaign suspension.
- **Fraudulent messages** - "counterfeit/fraudulent goods or activities" - are prohibited.
- The CTIA standard requires senders to prevent content that "is unlawful, harmful, abusive, malicious, misleading, harassing, excessively violent, obscene/illicit, or defamatory."

---

## 4. High-Risk / Restricted Financial Services

A large cluster of financial use cases is **forbidden or heavily restricted** because of their historical association with scams and predatory practices. Per Twilio's "Disallowed Content" vetting rejection (error 30897), the following are prohibited:

- **High-risk financial services** - loan marketing, stock alerts, cryptocurrency, and other risky investment content.
- **Payday / short-term / high-APR loans** - short-term, high-interest lending is a forbidden category. (Carrier-approved lending is generally limited to direct, properly licensed lenders, not lead-gen for loans.)
- **Third-party debt collection, debt reduction / debt forgiveness, and credit repair.**
- **Third-party lead generation** - sharing or selling opt-in data to other companies / lead generators. The privacy policy must explicitly state that mobile opt-in data will **not** be shared or sold to third parties, affiliates, or lead generators; the absence of that language is itself a major rejection reason.
- **"Get rich quick" schemes, deceptive work-from-home, and risky-investment marketing.**
- **Gambling, sweepstakes, and betting** - "Promotional Gambling or the act of betting" and "Illegal Sweepstakes" are explicit suspension triggers. Even lawful sweepstakes must follow all required sweepstakes laws; betting/gambling promotion is broadly disallowed.

> Note on first-party vs. third-party: The recurring theme is **third-party** monetization of the opt-in (lead gen, affiliate sharing, debt collection on behalf of others). First-party communication from a properly registered, licensed business to its own opted-in customers is the compliant baseline.

---

## 5. Phishing, Fraud, and Deceptive / Misleading Marketing

These are the most severely penalized categories on the network.

- **Phishing / smishing / social engineering** - messages "designed to gain access to information through deceptive means." This is the top-tier carrier violation (see §8). It includes **simulated phishing** sent for security testing - Twilio's AUP separately prohibits "sending any messages that are used for security testing, including simulated phishing and other activities that may resemble social engineering or similar attacks."
- **Sender ID spoofing / impersonation** - misrepresenting the sender's identity is prohibited under the AUP.
- **Deceptive or misleading marketing** - CTIA requires that "marketing content is not misleading and complies with the Federal Trade Commission's (FTC) Truth-In-Advertising rules." Content that "deceives or intends to deceive" is prohibited.
- **Malware** - content that "includes malware" or links that "are not intended to cause harm or deceive Consumers."
- **Spam / unsolicited bulk** - "any kind of unwanted or unsolicited messaging," and "sending any unsolicited or unwanted messages in bulk" is a prohibited action under Twilio's policy.

---

## 6. URL Shorteners - Public/Shared Shorteners Are Prohibited

This is one of the most common reasons compliant-looking campaigns get filtered or rejected.

- **Public / shared URL shorteners are prohibited** in message content. Named examples that trigger rejection include **bit.ly, TinyURL (tinyurl.com), goo.gl, and t.co**, plus "other generic URL shorteners." (Twilio errors 30525 and 30892.)
- **Why:** these services obscure the destination, don't reflect the sender's brand identity, and are heavily abused by spammers and scammers. Carriers strongly discourage them, so their use "will result in higher risk of filtering, with no recourse if filtering does occur."
- **What to use instead:** a **dedicated, branded short domain that belongs to your business** - a proprietary custom domain (not a free shared public shortener) that aligns with the sender identity shown in the message. The CTIA standard requires a shortener "with a web address and IP address(es) dedicated to the exclusive use of the Message Sender," and that links "unambiguously identify the website owner" and include contact information.
- **Embedded links generally** must not conceal or obscure the sender's identity. Unsecured (non-HTTPS) website URLs also trigger rejection in vetting.

---

## 7. Prohibited Messaging *Practices* (Filter Evasion)

Beyond content, certain *sending behaviors* are prohibited because they exist to evade carrier filtering. From Twilio's Messaging Policy "Prohibited Actions" and the CTIA best practices:

- **Snowshoeing** - "Spreading similar or identical messages across multiple phone numbers with the intent or effect of evading unwanted messaging detection and prevention mechanisms." Rotating numbers to dilute reputation and dodge filters is explicitly banned.
- **Filter-evasion text tricks** - "Intentionally misspelling words or non-standard opt-out phrases created to evade detection and prevention mechanisms."
- **Number recycling** - releasing and re-purchasing numbers to escape a damaged sender reputation is a filter-evasion technique and is disallowed.
- **Shared originating numbers across unrelated brands** - sending traffic for multiple unrelated brands/businesses through the same originating number (or reusing the same EIN/brand across unrelated campaigns) is a violation. CTIA addresses shared telephone numbers, common short codes, proxy numbers, and grey routes as practices requiring strict controls.
- **Affiliate marketing / opt-in sharing** - "sharing of opt-ins to affiliate companies" is a suspension trigger.
- **Grey routes** - using unauthorized/unofficial routes to deliver A2P traffic is prohibited.
- **Campaign-to-traffic mismatch** - in-market traffic that doesn't match the registered campaign use case will be suspended.

---

## 8. Penalties - Filtering, Blocking, Suspension, and Fines

Non-compliance is enforced at several escalating levels:

### Carrier filtering and number blocking
- **Silent filtering:** non-compliant or unregistered traffic is filtered (dropped) by carriers, often with no error returned to the sender. SHAFT and shortener violations frequently result in immediate blocking "with little warning."
- **Number / campaign blocking:** offending messages are blocked, and the originating number or campaign can be blocked from the network.

### Campaign suspension
- Carriers and ecosystem partners can **suspend an individual campaign** (even while the brand stays approved) for any of the violation rules above - spam, controlled substances, phishing, excessive complaints, illicit/fraudulent content, affiliate opt-in sharing, gambling, missing age gate, illegal sweepstakes, or campaign-to-traffic mismatch.
- Some content violations are **non-remediable** - the only remedy is to materially change the nature/content of the campaign (or the brand) or file an appeal with carrier support.

### Documented fine schedule (T-Mobile Sev-0)
T-Mobile issues **Sev-0 violations** (its most severe consumer violation) with non-compliance fines for prohibited A2P traffic across SMS/MMS toll-free and 10DLC on its network. **Twilio passes these fines through directly to the customer** (they appear on the customer's invoice), effective **February 15, 2024**. T-Mobile typically issues a warning before enforcement, giving the sender a chance to come into compliance before being fined. The documented tiers:

| Tier | Fine (per violation) | What triggers it |
|---|---|---|
| **Tier 1** | **$2,000** | Phishing (including **simulated** phishing sent for security testing), smishing, and social engineering |
| **Tier 2** | **$1,000** | Illegal content (content must be legal **federally and in all 50 states** - this is what catches cannabis) |
| **Tier 3** | **$500** | All other commercial-messaging violations, including but not limited to **SHAFT** (sex, hate, alcohol, firearms, tobacco) that don't follow federal and state law |

> Fines are assessed **per offending violation** and passed through by the messaging provider to the customer. They are in addition to - not instead of - filtering, blocking, and campaign suspension.

---

## 9. Compliant vs. Prohibited - Quick Examples

| Scenario | Status | Why |
|---|---|---|
| Dentist confirming an appointment to an opted-in patient | ✅ Compliant | First-party, transactional, opted-in. |
| Liquor store promo to recipients with a verified date-of-birth age gate | ⚠️ Restricted (allowed with robust age gate) | Alcohol is age-gateable, not banned. "Reply YES if 21+" is **not** a robust gate. |
| Gun shop announcing a sale on firearms/ammo | ❌ Prohibited | Firearms banned on all number types regardless of age gating. |
| Licensed dispensary texting opted-in customers in a legal-cannabis state | ❌ Prohibited | Cannabis/CBD prohibited on carriers; fails "legal in all 50 states + federally." |
| Marketing link `bit.ly/abc123` | ❌ Prohibited | Public/shared shortener; use a branded dedicated short domain. |
| Marketing link `links.yourbrand.com/abc123` | ✅ Compliant | Dedicated, branded short domain matching the sender. |
| Payday-loan / debt-relief lead-gen blast | ❌ Prohibited | High-risk financial + third-party lead generation. |
| Bank fraud-alert verification code to its own customer | ✅ Compliant | First-party transactional security alert (not phishing). |
| "You've won! Click to claim your prize" sweepstakes to a purchased list | ❌ Prohibited | Illegal sweepstakes + non-opted-in + deceptive. |
| Same number sending promos for 5 unrelated brands | ❌ Prohibited | Shared originating number across unrelated brands / snowshoeing. |
| Security team running a simulated-phishing test over SMS | ❌ Prohibited | Simulated phishing is a Tier 1 ($2,000) violation. |
| CBD wellness shop texting product discounts | ❌ Prohibited | CBD is a content violation on US carriers. |
| Hate-group recruitment or harassment messaging | ❌ Prohibited | Hate is banned outright - no age gate or approval applies. |

---

## 10. Practical Compliance Checklist

- **Confirm the business/use case isn't a forbidden category** before registering - rejection can be based on business type alone, not just message text.
- **No SHAFT in content or business model** unless it's an age-gateable category (alcohol, some adult-wellness) *with* a robust age gate and carrier approval. Never assume firearms or hate can be gated through.
- **No cannabis/CBD/marijuana**, period - regardless of state legality.
- **No high-risk financial, debt, credit-repair, third-party lead-gen, gambling, or get-rich-quick** content.
- **Branded dedicated short domain** for every shortened link - never bit.ly, TinyURL, goo.gl, or t.co.
- **One brand per originating number**; never snowshoe, recycle numbers, or share opt-ins to affiliates.
- **Privacy policy must explicitly state** mobile opt-in data is never shared/sold to third parties or lead generators.
- **Don't run simulated phishing / security tests** over the messaging channel - it's a Tier 1 fineable offense.
- **Match in-market traffic to the registered campaign** use case to avoid suspension.

---

*This document is operational guidance, not legal advice. Carrier policies and the CTIA Messaging Principles & Best Practices are updated periodically - verify against the cited primary sources before relying on any specific figure or category. Twilio's Messaging Policy was last updated April 13, 2026; the CTIA Messaging Principles and Best Practices cited here are the May 2023 edition.*
