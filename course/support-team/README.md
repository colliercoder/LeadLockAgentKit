# The support team (advanced course)

Everything the advanced course's AI support team is built from: a fictional heavy equipment rental company, **Granite Peak Equipment Rental**, with three AI desks.

- **Joanne**, rentals: availability, quotes, rental status, extensions, off-rent calls. Answers first.
- **Doug Jim Bob McGee**, maintenance: walks the caller through a breakdown, safety first, and opens a service ticket with the tech's arrival time.
- **Miss Hattie Mae**, billing: balance and invoices, and a secure payment link to the email or phone on file. Never takes card numbers.

Before any desk shares or changes account details, the caller verifies like at a bank: a 6-digit code goes to the email or phone **on file** (never one the caller gives), and they read it back.

## Install it

In Claude Code, from the kit folder, say **"install the support team"**. The `install-support-team` skill checks your setup, asks a few questions, builds everything in your Leadlock account and your n8n, and tests it. One piece at a time works too: "install the support team tables", "install the Verify Caller step", "install Joanne", "install Jim Bob", "install Miss Hattie Mae". "Uninstall the support team" removes it all.

You need: your Leadlock key, an n8n on a public URL with an API key (`N8N_API_URL`, `N8N_API_KEY` in `.env`), and a Gmail or SMTP credential in n8n for the codes. A GoHighLevel connection (for Contact Intelligence) and an A2P-registered number (for texting) are optional.

## What's in this folder

| Path | What it is |
|---|---|
| `data/customers.csv` | 6 customers. C-1001 (Ridgeline Aggregates) is you: the installer puts your name, email and phone on it in n8n. |
| `data/fleet.csv` | 20 machines: haul trucks, excavators, loaders, dozers, graders, water trucks, a drill, a generator, a light tower, with daily, weekly and monthly rates. |
| `data/rentals.csv` | 7 rentals, each with its invoice (id, total, Open / Paid / Overdue, due date). |
| `data/service.csv` | 4 open service tickets. |
| `data/troubleshooting.csv` | 26 troubleshooting entries: machine, symptom, likely cause, what to check (safety first), when to call a tech. |
| `data/verifications.csv` | Empty. Holds code hashes during a call, never the codes. |
| `workflows/*.json` | n8n workflow templates for Verify Caller, Rentals, Maintenance and Billing. No ids, credentials or hosts: the installer fills those in. |
| `src/` | The JavaScript inside the workflows, and `build_templates.py`, which rebuilds the templates after an edit. |

All the people, companies, numbers and emails in the CSVs are made up. The dates are written against 2026-10-24; the installer shifts them so the demo is always current.

## How verification works

- The code is 6 random digits, sent only to the email or phone on file.
- n8n stores only a hash of it: SHA-256 of a secret pepper, the code and the call id. The pepper lives only inside the Verify Caller workflow.
- A code lasts 10 minutes. Three wrong tries lock that call, and a resend never adds tries.
- Once verified, the caller stays verified for 60 minutes on that call, across handoffs between desks.
- Execution saving is off on Verify Caller, so n8n keeps no copy of a code.
