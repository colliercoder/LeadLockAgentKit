#!/usr/bin/env python3
"""Provision a talking-website voice agent + web demo slug on Leadlock.

Stdlib only. Does steps 2-4 of the talking-website skill: (optionally) discover a
GHL calendar to attach, create the agent with the page-control + booking tools and
a sales prompt, and create the public "web" demo (which bills as real call minutes
and logs as a Website conversation).

Env:
  LEADLOCK_API_KEY   (required)   your Leadlock key
  LEADLOCK_API_URL   default https://leadlock-app.onrender.com

Examples:
  # List calendars to pick one for booking:
  LEADLOCK_API_KEY=sk_live_... python3 provision.py --list-calendars

  # Create a talking-website agent (no booking):
  LEADLOCK_API_KEY=sk_live_... python3 provision.py \
      --name "Acme Website Assistant" --business "Acme Plumbing" --voice xai \
      --page "/ : Home" --page "/services : What we do" --page "/contact : Contact us"

  # ...with booking on a specific calendar:
  ... --calendar-integration-id <uuid> --calendar-id <ghl_calendar_id>

Prints the demo slug and the exact <script> tag to paste into the site.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_KEY = os.environ.get("LEADLOCK_API_KEY", "").strip()
BASE = os.environ.get("LEADLOCK_API_URL", "https://leadlock-app.onrender.com").rstrip("/")
WS_BASE = BASE.replace("https://", "wss://").replace("http://", "ws://")

WEB_TOOLS = [
    "web_navigate", "web_scroll", "web_scroll_to", "web_highlight",
    "web_clear_highlight", "web_fill", "web_click", "web_remember",
]
BOOKING_TOOLS = ["book_appointment", "check_availability", "get_appointments", "update_contact"]


def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        BASE + path, data=data, method=method,
        headers={"Content-Type": "application/json", "X-API-Key": API_KEY},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit("ERROR {} on {} {}:\n{}".format(e.code, method, path, e.read().decode("utf-8", "replace")))
    except urllib.error.URLError as e:
        sys.exit("Could not reach {}: {}".format(BASE, e))


def list_calendars():
    ints = call("GET", "/integrations/ghl/integrations")
    if not ints:
        print("No GHL integrations on this account. Connect GHL to enable booking.")
        return
    for i in ints:
        iid = i.get("id")
        print("\nIntegration {}  ({})".format(iid, i.get("location_name") or i.get("name")))
        cals = call("GET", "/integrations/ghl/calendars?integration_id=" + iid)
        for c in cals:
            print("  calendar_id={}  | {}".format(c.get("id"), c.get("name")))
    print("\nRe-run with --calendar-integration-id <uuid> --calendar-id <id> to attach one.")


def build_prompt(business, pages, booking):
    page_lines = "\n".join("- \"{}\" -> {}".format(p[0], p[1]) for p in pages) or "(no page map provided)"
    booking_block = (
        "\nBOOKING & LEADS:\n"
        "- Introduce yourself, get the visitor's name early, and call web_remember(name).\n"
        "- To book: collect name + phone + email (+ address if relevant), then check_availability and book_appointment.\n"
        "- As soon as you have a name + phone, call update_contact(first_name, phone, email, ...) so the lead is saved even if they don't book.\n"
        if booking else ""
    )
    return (
        "You are the friendly voice assistant for {biz}. You are talking to a visitor who is on the "
        "website right now, and you can CONTROL the page for them. Always CALL the matching tool "
        "IMMEDIATELY (do not just describe what you'd do), then say one short line.\n\n"
        "PAGE CONTROL: web_navigate(path) to change page; web_scroll(down/up/top/bottom); "
        "web_scroll_to(text) to a section on the current page; web_highlight(text)/web_clear_highlight() "
        "to spotlight an item; web_fill(field,value) and web_click(text) for native forms.\n\n"
        "PAGES you can navigate to:\n{pages}\n"
        "{booking}\n"
        "STYLE: warm, one or two short sentences, match the visitor's language. When someone asks to see, "
        "open, scroll to, or look at something, move the page first, then talk."
    ).format(biz=business, pages=page_lines, booking=booking_block)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-calendars", action="store_true")
    ap.add_argument("--name", default="Website Assistant")
    ap.add_argument("--business", default="our business")
    ap.add_argument("--voice", default="xai", choices=["xai", "openai"],
                    help="Only xai/openai execute page-control tools (gemini/elevenlabs do not).")
    ap.add_argument("--page", action="append", default=[], help='Repeatable: "/path : description"')
    ap.add_argument("--calendar-integration-id", default="")
    ap.add_argument("--calendar-id", default="")
    ap.add_argument("--max-duration", type=int, default=1800)
    args = ap.parse_args()

    if not API_KEY:
        sys.exit("Set LEADLOCK_API_KEY first.")
    if args.list_calendars:
        list_calendars()
        return

    pages = []
    for p in args.page:
        if ":" in p:
            path, desc = p.split(":", 1)
            pages.append((path.strip(), desc.strip()))
    booking = bool(args.calendar_id and args.calendar_integration_id)

    agent_payload = {
        "name": args.name,
        "voice_provider": args.voice,
        "ai_speaks_first": True,
        "greeting": "Hey there, thanks for stopping by. I can answer questions and show you around the site. What can I help with?",
        "tools_enabled": WEB_TOOLS + (BOOKING_TOOLS if booking else []),
        "system_prompt": build_prompt(args.business, pages, booking),
    }
    if booking:
        agent_payload["calendar_provider"] = "gohighlevel"
        agent_payload["calendar_integration_id"] = args.calendar_integration_id
        agent_payload["calendar_id"] = args.calendar_id

    print("Creating agent on {} ...".format(BASE))
    agent = call("POST", "/agents", agent_payload)
    agent_id = agent["id"]
    print("  agent_id = {}  (booking={})".format(agent_id, booking))

    demo = call("POST", "/demos/", {
        "agent_id": agent_id,
        "channel": "web",
        "name": args.name + " (Talking Website)",
        "config": {"session_mode": "web", "max_duration_seconds": args.max_duration},
    })
    slug = demo["slug"]
    print("  slug = {}".format(slug))

    print("\nDone. Drop this into the site (with voice-agent.js served alongside):\n")
    print('<script src="/voice-agent.js"')
    print('        data-leadlock-ws="{}"'.format(WS_BASE))
    print('        data-leadlock-slug="{}"></script>'.format(slug))


if __name__ == "__main__":
    main()
