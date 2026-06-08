#!/usr/bin/env python3
"""Dump a GoHighLevel workflow node-by-node, human-readable (stdlib only).

Read-only. For each node it prints order, type, name, a one-line summary of
the key attributes, and the `next` pointer, so you can see the whole flow
(waits, branches, GPT prompts, webhooks, tags, sub-workflow jumps) without
opening the builder.

Tokens expire ~hourly; re-capture on 401. See reference/token-capture.md.

Usage:
  python3 trace.py <location_id>                      list workflow names
  python3 trace.py <location_id> "Workflow Name"      trace one by name
  python3 trace.py <location_id> "Name A" "Name B"    trace several
  python3 trace.py <location_id> --id <workflow_id>   trace one by id
  python3 trace.py <location_id> --json "Name"        also dump raw json

Options:
  --headers <path>   path to headers.json (else $GHL_HEADERS or skill-local).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl  # noqa: E402


def summarize(n):
    """One-line summary of a node's attributes by type."""
    t = n.get("type")
    a = n.get("attributes", {})
    if t == "wait":
        w = a.get("window")
        sa = a.get("startAfter", {})
        if a.get("type") == "condition":
            cond = (
                a.get("condition", {})
                .get("branches", [{}])[0]
                .get("segments", [{}])[0]
                .get("conditions", [])
            )
            return (
                f"WAIT-CONDITION (timeout {sa.get('value')}{sa.get('type')}) "
                f"cond={json.dumps(cond)[:140]}"
            )
        return f"WAIT {sa.get('value')}{sa.get('type')} window={w}"
    if t == "if_else":
        conds = []
        for br in a.get("branches", []):
            for seg in br.get("segments", []):
                for c in seg.get("conditions", []):
                    conds.append(
                        f"{c.get('conditionType')}/{c.get('conditionSubType')} "
                        f"{c.get('conditionOperator')} "
                        f"{json.dumps(c.get('conditionValue'))[:50]}"
                    )
        return f"IF [{a.get('conditionName')}] " + " | ".join(conds)
    if t == "chatgpt":
        prompt = json.dumps((a.get("promptText") or "")[:160])
        return f"GPT model={a.get('model')} prompt[:160]={prompt}"
    if t == "custom_webhook":
        body = json.dumps(a.get("body", {}))[:160]
        return f"WEBHOOK {a.get('method')} {a.get('url')} body~{body}"
    if t in ("add_contact_tag", "remove_contact_tag"):
        return f"{t.upper()} {a.get('tags')}"
    if t == "create_opportunity":
        return (
            f"CREATE-OPP pipeline={a.get('pipeline_id')} "
            f"stage={a.get('pipeline_stage_id')}"
        )
    if t == "email":
        return f"EMAIL template={a.get('template_id')} html={bool(a.get('html'))}"
    if t == "update_contact_field":
        return f"UPDATE-FIELD {json.dumps(a)[:160]}"
    if t == "math_operation" or "math" in (t or "").lower():
        return f"MATH {json.dumps(a)[:160]}"
    if t in ("add_to_workflow", "remove_from_workflow"):
        return f"{t.upper()} -> {a.get('workflow_id')}"
    if t == "goto":
        return f"GOTO {json.dumps(a)[:100]}"
    return json.dumps(a)[:140]


def trace(loc, wfid, name, headers, dump_json=False):
    templates = ghl.load_workflow(loc, wfid, headers)
    print("\n" + "=" * 78)
    print(f"  {name}  ({len(templates)} nodes)")
    print("=" * 78)
    for n in templates:
        node_name = (n.get("name") or "")[:30]
        print(
            f"[{n.get('order')}] {str(n.get('type')):20} "
            f"'{node_name:30}' :: {summarize(n)}"
        )
        print(f"      next={json.dumps(n.get('next'))[:90]}")
    if dump_json:
        print("\n--- raw templates json ---")
        print(json.dumps(templates, indent=2))


def main(argv):
    hpath = ghl._resolve_headers_path(argv)
    if "--headers" in argv:
        i = argv.index("--headers")
        del argv[i : i + 2]

    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if argv else 1)

    dump_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]

    by_id = None
    if "--id" in argv:
        i = argv.index("--id")
        by_id = argv[i + 1]
        del argv[i : i + 2]

    loc = argv[0]
    names = argv[1:]
    headers = ghl.load_headers(hpath)

    if by_id:
        trace(loc, by_id, f"id:{by_id}", headers, dump_json)
        return

    wfs = ghl.list_workflows(loc, headers)
    name_to_id = {w["name"]: w["id"] for w in wfs}

    if not names:
        print(f"{len(wfs)} workflows in {loc}:")
        for w in wfs:
            print(f"  {w.get('status'):10}  {w['name']}")
        print('\nPass one or more names to trace, e.g. trace.py <loc> "My Workflow"')
        return

    for nm in names:
        if nm not in name_to_id:
            print(f"  (skipped) no workflow named '{nm}'")
            continue
        trace(loc, name_to_id[nm], nm, headers, dump_json)


if __name__ == "__main__":
    main(sys.argv[1:])
