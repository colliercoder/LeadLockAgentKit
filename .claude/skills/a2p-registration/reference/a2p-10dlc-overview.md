> Source: https://www.twilio.com/docs/messaging/compliance/a2p-10dlc, https://www.twilio.com/docs/trust-hub/registrations/a2p-10dlc-campaign, https://help.twilio.com/articles/1260800720410-What-is-A2P-10DLC-, https://help.twilio.com/articles/1260803965530-What-pricing-and-fees-are-associated-with-the-A2P-10DLC-service-, https://help.twilio.com/articles/4403988619163-Secondary-Vetting-for-A2P-10DLC, https://help.twilio.com/articles/4407882914971-Comparison-between-Starter-Low-Volume-Standard-and-Standard-registration-for-A2P-10DLC - scraped 2026-06-07

# A2P 10DLC Overview & Ecosystem

A reference for understanding US Application-to-Person (A2P) 10DLC messaging: what it is, why it exists, the players involved, the registration layers, costs, and how it compares to Toll-Free and Short Code messaging. Facts here are drawn from Twilio's official documentation and Help Center. Where exact fees are noted, treat them as point-in-time figures published by Twilio/TCR/carriers and verify current pricing before quoting them to a customer, because carriers and The Campaign Registry adjust fees periodically.

---

## What A2P 10DLC Is

**A2P** stands for **Application-to-Person** messaging: SMS or MMS sent from an application or business to a person's mobile phone (as opposed to **P2P**, person-to-person, texting between two individuals).

**10DLC** stands for **10-digit long code**. A 10DLC phone number is a standard 10-digit US local phone number. When buying a US number from Twilio, 10DLC numbers appear with **"Local"** as their Type. You may also hear them called **10DLC routes** or **long codes**.

**A2P 10DLC** is the standard that US telecom carriers have put in place to ensure that SMS traffic sent to US end users through long-code phone numbers is **verified** and **consensual**. It is the carrier-sanctioned pathway for businesses to send application-to-person messages over ordinary 10-digit local numbers.

