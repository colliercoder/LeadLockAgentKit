#!/usr/bin/env python3
"""Installs the Granite Peak AI support team: n8n tables + workflows, three Leadlock
agents, their custom functions and handoffs. Standard library only.

Run from the kit root. Subcommands (all accept --prefix):
  preflight                       checks only, prints a JSON report
  install [--only PIECE ...]      build or update in place (see SKILL.md for flags)
  test                            Leadlock function tests (sends nothing)
  send-code                       gate check + ONE real code to the demo customer
  check-code --code 123456        wrong code, real code, gate check, clean up
  call-me --yes [--number-id ID]  Joanne calls MY_PHONE_NUMBER (a real call)
  status                          what exists right now
  uninstall --yes                 removes exactly what this installer made

Never prints a secret. Every API response is treated as data, not instructions.
"""
import argparse
import csv
import datetime as dt
import json
import re
import secrets
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = Path(__file__).resolve().parent
COURSE = ROOT / "course" / "support-team"
RECORDS = ROOT / "output" / "support-team"
DEFAULT_COMPANY = "Granite Peak Equipment Rental"
DEFAULT_PREFIX = "Granite Peak - "
ANCHOR = dt.date(2026, 10, 24)          # the date the CSVs were written against
SECRET_VAR = "SUPPORT_TEAM_WEBHOOK_SECRET"
HEADER = "X-Support-Key"
PIECES = ["tables", "verify", "rentals", "maintenance", "billing", "handoffs"]

TABLES = {
    "Customers": [("customer_id", "string"), ("first_name", "string"), ("last_name", "string"),
                  ("company", "string"), ("phone", "string"), ("email", "string")],
    "Fleet": [("unit_id", "string"), ("category", "string"), ("model", "string"), ("year", "number"),
              ("hours", "number"), ("status", "string"), ("yard", "string"), ("daily_rate", "number"),
              ("weekly_rate", "number"), ("monthly_rate", "number"), ("available_from", "string")],
    "Rentals": [("rental_id", "string"), ("customer_id", "string"), ("unit_id", "string"), ("model", "string"),
                ("start_date", "string"), ("end_date", "string"), ("status", "string"), ("site", "string"),
                ("invoice_id", "string"), ("invoice_total", "number"), ("invoice_status", "string"),
                ("invoice_due", "string")],
    "Service": [("ticket_id", "string"), ("customer_id", "string"), ("unit_id", "string"), ("issue", "string"),
                ("status", "string"), ("tech_eta", "string"), ("created_at", "string")],
    "Troubleshooting": [("guide_id", "string"), ("category", "string"), ("machine", "string"),
                        ("symptom", "string"), ("likely_cause", "string"), ("what_to_check", "string"),
                        ("call_tech_when", "string")],
    "Verifications": [("call_sid", "string"), ("customer_id", "string"), ("code_hash", "string"),
                      ("expires_at", "string"), ("attempts", "number"), ("verified", "boolean")],
}
DATE_COLS = {"available_from", "start_date", "end_date", "invoice_due", "tech_eta", "created_at"}

WORKFLOWS = {  # piece -> (template file, workflow title, webhook suffix)
    "verify": ("verify-caller.json", "Verify Caller", "verify"),
    "rentals": ("rentals.json", "Rentals", "rentals"),
    "maintenance": ("maintenance.json", "Maintenance", "maintenance"),
    "billing": ("billing.json", "Billing", "billing"),
}


def obj(props, required=()):
    return {"type": "object", "properties": props, "required": list(required)}


