# Anti-patterns

Things we tried (or were tempted to try) that don't work. Don't redo without new evidence.

Each entry includes: date, tags, evidence link, rule, why, how to apply.

---

### Agent timezone must match prospect, not operator

Date: 2026-05-13
Tags: skill:prospect-demo, type:anti-pattern, surface:agent-config, integration:gohighlevel
Evidence: Northern Mister Sparky build (Twin Cities, set correctly to `America/Chicago`); user surfaced the gotcha while testing a 1:30 booking

**Rule:** When building or editing an agent for a prospect, set `agent.timezone` to the **prospect's** local timezone, not the operator's. Infer it from the scrape (the city/state on the contact page). When ambiguous, stop and ask.

**Why:** The agent reasons about times — "today", "tomorrow at 1:30", "first available this afternoon" — in its configured timezone. If the agent is on Eastern but the prospect is in Central, the agent's "1:30" lands an hour later than the caller intended, and the booking confirmation email shows a mismatched local time. The platform's GoHighLevel calendar has its OWN timezone setting inside GHL, separate from `agent.timezone` — so even if you set the agent right, the wired calendar can still book into a different timezone. Verify both before sending a demo out.

**How to apply:**
- In `prospect-demo`, infer timezone from the scrape's city/state. Twin Cities → `America/Chicago`. Phoenix → `America/Phoenix`. NYC/Miami → `America/New_York`. Denver → `America/Denver`. LA/Seattle → `America/Los_Angeles`. National / ambiguous businesses → stop and ask.
- After build, also check the wired GHL calendar's timezone in the GHL admin matches the prospect. The API doesn't expose this; check manually before sending.
- When a user reports "the agent booked the wrong time", look at three places: `agent.timezone`, the GHL calendar's tz, and the booker's browser tz on the confirmation email.
