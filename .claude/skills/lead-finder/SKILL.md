---
name: lead-finder
description: Build an outreach-ready lead list of local businesses for free with your own Apify, TREG and Reoon keys. Scrapes Google Maps for a business type in a city, flags which ones are running Facebook ads right now (the Facebook Ad Library), finds the owner's name and email, verifies the email, and writes one CSV (business, website, phone, owner_name, email, verified, source, ad_found). Shows a spend estimate and waits for the user's OK before any paid call. Triggers on /lead-finder, find leads, find roofers in [city], find [business type] in [city], build a lead list, scrape google maps, who is running facebook ads, find businesses running ads, find the owner's email, prospect list for [niche], get me leads for [city], layup list, leaky bucket leads.
---

# Lead Finder

Turn "roofers in Austin, TX" into a CSV of real businesses with the owner's name, a checked email, and a flag for who is spending money on Facebook ads right now. Those advertisers are the easiest first clients for a voice agent: they already pay for leads, and most of those leads hit voicemail after hours.

Everything runs through one stdlib Python script in this kit: `lead-finder/lead_finder.py`. The user brings their own keys. Nothing paid runs until they say yes to the estimate.

Full human docs (setup screenshots aside): `lead-finder/README.md`.

## When to invoke

- "Find roofers in Austin TX"
- "Build me a lead list of HVAC companies in Phoenix"
- "Which plumbers in Denver are running Facebook ads?"
- "Get me 50 med spas in Miami with owner emails"
- "I need leads for my first voice agent client"
- "/lead-finder"

Do NOT invoke for:

- Calling or texting leads. This skill builds the list; the user does the outreach.
- Consumer (B2C) lists. This is a B2B tool only.
- Anything that needs a Leadlock API key. This skill does not touch the Leadlock API.

## Setup check

Before the first run in a session, check the keys without printing them:

```python
from pathlib import Path
env = {}
p = Path("./.env")
if p.exists():
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")

def state(name):
    v = env.get(name, "")
    if not v or "paste_your" in v or v == "your-team-slug":
        return "missing"
    return "set"

for name in ("APIFY_TOKEN", "TREG_TOKEN", "TREG_ORG", "REOON_API_KEY"):
    print(name, state(name))
```

Then tell the user what they can do with what they have:

| Keys present | What works |
|---|---|
| APIFY_TOKEN only | Business list + `ad_found` flag. No owner names (`verified=skipped`). |
| + TREG_TOKEN and TREG_ORG | Owner names, email guesses, paid email finder. Emails say `not_checked`. |
| + REOON_API_KEY | Full run: every email checked, `verified` column is trustworthy. |

If `APIFY_TOKEN` is missing, stop and walk them through getting it:

```
Lead Finder needs an Apify token (free plan works).

  1. Sign up at https://apify.com
  2. Settings -> API & Integrations -> copy your personal API token
  3. Open .env in this kit and set:
       APIFY_TOKEN=<your token>

Optional but recommended:
  TREG_TOKEN + TREG_ORG  (https://treg.to)   owner names and paid email lookups
  REOON_API_KEY          (https://www.reoon.com)  email verification

Tell me when it's in and I'll run a free dry run first.
```

Never ask the user to paste a key into the chat. They edit `.env` themselves.

## Rules

- **Always dry run first.** Run with `--dry-run` and show the estimate before any paid run. A dry run makes zero network calls.
- **Get an explicit yes before spending.** Only add `--yes` after the user approves the estimate in this conversation. Claude's shell is not a TTY, so without `--yes` the script exits 2 and spends nothing; that is the safety catch, do not work around it.
- **Never print, echo or log a key.** The script masks keys (`abcd...wxyz`). Do not `cat .env`, do not print the env dict, do not put a key in a command line.
- **Never edit `.env` for the user.** Tell them what line to add.
- **Never commit the CSV.** Output goes to `output/`, which git ignores. Do not `git add` anything under `output/`.
- **A Maps run that returns 0 places is an input problem**, not "no businesses". The script exits 1 and says so. Fix the location or keyword, do not rerun the same thing.
- **`--treg-budget` is a hard cap.** Do not raise it without asking. Misses are free, hits cost about $0.02.
- **Do not send anything.** This skill builds a list and drafts messages. The user sends, calls and DMs. Point them at the compliance section every time they ask for outreach copy.
- **B2B only.** If the user describes a consumer list, say plainly that this tool is not for that.

## Required inputs

Ask only for what is missing, in one message:

1. **Business type** (`--keyword`). Plural trade words work best: "roofers", "hvac", "plumbers", "med spa", "dentists".
2. **Location** (`--location`). "City, ST" format: "Austin, TX". A metro name alone usually works; a ZIP code may not.
3. **How many** (`--limit`). Default 20 for a first run. Max 200.
4. **Advertisers only?** (`--ads-only`). Recommend yes for a first outreach batch: those are the layups.

Optional, only if they bring it up: `--contacts` (scrape website emails, +$0.002 per place), `--no-ads`, `--treg-budget`, `--no-treg`, `--no-verify`, `--out`.

## Execution

### Step 1: dry run

```bash
python3 lead-finder/lead_finder.py --keyword "roofers" --location "Austin, TX" --limit 20 --dry-run
```

Show the user the estimate block it prints, for example:

```
Spend estimate (upper bound, nothing has been charged yet):
  Google Maps via Apify    20 places x $0.004   = $0.0800
  Facebook ads via Apify   20 ads x $0.0058      = $0.1160
  TREG owner lookups       capped by --treg-budget = $0.2500  (misses are free)
  Reoon verification       up to 360 checks from your prepaid credits
  Cash ceiling this run    $0.45
```

Explain in one line: this is the most it can cost, the real number is usually lower because TREG misses are free.

