---
name: a2p-registration
description: Register your business for A2P 10DLC so your SMS actually gets delivered instead of silently filtered by US carriers. Walks you through all three layers in order - Customer Profile (business identity), Brand Registration (TCR), and Campaign Registration - and fills every field for a one-shot approval using battle-tested templates. Ships the full Twilio reference library (use cases, error codes, consent rules, throughput, prohibited content) plus a generator that turns your brand details into a copy-paste answer sheet. Triggers on /a2p-registration, register A2P, A2P 10DLC, 10DLC registration, register my brand, register a campaign, my texts aren't being delivered, SMS getting filtered, campaign rejected, brand rejected, error 30886, error 30891, error 30892, error 30896, error 30897, error 30909, set up SMS compliance, Twilio campaign registration, get my SMS approved, opt-in compliance, why are my texts not sending.
---

# A2P 10DLC Registration

Get your business registered so US carriers deliver your SMS instead of filtering it. This skill takes you through the whole thing - business identity, brand, and campaign - and fills every field for a **one-shot approval**, because every rejected resubmission costs a vetting fee and burns 1-2 weeks.

It is built from a real Marketing campaign that got **rejected three times** (errors 30896 → 30886 → 30891) before approval. The templates here are the version that finally passed, and `playbook/rejection-recovery.md` is the map of exactly what each rejection meant and how it was fixed. You are starting from the approved end state, not the naive first attempt that gets bounced.

## When to invoke

- "Register my business for A2P 10DLC" / "set up 10DLC"
- "My texts aren't getting delivered" / "SMS is being filtered"
- "My campaign got rejected - error 30886 / 30891 / 30896 / 30897 / 30909"
- "My brand was rejected" / "EIN mismatch"
- "Help me fill out the Twilio campaign registration"
- "What use case should I pick?"
- "Write my opt-in / consent flow"

## What A2P 10DLC is (30-second version)

US carriers require every business that sends **A**pplication-**to**-**P**erson messages from a **10-D**igit **L**ong **C**ode (a normal local number) to register. Unregistered traffic gets filtered, blocked, or fined. Registration has **three layers, in this order**:

1. **Customer Profile** (Trust Hub) - verify your business identity. Legal name + EIN must match IRS records exactly.
2. **Brand Registration** (via The Campaign Registry / TCR) - establishes your business with the carriers and assigns a **trust score** that drives your throughput.
3. **Campaign Registration** - describes *what* you send, *to whom*, *why*, and *how they consented*. This is where almost all rejections happen, and it is the part this skill spends the most effort on.

Full detail: `reference/a2p-10dlc-overview.md`.

## The #1 rule: do it once, correctly

The overwhelming majority of rejections come from **consent/opt-in** and **campaign description** problems - both fully preventable. Before you submit anything, the discipline is:

- **Marketing use case = marketing messages ONLY.** If you also send appointment reminders, order updates, or account alerts, you do **not** want Marketing - you want **Mixed** or **Low Volume Mixed**. Mixing transactional content into a Marketing registration is an instant 30886. (`reference/campaign-use-cases.md`)
- **Your opt-in checkbox must be unchecked by default and optional** (not required to submit the form). This is the single most common rejection. (`reference/consent-and-cta.md`)
- **Your website, privacy policy, and terms must be live and publicly reachable** (not behind a login, no typos in the URL field - Twilio does not validate the URL on submit). (`reference/error-codes.md` → 30891)
- **No URL shorteners** (bit.ly, tinyurl) in sample messages. Use your full domain. (30892)
- **Privacy policy must explicitly say mobile data is not shared** with third parties for marketing. (`templates/privacy-policy-clause.md`)

## How to run this

### Phase 1 - Identity & Brand (do first, they gate everything)

1. Read `reference/brand-registration.md`. Gather: legal business name (exactly as on your IRS CP-575 / 147c letter), EIN, business address, business type, website, an authorized representative, and a support email + phone.
2. If you have an EIN, register as a **Standard** brand. No EIN → **Sole Proprietor** path (lower throughput; see the reference for the tradeoff).
3. Submit the Customer Profile, then the Brand. Brand vetting takes days. While it processes, do Phase 2.

If the brand fails, it is almost always a **name/EIN/address mismatch with the IRS**. `reference/error-codes.md` (brand section) has the exact fix per code (30703, 30795, 18011).

### Phase 2 - Pick the use case (decide before you write anything)

Open `reference/campaign-use-cases.md` and choose honestly based on **everything** you actually send from this number:

- Only promotional content → **Marketing**
- Promotional + transactional, low volume → **Low Volume Mixed**
- Promotional + transactional, higher volume → **Mixed** / **Standard**

Picking the wrong use case is the root of the 30886 / 30893 rejection family. Decide this first; it determines how you word the description and samples.

### Phase 3 - Fill the campaign (where one-shot approval is won)

1. Run the generator to produce your filled answer sheet:
   ```bash
   python3 generate_answers.py
   ```
   It asks for your brand name, website, support email, booking/CTA link, and use case, then writes a `my-a2p-answers.md` with every field filled from the approved templates. (Stdlib only, no installs.)
2. Or fill by hand from `templates/` - each file maps to one Twilio field:
   - `templates/campaign-description.md` - the who/what/why compliance paragraph
   - `templates/sample-messages.md` - 5 compliant samples
   - `templates/consent-flow.md` - the "how do users consent?" field (most scrutinized)
   - `templates/keywords-and-autoreplies.md` - opt-in/out/help keywords + confirmation messages
   - `templates/privacy-policy-clause.md` - the required mobile-data language for your privacy page
3. Walk `playbook/one-shot-approval.md` field by field as you enter everything in the Twilio Console.
4. **Before clicking Create**, run every box in `pre-submission-checklist.md`. This is the gate that catches the typo, the missing footer link, the required checkbox.

### If you get rejected

Go straight to `playbook/rejection-recovery.md`. Find your error code, apply the documented fix, **edit** the existing campaign (don't delete and recreate - recreating triggers a fresh vetting fee), and resubmit. One exception: **30897 (disallowed content) cannot be resubmitted** - the content itself is the problem.

## Reference library (scraped from Twilio's official docs)

| File | Use it for |
|---|---|
| `reference/a2p-10dlc-overview.md` | The ecosystem, the 3 layers, timelines, full cost table |
| `reference/brand-registration.md` | Business identity, EIN exact-match rule, brand types, trust score |
| `reference/campaign-use-cases.md` | Every use case + the Marketing-only rule + how to choose |
| `reference/campaign-registration-fields.md` | Every campaign field with exact character limits |
| `reference/consent-and-cta.md` | Opt-in rules - the #1 rejection source |
| `reference/error-codes.md` | Every rejection code → root cause → fix (the troubleshooting bible) |
| `reference/throughput-and-trust-scores.md` | How many messages/day you can send and how to raise it |
| `reference/prohibited-content-shaft.md` | SHAFT + restricted content + carrier fines |

## Notes

- This skill prepares everything and tells you exactly what to enter, but the actual submission happens in **your** Twilio Console (or your messaging provider's portal) - there is no public API to bypass the human review, and you must be the one to attest to your own consent practices.
- A2P registration is the pre-launch gate for **every** number that sends business SMS. If you onboard clients, fold this into your onboarding so each new sending number is registered before it goes live.
- Throughput figures in the reference are carrier-controlled and shift over time. The docs flag where to verify live values; treat them as direction, not contracts.