S = {"type": "string"}
FUNCTIONS = {  # name -> (workflow piece, description, parameters, test arguments)
    "send_verification_code": ("verify",
        "Sends the caller a 6-digit code at the email or phone we already have ON FILE, to verify them before "
        "sharing or changing anything on their account. Never pass an address the caller gives you; it only goes "
        "to what is on file. Reply: sent true with a masked 'to' (tell the caller where it went and ask them to "
        "read the code), or sent false with a reason.",
        obj({"first_name": {**S, "description": "Caller's first name"},
             "phone_last4": {**S, "description": "Last 4 digits of the phone number on their account"},
             "channel": {"type": "string", "enum": ["email", "sms"], "description": "email (default) or sms"}}),
        None),
    "verify_code": ("verify",
        "Checks the 6-digit code the caller read back. Reply: verified true with their first name and company, "
        "or verified false with attempts_left, or locked.",
        obj({"code": {**S, "description": "The 6 digits the caller read out"}}, ["code"]),
        {"code": "000000"}),
    "fleet_availability": ("rentals",
        "Machines free for rent by type and start date, with yard and daily/weekly/monthly rates.",
        obj({"category": {**S, "description": "Machine type, e.g. haul truck, excavator, loader, dozer, grader, "
                                                "water truck, drill, generator, light tower"},
             "start_date": {**S, "description": "YYYY-MM-DD; today if not given"}}),
        {"category": "excavator"}),
    "rental_quote": ("rentals",
        "Rental price for a machine type or unit for a number of days. Rental only; delivery, fuel and tax "
        "are quoted by the yard.",
        obj({"category": {**S, "description": "Machine type"}, "unit_id": {**S, "description": "Unit id if known"},
             "days": {"type": "integer", "description": "How many days"}}, ["days"]),
        {"category": "haul truck", "days": 10}),
    "rental_status": ("rentals",
        "The verified caller's rentals: unit, dates, status and site. Returns verify_first if the caller "
        "is not verified on this call.", obj({}), {}),
    "extend_rental": ("rentals",
        "Moves the end date of one of the verified caller's rentals later.",
        obj({"rental_id": {**S, "description": "Rental id, e.g. R-5001"},
             "new_end_date": {**S, "description": "YYYY-MM-DD"}}, ["new_end_date"]),
        {"rental_id": "R-5001", "new_end_date": "2099-01-01"}),
    "call_off_rent": ("rentals",
        "Ends one of the verified caller's rentals and requests pickup. Confirm with the caller first.",
        obj({"rental_id": {**S, "description": "Rental id"}, "pickup_date": {**S, "description": "YYYY-MM-DD"}}),
        {"rental_id": "R-5001"}),
    "troubleshoot_machine": ("maintenance",
        "Troubleshooting guide entries for a machine and symptom: safety step, likely cause, what to check, "
        "and when to call a tech.",
        obj({"machine": {**S, "description": "Machine type or model"},
             "symptom": {**S, "description": "What it's doing, in the caller's words"}}, ["symptom"]),
        {"machine": "excavator", "symptom": "grinding when it swings"}),
    "create_service_ticket": ("maintenance",
        "Opens a service ticket on one of the verified caller's rented units and returns the ticket id and "
        "the tech's arrival time.",
        obj({"unit_id": {**S, "description": "Unit id, e.g. GP-102"}, "issue": {**S, "description": "Short problem"},
             "machine_down": {"type": "boolean", "description": "True if the machine can't run"}}, ["issue"]),
        {"unit_id": "GP-102", "issue": "installer test", "machine_down": False}),
    "service_ticket_status": ("maintenance",
        "The verified caller's service tickets and tech arrival times.",
        obj({"ticket_id": {**S, "description": "Ticket id if they have one"}}), {}),
    "account_balance": ("billing",
        "The verified caller's balance due and invoices.", obj({}), {}),
    "send_payment_link": ("billing",
        "Sends a secure payment link for one invoice or the whole balance to the phone (text) or email on file. "
        "Never take card numbers.",
        obj({"invoice_id": {**S, "description": "Invoice id; leave out for the whole balance"},
             "channel": {"type": "string", "enum": ["sms", "email"], "description": "sms (default) or email"}}),
        None),
}
VERIFY_FNS = ["send_verification_code", "verify_code"]
DESKS = {  # piece -> agent
    "rentals": {"title": "Joanne (Rentals)", "short": "Joanne", "prompt": "joanne.md", "voice": "eve",
                "greeting": "Well howdy, thanks for calling {COMPANY}, this is Joanne. What can I do for you, sugar?",
                "tag": "rental-lead",
                "when": "The caller wants machine availability, a quote, their rental status, an extension or to call a machine off rent."},
    "maintenance": {"title": "Doug Jim Bob McGee (Maintenance)", "short": "Jim Bob", "prompt": "jimbob.md", "voice": "rex",
                    "greeting": "This is Jim Bob in maintenance. Tell me what that machine's doing.",
                    "tag": "breakdown",
                    "when": "A rented machine broke down, is acting up, needs troubleshooting, or the caller wants a service ticket or a tech."},
    "billing": {"title": "Miss Hattie Mae (Billing)", "short": "Miss Hattie Mae", "prompt": "hattie.md", "voice": "ara",
                "greeting": "Hey there, baby, this is Miss Hattie Mae in billing. What can I help you with?",
                "tag": "payment-link-sent",
                "when": "The caller asks about a balance, an invoice, or paying."},
}
DESK_FNS = {p: [n for n, f in FUNCTIONS.items() if f[0] == p] for p in DESKS}
CRM_TOOLS = ["update_contact", "add_note", "add_tag"]


# ---------------------------------------------------------------- plumbing

def load_env():
    env = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def set_env(key, value):
    p = ROOT / ".env"
    lines = p.read_text().splitlines() if p.exists() else []
    lines = [l for l in lines if not l.strip().startswith(key + "=")]
    if value is not None:
        lines.append(f"{key}={value}")
    p.write_text("\n".join(lines) + "\n")


def e164(p):
    d = re.sub(r"\D", "", p or "")
    if len(d) == 10:
        d = "1" + d
    return "+" + d if len(d) == 11 and d.startswith("1") else ""


ENV = load_env()


def http(method, url, headers, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "leadlock-agent-kit/1.0"}
    h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, raw[:500]
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return 0, str(e)


def ll(method, path, body=None, timeout=60):
    h = {"X-API-Key": ENV.get("LEADLOCK_API_KEY", "")}
    if ENV.get("LEADLOCK_SUB_ACCOUNT_ID"):
        h["X-Sub-Account-Id"] = ENV["LEADLOCK_SUB_ACCOUNT_ID"]
    return http(method, ENV.get("LEADLOCK_API_URL", "https://leadlock-app.onrender.com").rstrip("/") + path, h, body, timeout)


def n8n_base():
    return ENV.get("N8N_API_URL", "").rstrip("/").removesuffix("/api/v1")


def n8n(method, path, body=None):
    return http(method, n8n_base() + "/api/v1" + path, {"X-N8N-API-KEY": ENV.get("N8N_API_KEY", "")}, body)


class Stop(Exception):
    pass


def must(status_body, what, ok=(200, 201, 204)):
    s, b = status_body
    if s not in ok:
        raise Stop(f"{what} failed: HTTP {s} {str(b)[:300]}")
    return b


def mask_phone(p):
    d = re.sub(r"\D", "", p or "")[-10:]
    return f"({d[:3]}) ***-**{d[-2:]}" if len(d) == 10 else "(hidden)"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


class Names:
    def __init__(self, prefix, explicit):
        self.prefix = prefix
        self.slug = slugify(prefix) or "support-team"
        self.fn_prefix = (re.sub(r"[^a-z0-9]+", "_", prefix.lower()).strip("_") + "_") if explicit else ""

    def table(self, t): return f"{self.prefix}{t}"
    def workflow(self, p): return f"{self.prefix}{WORKFLOWS[p][1]}"
    def agent(self, p): return f"{self.prefix}{DESKS[p]['title']}"
    def fn(self, n): return f"{self.fn_prefix}{n}"
    def webhook(self, p): return f"{n8n_base()}/webhook/{self.slug}-{WORKFLOWS[p][2]}"
    cred_webhook = property(lambda s: f"{s.prefix}Support team webhook key")
    cred_leadlock = property(lambda s: f"{s.prefix}Leadlock API key")
    record = property(lambda s: RECORDS / f"{s.slug}.json")


def load_record(names):
    return json.loads(names.record.read_text()) if names.record.exists() else {}


def save_record(names, rec):
    RECORDS.mkdir(parents=True, exist_ok=True)
    names.record.write_text(json.dumps(rec, indent=1) + "\n")


