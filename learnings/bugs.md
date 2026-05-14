# Bugs

Things that broke unexpectedly. Includes symptom, root cause if known, workaround.

Each entry includes: date, tags, evidence link, rule, why, how to apply.

---

### `PATCH /demos/{id}/` (trailing slash) silently drops the body via 307 redirect

Date: 2026-05-13
Tags: api:demos, http:redirect, type:bug
Evidence: `PATCH https://leadlock-app.onrender.com/demos/{id}/` returned 307; followed by GET that showed config keys not persisted. `PATCH /demos/{id}` (no slash) returned 200 with config stored correctly.

**Rule:** Use `PATCH /demos/{demo_id}` WITHOUT a trailing slash. The trailing-slash form returns 307 and urllib's default `urlopen` follows it but drops the request body in the redirected request, so the PATCH appears to succeed but the data never lands.

**Why:** FastAPI/Starlette typically configures route trailing-slash redirects via `redirect_slashes=True` (the default). The redirect uses HTTP 307 (preserve method), but most HTTP clients re-issue the request without preserving the body when they auto-follow. The result: 200-looking outcome with no state change. The `POST /demos/` endpoint (note the trailing slash) is fine because the route is defined that way — but `PATCH /demos/{id}` is defined WITHOUT trailing slash, and adding one triggers the redirect.

**How to apply:** In any new script hitting Leadlock endpoints, default to NO trailing slash on `PATCH` and `DELETE` routes. If a PATCH appears successful but the GET right after shows no change, the trailing-slash redirect is the most likely culprit. Also worth re-verifying with `urlopen(req).status` — a 307 sometimes leaks through if `MaxRedirects` is set to 0.
