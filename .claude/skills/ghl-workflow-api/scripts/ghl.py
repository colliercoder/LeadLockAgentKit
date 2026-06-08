#!/usr/bin/env python3
"""Core GoHighLevel private-API helper (stdlib only, urllib).

Reads auth headers from a local headers.json (gitignored) that YOU create by
capturing a live GHL browser session. See reference/token-capture.md.

This talks to GHL's UNOFFICIAL backend API (the one the app's own UI uses).
It is not a supported public API: tokens expire ~hourly and the shapes can
change without notice. Use at your own risk.

Hosts:
  - backend.leadconnectorhq.com   workflows, pipelines, emails (this file)
  - services.leadconnectorhq.com  inbound webhooks (not used here)

Usage:
  python3 ghl.py list <location_id>
  python3 ghl.py load <location_id> <workflow_id>
  python3 ghl.py pipelines <location_id>
  python3 ghl.py emails <location_id>

Headers file resolution (first that exists wins):
  1. --headers <path>           (any subcommand, anywhere on the line)
  2. $GHL_HEADERS env var
  3. headers.json next to this script's skill folder
"""
import json
import os
import sys
import urllib.error
import urllib.request

BACKEND = "https://backend.leadconnectorhq.com"

# The header KEYS the GHL backend expects. Values come from headers.json.
# (KEY NAMES only are encoded here; never any captured token value.)
HEADER_KEYS = (
    "authorization",
    "token-id",
    "channel",
    "source",
    "accept",
    "referer",
    "user-agent",
)


def _default_headers_path():
    # headers.json lives in the skill root, one dir up from scripts/.
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(here), "headers.json")


def _resolve_headers_path(argv):
    if "--headers" in argv:
        i = argv.index("--headers")
        if i + 1 < len(argv):
            return argv[i + 1]
    return os.environ.get("GHL_HEADERS") or _default_headers_path()


def load_headers(path=None):
    """Load and validate the captured auth headers.

    Raises a clear error if the file is missing or still has placeholders.
    """
    path = path or _default_headers_path()
    if not os.path.exists(path):
        raise SystemExit(
            f"headers file not found: {path}\n"
            "Copy headers.example.json to headers.json and paste a fresh "
            "captured token. See reference/token-capture.md."
        )
    with open(path) as fh:
        data = json.load(fh)
    auth = data.get("authorization", "")
    if "PASTE_YOUR" in auth or not auth.startswith("Bearer "):
        raise SystemExit(
            f"{path} still has placeholder values. Capture a real session "
            "token first (reference/token-capture.md)."
        )
    return data


def hdrs(headers, extra=None):
    """Build a request header dict from the captured headers plus extras."""
    out = {k: headers[k] for k in HEADER_KEYS if k in headers}
    if extra:
        out.update(extra)
    return out


def get(url, headers, extra=None, timeout=60):
    """GET a URL with the captured headers; returns the decoded body string.

    On HTTP 401 the message reminds you tokens expire hourly.
    """
    req = urllib.request.Request(url, headers=hdrs(headers, extra), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode()
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            raise SystemExit(
                "HTTP 401 from GHL. Your captured token has expired "
                "(tokens last ~1 hour). Re-capture it. See "
                "reference/token-capture.md."
            ) from exc
        body = exc.read().decode()[:500] if exc.fp else ""
        raise SystemExit(f"HTTP {exc.code} from {url}\n{body}") from exc


def get_json(url, headers, extra=None, timeout=60):
    return json.loads(get(url, headers, extra, timeout) or "{}")


def list_workflows(loc, headers):
    """Return the workflow list for a location: [{id, name, status, ...}]."""
    data = get_json(f"{BACKEND}/workflow/{loc}", headers)
    return data if isinstance(data, list) else data.get("workflows", [])


def load_workflow(loc, wfid, headers):
    """Round-trip a workflow's node JSON.

    meta -> signed fileUrl -> the actual workflow JSON.
    The fileUrl is a Firebase-signed URL: it must be fetched WITHOUT a
    content-type header or the signature breaks. We pass content-type=None
    via the captured headers (HEADER_KEYS deliberately omits content-type).

    Returns the templates (node) list. Node list lives at
    workflowData.templates, or templates at the top level on older shapes.
    """
    meta = get_json(f"{BACKEND}/workflow/{loc}/{wfid}", headers)
    wf = meta.get("workflow", meta)
    file_url = wf.get("fileUrl")
    if not file_url:
        raise SystemExit(f"workflow {wfid} has no fileUrl in its meta")
    # Fetch the signed file URL WITHOUT content-type (signature requirement).
    raw = get(file_url, headers)
    wd = json.loads(raw)
    return wd.get("workflowData", {}).get("templates") or wd.get("templates", [])


def pipelines(loc, headers):
    """Return the opportunity pipelines (with stages) for a location."""
    data = get_json(
        f"{BACKEND}/opportunities/pipelines?locationId={loc}",
        headers,
        {"version": "2021-07-28"},
    )
    return data.get("pipelines", [])


def email_library(loc, headers):
    """Return the set of email-template ids in the location's library.

    Recurses one level into folders (templateType == 'folder').
    """
    lib = set()
    root = get_json(
        f"{BACKEND}/emails/builder?locationId={loc}&limit=200",
        headers,
        {"version": "2021-07-28"},
    )
    for b in root.get("builders", []):
        if b.get("templateType") == "folder":
            kids = get_json(
                f"{BACKEND}/emails/builder?locationId={loc}"
                f"&parentId={b['id']}&limit=200",
                headers,
                {"version": "2021-07-28"},
            )
            lib |= {
                x.get("id")
                for x in kids.get("builders", [])
                if x.get("templateType") != "folder"
            }
        else:
            lib.add(b.get("id"))
    return lib


def _usage():
    print(__doc__)
    sys.exit(1)


def main(argv):
    # Strip the optional --headers <path> pair so positional parsing is clean.
    hpath = _resolve_headers_path(argv)
    if "--headers" in argv:
        i = argv.index("--headers")
        del argv[i : i + 2]

    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if not argv:
        _usage()

    cmd = argv[0]
    headers = load_headers(hpath)

    if cmd == "list":
        if len(argv) < 2:
            _usage()
        loc = argv[1]
        for w in list_workflows(loc, headers):
            print(f"{w.get('id')}  {w.get('status'):10}  {w.get('name')}")
    elif cmd == "load":
        if len(argv) < 3:
            _usage()
        loc, wfid = argv[1], argv[2]
        templates = load_workflow(loc, wfid, headers)
        print(json.dumps(templates, indent=2))
    elif cmd == "pipelines":
        if len(argv) < 2:
            _usage()
        loc = argv[1]
        for p in pipelines(loc, headers):
            print(f"{p['id']}  {p['name']}  ({len(p.get('stages', []))} stages)")
            for s in p.get("stages", []):
                print(f"    {s.get('id')}  {s.get('name')}")
    elif cmd == "emails":
        if len(argv) < 2:
            _usage()
        loc = argv[1]
        lib = email_library(loc, headers)
        print(f"{len(lib)} email templates in library")
        for tid in sorted(x for x in lib if x):
            print(f"  {tid}")
    else:
        _usage()


if __name__ == "__main__":
    main(sys.argv[1:])
