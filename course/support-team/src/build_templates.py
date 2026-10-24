"""Builds the four n8n workflow templates in ../workflows/ from the JS in this folder.

Maintainers only: run `python3 build_templates.py` after editing a .js file. The
templates carry no ids, credentials or hosts. The REPLACE_* markers and the
`const X = ...;` lines at the top of each Code node are filled in by
.claude/skills/install-support-team/install.py.
"""
import json
import os
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "workflows")

WEBHOOK_CRED = {"httpHeaderAuth": {"id": "REPLACE_CRED_WEBHOOK", "name": "Support team webhook key"}}
EMAIL_CRED = {"gmailOAuth2": {"id": "REPLACE_CRED_EMAIL", "name": "Email"}}
LEADLOCK_CRED = {"httpHeaderAuth": {"id": "REPLACE_CRED_LEADLOCK", "name": "Leadlock API key"}}
D = "$('Decide').first().json"


def js(*names):
    return "\n".join(open(os.path.join(HERE, n)).read() for n in names)


def node(wf, name, type_, ver, params, pos, **kw):
    n = {"id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"support-team/{wf}/{name}")), "name": name,
         "type": type_, "typeVersion": ver, "position": pos, "parameters": params}
    n.update(kw)
    return n


def table(table_name):
    return {"__rl": True, "mode": "id", "value": f"REPLACE_TABLE_{table_name}"}


def get_all(wf, table_name, pos):
    return node(wf, f"Get {table_name}", "n8n-nodes-base.dataTable", 1,
                {"resource": "row", "operation": "get", "dataTableId": table(table_name), "returnAll": True},
                pos, alwaysOutputData=True, executeOnce=True)


def get_verification(wf, pos):
    return node(wf, "Get Verification", "n8n-nodes-base.dataTable", 1,
                {"resource": "row", "operation": "get", "dataTableId": table("Verifications"),
                 "matchType": "allConditions",
                 "filters": {"conditions": [{"keyName": "call_sid", "condition": "eq",
                                             "keyValue": "={{ $('Unwrap').first().json.call_sid || '__none__' }}"}]},
                 "returnAll": True}, pos, alwaysOutputData=True, executeOnce=True)


def upsert(wf, name, table_name, key, cols, pos):
    return node(wf, name, "n8n-nodes-base.dataTable", 1, {
        "resource": "row", "operation": "upsert", "dataTableId": table(table_name), "matchType": "allConditions",
        "filters": {"conditions": [{"keyName": key, "condition": "eq", "keyValue": f"={{{{ $json.write.{key} }}}}"}]},
        "columns": {"mappingMode": "defineBelow", "matchingColumns": [],
                    "value": {c: f"={{{{ $json.write.{c} }}}}" for c, _ in cols},
                    "schema": [{"id": c, "displayName": c, "required": False, "defaultMatch": False, "display": True,
                                "type": t, "canBeUsedToMatch": True} for c, t in cols]},
        "options": {}}, pos)


def reply(wf, name, body, pos):
    return node(wf, name, "n8n-nodes-base.respondToWebhook", 1.1,
                {"respondWith": "json", "responseBody": body, "options": {}}, pos)


def head(wf, slug):
    return [
        node(wf, "Webhook", "n8n-nodes-base.webhook", 2,
             {"httpMethod": "POST", "path": f"REPLACE_SLUG-{slug}", "authentication": "headerAuth",
              "responseMode": "responseNode", "options": {}}, [0, 0],
             credentials=WEBHOOK_CRED, webhookId="REPLACE_WEBHOOK_ID"),
        node(wf, "Unwrap", "n8n-nodes-base.code", 2, {"jsCode": js("unwrap.js")}, [220, 0]),
    ]


def send_nodes(wf, x):
    """Email / Text / reply nodes shared by Verify Caller and Billing."""
    return [
        node(wf, "Send Via", "n8n-nodes-base.switch", 3,
             {"mode": "expression", "numberOutputs": 3,
              "output": f"={{{{ ({{email:0, sms:1}})[{D}.action] ?? 2 }}}}"}, [x, -100]),
        node(wf, "Email", "n8n-nodes-base.gmail", 2.1,
             {"sendTo": f"={{{{ {D}.send_to }}}}", "subject": f"={{{{ {D}.subject }}}}", "emailType": "text",
              "message": f"={{{{ {D}.message }}}}", "options": {"appendAttribution": False}},
             [x + 220, -260], credentials=EMAIL_CRED, onError="continueErrorOutput"),
        node(wf, "Text", "n8n-nodes-base.httpRequest", 4.2,
             {"method": "POST", "url": "REPLACE_LEADLOCK_API_URL/outbound/sms",
              "authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth",
              "sendBody": True, "specifyBody": "json",
              "jsonBody": f"={{{{ JSON.stringify({{to_number: {D}.send_to, message: {D}.message, "
                          f"from_phone_number_id: 'REPLACE_SMS_FROM_ID'}}) }}}}",
              "options": {"timeout": 4000}},
             [x + 220, -60], credentials=LEADLOCK_CRED, onError="continueRegularOutput"),
        reply(wf, "Reply Text", f"={{{{ JSON.stringify($json.success === true ? {D}.response : "
                                f"{{sent: false, error: 'send_failed'}}) }}}}", [x + 440, -60]),
        reply(wf, "Reply Send Failed", "={{ JSON.stringify({sent: false, error: 'send_failed'}) }}", [x + 440, -360]),
    ]


def c(*targets):
    return {"main": [[{"node": t, "type": "main", "index": 0} for t in outs] for outs in targets]}


