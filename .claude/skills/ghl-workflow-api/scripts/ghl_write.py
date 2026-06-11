#!/usr/bin/env python3
"""Write action-node edits back to a GoHighLevel workflow (stdlib only).

This is the hard-won half of the methodology. It writes ACTION-NODE
attributes (waits, fields, GPT prompts, webhook bodies, tags, opportunity
pipeline/stage) via GHL's private auto-save and publish endpoints.

It does NOT and CANNOT set triggers. GHL migrated workflow triggers to a
separate "trigger bucket" (isTriggerBucketMigrated=true); newTriggers /
oldTriggers come back null even on healthy workflows, so triggers and
inbound-webhook trigger URLs have to be added in the builder UI. See
reference/trigger-bucket-limitation.md.

THE VERSION GOTCHA (read this before you write anything):
  Every workflow carries an integer `version`. The server increments it on
  each save. You must send the CURRENT version, not current+1. Sending
  current+1 returns 422 "outdated" because the server thinks you are behind.
  Always call get_state() first to read the live version, edit the templates
  it returns, then pass that SAME version back to auto_save() / publish().

Endpoints:
  PUT /workflow/{loc}/{wfid}/auto-save   draft save  (version pinned)
  PUT /workflow/{loc}/{wfid}             publish      (status=published,
                                                       version pinned,
                                                       autoSaveSession=null)

Tokens expire ~hourly; re-capture on 401. See reference/token-capture.md.

Usage (inspect current state, the safe first step):
  python3 ghl_write.py state <location_id> <workflow_id>

Programmatic use (the normal path):
  import ghl, ghl_write
  h = ghl.load_headers()
  version, templates = ghl_write.get_state(loc, wfid, h)
  # ... mutate templates in place ...
  ghl_write.auto_save(loc, wfid, templates, version, h)   # draft
  ghl_write.publish(loc, wfid, templates, version, h)      # go live
"""
import json
import os
import sys
import urllib.error
import urllib.request

# Import the read helper that lives beside this file.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl  # noqa: E402

BACKEND = ghl.BACKEND


def _put(url, body, headers, timeout=60):
    """PUT JSON with the captured headers. Writes DO send content-type."""
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method="PUT",
        headers=ghl.hdrs(headers, {"content-type": "application/json"}),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        body_txt = exc.read().decode()[:600] if exc.fp else ""
        if exc.code == 401:
            raise SystemExit(
                "HTTP 401 on write. Token expired (~1h). Re-capture it."
            ) from exc
        if exc.code == 422 and "outdated" in body_txt.lower():
            raise SystemExit(
                "HTTP 422 'outdated': you sent the wrong version. Call "
                "get_state() again to read the CURRENT version and pass that "
                "exact value (NOT current+1). See the version gotcha at the "
                "top of this file."
            ) from exc
        raise SystemExit(f"HTTP {exc.code} on write\n{body_txt}") from exc


def get_state(loc, wfid, headers):
    """Return (current_version, templates) for a workflow.

    Always call this immediately before a write so the version is fresh.
    templates is the live node list (mutate it, then save it).
    """
    meta = ghl.get_json(f"{BACKEND}/workflow/{loc}/{wfid}", headers)
    wf = meta.get("workflow", meta)
    version = wf.get("version")
    if version is None:
        raise SystemExit(
            f"workflow {wfid} meta has no 'version' field; cannot safely write"
        )
    templates = ghl.load_workflow(loc, wfid, headers)
    return version, templates


def auto_save(loc, wfid, templates, version, headers):
    """Save a DRAFT (does not publish). version must be the CURRENT version.

    Returns (status, response). Use this to stage changes, then publish().
    """
    # The server reads the node list from workflowData.templates. Sending only a
    # top-level "templates" key is accepted (HTTP 200) but stores an EMPTY
    # workflow - silently wiping every node. Always nest under workflowData.
    body = {
        "templates": templates,
        "workflowData": {"templates": templates},
        "version": version,
    }
    return _put(f"{BACKEND}/workflow/{loc}/{wfid}/auto-save", body, headers)


def publish(loc, wfid, templates, version, headers, allow_multiple=None):
    """PUBLISH the workflow live. version must be the CURRENT version.

    Sends status=published and autoSaveSession=null (clears any pending draft
    session so the publish is not rejected as conflicting). The server
    increments the version itself; do not pre-increment it.

    Pass allow_multiple (read from the workflow meta) to PRESERVE re-entry -
    publish defaults it to false otherwise, breaking dunning-style re-entry.

    NOTE: publish VALIDATES nodes. Snapshot-imported workflows often have nodes
    missing required config (internal_notification with no user, emails pointing
    at the old location). Those fail publish with 400 MISSING_REQUIRED_FIELDS -
    finish/publish them in the GHL UI. auto_save (draft) does not validate.

    Returns (status, response).
    """
    body = {
        "templates": templates,
        "workflowData": {"templates": templates},
        "version": version,
        "status": "published",
        "autoSaveSession": None,
    }
    if allow_multiple is not None:
        body["allowMultiple"] = allow_multiple
    return _put(f"{BACKEND}/workflow/{loc}/{wfid}", body, headers)


def _usage():
    print(__doc__)
    sys.exit(1)


def main(argv):
    hpath = ghl._resolve_headers_path(argv)
    if "--headers" in argv:
        i = argv.index("--headers")
        del argv[i : i + 2]

    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if not argv:
        _usage()

    cmd = argv[0]
    headers = ghl.load_headers(hpath)

    if cmd == "state":
        if len(argv) < 3:
            _usage()
        loc, wfid = argv[1], argv[2]
        version, templates = get_state(loc, wfid, headers)
        print(f"current version: {version}")
        print(f"nodes: {len(templates)}")
        print(
            "edit the templates list, then call auto_save()/publish() with "
            f"version={version}. Re-read state right before writing."
        )
    else:
        _usage()


if __name__ == "__main__":
    main(sys.argv[1:])