Ask: "Run it for real?"

### Step 2: real run (only after a yes)

```bash
python3 lead-finder/lead_finder.py --keyword "roofers" --location "Austin, TX" --limit 20 --yes
```

Add `--ads-only` if they chose it. Runs take 1 to 5 minutes: the Maps and Facebook stages wait on Apify, and each TREG lookup can take 30 to 60 seconds. Tell the user it is running and roughly how long.

### Step 3: read the result

The last stdout lines are:

```
rows=18 verified=7 ads_found=6 treg_spent=$0.1120
Saved: output/leads-roofers-austin-tx-2026-10-19.csv
```

Exit codes:

| Code | Meaning | What to tell the user |
|---|---|---|
| 0 | CSV written with rows | Summarize the counts, offer the next step |
| 1 | Maps stage failed or APIFY_TOKEN missing | Read the ERROR line; fix the key or the location |
| 2 | Not confirmed | You forgot `--yes` after their approval, or they declined |
| 3 | 0 rows (header-only CSV) | Nothing matched; widen the keyword or location, or drop `--ads-only` |

Every `WARNING:` line on stderr matters. Relay them, in plain words:

- `fb_ads=0` means no active advertisers turned up for that search. The list still works; `ad_found` is just `no` everywhere.
- `treg refused the token` means TREG_TOKEN or TREG_ORG is wrong.
- `treg balance is too low` means their TREG account needs a top up, or rerun with `--no-treg`.
- `TREG budget spent` means the cap was hit; some rows were not looked up.
- `rejected the request fields` is a bug in the script, not a miss. Ask them to report it.
- `reoon returned HTTP 402` means Reoon credits ran out.

### Step 4: summarize the CSV

Read the CSV (stdlib `csv`) and report:

```
18 roofers in Austin, TX
  6 running Facebook ads right now
  7 with a verified owner email
  4 catch-all (email is a best guess, call instead)

Top layups (running ads + verified email):
  1. <business>  <owner>  <email>
  2. ...

File: output/leads-roofers-austin-tx-2026-10-19.csv
```

Sort the "top layups" by `ad_found=yes` first, then `verified=verified`, then `catch_all`. Show at most 10.

### Step 5: offer the next move

Offer, do not do:

- "Want me to draft the after-hours call script, email and DM for the top layups?" (Templates below.)
- "Want a demo agent for one of them?" Hand off to the `prospect-demo` skill with the business's website.
- "Want a bigger list?" Rerun with a higher `--limit` or a nearby city.

## Templates

Fill these per lead from the CSV. Keep them short. The user sends them; you never do.

### After-hours call (the user dials by hand, around 7pm their time)

```
If it goes to voicemail, hang up. That's the proof.
Next morning, call back:

"Hi, is this <owner first name>? This is <your name>. Quick one:
I called your shop last night around 7 and got voicemail.
I saw you're running Facebook ads right now, so some of those
leads are probably calling after hours too.
I set up voice agents that answer every call, day or night,
and book the job on your calendar. Worth a 10-minute look?"
```

### Email (verified rows only)

```
Subject: your 7pm calls

Hi <owner first name>,

I called <business> last night around 7 and hit voicemail.
You're running Facebook ads right now, so I'm guessing some of
the leads you pay for are calling after hours too.

I build voice agents that pick up every call, answer questions,
and book the job straight onto your calendar.

Want me to send a 2-minute demo built for <business>?

<your name>
<your business name>
<your physical mailing address>
Not interested? Reply "stop" and I won't email again.
```

The address and the opt-out line are required by CAN-SPAM. Do not remove them.

### Facebook page DM

```
Hey <owner first name>, saw your ad. Called the shop last night
around 7 and got voicemail. Do after-hours callers get a call
back, or do they go to whoever picks up first?
```

## Compliance

Say this whenever the user asks for outreach copy or a calling plan. It is not legal advice.

- **B2B only.** Business owners about their business.
- **Email (CAN-SPAM):** real name and business, honest subject, physical mailing address, working unsubscribe, honor opt-outs within 10 business days, keep a suppression list.
- **Calls and texts (TCPA):** no autodialed or prerecorded calls and no automated texts to cell phones without prior express consent. Many Google Maps numbers are the owner's cell, so dial by hand.
- **Do Not Call:** check the national and state registries, keep an internal do-not-call list, stop the moment anyone asks.
- **State rules** (for example Florida, Oklahoma, Washington) can be stricter. Check theirs and the user's.

## Gotchas

- **The official Meta Ad Library API will not work for this.** In the US it only covers political and issue ads; regular business ads are EU and UK only. The script uses the Apify actor that reads the public Ad Library search page instead.
- **The Facebook search has no location filter.** The script searches "<keyword> <city>" and then matches advertisers to Maps listings by website domain or business name. Advertisers it cannot match still appear as `source=facebook_ads` rows.
- **Name matching only strips legal suffixes** (LLC, Inc, Co, Corp, Ltd). "Lone Star Roofing" and "Lone Star Roofing Company" do not match on name; they match only if the websites match.
- **Catch-all domains accept every address**, so Reoon cannot prove anything. The row says `catch_all`. Call those businesses instead of emailing blind.
- **`not_checked` emails are guesses.** Without a Reoon key the script still fills in the most common pattern. Do not send to those without verifying.
- **TREG needs both TREG_TOKEN and TREG_ORG.** The org is the team slug; an identity token without it is refused.
- **TREG lookups are slow** (30 to 60 seconds each). `--workers 3` is the default; going much higher can trip rate limits.
- **Websites that are a Facebook page** count as "no website": there is no domain to look up an owner on, so the row says `skipped`.
- **Prices drift.** The estimate uses published per-event prices from October 2026. The Apify console shows the real charge per run.

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
