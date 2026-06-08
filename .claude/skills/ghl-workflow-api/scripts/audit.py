#!/usr/bin/env python3
"""Audit every workflow in a GoHighLevel location for common breakage.

Generalized from a real workflow-validation battery. Read-only: it never
writes. It fetches all workflows, walks every action node, and flags issues.

Checks:
  - builder errors        (node.incompleteData == True)
  - opportunity nodes     (pipeline_id matches expected, stage id is valid,
                           no stray legacy 'stage' key)
  - custom_webhook        (saveResponse set but webhookResponse sample empty;
                           url host not in an allow-list, if you pass one)
  - email                 (template_id is actually in the email library;
                           node has either a template or inline html)
  - dead workflow refs    (add_to_workflow / remove_from_workflow / if_else
                           workflow_contact conditions pointing at ids that
                           no longer exist in this location)
  - publish status        (every workflow should be 'published')

Tokens expire ~hourly; re-capture on 401. See reference/token-capture.md.

Usage:
  python3 audit.py <location_id> [options]

Options:
  --expected-pipeline <id>   pipeline id that create_opportunity nodes MUST
                             use. If omitted, pipeline membership is not
                             enforced (only stage-within-its-own-pipeline is).
  --webhook-host <host>      substring every custom_webhook url must contain
                             (e.g. your prod host). Repeatable. If omitted,
                             webhook host is not checked.
  --require-published        flag any workflow whose status != published.
  --headers <path>           path to headers.json (else $GHL_HEADERS or the
                             skill-local headers.json).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl  # noqa: E402


def _parse_args(argv):
    opts = {
        "loc": None,
        "expected_pipeline": None,
        "webhook_hosts": [],
        "require_published": False,
    }
    i = 0
    positional = []
    while i < len(argv):
        a = argv[i]
        if a in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif a == "--expected-pipeline":
            opts["expected_pipeline"] = argv[i + 1]
            i += 2
        elif a == "--webhook-host":
            opts["webhook_hosts"].append(argv[i + 1])
            i += 2
        elif a == "--require-published":
            opts["require_published"] = True
            i += 1
        else:
            positional.append(a)
            i += 1
    if not positional:
        print(__doc__)
        sys.exit(1)
    opts["loc"] = positional[0]
    return opts


def check_workflow(name, templates, stages_by_pipeline, lib, live_ids,
                   expected_pipeline=None, webhook_hosts=None):
    """Pure node-checking battery for ONE workflow's templates list.

    Takes an already-loaded `templates` (node array) plus the reference data
    (valid stages per pipeline, the email-template-id set, the live workflow-id
    set) and returns a list of issue strings. No network, no globals: this is
    the testable core of the audit and can be exercised entirely offline.
    """
    webhook_hosts = webhook_hosts or []
    issues = []
    for n in templates:
        t = n.get("type")
        a = n.get("attributes", {})
        label = n.get("name") or "(unnamed)"

        if n.get("incompleteData"):
            issues.append(f"{name}: '{label}' incompleteData=True (builder error)")

        if t == "create_opportunity":
            pid = a.get("pipeline_id")
            if expected_pipeline and pid != expected_pipeline:
                issues.append(
                    f"{name}: opp '{label}' wrong pipeline {pid}"
                )
            valid = stages_by_pipeline.get(pid, set())
            if a.get("pipeline_stage_id") not in valid:
                issues.append(f"{name}: opp '{label}' invalid stage")
            if "stage" in a:
                issues.append(f"{name}: opp '{label}' stray legacy 'stage' key")

        elif t == "custom_webhook":
            if a.get("saveResponse") and a.get("webhookResponse") == {}:
                issues.append(
                    f"{name}: webhook '{label}' saveResponse with empty sample"
                )
            url = a.get("url", "")
            if url and webhook_hosts and not any(h in url for h in webhook_hosts):
                issues.append(
                    f"{name}: webhook '{label}' url not in allow-list {url[:60]}"
                )

        elif t == "email":
            tid = a.get("template_id")
            if tid and tid not in lib:
                issues.append(
                    f"{name}: email '{label}' template {tid} not in library"
                )
            if not tid and not a.get("html"):
                issues.append(f"{name}: email '{label}' has no content")

        elif t in ("add_to_workflow", "remove_from_workflow"):
            tgts = a.get("workflow_id") or []
            if isinstance(tgts, str):
                tgts = [tgts]
            for x in tgts:
                if x not in live_ids:
                    issues.append(f"{name}: {t} -> dead workflow {str(x)[:8]}")

        elif t == "if_else":
            for br in a.get("branches", []):
                for seg in br.get("segments", []):
                    for c in seg.get("conditions", []):
                        if (
                            c.get("conditionType") == "workflow_contact"
                            and c.get("conditionValue") not in live_ids
                        ):
                            issues.append(
                                f"{name}: if_else references dead workflow "
                                f"{str(c.get('conditionValue'))[:8]}"
                            )
    return issues


def audit(loc, headers, expected_pipeline=None, webhook_hosts=None,
          require_published=False):
    """Run the full battery against a live location. Returns issue strings.

    Fetches reference data and every workflow's node list from the API, then
    delegates the per-workflow node checks to check_workflow() (the pure,
    offline-testable core).
    """
    webhook_hosts = webhook_hosts or []
    issues = []

    # Build the valid-stage map per pipeline (and overall valid stage set).
    pls = ghl.pipelines(loc, headers)
    stages_by_pipeline = {
        p["id"]: {s["id"] for s in p.get("stages", [])} for p in pls
    }
    if expected_pipeline and expected_pipeline not in stages_by_pipeline:
        issues.append(
            f"CRITICAL: expected pipeline {expected_pipeline} not found in "
            "this location"
        )

    # Email-template library.
    lib = ghl.email_library(loc, headers)

    # All workflows + the set of live ids (for dead-ref detection).
    wfs = ghl.list_workflows(loc, headers)
    live_ids = {w["id"] for w in wfs}

    workflows = {}
    for w in wfs:
        if require_published and w.get("status") != "published":
            issues.append(f"{w['name']}: status={w.get('status')}")
        workflows[w["name"]] = ghl.load_workflow(loc, w["id"], headers)

    for name, templates in workflows.items():
        issues.extend(
            check_workflow(
                name, templates, stages_by_pipeline, lib, live_ids,
                expected_pipeline=expected_pipeline, webhook_hosts=webhook_hosts,
            )
        )
    return issues


def main(argv):
    hpath = ghl._resolve_headers_path(argv)
    if "--headers" in argv:
        i = argv.index("--headers")
        del argv[i : i + 2]
    opts = _parse_args(argv)
    headers = ghl.load_headers(hpath)

    issues = audit(
        opts["loc"],
        headers,
        expected_pipeline=opts["expected_pipeline"],
        webhook_hosts=opts["webhook_hosts"],
        require_published=opts["require_published"],
    )

    print("=" * 60)
    print("WORKFLOW AUDIT RESULT")
    print("=" * 60)
    if issues:
        for i in issues:
            print(f"  FAIL  {i}")
        print(f"\n{len(issues)} issue(s) found.")
        sys.exit(1)
    else:
        print("  PASS  0 issues across all workflows")


if __name__ == "__main__":
    main(sys.argv[1:])
