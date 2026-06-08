# Capturing a GHL session token

This skill talks to GoHighLevel's private backend API using the same auth
headers your browser sends when you use the workflow builder. You capture
those headers from a live session and paste them into a local `headers.json`.

> Unofficial API. Tokens expire about every hour. Re-capture when calls start
> returning 401.

## What you need

Two tokens and a few static headers:

| Header | What it is |
|---|---|
| `authorization` | `Bearer <authToken>`. The main GHL auth token. Authorizes most calls on its own. |
| `token-id` | A Firebase identity token. Needed for some calls; harmless to always send. |
| `channel` | Always `APP`. |
| `source` | Always `WEB_USER`. |
| `accept` | `application/json, text/plain, */*`. |
| `referer` | `https://app.gohighlevel.com/`. |
| `user-agent` | Any normal desktop browser UA string. |
| `content-type` | `application/json` (used only on writes; see note below). |

## Step by step

1. Open GoHighLevel in Chrome and log in. Navigate to the sub-account
   (location) whose workflows you want to read or edit.
2. Open DevTools (Cmd-Option-I on macOS, F12 on Windows) and click the
   **Network** tab.
3. Open a workflow in the builder, or just click around the Automation area,
   so the app fires requests.
4. In the Network filter box type `backend.leadconnectorhq.com` to narrow the
   list. Click any XHR request to that host (a `workflow/...` request is ideal).
5. In the request's **Headers** panel, find **Request Headers**. Copy the
   values of `authorization` and `token-id`.
6. Open `headers.example.json`, save it as `headers.json` in the skill folder,
   and paste your real values over the placeholders. Leave `channel`, `source`,
   `accept`, `referer`, `user-agent`, `content-type` as they are.

`headers.json` is gitignored. Never commit it. Never paste a real token into
any other file.

## Finding your location id

The location (sub-account) id is in the GHL app URL while you are inside a
sub-account, e.g. `app.gohighlevel.com/location/<your-location-id>/...`. You
pass it to every script as the first argument. The scripts never hardcode it.

## When it stops working

A 401 means the `authToken` expired (about a 1-hour lifetime). Repeat the
capture: grab a fresh `authorization` (and `token-id`) and overwrite the
values in `headers.json`. The scripts detect 401 and tell you to re-capture.

## Why `content-type` is special

The signed workflow-file URL (the Firebase-signed `fileUrl`) must be fetched
**without** a `content-type` header, or the signature check fails. The read
helper deliberately omits `content-type` on GETs and only adds it on writes.
You still keep `content-type` in `headers.json`; the code decides when to send
it.