def chain(names):
    return {a: c([b]) for a, b in zip(names, names[1:])}


SETTINGS_PRIVATE = {"executionOrder": "v1", "saveDataSuccessExecution": "none", "saveDataErrorExecution": "none",
                    "saveManualExecutions": False, "saveExecutionProgress": False}
SETTINGS = {"executionOrder": "v1", "saveDataSuccessExecution": "none", "saveDataErrorExecution": "all",
            "saveManualExecutions": True, "saveExecutionProgress": False}
VCOLS = [("call_sid", "string"), ("customer_id", "string"), ("code_hash", "string"),
         ("expires_at", "string"), ("attempts", "number"), ("verified", "boolean")]
RCOLS = [("rental_id", "string"), ("customer_id", "string"), ("unit_id", "string"), ("model", "string"),
         ("start_date", "string"), ("end_date", "string"), ("status", "string"), ("site", "string"),
         ("invoice_id", "string"), ("invoice_total", "number"), ("invoice_status", "string"), ("invoice_due", "string")]
SCOLS = [("ticket_id", "string"), ("customer_id", "string"), ("unit_id", "string"), ("issue", "string"),
         ("status", "string"), ("tech_eta", "string"), ("created_at", "string")]


def verify_caller():
    wf = "verify"
    nodes = head(wf, "verify") + [
        get_all(wf, "Customers", [440, 0]),
        get_verification(wf, [660, 0]),
        node(wf, "Random", "n8n-nodes-base.crypto", 1,
             {"action": "generate", "dataPropertyName": "rand", "encodingType": "hex", "stringLength": 16},
             [770, 120], executeOnce=True),
        node(wf, "Decide", "n8n-nodes-base.code", 2, {"jsCode": js("decide-verify.js")}, [880, 0], executeOnce=True),
        node(wf, "Needs Save?", "n8n-nodes-base.switch", 3,
             {"mode": "expression", "numberOutputs": 2, "output": "={{ $json.write ? 0 : 1 }}"}, [1100, 0]),
        upsert(wf, "Save Verification", "Verifications", "call_sid", VCOLS, [1320, -100]),
        reply(wf, "Reply", f"={{{{ JSON.stringify({D}.response) }}}}", [2200, 0]),
    ] + send_nodes(wf, 1540)
    conn = chain(["Webhook", "Unwrap", "Get Customers", "Get Verification", "Random", "Decide", "Needs Save?"])
    conn.update({"Needs Save?": c(["Save Verification"], ["Reply"]), "Save Verification": c(["Send Via"]),
                 "Send Via": c(["Email"], ["Text"], ["Reply"]), "Email": c(["Reply"], ["Reply Send Failed"]),
                 "Text": c(["Reply Text"])})
    return {"name": "Verify Caller", "nodes": nodes, "connections": conn, "settings": SETTINGS_PRIVATE}


def desk(wf, slug, title, tables, decide_js, write=None):
    nodes = head(wf, slug) + [get_verification(wf, [440, 0])]
    names = ["Webhook", "Unwrap", "Get Verification"]
    x = 660
    for t in ["Customers"] + tables:
        nodes.append(get_all(wf, t, [x, 0]))
        names.append(f"Get {t}")
        x += 220
    nodes.append(node(wf, "Decide", "n8n-nodes-base.code", 2, {"jsCode": js("gate.js", decide_js)}, [x, 0],
                      executeOnce=True))
    names.append("Decide")
    reply_pos = [x + 660, 0]
    conn = chain(names)
    if write:
        wname, wtable, key, cols = write
        nodes += [node(wf, "Needs Save?", "n8n-nodes-base.switch", 3,
                       {"mode": "expression", "numberOutputs": 2, "output": "={{ $json.write ? 0 : 1 }}"}, [x + 220, 0]),
                  upsert(wf, wname, wtable, key, cols, [x + 440, -100])]
        conn.update({"Decide": c(["Needs Save?"]), "Needs Save?": c([wname], ["Reply"]), wname: c(["Reply"])})
    nodes.append(reply(wf, "Reply", f"={{{{ JSON.stringify({D}.response) }}}}", reply_pos))
    if not write:
        conn["Decide"] = c(["Reply"])
    return {"name": title, "nodes": nodes, "connections": conn, "settings": SETTINGS}


def billing():
    wf = desk("billing", "billing", "Billing", ["Rentals"], "decide-billing.js")
    x = wf["nodes"][-2]["position"][0]
    wf["nodes"].extend(send_nodes("billing", x + 220))
    wf["connections"].update({"Decide": c(["Send Via"]), "Send Via": c(["Email"], ["Text"], ["Reply"]),
                              "Email": c(["Reply"], ["Reply Send Failed"]), "Text": c(["Reply Text"])})
    return wf


TEMPLATES = {
    "verify-caller.json": verify_caller(),
    "rentals.json": desk("rentals", "rentals", "Rentals", ["Fleet", "Rentals"], "decide-rentals.js",
                         ("Save Rental", "Rentals", "rental_id", RCOLS)),
    "maintenance.json": desk("maintenance", "maintenance", "Maintenance", ["Troubleshooting", "Rentals", "Service"],
                             "decide-maintenance.js", ("Save Ticket", "Service", "ticket_id", SCOLS)),
    "billing.json": billing(),
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fname, wf in TEMPLATES.items():
        with open(os.path.join(OUT, fname), "w") as f:
            json.dump(wf, f, indent=1)
            f.write("\n")
        print(f"wrote workflows/{fname}: {len(wf['nodes'])} nodes")
