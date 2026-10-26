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

### The signup link

Some messages below tell a user with no Leadlock account where to sign up. The plain link is https://app.leadlock.ai/signup?channel=kit. Add a partner code when one is known, in this order:

1. The plugin's partner code: `${user_config.partner_code}`. Use it only if it is not empty and does not start with `${` (in a cloned kit it shows as the raw placeholder, which means there is no code).
2. Otherwise `LEADLOCK_PARTNER_CODE` from `.env` (parsed in Step 2), if it is set. Read only that one value.
3. Otherwise no code.

A partner code is used only when it is 1 to 64 characters of letters, digits, hyphens or underscores (no spaces or other symbols). Any other value is ignored and the plain link is printed, so the code never needs URL-encoding. With a valid code, print `https://app.leadlock.ai/signup?channel=kit&fpr=<code>`. With no valid code, print the plain link and leave the fpr part off entirely. If a code was given but is not valid, add one short line after the link: "That partner code is not valid, so this is the plain signup link." Wherever a message below shows the signup link, print the one built here.

### Step 1 — Find `.env`

Check that `./.env` exists in the kit root. If not:

```
✗ No .env file found at the kit root.

  Fix: copy .env.example to .env, then paste your Leadlock API key:
    cp .env.example .env
    # then open .env and paste your key

  Get a key: https://app.leadlock.ai/dashboard/settings/api-keys
  No Leadlock account yet? Sign up: https://app.leadlock.ai/signup?channel=kit
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
- `RETELL_API_KEY` — optional; only the `retell-to-leadlock` skill needs it (the source platform, read-only). Ignore it if you're not porting from Retell.
- `MY_PHONE_NUMBER`: optional, recommended. The user's own cell in `+1` format; test-call steps default to it.
- `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN`: optional. Fall back to the older `LEADLOCK_TWILIO_SID` / `LEADLOCK_TWILIO_AUTH` names when the new ones are empty.
- `LEADLOCK_PARTNER_CODE`: optional. A partner code for the signup link (see "The signup link" above). Never required.

If `LEADLOCK_API_KEY` is missing or still contains the placeholder `sk_live_paste_your_key_here`, stop with:

```
✗ LEADLOCK_API_KEY is not set in .env.

  Fix: open .env and replace the placeholder with your real Leadlock API key.
  Get a key: https://app.leadlock.ai/dashboard/settings/api-keys
  No Leadlock account yet? Sign up: https://app.leadlock.ai/signup?channel=kit
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
    ✓ build-agent
    ✓ prospect-demo
    ✓ prompt-tuner
    ✓ call-audit
    ✓ knowledge-base-builder
    ✓ agent-from-recording
    ✓ agent-to-agent-call-testing
    <✓ or ✗> retell-to-leadlock  (requires RETELL_API_KEY in .env)
    <✓ or ✗> subaccount-onboarding  (requires agency-tier key — you are: <tenant_type>)
    ✓ pick-your-offer  (no key needed)
    ✓ clarify-voice  (no key needed)
    ✓ connect-n8n  (no Leadlock key needed to connect)
    <✓ or ✗> install-support-team  (requires N8N_API_URL + N8N_API_KEY in .env)
    <✓ or ✗> install-addon  (needs a paid add-on in ./addons/)
    ✓ kit-audit  (maintainer self-check — no key needed for the static half)

  Try: "Build a demo for https://example.com"
```

Mask the API key: show the first 6 chars + last 4 chars only.

**HTTP 401 Unauthorized** — bad key:

```
✗ API key was rejected (401 Unauthorized).

  The key in your .env is either invalid, revoked, or expired.

  Fix: log in at https://app.leadlock.ai/dashboard/settings/api-keys,
  rotate the key, paste the new one into .env, and run /setup-check again.
  No Leadlock account yet? Sign up: https://app.leadlock.ai/signup?channel=kit
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

### Step 4b: Optional settings: phone and Twilio

Report each as set or not set. Never print a value: the phone shows only its area code, the SID only its first 4 characters, the token never.

**`MY_PHONE_NUMBER`**: set means non-empty. Also check it looks like E.164 (`+` then 10-15 digits). If set but malformed, say so and show the expected shape (`+15555550123`), not the user's value.

**Twilio**: resolve the credentials first, new names winning:

```python
sid = env.get("TWILIO_ACCOUNT_SID") or env.get("LEADLOCK_TWILIO_SID") or ""
token = env.get("TWILIO_AUTH_TOKEN") or env.get("LEADLOCK_TWILIO_AUTH") or ""
```

If both are present, run one read-only auth check (a GET on the account itself, which changes nothing):

```python
import base64
auth = base64.b64encode(f"{sid}:{token}".encode()).decode()
req = urllib.request.Request(
    f"https://api.twilio.com/2010-04-01/Accounts/{sid}.json",
    headers={"Authorization": f"Basic {auth}"},
)
# 200 -> credentials work; read body["status"] (active / suspended) and body["friendly_name"]
# 401 -> SID or token is wrong
```

Report block (append to the Step 4 output):

```
  Optional settings:
    MY_PHONE_NUMBER      ✓ set (+1 512 area code)      | ✗ not set: test calls will ask for a number
    Twilio credentials   ✓ valid (account active, ACxx...)  | ✗ rejected (401): re-copy both from console.twilio.com
                         | ✗ not set: Twilio features (numbers, A2P status, call logs, call backstop) are off
                         | (note "using the older LEADLOCK_TWILIO_* names" when the fallback was used)
```

Only one of the two Twilio values set counts as not set; name the missing one.

### Step 5 — Tenant-tier skills check

If `tenant_type` is `agency` or higher: all production skills are available.
If `tenant_type` is `sub_account`: every skill except `subaccount-onboarding` is available; it will 403 if run (the skill checks this gate at its Step 0).

Report this clearly so the user isn't surprised later.

### Step 6 — Output `.claude/.setup-ok` marker (optional)

If everything passed, write a tiny file at `.claude/.setup-ok` containing the date of the last successful check. Other skills can read this to skip redundant probes. (Add `.claude/.setup-ok` to `.gitignore` if not already.)

## Rules

- **Never print the full API key.** Always mask: `sk_live_xxxxxx...xxxx`.
- **Never print the phone number or Twilio credentials.** Phone: area code only. SID: first 4 characters. Auth token: never, not even masked.
- **The Twilio check is read-only.** One GET on the account. Never buy, release, or reconfigure anything from setup-check.
- **Don't auto-create `.env`.** Tell the user to copy `.env.example` to `.env`. They need to be aware of the file.
- **Don't write to `.env`.** Read-only. The user owns the contents.
- **Fail loud, fail fast.** Each failure mode has a specific remediation message above. Don't be vague.
