---
name: connect-n8n
description: Connect Claude Code to an n8n instance through n8n's built-in MCP server, so Claude can build, edit and run n8n workflows (the backend for Leadlock custom functions) in plain English. Explains what n8n is, n8n Cloud vs self-hosted, enabling Instance-level MCP, connecting with OAuth or a token, and checks the connection. Triggers on /connect-n8n, connect n8n, set up n8n, n8n MCP, install the n8n MCP server, hook up n8n, what is n8n, build me an n8n workflow (when n8n is not connected yet).
---

# Connect n8n

n8n is a workflow automation tool: a trigger (like a webhook) starts a chain of steps (look
up a Google Sheet, call an API, write to a CRM) and returns a result. For a Leadlock agency
it is the easiest backend for **custom functions**: the voice agent calls an n8n webhook
mid-call, n8n does the work against any system with an API, and the agent reads back the
answer.

This skill connects Claude Code to n8n's **built-in MCP server**, so you can say "build me
an n8n workflow that looks up a car by stock number in my Google Sheet" and Claude builds it
in your n8n.

## When to invoke

- "Connect n8n" / "set up the n8n MCP" / "what is n8n?"
- The user asks for an n8n workflow and `claude mcp list` shows no n8n server
- Before building a Leadlock custom function that needs a backend the user does not have yet

## Setup check

No Leadlock key is needed to connect n8n. Before you build a custom function on top of it,
confirm `LEADLOCK_API_KEY` is set (fire `setup-check` if not).

## Rules

1. **Use n8n's own built-in MCP server** (Settings > Instance-level MCP). Do not install a
   third-party n8n MCP package unless the user asks for one by name.
2. **Never write a token into a committed file.** `.mcp.json` is gitignored in this kit; still
   prefer OAuth, which stores nothing in the repo.
3. **The instance must be reachable from the internet** for Leadlock to call its webhooks.
   n8n Cloud is. A self-hosted n8n on `localhost` works for Claude but Leadlock cannot reach
   it, so custom functions will fail. Say so before building.
4. **Building and editing workflows over MCP needs n8n 2.13.0 or newer.** Older instances can
   only search and run workflows. n8n Cloud is on the latest stable version.
5. **Every workflow must be switched on for MCP individually**, except search. If Claude
   cannot see a workflow, that switch is the first thing to check.
6. **Production vs test webhooks**: Leadlock must call the **production** webhook URL, which
   only answers once the workflow is published (active). The test URL only works while the
   editor is listening.
7. Never run `publish_workflow` or execute a workflow that writes to a real system without
   showing the user what it will do first.

## Required inputs

Ask which applies:

- **(A) n8n Cloud** (recommended for most agencies): sign up at https://n8n.io, which
  creates `https://<name>.app.n8n.cloud`.
- **(B) Self-hosted n8n** on a public URL, version 2.13.0 or newer, and the user is the
  instance owner or an admin.

## Execution

### Step 1: Turn on MCP in n8n

In n8n: **Settings > Instance-level MCP > Enable MCP access**. Only the owner or an admin can
do this.

### Step 2: Connect Claude Code

In the same page open **Connection details > Connect**.

**OAuth (recommended).** Pick the **OAuth** tab, choose Claude Code, and run the command it
shows from the kit folder. It looks like:

```bash
claude mcp add --transport http n8n https://<your-instance>/mcp-server/http
```

Then inside Claude Code run `/mcp`, select `n8n`, choose **Authenticate**, and approve in
the browser.

**Token instead.** Open the **API key** tab (n8n shows the token once; rotating it revokes
the old one) and run:

```bash
claude mcp add --transport http n8n https://<your-instance>/mcp-server/http \
  --header "Authorization: Bearer <TOKEN>"
```

**Optional: n8n's official Claude skills.** n8n publishes skills that teach Claude its node
conventions. Install them inside Claude Code with:

```
/plugin marketplace add n8n-io/skills
/plugin install n8n-skills@n8n-io
/reload-plugins
```

### Step 3: Verify

Restart Claude Code in the kit folder, then:

```bash
claude mcp list
```

`n8n` should show as connected. Then ask Claude to "list my n8n workflows". An empty
list on a new account is a pass; an auth error means re-run `/mcp` > Authenticate.

### Step 4: Make a workflow visible to Claude

New workflows may need switching on: open the workflow, **... > Settings > Available in
MCP**, or **Settings > Instance-level MCP > Workflows enabled > Enable workflows**.

### Step 5: Hand off

Tell the user what they can say next:

```
n8n is connected. Try:
  "Build an n8n workflow: webhook in, look up the row in my Google Sheet, return a short JSON answer"
  "Turn that workflow into a Leadlock custom function on my agent"
```

## Templates

Shape of a workflow that backs a Leadlock custom function:

```
Webhook (POST, production URL)  ->  lookup step (Google Sheets / HTTP Request / CRM node)
  ->  Respond to Webhook with a SHORT JSON, e.g. {"status": "available", "detail": "2022 Tacoma, silver, stock 1042"}
```

Keep the response small and readable: Leadlock passes whatever JSON comes back straight to
the agent.

## Gotchas

- Google Sheets and other OAuth credentials are created inside n8n (on Cloud it is a "Sign in
  with Google" click). Claude cannot click that for the user; it tells them which node needs a
  credential.
- **Leadlock sends everything the agent collected inside a field named `arguments`, and n8n
  expressions refuse to read a field with that name.** Put a Code node right after the Webhook
  that copies `arguments` out into normal fields, then build the rest on those.
- Workflows Claude creates over MCP are already "Available in MCP"; ones you build by hand
  need the switch (Step 4).
- A workflow that works in the editor but fails from Leadlock is almost always the test URL
  or an unpublished workflow (Rule 6).
- Every client connected to the MCP server sees every MCP-enabled workflow the user can
  access. Do not enable workflows that touch another client's data.

## Rule capture

<!-- Append new rules here as the maintainer learns from real runs. -->
