# Leadlock course materials

Everything shown in the Leadlock course videos: the slide decks, the setup checklist, the n8n outbound-call workflow and the support team from the advanced course. Nothing here needs a server, an install or an API key to open.

## The presentations

Each deck opens two ways:

- **PDF**: one slide per page. Opens anywhere.
- **Interactive deck**: double-click `index.html` in the deck's folder. It opens in your browser with the click-builds and videos.

| Video | Deck | Slides | PDF | Interactive |
|---|---|---|---|---|
| 2a | Voice agents 101: what you're actually selling | 11 | [PDF](presentations/2a-voice-agents-101.pdf) | [index.html](presentations/2a-voice-agents-101/index.html) |
| 2b | Pick your offer: speed beats everything | 14 | [PDF](presentations/2b-pick-your-offer.pdf) | [index.html](presentations/2b-pick-your-offer/index.html) |
| 2c | Get your first clients: the layup offer | 16 | [PDF](presentations/2c-get-clients.pdf) | [index.html](presentations/2c-get-clients/index.html) |
| 3 | Lead lists: build your lead list | 14 | [PDF](presentations/3-lead-lists.pdf) | [index.html](presentations/3-lead-lists/index.html) |
| 4 | Build an agent: prompt, settings, tools, testing | 16 | [PDF](presentations/4-build-an-agent.pdf) | [index.html](presentations/4-build-an-agent/index.html) |
| 5 | Mindset: win it in your head first | 14 | [PDF](presentations/5-mindset.pdf) | [index.html](presentations/5-mindset/index.html) |
| 6 | Cold calling: the call that books the demo | 16 | [PDF](presentations/6-cold-calling.pdf) | [index.html](presentations/6-cold-calling/index.html) |
| 7 | Contact Intelligence: your agent knows who's calling | 16 | [PDF](presentations/7-contact-intelligence.pdf) | [index.html](presentations/7-contact-intelligence/index.html) |
| 8 | Outbound triggers: make your agent call first | 12 | [PDF](presentations/8-outbound-triggers.pdf) | [index.html](presentations/8-outbound-triggers/index.html) |
| 9 | Agentic setup: set up Claude Code to build your agents | 16 | [PDF](presentations/9-agentic-setup.pdf) | [index.html](presentations/9-agentic-setup/index.html) |
| 10 | Advanced course kickoff: build an AI customer support team | 17 | [PDF](presentations/10-support-team.pdf) | [index.html](presentations/10-support-team/index.html) |

GitHub shows the PDFs in the browser. For the interactive decks, clone or download the repo first, then double-click `index.html`.

### Driving an interactive deck

| Key | What it does |
|---|---|
| Right arrow, Space, Page Down | Next build or slide |
| Left arrow, Page Up | Back |
| Home / End | First / last slide |
| N | Speaker notes |
| F | Full screen |
| S | Presenter window (notes, next slide, timer) |

## The setup checklist

[checklists/agent-kit-setup.html](checklists/agent-kit-setup.html): from zero to Claude building your voice agents, with Mac and Windows commands. Double-click to open it. Tick each step as you go; your ticks are saved in that browser.

## The n8n outbound-call workflow (video 8)

[n8n/leadlock-outbound-call.json](n8n/leadlock-outbound-call.json): three nodes. A manual trigger, a "Who to call" node, and an HTTP Request that tells Leadlock to start the call.

### How to import

1. In n8n, create a new workflow, open the **...** menu and pick **Import from File**. Choose `leadlock-outbound-call.json`.
2. Open the **Leadlock: start the call** node. Under Credential, create a new **Header Auth** credential: Name `X-API-Key`, Value your Leadlock API key (Leadlock: Settings, API Keys, Create).
3. Open **Who to call** and replace the two placeholders:
   - `agent_id`: `PASTE-YOUR-AGENT-ID`, your agent's ID from Leadlock
   - `to_number`: `PASTE-YOUR-NUMBER`, the number to call, with `+1` first
4. Click **Execute workflow**. The response shows a `call_id`, and the phone rings.

Before your first test, turn on outbound calling in Leadlock and set the agent to Outbound or Both, with a phone number assigned. Swap the manual trigger for a webhook, a form or a schedule when you're ready.

### The GoHighLevel version

No n8n needed. In a GoHighLevel workflow:

1. Trigger: **Contact Tag** added, tag `call-me-now`.
2. Action: **Custom Webhook**, `POST https://leadlock-app.onrender.com/outbound/trigger`, header `X-API-Key: <your Leadlock key>`, body:
   ```json
   { "customData": { "agent_id": "PASTE-YOUR-AGENT-ID", "to_number": "{{contact.phone}}" } }
   ```
3. Action: remove the tag `call-me-now`, so it can fire again.

Add the tag to a test contact with your own number on it, and your phone rings in about 10 seconds. The Leadlock app in GoHighLevel also has a ready-made Outbound Call action that needs no key.

## The support team (advanced course)

[support-team/](support-team/README.md): the data, n8n workflow templates and source for Granite Peak Equipment Rental's three AI desks (Joanne on rentals, Jim Bob on maintenance, Miss Hattie Mae on billing) with bank-style caller verification.

To build it in your own Leadlock account and n8n, open Claude Code in the kit folder and say **"install the support team"**. It checks your setup first (Leadlock key, GoHighLevel, n8n, an email credential in n8n, an A2P-registered number, `MY_PHONE_NUMBER`) and tells you what to fix, then builds, tests and reports. Following along one video at a time? Say "install the support team tables", then "install the Verify Caller step", "install Joanne", "install Jim Bob" and "install Miss Hattie Mae".
