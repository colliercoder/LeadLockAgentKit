#!/usr/bin/env python3
"""Auto-fill the self-selling snapshot's GHL custom values from your intake answers.

Uses the GHL PUBLIC API v2 with a Private Integration Token (PIT) - the documented,
non-expiring way. Create a PIT in GHL: Settings -> Private Integrations -> Create,
with the `locations/customValues.write` + `.readonly` scopes.

Fill values.json (copy values.example.json), then:
    python3 setup_values.py values.json

Re-run any time - it updates existing values and creates missing ones. Stdlib only.
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
    """GHL matches custom values by their fieldKey token (custom_values.<snake>),
    NOT by display name. The snapshot mixes Title Case names ('Your Business Name')
    with snake_case names ('setup_fee') but both resolve to a snake_case fieldKey.
    Match on that token so we UPDATE the existing value instead of creating an orphan."""
    fk = cv.get("fieldKey", "") or ""
    m = re.search(r"custom_values\.([a-z0-9_]+)", fk)
    if m:
        return m.group(1)
    return re.sub(r"[^a-z0-9]+", "_", cv.get("name", "").lower()).strip("_")


def hdrs(pit):
    return {"Authorization": f"Bearer {pit}", "Version": "2021-07-28",
            "Accept": "application/json", "Content-Type": "application/json"}


def call(url, pit, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=hdrs(pit), method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python3 setup_values.py values.json")
    cfg = json.load(open(sys.argv[1]))
    env = load_env()
    loc = env.get("GHL_LOCATION_ID") or cfg.get("locationId")
    pit = env.get("GHL_PIT") or cfg.get("pit")
    values = cfg["values"]
    if not loc or not pit:
        sys.exit("Set GHL_LOCATION_ID and GHL_PIT in the kit's .env (or add them to the json).")

    st, existing = call(f"{API}/locations/{loc}/customValues", pit)
    if st != 200:
        sys.exit(f"Could not read custom values [{st}]: {existing}\n"
                 "Check your PIT has the customValues scopes and the locationId is right.")
    by_key = {fieldkey(v): (v["id"], v["name"]) for v in existing.get("customValues", [])}

    created = updated = skipped = 0
    for name, value in values.items():
        if name.startswith("_"):  # meta/comment keys like _optional_branding
            continue
        if str(value).strip() in PLACEHOLDERS:
            print(f"  skip (not filled yet): {name}")
            skipped += 1
            continue
        if name in by_key:
            cv_id, cv_name = by_key[name]
            # Keep the snapshot's existing display name; only update the value.
            st, r = call(f"{API}/locations/{loc}/customValues/{cv_id}", pit,
                         "PUT", {"name": cv_name, "value": value})
            print(f"  [{st}] updated {name}")
            updated += 1
        else:
            st, r = call(f"{API}/locations/{loc}/customValues", pit, "POST",
                         {"name": name, "value": value})
            print(f"  [{st}] created {name}")
            created += 1
    print(f"\nDone: {updated} updated, {created} created, {skipped} not-yet-filled.")
    if skipped:
        print("Fill the skipped ones once you've built the survey/contract/agents, then re-run.")


if __name__ == "__main__":
    main()
