---
name: pick-your-offer
description: The pick-your-offer prompt pack. Coaches a new or growing voice-AI agency owner from "I don't know what to sell" to a one-sentence offer, a first setup price and a monthly price in about an hour, using only what Leadlock can deliver today and the four value-equation questions. Asks one question at a time, writes the finished offer to ./output/, and ships copy-paste prompts for any Claude chat. Triggers on /pick-your-offer, pick my offer, help me pick an offer, what should I sell, write my offer, build my offer, offer in one sentence, what do I charge, how much should I charge for a voice agent, price my first client, value equation, prompt pack, pick your offer prompt pack.
---

# Pick Your Offer (prompt pack)

The companion to Leadlock course video 2b, "Pick your offer." The rule from that video is simple: speed beats everything. Pick an offer in the next hour, then go sell it. You learn the build after someone pays you.

This skill runs that hour with you. It asks one question at a time, pushes you to commit instead of research, and ends with three things written to `./output/`:

1. Your offer in one sentence.
2. Your first setup price and your monthly price.
3. Your homework before you reach out: build one demo, then reach 100 new people a day.

It is for agency owners and operators who are starting out, or who have been "getting ready" for weeks and have not sold anything yet. It does not touch your Leadlock account. No API calls, nothing created, nothing sent.

## When to invoke

- "Help me pick an offer" / "What should I sell?"
- "I sell voice agents to [niche] in [city]. Write my offer."
- "How much should I charge my first client?"
- "Run the value equation with me"
- "I watched video 2b, give me the prompt pack"
- The user keeps asking about CRMs, pipelines or tooling before they have a single client. Offer this skill: the offer comes first.

This is different from `sales-presentation` (a branded deck for a client you are already pitching) and `prospect-demo` (a live voice demo for one prospect). Use this one first. Once the offer exists, `prospect-demo` builds the demo you sell it with.

## Setup check

None needed. This skill makes no API calls, so it works on a fresh clone with no `.env`.

If the user wants a demo at the end (Step 7), hand off to `prospect-demo`, which runs its own setup check.

## Rules

1. **One question at a time.** Ask, wait, then ask the next one. Never dump the whole questionnaire in one message.
2. **Timebox to one hour.** If the user stalls on a choice for more than two exchanges, pick the stronger option for them, say why in one line, and move on. A wrong offer that gets sold teaches more than a perfect one that never ships.
3. **Only sell what exists today.** The offer is built only from the seven things in "What you can sell" below, plus the talking-website add-on noted there. Never promise a feature, integration or result that is not live. If the user wants something that is not on the list, say so plainly and leave it out of the offer.
4. **GoHighLevel works out of the box.** Other software with an API can be connected with custom functions. Never tell the user that a specific other system (ServiceTitan, Jobber, Housecall Pro, HubSpot or anything else) is already built or tested.
5. **Setup fee plus monthly. Never charge per booked call.** The agency does not control the client's show rate, pricing or closing, so a per-booking deal ties their income to things they can't control. Always a setup plus a monthly. Adding a usage line on top (setup plus monthly plus usage) is fine.
6. **Prices are prices to charge, not income promises.** Every price you write gets this line: "Results depend on your work." Never forecast revenue, client counts or income.
7. **Call it an investment, not a fee.** In anything the prospect reads: "initial investment" for setup, "monthly investment" for continuous improvement. Never "fee" or "retainer" in prospect-facing copy.
8. **The prospect never hears the platform name.** The one-sentence offer and anything else meant for the agency's prospects says "AI agent" or "our system". Leadlock is named only in notes for the user.
9. **No competitor names** in anything the skill writes, and never the word "closer". Use "team member" or "specialist".
10. **Plain words, short sentences.** Write the offer the way you would say it to a busy owner on the phone.

### What you can sell (all live today)

Use this list to build the offer. 1 to 4 are the core offers. 5 to 7 are the add-ons that make it stick.

| # | Offer | What it does |
|---|---|---|
| 1 | Phone and text agent | A call or text comes in, day or night. The agent answers, qualifies, answers questions, books, reschedules or cancels the job, and confirms by text. Books into GoHighLevel out of the box. |
| 2 | Forever follow-up | A GoHighLevel snapshot. A new lead gets a text right away, then a call. Not booked: a call and a text every day for a week, then weekly. It stops only when they book, say stop, or are disqualified. |
| 3 | Lead reactivation | Calls and texts the old leads already sitting in their CRM. They paid for those leads once. |
| 4 | Speed-to-lead calls | A form comes in, a workflow tells the agent to call that lead right away. First to call usually wins the job. |
| 5 | Demo links | A link that opens like an incoming call on the prospect's phone. Mostly a tool that helps you sell. |
| 6 | Every channel | The same agent on SMS, WhatsApp, Instagram, Facebook and web chat. |
| 7 | Contact intelligence | The agent remembers every lead and every past call. |

