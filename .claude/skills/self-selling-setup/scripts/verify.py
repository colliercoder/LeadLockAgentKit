#!/usr/bin/env python3
"""Verify the self-selling snapshot is configured: every required custom value is
filled (no placeholders), and the 2 products exist. GHL public API + PIT. Stdlib.

    python3 verify.py values.json
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

API = "https://services.leadconnectorhq.com"
PLACEHOLDERS = {"", "PASTE_HERE", "PASTE_LINK_HERE", "FILL_ME", "TBD"}


def load_env():
    """Read .env from the kit root (walk up from this file); process env overrides.
    Same convention as the rest of the kit - stdlib only, no python-dotenv."""
    env = {}
    here = Path(__file__).resolve()
    for path in [here.parent / ".env"] + [p / ".env" for p in here.parents]:
        if path.is_file():
            for line in path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
            break
    for k in ("GHL_LOCATION_ID", "GHL_PIT"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def fieldkey(cv):
    """Match on the custom_values.<snake> fieldKey token, not the display name.
    The snapshot mixes Title Case and snake_case names that both resolve to a
    snake_case fieldKey - matching by name.lower() would false-flag the Title
    Case ones (e.g. 'Your Business Name') as missing."""
    fk = cv.get("fieldKey", "") or ""
    m = re.search(r"custom_values\.([a-z0-9_]+)", fk)
    if m:
        return m.group(1)
    return re.sub(r"[^a-z0-9]+", "_", cv.get("name", "").lower()).strip("_")
REQUIRED = [
    "your_business_name", "your_name", "your_email", "ai_assistant_name",
    "setup_fee", "monthly_retainer", "frequently_asked_questions",
    "intake_form_link", "agreement_link", "leadlock_api_key",
    "leadlock_agent_id", "leadlock_reminder_agent_id",
]


def call(url, pit):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {pit}", "Version": "2021-07-28", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, None


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python3 verify.py values.json")
    cfg = json.load(open(sys.argv[1]))
    env = load_env()
    loc = env.get("GHL_LOCATION_ID") or cfg.get("locationId")
    pit = env.get("GHL_PIT") or cfg.get("pit")
    if not loc or not pit:
        sys.exit("Set GHL_LOCATION_ID and GHL_PIT in the kit's .env (or add them to the json).")
    issues = []

    st, cv = call(f"{API}/locations/{loc}/customValues", pit)
    if st != 200:
        sys.exit(f"Could not read custom values [{st}] - check PIT scopes + locationId")
    live = {fieldkey(v): str(v.get("value", "")) for v in cv.get("customValues", [])}
    print("CUSTOM VALUES:")
    for name in REQUIRED:
        val = live.get(name)
        if val is None:
            print(f"  MISSING  {name}")
            issues.append(f"custom value missing: {name}")
        elif val.strip() in PLACEHOLDERS:
            print(f"  EMPTY    {name}")
            issues.append(f"custom value not filled: {name}")
        else:
            preview = " ".join(val.split())[:40]  # collapse newlines (FAQ is multiline)
            print(f"  ok       {name} = {preview}")

    st, prod = call(f"{API}/products/?locationId={loc}", pit)
    n = len(prod.get("products", [])) if st == 200 and isinstance(prod, dict) else "?"
    print(f"\nPRODUCTS: {n} found (expect 2: Setup/Build Fee + AI Receptionist - Monthly)")
    if st == 200 and isinstance(n, int) and n < 2:
        issues.append("fewer than 2 products - create the setup + monthly products")

    print("\n" + ("READY: no config gaps." if not issues else f"{len(issues)} GAP(S):"))
    for i in issues:
        print("  -", i)
    print("\nNote: this checks values + products via the public API. Workflow publish status,"
          " triggers, and the contract are verified in the GHL UI per the checklist.")


if __name__ == "__main__":
    main()
