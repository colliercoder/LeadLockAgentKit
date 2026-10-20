# Lead Finder

Free lead list builder for the Leadlock Agent Kit. Give it a business type and a city. It hands back one CSV of local businesses with the owner's name, a checked email, and a flag for who is running Facebook ads right now.

```
business,website,phone,owner_name,email,verified,source,ad_found
Summit Roofing LLC,https://summitroofing.com,(512) 555-0101,John Smith,john@summitroofing.com,verified,both,yes
```

(Sample row, made-up business.)

## What it does

| Stage | Tool | What you get |
|---|---|---|
| 1. Google Maps | Apify `compass/crawler-google-places` | Business name, website, phone for every open listing |
| 2. Facebook Ad Library | Apify `apify/facebook-ads-scraper` | Which of those businesses are running ads right now (`ad_found=yes`) |
| 3. Owner + email | TREG people search, free email patterns, TREG email finder | Owner name and the most likely email, cheapest source first |
| 4. Verify | Reoon | `verified`, `catch_all`, `miss` or `not_checked` per email |

Everything is one stdlib Python file. No `pip install`, works on the Python 3.9 that ships with macOS.

## Setup (10 minutes, once)

You bring your own accounts. Every key lives in the kit's `.env`, which git ignores.

1. **Apify** (required). Sign up at https://apify.com, then Settings, then API & Integrations, and copy your personal API token. The free plan includes monthly credit, enough for a few hundred listings.
2. **TREG** (optional, for owner names and paid email lookups). Sign up at https://treg.to and create an API token. Copy your team slug too: an identity token must say which team it is acting for, and TREG rejects calls without it.
3. **Reoon** (optional, strongly recommended). Sign up at https://www.reoon.com, open the Email Verifier dashboard, and copy the API key. Credits are prepaid and cheap.

Then open `.env` at the kit root (copy `.env.example` first if you have not) and fill in:

```
APIFY_TOKEN=paste_your_apify_token_here
TREG_TOKEN=paste_your_treg_token_here
TREG_ORG=your-team-slug
REOON_API_KEY=paste_your_reoon_key_here
```

Only `APIFY_TOKEN` is required. Without TREG you get the business list and the ad flag but no owner names. Without Reoon every email says `not_checked`, which means a guess: verify it before you send.

Check it with a dry run. It prints the plan and a spend estimate and makes zero network calls:

```
python3 lead-finder/lead_finder.py --keyword roofers --location "Austin, TX" --limit 20 --dry-run
```

## Example: roofers in Austin, TX

```
python3 lead-finder/lead_finder.py --keyword roofers --location "Austin, TX" --limit 20
```

It shows the spend estimate (about $0.20 of Apify at 20 places with the ad check on, plus up to your TREG budget) and asks before spending anything. Add `--yes` to skip the prompt in scripts.

The CSV lands in `output/leads-roofers-austin-tx-<date>.csv`. The last line of the run looks like:

```
rows=27 verified=11 ads_found=9 treg_spent=$0.1340
```

Useful flags:

| Flag | What it does |
|---|---|
| `--ads-only` | Keep only businesses running Facebook ads. The best list to start with. |
| `--no-ads` | Skip the Facebook stage (saves about $0.006 per ad). |
| `--contacts` | Also pull emails from each website (+$0.002 per place). |
| `--treg-budget 0.10` | Hard cap on TREG spend for the run (default $0.25). Misses are free. |
| `--no-treg` / `--no-verify` | Skip a paid stage entirely. |
| `--limit 50` | More listings (max 200). |
| `--out my-list.csv` | Pick the file name. |
| `--env-file path` | Read keys from a different env file. |

### What the columns mean

- `source`: `google_maps`, `facebook_ads`, or `both` (on Maps and advertising).
- `ad_found`: `yes` when the business is running an active Facebook ad.
- `verified`:
  - `verified`: Reoon says the mailbox exists and is safe to send.
  - `catch_all`: the domain accepts every address, so nothing can be proven. Send with care, or call instead.
  - `miss`: no address held up.
  - `not_checked`: Reoon was off. Treat it as a guess.
  - `skipped`: no website, or owner lookup was off.

### How the email gets found (cheapest first)

1. TREG people search on the website's domain for the owner's name.
2. Free guesses from that name (`first@`, `first.last@`, `firstlast@`, `flast@`, `firstl@`, `first_last@`, `last@`), each checked with Reoon, stopping at the first verified one.
3. Only if nothing verified (or the domain is catch-all): TREG's paid email finder, then Reoon checks that too.

TREG charges only for hits, and the run stops calling TREG once `--treg-budget` is spent.

### Why not Meta's official Ad Library API?

Meta's official API only returns political and issue ads for the US. Regular business ads are only available through it for the EU and UK. So for a US roofer it returns nothing. The Apify actor reads the public Ad Library search page instead, with the same Apify token, and no Meta developer app or ID check needed.

## The offer: fix the leaky bucket

A business running Facebook ads is paying for every lead. Most of them leak:

- calls after 5pm and on weekends go to voicemail, and the caller hires whoever picks up
- form fills sit for hours before anyone calls back
- nobody follows up after the first try

That is the pitch. You are not selling them more leads. You are plugging the hole in the bucket they already pay to fill. The `ad_found=yes` rows are your layups: they already spend money on leads, so the math is easy for them.

How to reach them, in order:

1. **Call after hours.** Call the business at 7pm. If it goes to voicemail, you have the proof. Open with: "I called your shop last night at 7 and got voicemail. You're running Facebook ads right now, so I'm guessing some of those leads are calling after hours too."
2. **Email the owner.** Use `verified` rows only. Keep it short: one line about the missed call, one line about what an after-hours voice agent does, one yes/no question.
3. **DM the Facebook page.** Same message, shorter. The page is in the Ad Library, and owners of small shops often read their own messages.

Then show, do not tell: build a demo agent for them with the kit's `prospect-demo` skill and send the link.

## Compliance (read this before you send anything)

This is not legal advice. It is the floor you should stay above.

- **B2B only.** This list is for reaching businesses about their business. Do not use it to market to consumers.
- **CAN-SPAM (email).** Use your real name and business, a truthful subject line, your physical mailing address, and a working unsubscribe in every email. Honor opt-outs within 10 business days, and keep a suppression list so a removed address never comes back.
- **TCPA (calls and texts).** No autodialed or prerecorded calls, and no automated texts, to cell phones without prior express consent. Many small-business numbers on Google Maps are the owner's cell. A manual call dialed by a person is the safe default.
- **Do Not Call.** Check numbers against the National Do Not Call Registry and your state's list before calling, and keep your own internal do-not-call list. Stop the moment someone asks you to.
- **Honor every opt-out**, on every channel, the first time they ask.
- State laws (for example Florida, Oklahoma and Washington) add stricter rules for calls and texts. Check your state and theirs.

## Costs at a glance

| Item | Price (Apify free tier, Oct 2026) |
|---|---|
| Google Maps place | $0.004 each (+$0.002 with `--contacts`) |
| Facebook ad record | $0.0058 each |
| TREG email hit | about $0.02 each, misses are free |
| Reoon check | prepaid credits, fractions of a cent |

The script prints its own estimate before every run, and `--dry-run` shows it without spending anything.

## Running the tests

```
python3 -m pytest lead-finder -q
```

Every network call is mocked, so tests never touch Apify, TREG or Reoon and never cost anything.

## Claude Code

Ask Claude in this kit "find roofers in Austin TX" and the `lead-finder` skill (`.claude/skills/lead-finder/SKILL.md`) runs this for you, shows the estimate, and waits for your OK before spending.
