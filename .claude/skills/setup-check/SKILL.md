---
name: setup-check
description: Verify the kit is configured correctly. Probes the .env file, tests the API key against the Leadlock API, identifies the user's tenant tier (agency or sub-account), and reports which skills they can run. Use proactively when ANY other skill fails with a 401, when the user reports "it's not working", "I'm getting errors", "is my key right", "test my connection", "diagnose", "/setup", "/setup-check", "check the config", or as the first thing on a fresh clone.
---

# Setup Check

Verify the kit is ready to use. Diagnoses the most common failure: missing or invalid API key. Saves a lot of "why is this not working" confusion.

## When to invoke

- User just cloned the kit and is testing it
- Another skill returned 401 / 403 — fire this automatically to diagnose
- User asks "is my setup correct?" / "test my connection" / "diagnose" / "/setup"
- Before running a destructive skill (e.g. `subaccount-onboarding`) for the first time

## Execution

### Step 1 — Find `.env`

Check that `./.env` exists in the kit root. If not:

```
✗ No .env file found at the kit root.

  Fix: copy .env.example to .env, then paste your Leadlock API key:
    cp .env.example .env
    # then open .env and paste your key

  Get a key: https://app.leadlock.ai/dashboard/settings/api-keys
```

Stop here.

### Step 2 — Parse `.env`

Read `./.env` (stdlib only, no `python-dotenv`):

```python
from pathlib import Path
env = {}
for line in Path("./.env").read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, _, v = line.partition("=")
    env[k.strip()] = v.strip().strip('"').strip("'")
```

Verify both keys exist:

- `LEADLOCK_API_KEY` — required
- `LEADLOCK_API_URL` — required (default to `https://leadlock-app.onrender.com` if missing)

If `LEADLOCK_API_KEY` is missing or still contains the placeholder `sk_live_paste_your_key_here`, stop with:

```
✗ LEADLOCK_API_KEY is not set in .env.

  Fix: open .env and replace the placeholder with your real Leadlock API key.
  Get a key: https://app.leadlock.ai/dashboard/settings/api-keys
```

### Step 3 — Probe the API

Hit `GET /tenants/me` with `X-API-Key: <key>`:

```python
import urllib.request, urllib.error, json

url = env["LEADLOCK_API_URL"].rstrip("/") + "/tenants/me"
req = urllib.request.Request(url, headers={"X-API-Key": env["LEADLOCK_API_KEY"]})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = json.loads(resp.read().decode())
        # success path
except urllib.error.HTTPError as e:
    code = e.code  # 401, 403, etc.
except Exception as e:
    # network error
```

### Step 4 — Interpret the response

**HTTP 200** — auth works. Report:

```
✓ Setup is good.

  API: https://leadlock-app.onrender.com
  Key: sk_live_xxxx...xxxx  (masked)
  Tenant: <name>  (<tenant_type>)
  Plan: <plan_name>

  Skills available to this key:
    ✓ prospect-demo
    ✓ prompt-tuner
    ✓ call-audit
    ✓ knowledge-base-builder
    ✓ agent-from-recording
    <✓ or ✗> subaccount-onboarding  (requires agency-tier key — you are: <tenant_type>)

  Try: "Build a demo for https://example.com"
```

Mask the API key: show the first 6 chars + last 4 chars only.

**HTTP 401 Unauthorized** — bad key:

```
✗ API key was rejected (401 Unauthorized).

  The key in your .env is either invalid, revoked, or expired.

  Fix: log in at https://app.leadlock.ai/dashboard/settings/api-keys,
  rotate the key, paste the new one into .env, and run /setup-check again.
```

**HTTP 403 Forbidden** — auth worked but the endpoint is gated:

```
⚠ Auth worked but /tenants/me returned 403.
  This is unusual. The key may be scoped narrower than expected.
  Try: hit /agents instead, see if that works.
```

**Network error** (timeout, DNS, connection refused):

```
✗ Could not reach the Leadlock API at <URL>.

  Possible causes:
    - LEADLOCK_API_URL is wrong (should be https://leadlock-app.onrender.com)
    - The Leadlock API is temporarily down
    - Your machine has no internet / a firewall is blocking it

  Fix: check LEADLOCK_API_URL in .env. If still failing, try:
    curl -s https://leadlock-app.onrender.com/health
  If that fails, the platform is down or your network is blocked.
```

### Step 5 — Tenant-tier skills check

If `tenant_type` is `agency` or higher: all 6 production skills are available.
If `tenant_type` is `sub_account`: 5 skills available; `subaccount-onboarding` will 403 if run (the skill checks this gate at its Step 0).

Report this clearly so the user isn't surprised later.

### Step 6 — Output `.claude/.setup-ok` marker (optional)

If everything passed, write a tiny file at `.claude/.setup-ok` containing the date of the last successful check. Other skills can read this to skip redundant probes. (Add `.claude/.setup-ok` to `.gitignore` if not already.)

## Rules

- **Never print the full API key.** Always mask: `sk_live_xxxxxx...xxxx`.
- **Don't auto-create `.env`.** Tell the user to copy `.env.example` to `.env`. They need to be aware of the file.
- **Don't write to `.env`.** Read-only. The user owns the contents.
- **Fail loud, fail fast.** Each failure mode has a specific remediation message above. Don't be vague.