def say(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------- lookups

def n8n_list(path):
    out, cursor = [], None
    while True:
        q = f"{path}{'&' if '?' in path else '?'}limit=100" + (f"&cursor={cursor}" if cursor else "")
        b = must(n8n("GET", q), f"n8n GET {path}")
        out += b.get("data", [])
        cursor = b.get("nextCursor")
        if not cursor:
            return out


def find_table(name):
    return next((t for t in n8n_list("/data-tables") if t["name"] == name), None)


def find_workflow(name):
    return next((w for w in n8n_list("/workflows") if w["name"] == name), None)


def find_credential(name):
    s, b = n8n("GET", "/credentials?limit=250")
    if s != 200:
        return None
    return next((c for c in b.get("data", []) if c["name"] == name), None)


def ll_agents():
    b = must(ll("GET", "/agents"), "GET /agents")
    return b if isinstance(b, list) else b.get("agents", [])


def ll_functions():
    return must(ll("GET", "/functions"), "GET /functions").get("functions", [])


def ours(fn, names):
    return f"/webhook/{names.slug}-" in (fn.get("webhook_url") or "")


def table_rows(tid):
    out, cursor = [], None
    while True:
        b = must(n8n("GET", f"/data-tables/{tid}/rows?limit=250" + (f"&cursor={cursor}" if cursor else "")), "read rows")
        out += b.get("data", [])
        cursor = b.get("nextCursor")
        if not cursor:
            return out


def clear_test_row(names):
    t = find_table(names.table("Verifications"))
    if t:
        f = json.dumps({"type": "and", "filters": [{"columnName": "call_sid", "condition": "eq", "value": "test-call-sid"}]})
        n8n("DELETE", f"/data-tables/{t['id']}/rows/delete?filter={urllib.parse.quote(f)}")


# ---------------------------------------------------------------- preflight

def preflight(names):
    checks = []

    def add(name, status, detail, fix=""):
        checks.append({"check": name, "status": status, "detail": detail, "fix": fix})

    key = ENV.get("LEADLOCK_API_KEY", "")
    if not key or "paste" in key:
        add("leadlock_key", "fail", "LEADLOCK_API_KEY is missing from .env.", "Run /setup-check.")
        return checks
    s, b = ll("GET", "/agents")
    if s != 200:
        add("leadlock_key", "fail", f"GET /agents returned {s}.", "Run /setup-check: the key is wrong, revoked or for another host.")
        return checks
    s, me = ll("GET", "/tenants/me")
    tier = me.get("tenant_type") if s == 200 and isinstance(me, dict) else "unknown"
    if tier == "agency" and not ENV.get("LEADLOCK_SUB_ACCOUNT_ID"):
        add("leadlock_key", "fail", "This is an agency key. Agents and functions must live in a sub-account.",
            "Use the sub-account's own key, or set LEADLOCK_SUB_ACCOUNT_ID in .env.")
        return checks
    add("leadlock_key", "ok", f"Key {key[:6]}...{key[-4:]} works ({tier}: {me.get('name', '?') if isinstance(me, dict) else '?'}).")

    s, g = ll("GET", "/integrations/ghl/status")
    if s == 200 and isinstance(g, dict) and g.get("connected"):
        add("crm", "ok", f"GoHighLevel connected ({g.get('location_name', 'location')}). Contact Intelligence and update_contact will be on.")
    else:
        add("crm", "warn", "No GoHighLevel CRM connected. Installing in calls-only memory mode: no Contact Intelligence, "
            "no update_contact / add_note / add_tag. Callers verify with first name + last 4 digits.",
            "Connect GoHighLevel in Leadlock (Integrations), then re-run the install to switch those on.")

    base, nkey = n8n_base(), ENV.get("N8N_API_KEY", "")
    if not base or not nkey:
        missing = " and ".join(k for k, v in [("N8N_API_URL", base), ("N8N_API_KEY", nkey)] if not v)
        add("n8n", "fail", f"{missing} not set in .env.",
            "Add N8N_API_URL (your n8n address, e.g. https://you.app.n8n.cloud) and N8N_API_KEY "
            "(n8n: Settings > n8n API > Create an API key) to .env. No n8n yet? Say \"connect n8n\".")
    elif re.search(r"//(localhost|127\.|0\.0\.0\.0|[^/]*\.local)(:|/|$)", base):
        add("n8n", "fail", "n8n is on this computer, so Leadlock can't reach its webhooks.", "Use n8n Cloud or a self-hosted n8n on a public URL.")
    else:
        s, b = n8n("GET", "/workflows?limit=1")
        if s == 200:
            s2, _ = n8n("GET", "/data-tables?limit=1")
            if s2 == 200:
                add("n8n", "ok", f"n8n API reachable at {base} and data tables are available.")
            else:
                add("n8n", "fail", f"n8n API works but data tables don't (HTTP {s2}).", "Update n8n to a version with Data tables (n8n Cloud has them).")
        elif s in (401, 403):
            add("n8n", "fail", f"n8n rejected N8N_API_KEY (HTTP {s}).", "Create a new key in n8n: Settings > n8n API.")
        else:
            add("n8n", "fail", f"Can't reach n8n at {base} ({s}: {str(b)[:120]}).", "Check N8N_API_URL; it's the address you open n8n at.")

    mcp = "unknown"
    if shutil.which("claude"):
        try:
            r = subprocess.run(["claude", "mcp", "list"], capture_output=True, text=True, timeout=45, cwd=ROOT)
            mcp = "ok" if re.search(r"^n8n.*Connected", r.stdout, re.M | re.I) else "missing"
        except (subprocess.TimeoutExpired, OSError):
            pass
    if mcp == "ok":
        add("n8n_mcp", "ok", "n8n MCP connected in Claude Code, so you can edit these workflows by asking.")
    else:
        add("n8n_mcp", "warn", "n8n MCP isn't connected in Claude Code. The install doesn't need it (it uses the n8n API), "
            "but you'll want it to change the workflows by asking.", "Say \"connect n8n\" after the install, then check with /mcp.")

    email_creds = []
    if any(c["check"] == "n8n" and c["status"] == "ok" for c in checks):
        s, b = n8n("GET", "/credentials?limit=250")
        if s == 200:
            email_creds = [{"id": c["id"], "name": c["name"], "type": c["type"]} for c in b.get("data", [])
                           if c["type"] in ("gmailOAuth2", "smtp")]
            if email_creds:
                add("email", "ok", "Email credential(s) in n8n: " + ", ".join(f"{c['name']} ({c['type']})" for c in email_creds))
            else:
                add("email", "warn", "No Gmail or SMTP credential in n8n, so codes can't go by email.",
                    "In n8n: Credentials > Add credential > Gmail OAuth2 (Sign in with Google) or SMTP. "
                    "Without one, codes and payment links go by text only, which needs an A2P-registered number.")
        else:
            add("email", "warn", f"Can't list n8n credentials (HTTP {s}).", "Pass --email-cred <id> with your Gmail or SMTP credential id.")

    numbers = []
    s, b = ll("GET", "/phone-numbers")
    if s == 200 and isinstance(b, dict):
        for n in b.get("phone_numbers", []):
            numbers.append({"id": n["id"], "masked": mask_phone(n.get("phone_number")), "agent_id": n.get("agent_id"),
                            "a2p_status": n.get("a2p_status"), "sms_ready": bool(n.get("sms_capable") and n.get("messaging_enabled"))})
        ready = [n for n in numbers if n["sms_ready"]]
        if not numbers:
            add("phone", "warn", "No phone number on this account. The agents still work in the web playground and test calls.",
                "Buy or import a number in Leadlock (Phone Numbers), then re-run to switch texting on.")
        elif ready:
            add("phone", "ok", "A2P-registered number(s) ready for texting codes and payment links: " + ", ".join(n["masked"] for n in ready))
        else:
            add("phone", "warn", "Your number(s) aren't A2P registered: " + ", ".join(f"{n['masked']} ({n['a2p_status']})" for n in numbers) +
                ". US carriers block business texts from unregistered numbers, and A2P 10DLC is the registration that fixes it. "
                "Installing in email-code mode.", "Say \"register A2P\" to run the a2p-registration skill, then re-run to switch texting on.")
    else:
        add("phone", "warn", f"Can't read phone numbers with this key (HTTP {s}). Installing in email-code mode.",
            "Check the number in the Leadlock dashboard; texting can be switched on later with --sms-number-id.")

    mine = e164(ENV.get("MY_PHONE_NUMBER"))
    if mine:
        add("my_phone", "ok", f"MY_PHONE_NUMBER set {mask_phone(mine)}. It goes on file as the demo customer's phone.")
    else:
        add("my_phone", "warn", "MY_PHONE_NUMBER isn't set (or isn't +1 and 10 digits).",
            "Add your cell to .env as MY_PHONE_NUMBER=+15555550123. It's needed for test calls and to put you on file as the demo customer.")

    for c in checks:
        if c["check"] == "email":
            c["email_credentials"] = email_creds
        if c["check"] == "phone":
            c["numbers"] = numbers
    return checks


# ---------------------------------------------------------------- build: tables

def shift(value, days):
    m = re.match(r"^(\d{4}-\d{2}-\d{2})(.*)$", value or "")
    if not m:
        return value
    return (dt.date.fromisoformat(m.group(1)) + dt.timedelta(days=days)).isoformat() + m.group(2)


def seed_rows(table, cfg):
    days = (dt.date.today() - ANCHOR).days
    types = dict(TABLES[table])
    rows = []
    with open(COURSE / "data" / f"{table.lower()}.csv", newline="") as f:
        for r in csv.DictReader(f):
            row = {}
            for k, v in r.items():
                t = types[k]
                if t == "number":
                    row[k] = float(v) if "." in v else int(v or 0)
                elif t == "boolean":
                    row[k] = v.lower() == "true"
                else:
                    row[k] = shift(v, days) if k in DATE_COLS else v
            rows.append(row)
    if table == "Customers":
        for r in rows:
            if r["customer_id"] == "C-1001":
                r.update({k: cfg[k] for k in ("first_name", "last_name", "email", "phone") if cfg.get(k)})
    return rows


def build_tables(names, cfg, rec, reseed):
    ids = {}
    for t, cols in TABLES.items():
        name = names.table(t)
        existing = find_table(name)
        if existing:
            have = {c["name"] for c in existing["columns"]}
            missing = [c for c, _ in cols if c not in have]
            if missing:
                raise Stop(f"Table '{name}' exists but is missing columns {missing}. Rename or delete it, then re-run.")
            ids[t] = existing["id"]
            if reseed and t != "Verifications":
                n8n("DELETE", f"/data-tables/{existing['id']}")
                existing = None
            else:
                say(f"  table {name}: exists, kept its rows")
        if not existing:
            b = must(n8n("POST", "/data-tables", {"name": name, "columns": [{"name": c, "type": ty} for c, ty in cols]}),
                     f"create table {name}")
            ids[t] = b["id"]
            rows = seed_rows(t, cfg)
            if rows:
                must(n8n("POST", f"/data-tables/{ids[t]}/rows", {"data": rows, "returnType": "count"}), f"seed {name}")
            say(f"  table {name}: created, {len(rows)} rows")
    # You are the demo customer: keep C-1001 in step with the answers on every run.
    if any(cfg.get(k) for k in ("first_name", "email", "phone")):
        upd = {k: cfg[k] for k in ("first_name", "last_name", "email", "phone") if cfg.get(k)}
        f = {"type": "and", "filters": [{"columnName": "customer_id", "condition": "eq", "value": "C-1001"}]}
        must(n8n("PATCH", f"/data-tables/{ids['Customers']}/rows/update", {"filter": f, "data": upd}), "update C-1001")
    rec["tables"] = ids
    return ids


# ---------------------------------------------------------------- build: credentials + workflows

def ensure_credential(name, header, value):
    body = {"name": name, "type": "httpHeaderAuth", "data": {"name": header, "value": value}}
    c = find_credential(name)
    if c:
        must(n8n("PATCH", f"/credentials/{c['id']}", {"data": body["data"]}), f"update credential {name}")
        return c["id"]
    return must(n8n("POST", "/credentials", body), f"create credential {name}")["id"]


def set_const(code, name, value):
    return re.sub(rf"^const {name} = .*;$", f"const {name} = {json.dumps(value)};", code, count=1, flags=re.M)


def render_workflow(piece, names, cfg, rec, existing):
    tpl, title, _ = WORKFLOWS[piece]
    raw = (COURSE / "workflows" / tpl).read_text()
    raw = raw.replace("REPLACE_SLUG", names.slug).replace("REPLACE_WEBHOOK_ID", str(uuid.uuid5(uuid.NAMESPACE_URL, names.webhook(piece))))
    raw = raw.replace("REPLACE_LEADLOCK_API_URL", ENV.get("LEADLOCK_API_URL", "https://leadlock-app.onrender.com").rstrip("/"))
    raw = raw.replace("REPLACE_SMS_FROM_ID", cfg.get("sms_number_id") or "")
    for t, tid in rec["tables"].items():
        raw = raw.replace(f"REPLACE_TABLE_{t}", tid)
    wf = json.loads(raw)
    email = cfg.get("email_cred")
    sms = bool(cfg.get("sms_number_id"))
    keep_pepper = None
    if existing:
        for n in existing.get("nodes", []):
            m = re.search(r"^const PEPPER = (\".*?\");$", n.get("parameters", {}).get("jsCode", ""), re.M)
            if m:
                keep_pepper = json.loads(m.group(1))
    for n in wf["nodes"]:
        creds = n.get("credentials", {})
        if creds.get("httpHeaderAuth", {}).get("id") == "REPLACE_CRED_WEBHOOK":
            n["credentials"] = {"httpHeaderAuth": {"id": rec["cred_webhook"], "name": names.cred_webhook}}
        if creds.get("httpHeaderAuth", {}).get("id") == "REPLACE_CRED_LEADLOCK":
            n["credentials"] = {"httpHeaderAuth": {"id": rec.get("cred_leadlock", ""), "name": names.cred_leadlock}}
        code = n["parameters"].get("jsCode")
        if code:
            code = set_const(code, "COMPANY", cfg["company"])
            code = set_const(code, "EMAIL_ENABLED", bool(email))
            code = set_const(code, "SMS_ENABLED", sms)
            code = set_const(code, "PAY_LINK_BASE", cfg.get("pay_link_base") or "https://example.com/pay/")
            if "const PEPPER" in code:
                code = set_const(code, "PEPPER", keep_pepper or secrets.token_hex(16))
            n["parameters"]["jsCode"] = code
    by_name = {n["name"]: n for n in wf["nodes"]}
    if "Email" in by_name:
        node = by_name["Email"]
        if email and email["type"] == "smtp":
            p = node["parameters"]
            node.update({"type": "n8n-nodes-base.emailSend", "typeVersion": 2.1,
                         "credentials": {"smtp": {"id": email["id"], "name": email["name"]}},
                         "parameters": {"fromEmail": cfg.get("smtp_from") or cfg.get("email") or "", "toEmail": p["sendTo"],
                                        "subject": p["subject"], "emailFormat": "text", "text": p["message"],
                                        "options": {"appendAttribution": False}}})
        elif email:
            node["credentials"] = {"gmailOAuth2": {"id": email["id"], "name": email["name"]}}
        else:
            node.update({"type": "n8n-nodes-base.noOp", "typeVersion": 1, "parameters": {}})
            node.pop("credentials", None)
            node.pop("onError", None)
            wf["connections"]["Email"] = {"main": [[{"node": "Reply Send Failed", "type": "main", "index": 0}]]}
        if not sms:
            t = by_name["Text"]
            t.update({"type": "n8n-nodes-base.noOp", "typeVersion": 1, "parameters": {}})
            t.pop("credentials", None)
            t.pop("onError", None)
            wf["connections"]["Text"] = {"main": [[{"node": "Reply Send Failed", "type": "main", "index": 0}]]}
    wf["name"] = names.workflow(piece)
    return wf


def build_workflow(piece, names, cfg, rec):
    name = names.workflow(piece)
    found = find_workflow(name)
    full = must(n8n("GET", f"/workflows/{found['id']}"), "read workflow") if found else None
    wf = render_workflow(piece, names, cfg, rec, full)
    body = {k: wf[k] for k in ("name", "nodes", "connections", "settings")}
    if found:
        if found.get("active"):
            n8n("POST", f"/workflows/{found['id']}/deactivate")
        must(n8n("PUT", f"/workflows/{found['id']}", body), f"update workflow {name}")
        wid = found["id"]
    else:
        wid = must(n8n("POST", "/workflows", body), f"create workflow {name}")["id"]
    s, b = n8n("POST", f"/workflows/{wid}/activate")
    if s != 200:
        raise Stop(f"Workflow '{name}' saved but won't publish: {str(b)[:300]}. If another workflow already uses the "
                   f"webhook path {names.slug}-{WORKFLOWS[piece][2]}, re-run with a different --prefix.")
    url = names.webhook(piece)
    s, _ = http("POST", url, {}, {"function": "probe"})
    s2, b2 = http("POST", url, {HEADER: ENV[SECRET_VAR]}, {"function": "probe", "arguments": {}, "call_context": {}})
    if s2 != 200 or s in (200,):
        raise Stop(f"Webhook check failed for {name}: without key HTTP {s} (want 403), with key HTTP {s2} {str(b2)[:200]}")
    rec.setdefault("workflows", {})[piece] = {"id": wid, "url": url}
    say(f"  workflow {name}: {'updated' if found else 'created'}, published, webhook answers (no key -> {s}, key -> 200)")


# ---------------------------------------------------------------- build: Leadlock

def build_functions(piece_list, names, rec):
    lib = {f["name"]: f for f in ll_functions()}
    for fname, (piece, desc, params, _) in FUNCTIONS.items():
        if piece not in piece_list:
            continue
        name = names.fn(fname)
        body = {"name": name, "description": desc, "parameters": params, "webhook_url": rec["workflows"][piece]["url"],
                "webhook_method": "POST", "webhook_headers": {HEADER: ENV[SECRET_VAR]},
                "webhook_timeout_ms": 10000 if fname in ("send_verification_code", "send_payment_link") else 6000,
                "is_enabled": True, "speak_during_execution": True}
        f = lib.get(name)
        if f and not ours(f, names):
            raise Stop(f"A function named '{name}' already exists and points somewhere else. Re-run with --prefix to install alongside it.")
        if f:
            must(ll("PUT", f"/functions/{f['id']}", body), f"update function {name}")
            fid = f["id"]
        else:
            fid = must(ll("POST", "/functions", body), f"create function {name}")["id"]
        rec.setdefault("functions", {})[fname] = fid
        say(f"  function {name}: {'updated' if f else 'created'}")


def render_prompt(piece, names, cfg, present, crm):
    def fill(text):
        text = text.replace("{COMPANY}", cfg["company"])
        return re.sub(r"\{fn:([a-z_]+)\}", lambda m: names.fn(m.group(1)), text)

    def keep(line):
        m = re.match(r"^\[(crm|to:[a-z]+)\]", line)
        if not m:
            return line
        tag, rest = m.group(1), line[m.end():]
        if tag == "crm":
            return rest if crm else None
        target = tag[3:]
        others = [p for p in present if p != piece]
        return rest if (others if target == "any" else target in others) else None

    def strip_inline(text):  # "[to:billing] Balances..." inside a paragraph
        others = [p for p in present if p != piece]
        return re.sub(r"\[to:([a-z]+)\]([^\[\n]*)", lambda m: m.group(2) if m.group(1) in others else "", text)

    shared = (SKILL / "prompts" / "_shared.md").read_text()
    body = (SKILL / "prompts" / DESKS[piece]["prompt"]).read_text().replace("{SHARED}", shared.rstrip())
    lines = [l for l in (keep(l) for l in body.splitlines()) if l is not None]
    text = strip_inline("\n".join(lines))
    # renumber Call Flow steps after dropped lines
    n = 0
    out = []
    for l in text.splitlines():
        if l.startswith("## "):
            n = 0
        m = re.match(r"^\d+\. ", l)
        if m:
            n += 1
            l = f"{n}. " + l[m.end():]
        out.append(l)
    text = fill("\n".join(out))
    if crm:
        text += ("\n\n## Caller Intelligence\nA CALLER CONTEXT block above this prompt may show who is calling: name, "
                 "company, past calls, notes and tags. Use their first name on your second turn, not in the greeting. "
                 "A phone match isn't proof of identity, so still verify before sharing account details.")
    return text.strip() + "\n"


def agent_payload(piece, names, cfg, present, crm, agent_ids):
    d = DESKS[piece]
    targets = [{"agent_id": agent_ids[p], "name": DESKS[p]["short"], "when": DESKS[p]["when"]}
               for p in present if p != piece and p in agent_ids]
    tools = ["end_call", "schedule_callback"] + (CRM_TOOLS if crm else []) + (["transfer_to_agent"] if targets else [])
    return {
        "name": names.agent(piece), "system_prompt": render_prompt(piece, names, cfg, present, crm),
        "greeting": d["greeting"].replace("{COMPANY}", cfg["company"]), "business_name": cfg["company"],
        "industry": "Heavy equipment rental", "timezone": "America/Denver",
        "voice_provider": "xai", "voice": d["voice"], "temperature": 0.7,
        # Joanne answers first, and is the one the test call comes from, so she also dials out.
        "agent_mode": "both" if piece == "rentals" else "inbound", "voice_enabled": True, "text_enabled": False,
        "ai_speaks_first": True, "finish_greeting_before_listening": False,
        "ai_speaks_first_outbound": True,
        "greeting_outbound": f"Hey there, it's Joanne at {cfg['company']}, giving you a ring. What can I do for you, sugar?",
        "tools_enabled": tools, "transfer_to_agents": targets,
        "ghl_tags": [{"name": d["tag"]}] if crm else [],
        "enable_contact_intelligence": crm, "prompt_includes_contact_intelligence": crm,
        "max_call_duration_minutes": 15, "max_silence_seconds": 30,
    }


def build_agents(desk_pieces, names, cfg, rec, crm):
    agents = {a["name"]: a for a in ll_agents()}
    present = [p for p in DESKS if p in desk_pieces or names.agent(p) in agents]
    ids = {p: agents[names.agent(p)]["id"] for p in present if names.agent(p) in agents}
    # create missing desks first so every handoff target has an id
    for p in desk_pieces:
        if p not in ids:
            body = agent_payload(p, names, cfg, present, crm, ids)
            b = must(ll("POST", "/agents", {**body, "transfer_to_agents": [],
                                            "tools_enabled": [t for t in body["tools_enabled"] if t != "transfer_to_agent"]}),
                     f"create agent {body['name']}")
            ids[p] = b["id"]
            say(f"  agent {body['name']}: created")
    for p in present:
        body = agent_payload(p, names, cfg, present, crm, ids)
        must(ll("PATCH", f"/agents/{ids[p]}", body), f"update agent {body['name']}")
        got = must(ll("GET", f"/agents/{ids[p]}"), "read agent")
        problems = [k for k in ("voice_provider", "voice", "enable_contact_intelligence") if got.get(k) != body[k]]
        if sorted(got.get("tools_enabled") or []) != sorted(body["tools_enabled"]):
            problems.append("tools_enabled")
        if {t["agent_id"] for t in got.get("transfer_to_agents") or []} != {t["agent_id"] for t in body["transfer_to_agents"]}:
            problems.append("transfer_to_agents")
        if problems:
            raise Stop(f"Agent {body['name']} didn't save {problems}.")
        say(f"  agent {body['name']}: saved and checked (voice {got.get('voice')}, handoffs to "
            f"{', '.join(t['name'] for t in body['transfer_to_agents']) or 'none yet'})")
    rec["agents"] = ids
    return ids, present


def attach_functions(desk_pieces, ids, rec):
    for p in desk_pieces:
        want = [rec["functions"][f] for f in VERIFY_FNS + DESK_FNS[p]]
        s, b = ll("GET", f"/agents/{ids[p]}/functions")
        rows = (b.get("attached") or b.get("functions") or []) if isinstance(b, dict) else (b or [])
        have = {f.get("function_id") or f.get("id"): f for f in rows}
        for fid in want:
            if fid in have:
                if have[fid].get("is_enabled") is False:
                    ll("POST", f"/agents/{ids[p]}/functions/{fid}/enable")
                continue
            must(ll("POST", f"/agents/{ids[p]}/functions/attach", {"function_id": fid, "is_enabled": True}), "attach function")
        say(f"  {DESKS[p]['short']}: {len(want)} functions attached")


# ---------------------------------------------------------------- commands

def config_from(args, names):
    rec = load_record(names)
    cfg = dict(rec.get("config", {}))
    for k in ("company", "first_name", "last_name", "email", "sms_number_id", "smtp_from", "pay_link_base"):
        v = getattr(args, k, None)
        if v is not None:
            cfg[k] = v
    cfg.setdefault("company", DEFAULT_COMPANY)
    if e164(ENV.get("MY_PHONE_NUMBER")):
        cfg["phone"] = e164(ENV["MY_PHONE_NUMBER"])
    if args.email_cred:
        s, b = n8n("GET", "/credentials?limit=250")
        c = next((c for c in (b or {}).get("data", []) if c["id"] == args.email_cred), None) if s == 200 else None
        cfg["email_cred"] = {"id": args.email_cred, "name": c["name"] if c else "Email", "type": c["type"] if c else "gmailOAuth2"}
    if args.codes == "sms" and not cfg.get("sms_number_id"):
        raise Stop("--codes sms needs --sms-number-id (an A2P-registered number).")
    if args.no_email:
        cfg["email_cred"] = None
    if args.no_sms:
        cfg["sms_number_id"] = None
    return rec, cfg


def cmd_install(args, names):
    rec, cfg = config_from(args, names)
    pieces = args.only or PIECES
    deps = {"verify": ["tables"], "rentals": ["tables", "verify"], "maintenance": ["tables", "verify"],
            "billing": ["tables", "verify"], "handoffs": []}
    todo = []
    for p in pieces:
        for d in deps.get(p, []) + [p]:
            if d not in todo:
                todo.append(d)
    if not cfg.get("email_cred") and not cfg.get("sms_number_id") and "verify" in todo:
        raise Stop("No way to deliver codes: pass --email-cred (Gmail/SMTP credential in n8n) or --sms-number-id (A2P number).")
    if not ENV.get(SECRET_VAR):
        set_env(SECRET_VAR, secrets.token_urlsafe(32))
        ENV.update(load_env())
        say(f"  generated {SECRET_VAR} and saved it to .env")
    s, g = ll("GET", "/integrations/ghl/status")
    crm = bool(s == 200 and isinstance(g, dict) and g.get("connected"))
    cfg["crm"] = crm
    rec["config"] = {k: v for k, v in cfg.items() if k not in ("phone",)}
    say(f"Installing {', '.join(todo)} with prefix '{names.prefix}' ({'CRM on' if crm else 'calls-only memory mode'}, "
        f"codes by {'text' if cfg.get('sms_number_id') else 'email'})")
    try:
        if "tables" in todo:
            needs = "tables" in pieces or not all(find_table(names.table(t)) for t in TABLES)
            if needs:
                build_tables(names, cfg, rec, args.reseed)
            else:
                rec["tables"] = {t: find_table(names.table(t))["id"] for t in TABLES}
        wf_pieces = [p for p in todo if p in WORKFLOWS]
        if wf_pieces:
            rec["cred_webhook"] = ensure_credential(names.cred_webhook, HEADER, ENV[SECRET_VAR])
            if cfg.get("sms_number_id"):
                rec["cred_leadlock"] = ensure_credential(names.cred_leadlock, "X-API-Key", ENV["LEADLOCK_API_KEY"])
            for p in wf_pieces:
                if p == "verify" and "verify" not in pieces and find_workflow(names.workflow("verify")):
                    w = find_workflow(names.workflow("verify"))
                    rec.setdefault("workflows", {})["verify"] = {"id": w["id"], "url": names.webhook("verify")}
                    continue
                build_workflow(p, names, cfg, rec)
            build_functions(wf_pieces, names, rec)
        desk_pieces = [p for p in todo if p in DESKS]
        if desk_pieces or "handoffs" in todo:
            ids, present = build_agents(desk_pieces, names, cfg, rec, crm)
            if desk_pieces:
                attach_functions(desk_pieces, ids, rec)
    finally:
        save_record(names, rec)
    say("Install done. Record: " + str(names.record.relative_to(ROOT)))
    return rec


def test_fn(names, fname, args):
    fid = next((f["id"] for f in ll_functions() if f["name"] == names.fn(fname)), None)
    if not fid:
        return {"function": names.fn(fname), "ok": False, "result": "not installed"}
    s, b = ll("POST", f"/functions/{fid}/test", {"arguments": args}, timeout=40)
    b = b if isinstance(b, dict) else {"error": str(b)}
    return {"function": names.fn(fname), "ok": False, "webhook_ok": s == 200 and b.get("success") is True,
            "ms": b.get("response_time_ms"), "result": b.get("response_body", b.get("error"))}


def cmd_test(args, names):
    clear_test_row(names)
    results = []
    for fname, (_, _, _, targs) in FUNCTIONS.items():
        if targs is None:
            continue  # these two send a real message; send-code covers them
        r = test_fn(names, fname, targs)
        txt = json.dumps(r.get("result"))
        res = r.get("result") if isinstance(r.get("result"), dict) else {}
        gated = fname not in ("fleet_availability", "rental_quote", "troubleshoot_machine", "verify_code")
        if fname == "verify_code":
            r["ok"] = r["webhook_ok"] and res.get("error") == "no_code_sent"
        elif gated:
            r["ok"] = r["webhook_ok"] and res.get("error") == "verify_first"
        else:
            r["ok"] = r["webhook_ok"] and "error" not in res
        results.append(r)
        say(f"  {'PASS' if r['ok'] else 'FAIL'} {r['function']} ({r['ms']} ms): {txt[:150]}")
    return results


def demo_last4():
    return re.sub(r"\D", "", ENV.get("MY_PHONE_NUMBER", ""))[-4:]


def cmd_send_code(args, names):
    rec, cfg = config_from(args, names)
    clear_test_row(names)
    before = test_fn(names, "rental_status", {})
    say(f"  gate before: {json.dumps(before['result'])[:120]}")
    channel = "sms" if args.codes == "sms" else "email"
    sent = test_fn(names, "send_verification_code", {"first_name": cfg.get("first_name", ""), "phone_last4": demo_last4(), "channel": channel})
    say(f"  send code: {json.dumps(sent['result'])[:200]}")
    return {"gate_before": before, "send": sent}


def cmd_check_code(args, names):
    wrong = "000000" if args.code != "000000" else "111111"
    w = test_fn(names, "verify_code", {"code": wrong})
    say(f"  wrong code {wrong}: {json.dumps(w['result'])[:160]}")
    ok = test_fn(names, "verify_code", {"code": args.code})
    say(f"  your code: {json.dumps(ok['result'])[:160]}")
    after = test_fn(names, "rental_status", {})
    say(f"  gate after: {json.dumps(after['result'])[:300]}")
    clear_test_row(names)
    say("  cleared the test-call-sid verification row")
    return {"wrong": w, "right": ok, "gate_after": after}


def cmd_call_me(args, names):
    if not args.yes:
        raise Stop("This places a real call to MY_PHONE_NUMBER. Re-run with --yes after the user confirms.")
    to = e164(ENV.get("MY_PHONE_NUMBER"))
    if not to:
        raise Stop("MY_PHONE_NUMBER isn't set in .env.")
    joanne = next((a for a in ll_agents() if a["name"] == names.agent("rentals")), None)
    if not joanne:
        raise Stop("Joanne isn't installed yet.")
    body = {"to_number": to}
    if args.number_id:
        body["from_phone_number_id"] = args.number_id
    b = must(ll("POST", f"/outbound/agents/{joanne['id']}/call", body), "test call")
    say(f"  calling {mask_phone(to)} from Joanne: call {str((b or {}).get('call_sid') or (b or {}).get('call_id') or '')[:12]}...")
    return b


def cmd_status(args, names):
    out = {"tables": {t: bool(find_table(names.table(t))) for t in TABLES},
           "workflows": {p: (lambda w: w and w.get("active"))(find_workflow(names.workflow(p))) for p in WORKFLOWS},
           "credentials": {n: bool(find_credential(n)) for n in (names.cred_webhook, names.cred_leadlock)},
           "functions": sorted(f["name"] for f in ll_functions() if ours(f, names)),
           "agents": sorted(a["name"] for a in ll_agents() if a["name"] in {names.agent(p) for p in DESKS})}
    print(json.dumps(out, indent=1))
    return out


def cmd_uninstall(args, names):
    if not args.yes:
        raise Stop("Uninstall deletes the agents, functions, workflows, credentials and tables. Re-run with --yes after the user confirms.")
    gone = []
    for a in ll_agents():
        if a["name"] in {names.agent(p) for p in DESKS}:
            must(ll("DELETE", f"/agents/{a['id']}"), f"delete agent {a['name']}")
            gone.append(f"agent {a['name']}")
    for f in ll_functions():
        if ours(f, names) and f["name"] in {names.fn(n) for n in FUNCTIONS}:
            must(ll("DELETE", f"/functions/{f['id']}"), f"delete function {f['name']}")
            gone.append(f"function {f['name']}")
    for p in WORKFLOWS:
        w = find_workflow(names.workflow(p))
        if w:
            if w.get("active"):
                n8n("POST", f"/workflows/{w['id']}/deactivate")
            must(n8n("DELETE", f"/workflows/{w['id']}"), f"delete workflow {w['name']}")
            gone.append(f"workflow {w['name']}")
    for n in (names.cred_webhook, names.cred_leadlock):
        c = find_credential(n)
        if c:
            must(n8n("DELETE", f"/credentials/{c['id']}"), f"delete credential {n}")
            gone.append(f"credential {n}")
    for t in TABLES:
        tb = find_table(names.table(t))
        if tb:
            must(n8n("DELETE", f"/data-tables/{tb['id']}"), f"delete table {tb['name']}")
            gone.append(f"table {tb['name']}")
    if names.record.exists():
        names.record.unlink()
    if not any(RECORDS.glob("*.json")) and ENV.get(SECRET_VAR):
        set_env(SECRET_VAR, None)
        gone.append(f".env {SECRET_VAR}")
    for g in gone:
        say(f"  removed {g}")
    say(f"Uninstall done: {len(gone)} items removed.")
    return gone


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["preflight", "install", "test", "send-code", "check-code", "call-me", "status", "uninstall"])
    ap.add_argument("--prefix", help=f"Name prefix for everything made (default '{DEFAULT_PREFIX}')")
    ap.add_argument("--only", nargs="+", choices=PIECES)
    ap.add_argument("--company")
    ap.add_argument("--first-name", dest="first_name")
    ap.add_argument("--last-name", dest="last_name")
    ap.add_argument("--email", help="Your email: goes on file as the demo customer's email")
    ap.add_argument("--email-cred", dest="email_cred", help="n8n Gmail or SMTP credential id")
    ap.add_argument("--smtp-from", dest="smtp_from")
    ap.add_argument("--sms-number-id", dest="sms_number_id", help="Leadlock id of an A2P-registered number")
    ap.add_argument("--codes", choices=["email", "sms"], default="email")
    ap.add_argument("--pay-link-base", dest="pay_link_base")
    ap.add_argument("--no-email", action="store_true")
    ap.add_argument("--no-sms", action="store_true")
    ap.add_argument("--reseed", action="store_true", help="Reset the demo tables to the CSVs")
    ap.add_argument("--code")
    ap.add_argument("--number-id", dest="number_id", help="Leadlock number id the test call comes from")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    explicit = args.prefix is not None
    prefix = args.prefix if explicit else (DEFAULT_PREFIX if not args.company or args.company == DEFAULT_COMPANY
                                           else args.company.split(" Equipment")[0] + " - ")
    names = Names(prefix, explicit)
    try:
        if args.command == "preflight":
            print(json.dumps(preflight(names), indent=1))
        elif args.command == "install":
            cmd_install(args, names)
        elif args.command == "test":
            r = cmd_test(args, names)
            say(f"{sum(x['ok'] for x in r)}/{len(r)} function tests passed")
        elif args.command == "send-code":
            cmd_send_code(args, names)
        elif args.command == "check-code":
            if not args.code:
                raise Stop("--code is required")
            cmd_check_code(args, names)
        elif args.command == "call-me":
            cmd_call_me(args, names)
        elif args.command == "status":
            cmd_status(args, names)
        elif args.command == "uninstall":
            cmd_uninstall(args, names)
    except Stop as e:
        say(f"STOPPED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