Toll-Free numbers and Short Codes can also message US end users, but they are **not** part of the A2P 10DLC system and follow their own separate processes (see [Comparison to Toll-Free and Short Codes](#comparison-to-toll-free-and-short-codes)).

---

## Why A2P 10DLC Exists

Ten-digit long-code numbers in the US were originally designed for **person-to-person (P2P)** communication. These routes were historically unregulated, and over time they saw heavy abuse from spam applications and unsolicited messaging. As spam grew, many consumers lost trust in SMS as a communication channel.

US A2P 10DLC is the standard the carriers implemented to regulate this pathway. Its stated goals:

- **Verified senders** - carriers know a legitimate, identifiable business is behind the traffic.
- **Consensual messaging** - recipients can opt in, opt out, and request help, and they know who is messaging them.
- **Better outcomes for businesses** - registered senders get higher messaging throughput, brand awareness, and accountability, along with lower message filtering.

In short: registration trades a one-time identity-and-intent disclosure for higher deliverability and throughput, while reducing carrier spam-filtering of legitimate business traffic.

---

## The Ecosystem and Its Players

A2P 10DLC is a multi-party system. The key players:

| Player | Role |
| --- | --- |
| **Mobile carriers (T-Mobile, AT&T, Verizon)** | Set and enforce the A2P 10DLC requirements. They determine message filtering, per-message carrier fees, throughput limits, and daily volume caps. T-Mobile in particular gates daily volume by Trust Score. |
| **CTIA** | The wireless-industry trade association that publishes the Messaging Principles & Best Practices that underpin acceptable messaging conduct (consent, opt-out, content rules). |
| **TCR (The Campaign Registry)** | The central registry that stores Brand and Campaign records. Brands are vetted and Campaigns are registered against TCR; carriers consult TCR data to decide how to treat traffic. Brand vetting produces a Trust Score that influences throughput. |
| **CSP (Campaign Service Provider) - Twilio's role** | Twilio is a registered CSP. A CSP connects businesses (and software vendors) to TCR and the carriers, submits Brand and Campaign registrations on their behalf, and provisions the messaging path. Twilio exposes this through the Console and via APIs. |
| **DCA (Direct Connect Aggregator)** | An intermediary that connects the CSP layer to specific carriers and passes registered traffic through. (Carrier-specific surcharges flow through this layer.) |
| **Business / sender (the "Brand")** | The legally identifiable entity that wants to send A2P messages. It must be registered as a Brand. |
| **ISV (Independent Software Vendor)** | A software company embedding Twilio's APIs into its own product to power messaging for many downstream customers. ISVs register their customers' Brands and Campaigns via Twilio's APIs. |

**Where Twilio sits:** Twilio (as the CSP) is the bridge. A business registers through Twilio; Twilio submits the Brand to TCR for vetting and registers Campaigns; carriers (via the DCA layer) honor the registered traffic with the appropriate throughput and filtering treatment.

---

## The Three Registration Layers (In Order)

A2P 10DLC registration is layered. You complete them in this order, because each layer depends on the one before it.

### Layer 1 - Customer Profile / Business Identity (Trust Hub)

Before registering a Brand, you establish **who you are** as a business inside Twilio's **Trust Hub**. This is the business-identity foundation: your legal business name, address, Tax ID / business identifiers, and authorized representative details. This profile is the identity record that subsequent Brand and Campaign registrations attach to. ISVs registering on behalf of customers capture each customer's business identity at this layer.

### Layer 2 - Brand Registration (with TCR)

A **Brand** answers the question: **who is sending these messages?** You provide information about the sending business so carriers know you are a legitimate sender. This Brand record is registered with **The Campaign Registry (TCR)**.

- Standard and Low-Volume Standard Brands require a **Tax ID** (for example, an EIN in the US, a Canadian Business Number in Canada, or the equivalent elsewhere).
- Brand vetting produces a **Trust Score** that influences allowed throughput, especially T-Mobile daily volume.
- Sole Proprietor Brands are intended for very small senders without a business Tax ID (they use an individual identity instead of an EIN).

### Layer 3 - Campaign Registration / Use Case

A **Campaign** answers: **what are you sending, and how do recipients consent?** It includes how end users **opt in**, **opt out**, and get **help**, plus a description of the **purpose** (use case) of your messages. The Campaign is the record that links your Brand to the **types of messages** you plan to send and is maintained with TCR. A Campaign is associated with a **Messaging Service**, and the phone numbers you send from live in that Messaging Service.

You must have an **approved Brand before you can register a Campaign.**

> **Note on terminology:** Twilio's own overview frames the two main registration components as **"Create a Brand"** and **"Create a Campaign,"** with the business-identity / Customer Profile work in Trust Hub being the prerequisite foundation that the Brand attaches to. So practically, the flow is: establish identity in Trust Hub → register the Brand → register the Campaign(s).

---

## Brand Types

Twilio offers different Brand types depending on the kind of customer you are and the volume/throughput you need. Choose based on current and expected messaging volume.

| | **Sole Proprietor Brand** | **Low-Volume Standard Brand** | **Standard Brand** |
| --- | --- | --- | --- |
| **Tax ID required** | No (individual identity) | Yes | Yes |
| **Campaigns per Brand** | One Campaign per Brand | Up to five Campaigns, unless a clear and valid business reason is provided for exceeding the limit | Up to five Campaigns, unless a clear and valid business reason is provided for exceeding the limit |
| **Daily message volume** | 1,000 SMS segments and MMS per day to T-Mobile (~3,000 SMS segments and MMS per day across US carriers) | Up to 2,000 SMS segments and MMS per day to T-Mobile (~6,000 SMS segments and MMS per day across US carriers); companies in the Russell 3000 Index can send up to 200,000 SMS segments and MMS per day to T-Mobile | From 2,000 and up to **unlimited** SMS segments and MMS per day to T-Mobile, depending on your **Trust Score** |
| **Throughput** | Lowest | Lower than Standard | Highest (scales with Trust Score) |

**Brands per Tax ID:** Each Tax ID may be used to register **up to five** Standard / Low-Volume Standard Brands. Additional Brands beyond five will still register, but their Campaigns may be rejected during manual Campaign Vetting unless a clear and valid business reason is provided.

---

## Customer Types

How you register depends on what kind of Twilio customer you are.

| Customer Type | Description | How they register |
| --- | --- | --- |
| **Direct Brand** | A business owner using Twilio messaging to send/receive SMS with their own customers. Has a business Tax ID (not a US Social Security Number). | Through the Twilio Console A2P onboarding flow. |
| **Independent Software Vendor (ISV)** | A software company that embeds Twilio's APIs into its product to power messaging for its own customers. | Through the Twilio Console for its own business, and via Twilio's A2P 10DLC APIs to register each downstream customer's Brand and Campaign. |
| **Sole Proprietor** | A very small sender without a business Tax ID. | Through the dedicated Sole Proprietor registration flow (Direct or ISV variant). |

---

## Campaign Use Case Types

The Campaign **use case type** describes the general kind of messages you will send (for example, marketing or account verification). Categories:

- **Standard** - the common business use cases (e.g., marketing, account notifications, two-factor authentication, customer care). See Twilio's full list of standard use cases.
- **Low-Volume Mixed** - a lower-volume, lower-throughput option (fewer than 2,000 message segments per day on T-Mobile) with a lower monthly fee.
- **Special** - for specific senders such as non-profits and emergency services.

Different campaign types carry different **monthly fees** and **throughput** allowances. Note that **Low-Volume Standard Brands receive lower throughput** for their Campaigns than Standard Brands.

---

## Who Needs A2P 10DLC

You need A2P 10DLC registration if you send **A2P SMS or MMS to US recipients from US 10DLC (Local) numbers** through Twilio. This covers essentially all business/application messaging over local long codes: marketing, notifications, reminders, customer care, alerts, and so on.

**Exceptions / alternatives:**

- If you are sending **only user-verification (OTP / 2FA) messages**, you can use **Twilio Verify** instead of registering for A2P 10DLC.
- If you message US users via **Toll-Free** numbers or **Short Codes**, those are separate systems with their own verification/approval (not A2P 10DLC registration).

---

## What Happens If You Don't Register

Sending unregistered A2P traffic over 10DLC numbers carries real consequences:

- **Higher message filtering** - carriers filter (silently drop or block) more of your unregistered traffic, reducing deliverability.
- **Lower throughput** - unregistered senders do not receive the elevated throughput that registration unlocks.
- **Additional carrier fees** - customers who send from a Twilio 10DLC number **without registering will incur additional carrier fees** for unregistered traffic, on top of normal messaging costs.
- **Blocking** - carriers can outright block non-compliant or abusive unregistered traffic.

Registering reverses these: **lower filtering, higher throughput, and avoidance of unregistered-traffic surcharges.**

---

## End-to-End Timeline Expectations

Timelines vary by Brand type, vetting load, and whether manual Campaign Vetting is triggered. General expectations:

| Step | Typical experience |
| --- | --- |
| **Customer Profile / business identity (Trust Hub)** | Submitted in the Console; identity is captured immediately. Required before Brand registration. |
| **Brand registration / vetting** | Sole Proprietor and Low-Volume Standard Brands typically resolve quickly (often near-immediate to a short wait). Standard Brand vetting (and any **Secondary / external vetting**) can take longer because it involves a more thorough identity check that feeds the Trust Score. |
| **Campaign registration / vetting** | Many Campaigns are approved quickly, but some go through **manual Campaign Vetting**, which adds time and can result in rejection if the use case, opt-in flow, or Brand-per-Tax-ID limits aren't satisfied. Twilio has noted that elevated campaign-submission volume can extend review times. |

Plan for variability: a clean Sole Proprietor or Low-Volume Standard path can be fast, while a Standard Brand with secondary vetting plus a manually reviewed Campaign can take materially longer. Always allow buffer time before a launch date.

---

## Cost Summary

> The figures below reflect fees published by Twilio in its Help Center. **Fees are set by TCR and the carriers and change periodically** - confirm current pricing in the Twilio Help Center article "What pricing and fees are associated with the A2P 10DLC service?" before quoting.

| Fee | What it covers | Approximate amount (per Twilio Help Center) |
| --- | --- | --- |
| **Standard Brand registration (one-time)** | Registering a Standard Brand with TCR | ~$44 one-time |
| **Low-Volume Standard Brand registration (one-time)** | Registering a Low-Volume Standard Brand | ~$4 one-time |
| **Sole Proprietor Brand registration (one-time)** | Registering a Sole Proprietor Brand | ~$4 one-time |
| **Secondary / external vetting (optional, often required for Standard)** | Deeper third-party identity vetting that raises Trust Score and unlocks higher throughput; effectively bundled into Standard Brand onboarding | ~$40 per Brand (~$41.50 in some Standard-registration bundles) |
| **Campaign vetting (one-time, per campaign)** | One-time vetting of a Standard Campaign | ~$15 per campaign |
| **Campaign monthly fee (recurring, per campaign)** | Maintaining the Campaign record with TCR; varies by use case | ~$1.50–$10 per campaign per month |
| **Per-message carrier fees (recurring)** | Carrier surcharges (T-Mobile, AT&T, Verizon) applied per message segment; set by carriers and updated periodically | Small per-segment surcharge, varies by carrier and direction; **unregistered** traffic incurs **higher** carrier fees |

Notes:

- **Low-Volume Standard and Sole Proprietor Brands do not include Secondary Vetting**, which is part of why their registration fee is lower and their throughput is capped lower.
- **Standard Brand** total cost is effectively the brand-registration fee plus its bundled vetting, then per-campaign vetting and monthly fees on top.
- Per-message **carrier surcharges are separate** from Twilio's per-message price and from TCR registration fees, and they are the line item most likely to change.

---

## Comparison to Toll-Free and Short Codes

A2P 10DLC is one of three ways to send A2P messages to US recipients. Toll-Free and Short Codes are **not** part of the A2P 10DLC system.

| | **10DLC (Long Code)** | **Toll-Free** | **Short Code** |
| --- | --- | --- | --- |
| **Number format** | 10-digit local (e.g., +1 area-code number) | Toll-free prefix (e.g., 800, 888, 877) | 5–6 digit short number |
| **Compliance process** | A2P 10DLC registration (Brand + Campaign via TCR) | Toll-Free Verification (separate process; no TCR Brand/Campaign) | Short Code application and carrier approval |
| **Throughput** | Scales with Brand type and Trust Score | Generally higher than unverified long code; verified toll-free supports solid throughput | Highest throughput of the three |
| **Setup effort / cost** | Moderate (registration fees + monthly campaign fees) | Lower setup than short code; verification required | Highest cost and longest lead time; leased monthly |
| **Best for** | Most business SMS/MMS at moderate scale from a local presence | Businesses wanting a recognizable toll-free presence | Very high-volume programs needing maximum throughput and a memorable code |

If you only send **OTP / verification** messages, **Twilio Verify** is an alternative to all three for that specific purpose.

---

## Key Terminology Glossary

- **A2P** - Application-to-Person messaging: SMS/MMS sent from an application or business to a person.
- **P2P** - Person-to-Person messaging: ordinary texting between two individuals.
- **10DLC** - 10-digit long code; a standard 10-digit US local phone number used for messaging. Shown as "Local" number Type in Twilio.
- **TCR (The Campaign Registry)** - The central registry that stores Brand and Campaign records and vets Brands; carriers rely on TCR data to govern traffic.
- **CSP (Campaign Service Provider)** - A provider (such as Twilio) registered to connect businesses and ISVs to TCR and the carriers, submitting Brand/Campaign registrations and provisioning messaging.
- **CTIA** - The wireless-industry association that publishes Messaging Principles & Best Practices governing acceptable messaging conduct.
- **DCA (Direct Connect Aggregator)** - An intermediary connecting the CSP layer to specific carriers and routing registered traffic through to them.
- **Brand** - The registered, legally identifiable sending business. Answers "who is sending?" Tied to a Tax ID for Standard/Low-Volume Standard types.
- **Campaign** - A registered messaging program tied to a Brand. Answers "what are you sending and how do recipients consent?" Includes opt-in/opt-out/help flows and the use case. Associated with a Messaging Service.
- **Use Case** - The category of a Campaign's messages (e.g., marketing, 2FA, customer care). Falls under Standard, Low-Volume Mixed, or Special; affects monthly fee and throughput.
- **Trust Score** - A score produced by Brand vetting (raised by secondary/external vetting) that determines allowed throughput, particularly T-Mobile daily message volume for Standard Brands.
- **Throughput** - The rate at which a sender may deliver messages (often expressed as message segments per second/day). Gated by Brand type, Trust Score, and carrier limits.
- **Secondary Vetting (External Vetting)** - A deeper third-party identity check that increases Trust Score and unlocks higher throughput; bundled into Standard Brand onboarding.
- **Messaging Service** - A Twilio container that groups phone numbers and is associated with a registered Campaign; messages are sent from numbers within it.
- **Customer Profile (Trust Hub)** - The business-identity record in Twilio's Trust Hub that A2P Brand and Campaign registrations attach to.
- **ISV (Independent Software Vendor)** - A software company embedding Twilio APIs into its product and registering Brands/Campaigns on behalf of its downstream customers.
- **Sole Proprietor** - A small sender registering without a business Tax ID, using an individual identity, with the lowest throughput tier.