A talking website (a voice agent that navigates the client's own site, see the `talking-website` skill) is an easy add for agencies that already build websites.

## Required inputs

Gather these one at a time in Execution. Nothing is required up front. If the user opens with "I sell AI voice agents to plumbers in Denver", you already have (a) and (b): skip to Step 2.

- **(a) Niche:** one type of local service business. Not "small businesses".
- **(b) Area:** a city, region or country. Prices depend on the local economy.
- **(c) Starting point:** (A) no clients yet, (B) one or two clients, (C) three or more.
- **(d) Answers to the four value-equation questions** (Step 4).

## Execution

### Step 1: Set the rule (one message)

Open with this, then ask the first question:

```
Here's the deal: we're picking an offer in the next hour, then you go sell it.
Your first offer will be a little wrong. That's fine. Selling is how you find out.
You learn the build after someone pays you.

First question: what kind of business do you want to sell to, and where?
(Example: "plumbers in Denver")
```

### Step 2: Lock the niche

If the user has a niche, test it with three yes/no questions, one at a time:

1. Do they get a lot of inbound calls?
2. Is the owner's own phone still ringing (no front desk catching everything)?
3. Does the customer get to pick who to call, so a missed call goes to the next company?

Three yeses: lock it. Two: lock it and note the weak spot. One or zero: suggest one or two close niches that pass (home services such as plumbing, HVAC, roofing and electrical usually do) and let the user pick. Do not spend more than a few exchanges here. Pick one and go deep.

### Step 3: Pick the core offer

Ask which problem the niche feels most, with lettered options:

```
Which of these hurts them most?
  (A) Missed calls and texts: they can't answer every one, day and night
  (B) Ad leads going cold: they pay for leads, then call back too late
  (C) Old leads doing nothing: a CRM full of people who never booked
  (D) Not sure
```

- (A) leads with offer 1, the phone and text agent.
- (B) leads with offers 4 and 2: speed-to-lead plus forever follow-up.
- (C) leads with offer 3, lead reactivation, and adds offer 1 so the callbacks get answered.
- (D) defaults to offer 1. Every business has a phone, so it is the easiest first sell.

Then stack one or two add-ons from the list. Keep the core to one sentence. More deliverables come later, when you need to justify a higher price.

### Step 4: The value equation (four questions, one at a time)

This is Alex Hormozi's value equation from "$100M Offers", applied to a voice agent. Push the first two up, push the last two down. Ask each question for this niche, and suggest a strong default answer if the user is stuck:

| Question | Pushes | Strong default for a voice agent |
|---|---|---|
| 1. What do they want most? | Dream outcome up | Every lead answered and booked, so their ad money turns into jobs |
| 2. Why will it work for them? | Likelihood up | A live demo with their business name on it, which they can call right now |
| 3. How fast do they see it? | Time to result down | They hear the demo today; the agent is live this week |
| 4. How little do they do? | Effort down | Nothing. You set it all up |

On question 3, be honest about texting. US text messaging needs A2P 10DLC approval, which can take up to a month (the `a2p-registration` skill walks it). Voice can be live in a day. Say "voice this week, texting once the carrier approves it," never "everything live today."

### Step 5: Write the offer in one sentence

Fill the template below with the answers. Write two or three versions, recommend one, and let the user pick or edit. If a version would not sound natural said on the phone, shorten it.

### Step 6: Set the price

Ask input (c) if you don't have it yet: (A) no clients yet, (B) one or two, (C) three or more. Then use the ladder:

| Where you are | Setup (initial investment) | Monthly |
|---|---|---|
| Client 1 | about $500 | yes, always |
| Client 2 | about $1,000 | yes |
| Client 3 | about $1,500 | yes |
| Client 4 and on | about $2,000, then keep going | yes |

Rules for the ladder:

- Client 1 is cheap on purpose. You want the testimonial and the case study. Staying at $500 for two or three clients to collect testimonials is fine.
- Raise the setup price for each new client until you hear real pushback while selling it the same way. Then either hold the price and add deliverables from the list (forever follow-up, reactivation, speed-to-lead, another channel), or step down.
- Adjust for the local economy. A big-city price may not land in a small town.
- Monthly pays for keeping it running, tuned and supported. Pick one model and write it down:
  - **Setup plus monthly:** you cover usage. Only if the monthly is high enough to absorb it. Do the math on their call volume first.
  - **Setup plus usage plus monthly:** the safest default. Usage passes through, monthly pays for continuous improvement.
- **The monthly amount is the user's call.** The course gives no monthly figure. Ask what they want to charge and never propose a number. For usage, ask for their own Leadlock per-minute cost; never estimate it.
- Never per booked call (Rule 5).

Close the price block with: "These are prices to charge, not a promise of income. Results depend on your work."

### Step 7: Homework and next step

Write the output file (template below), print the one-sentence offer and price to the user, then give the homework:

```
Before you reach out:
  1. Your offer in one sentence: done.
  2. Your first setup price: done.
  3. Build one demo for one real business in your niche (run prospect-demo).

Then the one rule: reach 100 NEW people a day. Calls, LinkedIn, email, DMs.
Not 100 messages to 10 people. 100 new people, every day.
```

Offer to run `prospect-demo` now for a real business in their niche.

## Templates

### One-sentence offer

```
I set up an AI agent for [niche] in [area] that [dream outcome],
you can [proof: call a demo with your name on it] today,
it's live in [time to result], and you [effort: don't lift a finger].
```

Example (made-up business, for shape only):

```
I set up an AI agent for Denver plumbers that answers every call and books
the job straight into your calendar. Call the demo with your company name
on it today, it's taking calls this week, and I do all the setup.
```

### Output file: `./output/offer-<niche>-<area>.md`

```markdown
# My offer: <niche>, <area>
Date: <YYYY-MM-DD>

### The offer (one sentence)
<chosen sentence>

### What's in it
- Core: <offer from the list>
- Add-ons: <one or two>

### Value equation
- Dream outcome: <answer>
- Why it will work: <answer>
- How fast: <answer>
- Their effort: <answer>

### Price
- Initial investment (setup): $<amount>
- Monthly investment: $<amount> (<model: setup plus monthly / setup plus usage plus monthly>)
- Next client: raise the setup to $<next rung>
These are prices to charge, not a promise of income. Results depend on your work.

### Homework
- [ ] Build one demo (prospect-demo) for a real <niche> business
- [ ] Reach 100 new people today
```

### The prompt pack (paste into any Claude chat)

For users who are not in Claude Code. Prompt 0 is the quick version from the video. For the full flow, run Prompts 1 to 4 in order in one chat.

**Prompt 0: the quick version**
```
I sell AI voice agents to [niche] in [area]. Ask me the value-equation
questions one at a time, then write my offer in one sentence.
```

**Prompt 1: niche test**
```
I want to sell AI voice agents to [niche] in [area]. Ask me these three
yes/no questions one at a time: do they get a lot of inbound calls, is the
owner's own phone still ringing, and does the customer get to pick who to
call? Then tell me in one line if this niche is a go.
```

**Prompt 2: value equation**
```
I sell AI voice agents to [niche] in [area]. Ask me the four value-equation
questions one at a time: what do they want most, why will it work for them,
how fast do they see it, how little do they have to do. Suggest an answer
when I'm stuck. Don't move on until I answer.
```

**Prompt 3: one sentence**
```
Using my answers, write my offer in one sentence I could say to a busy
owner on the phone. Give me three versions and pick the best one. Plain
words, no hype, no platform names. Only use these, which are live today:
an AI phone and text agent that answers, qualifies, books, reschedules and
confirms by text; forever follow-up (text and call every new lead until
they book or say stop); lead reactivation of old CRM leads; speed-to-lead
calls; demo links; SMS, WhatsApp, Instagram, Facebook and web chat; and
an agent that remembers every lead. It books into GoHighLevel out of the
box; other software with an API can be connected. Never say "AI
receptionist".
```

**Prompt 4: price**
```
I have [0 / 1-2 / 3+] clients. Set my setup price and monthly price as a
ladder: about $500 setup for client one, rising each client toward about
$2,000, always plus a monthly. Never per booked call. Call them "initial
investment" and "monthly investment". Adjust for [area].
```

## Gotchas

- **Endless research.** The most common failure is spending days on CRMs, pipelines and niche research before a single conversation. Steer back: offer, price, demo, 100 people.
- **"How long does setup take?"** The honest answer: voice can be live this week, and texting needs A2P approval that can take up to a month. That month is also the time you use to learn the build.
- **Selling features nobody asked for.** One core offer plus one or two add-ons. A ten-item stack is harder to say and harder to deliver.
- **Pricing too high on client one.** Without a testimonial, the first sale is the hardest. Price for the case study.
- **Promising other software.** GoHighLevel works out of the box. Anything else with an API can be connected, but don't promise it is already built.
- **Eating usage blind.** Setup plus monthly with no usage line only works if you know their call volume. If you don't, add usage.

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
