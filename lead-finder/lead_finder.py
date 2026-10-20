#!/usr/bin/env python3
"""lead-finder: build an outreach-ready list of local businesses.

Four stages, one CSV:
  1. Google Maps listings for a keyword + location (Apify, compass~crawler-google-places)
  2. Which of them are running Facebook ads right now (Apify, apify~facebook-ads-scraper)
  3. The owner's name and email (TREG people search, free email patterns, TREG email finder)
  4. Email verification (Reoon), so you only mail addresses that exist

Output columns: business,website,phone,owner_name,email,verified,source,ad_found

Stdlib only, Python 3.9+. Every key is read from the kit's .env (or the real
environment). Keys are never printed in full. Nothing paid runs until you confirm
the spend estimate (or pass --yes). --dry-run makes zero network calls.

Example:
  python3 lead-finder/lead_finder.py --keyword roofers --location "Austin, TX" --limit 20
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import datetime
import json
import math
import os
import re
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CSV_HEADER = ["business", "website", "phone", "owner_name", "email", "verified", "source",
              "ad_found"]

APIFY_BASE = "https://api.apify.com/v2/acts"
MAPS_ACTOR = "compass~crawler-google-places"
FB_ACTOR = "apify~facebook-ads-scraper"
TREG_BASE = "https://treg.to/call"
REOON_URL = "https://emailverifier.reoon.com/api/v1/verify"
USER_AGENT = "leadlock-agent-kit-lead-finder/1.0"

# Published per-event prices (FREE Apify tier), used only for the up-front estimate.
MAPS_PER_PLACE = 0.004
MAPS_CONTACTS_PER_PLACE = 0.002
FB_PER_AD = 0.0058
TREG_ROUTE_MAX = 0.05  # per-call ceiling, enforced by TREG itself

KEY_NAMES = ("APIFY_TOKEN", "TREG_TOKEN", "TREG_ORG", "REOON_API_KEY")
PLACEHOLDER_HINTS = ("paste_your", "paste-your", "your-team-slug", "your_", "changeme")

LEGAL_SUFFIXES = {"llc", "inc", "co", "corp", "ltd"}
NAME_NOISE = {"mr", "mrs", "ms", "dr", "jr", "sr", "ii", "iii", "iv", "llc", "inc"}
OWNER_TITLES = ("owner", "founder", "president", "ceo", "principal", "proprietor")
NOT_A_WEBSITE = ("facebook.com", "fb.me", "fb.com", "instagram.com", "m.me", "wa.me",
                 "messenger.com", "google.com", "goo.gl", "g.page")


# ---------------------------------------------------------------- errors

class LeadFinderError(Exception):
    """Base error. Messages never carry a key or a key-bearing URL."""


class NetworkError(LeadFinderError):
    pass


class ApifyError(LeadFinderError):
    pass


class EmptyRunError(ApifyError):
    pass


class TregError(LeadFinderError):
    pass


class TregFieldError(TregError):
    """422 / identity_incomplete: the request had the wrong fields. Free, and a bug,
    never a miss. Counting it as a miss would hide broken requests forever."""


class TregStopped(TregError):
    """TREG refused the token or the balance is empty. No more TREG calls this run."""


class TregBudgetExhausted(TregError):
    """--treg-budget is spent. No more TREG calls this run."""


# ---------------------------------------------------------------- the one network seam

def _parse_body(raw: bytes):
    text = raw.decode("utf-8", "replace")
    try:
        return json.loads(text)
    except ValueError:
        return text


def _scrub(msg: str) -> str:
    """Drop any query string from an error message (Reoon puts its key there)."""
    return re.sub(r"\?\S*", "?...", str(msg))[:200]


def http_request(method: str, url: str, headers: dict | None = None, body=None,
                 timeout: int = 60):
    """All network I/O goes through here. Returns (status, headers, json_or_text).

    HTTP errors come back as a status, never an exception, so each caller decides
    what a 422 or a 502 means. A transport failure raises NetworkError whose
    message names only the host, never the URL.
    """
    data = body.encode("utf-8") if isinstance(body, str) else body
    hdrs = {"User-Agent": USER_AGENT}
    hdrs.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers.items()), _parse_body(resp.read())
    except urllib.error.HTTPError as exc:
        hdr = dict(exc.headers.items()) if exc.headers else {}
        try:
            payload = _parse_body(exc.read())
        except OSError:
            payload = ""
        return exc.code, hdr, payload
    except (urllib.error.URLError, OSError, ValueError) as exc:
        host = urllib.parse.urlsplit(url).netloc
        reason = getattr(exc, "reason", "") or type(exc).__name__
        raise NetworkError(f"network error talking to {host}: {_scrub(reason)}") from None


def _header(headers: dict, name: str) -> str:
    for k, v in (headers or {}).items():
        if k.lower() == name.lower():
            return str(v)
    return ""


# ---------------------------------------------------------------- .env and keys

def load_env(path: str) -> dict:
    """Parse a .env file: KEY=value per line, '#' comments, quotes stripped."""
    env: dict = {}
    p = Path(path)
    if not p.is_file():
        return env
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _is_placeholder(value: str) -> bool:
    low = value.lower()
    return any(h in low for h in PLACEHOLDER_HINTS)


def get_keys(env_file: str) -> dict:
    """The four keys. A real environment variable wins over the file; a
    placeholder copied from .env.example counts as missing."""
    file_env = load_env(env_file)
    keys = {}
    for name in KEY_NAMES:
        value = (os.environ.get(name) or file_env.get(name) or "").strip()
        keys[name] = "" if _is_placeholder(value) else value
    return keys


def mask(key: str) -> str:
    if not key:
        return "(missing)"
    if len(key) <= 10:
        return "****"
    return key[:4] + "..." + key[-4:]


# ---------------------------------------------------------------- normalizing

def norm_domain(url: str) -> str:
    """'https://www.Acme.com/contact' -> 'acme.com'. Social and Google links -> ''."""
    s = (url or "").strip().lower()
    if not s:
        return ""
    s = re.sub(r"^[a-z][a-z0-9+.-]*://", "", s)
    s = s.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0].split(":", 1)[0]
    if s.startswith("www."):
        s = s[4:]
    if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", s):
        return ""
    for bad in NOT_A_WEBSITE:
        if s == bad or s.endswith("." + bad):
            return ""
    return s


def norm_name(name: str) -> str:
    """Lowercase, '&' -> 'and', punctuation out, trailing legal suffixes dropped."""
    s = (name or "").lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    words = s.split()
    while len(words) > 1 and words[-1] in LEGAL_SUFFIXES:
        words.pop()
    return " ".join(words)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:60] or "leads"


def _new_row(**fields) -> dict:
    row = {k: "" for k in CSV_HEADER}
    row.update({"domain": "", "location": "", "site_emails": []})
    row.update(fields)
    return row


# ---------------------------------------------------------------- Apify

def _apify_run(actor: str, payload: dict, *, token: str, max_charge_usd: float,
               timeout: int = 320) -> list:
    """Run an actor synchronously and return its dataset items.

    The token goes in the Authorization header, never the URL, so it cannot land
    in a log, a traceback or a proxy record.
    """
    query = urllib.parse.urlencode({"timeout": 300, "format": "json", "clean": "true",
                                    "maxTotalChargeUsd": f"{max_charge_usd:.2f}"})
    url = f"{APIFY_BASE}/{actor}/run-sync-get-dataset-items?{query}"
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json",
               "Accept": "application/json"}
    status, _hdrs, data = http_request("POST", url, headers, json.dumps(payload),
                                       timeout=timeout)
    if not 200 <= status < 300:
        detail = ""
        if isinstance(data, dict):
            err = data.get("error")
            detail = err.get("message", "") if isinstance(err, dict) else str(err or "")
        hint = " (check APIFY_TOKEN)" if status in (401, 403) else ""
        raise ApifyError(f"Apify {actor} returned HTTP {status}{hint}: {_scrub(detail)}")
    if not isinstance(data, list):
        raise ApifyError(f"Apify {actor} returned an unexpected response shape")
    return data


def parse_maps(items: list) -> list:
    """Google Maps dataset items -> rows. Closed businesses dropped, placeId deduped."""
    rows, seen = [], set()
    for it in items or []:
        if not isinstance(it, dict) or it.get("permanentlyClosed"):
            continue
        name = (it.get("title") or "").strip()
        if not name:
            continue
        pid = it.get("placeId") or ""
        if pid:
            if pid in seen:
                continue
            seen.add(pid)
        website = (it.get("website") or "").strip()
        city, state = (it.get("city") or "").strip(), (it.get("state") or "").strip()
        emails = it.get("emails") if isinstance(it.get("emails"), list) else []
        rows.append(_new_row(
            business=name, website=website, phone=(it.get("phone") or "").strip(),
            source="google_maps", ad_found="no", domain=norm_domain(website),
            location=", ".join(x for x in (city, state) if x),
            site_emails=[e.strip().lower() for e in emails if isinstance(e, str) and "@" in e],
        ))
    return rows


def maps_search(keyword: str, location: str, limit: int, *, token: str,
                contacts: bool = False) -> list:
    payload = {"searchStringsArray": [keyword], "locationQuery": location,
               "maxCrawledPlacesPerSearch": limit, "language": "en",
               "scrapeContacts": bool(contacts)}
    per = MAPS_PER_PLACE + (MAPS_CONTACTS_PER_PLACE if contacts else 0)
    items = _apify_run(MAPS_ACTOR, payload, token=token,
                       max_charge_usd=max(0.05, limit * per * 2 + 0.02))
    if not items:
        # Learned the hard way: a successful run that returns [] means the input
        # was wrong (location not recognized, bad field), not "no businesses".
        raise EmptyRunError(
            "Google Maps run succeeded but returned 0 places. That means the input "
            "was wrong, not that there are no businesses. Check --location (try "
            "'City, ST') and --keyword, then run again.")
    return parse_maps(items)


def fb_library_url(keyword: str, location: str) -> str:
    city = (location or "").split(",")[0].strip()
    q = f"{keyword} {city}".strip()
    return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode({
        "active_status": "active", "ad_type": "all", "country": "US",
        "media_type": "all", "q": q, "search_type": "keyword_unordered"})


def _domain_from_caption(caption: str) -> str:
    c = (caption or "").strip().lower()
    if not c or " " in c:
        return ""
    return norm_domain(c)


def parse_fb_ads(items: list) -> list:
    """Ad-level records -> one row per advertiser page. Field names vary between
    runs, so every field is read defensively."""
    pages: dict = {}
    order = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        snap = it.get("snapshot") if isinstance(it.get("snapshot"), dict) else {}
        pid = str(it.get("pageId") or it.get("page_id") or snap.get("page_id")
                  or snap.get("pageId") or "").strip()
        name = (snap.get("pageName") or snap.get("page_name") or it.get("pageName")
                or it.get("page_name") or "").strip()
        if not pid and not name:
            continue
        key = pid or ("name:" + norm_name(name))
        link = (snap.get("linkUrl") or snap.get("link_url") or it.get("linkUrl")
                or it.get("link_url") or "")
        cards = snap.get("cards") if isinstance(snap.get("cards"), list) else []
        if not link and cards and isinstance(cards[0], dict):
            link = cards[0].get("linkUrl") or cards[0].get("link_url") or ""
        domain = norm_domain(link) or _domain_from_caption(snap.get("caption") or "")
        page_url = (snap.get("pageProfileUri") or it.get("pageProfileUri")
                    or it.get("pageUrl") or snap.get("page_profile_uri") or "")
        if key not in pages:
            pages[key] = {"page_id": pid, "name": name, "domain": domain,
                          "page_url": page_url, "ads": 0}
            order.append(key)
        page = pages[key]
        page["ads"] += 1
        for field, value in (("name", name), ("domain", domain), ("page_url", page_url)):
            if value and not page[field]:
                page[field] = value
    return [pages[k] for k in order]


def fb_ads_search(keyword: str, location: str, limit: int, *, token: str) -> list:
    payload = {"startUrls": [{"url": fb_library_url(keyword, location)}],
               "resultsLimit": limit, "activeStatus": "active",
               "includeAboutPage": True, "isDetailsPerAd": False}
    items = _apify_run(FB_ACTOR, payload, token=token,
                       max_charge_usd=max(0.05, limit * FB_PER_AD * 2 + 0.02))
    return parse_fb_ads(items)


# ---------------------------------------------------------------- join

def join(maps_rows: list, fb_pages: list) -> list:
    """Mark Maps businesses that advertise; FB advertisers with no Maps match
    become their own rows."""
    rows = [dict(r) for r in maps_rows]
    by_domain = {r["domain"]: r for r in rows if r.get("domain")}
    by_name = {norm_name(r["business"]): r for r in rows if r.get("business")}
    extra = []
    for page in fb_pages:
        match = by_domain.get(page.get("domain") or "") if page.get("domain") else None
        if match is None and page.get("name"):
            match = by_name.get(norm_name(page["name"]))
        if match is not None:
            match["ad_found"] = "yes"
            match["source"] = "both"
            if not match.get("domain") and page.get("domain"):
                match["domain"] = page["domain"]
                match["website"] = match.get("website") or "https://" + page["domain"]
            continue
        website = ("https://" + page["domain"]) if page.get("domain") else page.get("page_url", "")
        extra.append(_new_row(business=page.get("name") or "(unnamed page)",
                              website=website, source="facebook_ads", ad_found="yes",
                              domain=page.get("domain") or ""))
    return rows + extra


def ads_only(rows: list) -> list:
    return [r for r in rows if r.get("ad_found") == "yes"]


# ---------------------------------------------------------------- names and patterns

def name_parts(full_name: str) -> tuple:
    """(first, last) in lowercase letters; '' for a missing or one-letter last name."""
    raw = re.sub(r"[^A-Za-z .'-]", "", full_name or "").replace("'", "")
    parts = [re.sub(r"[^a-z]", "", p.lower()) for p in raw.split()]
    parts = [p for p in parts if p and p not in NAME_NOISE]
    if not parts:
        return "", ""
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ""
    if len(last) < 2:
        last = ""
    return first, last


def email_patterns(first: str, last: str, domain: str) -> list:
    """Guesses in the order small businesses actually use them."""
    f = re.sub(r"[^a-z]", "", (first or "").lower())
    la = re.sub(r"[^a-z]", "", (last or "").lower())
    d = (domain or "").strip().lower()
    if not f or not d:
        return []
    out = [f"{f}@{d}"]
    if la:
        out += [f"{f}.{la}@{d}", f"{f}{la}@{d}", f"{f[0]}{la}@{d}", f"{f}{la[0]}@{d}",
                f"{f}_{la}@{d}", f"{la}@{d}"]
    seen, uniq = set(), []
    for e in out:
        if e not in seen:
            seen.add(e)
            uniq.append(e)
    return uniq


# ---------------------------------------------------------------- Reoon

def reoon_verdict(resp: dict) -> str:
    status = str((resp or {}).get("status") or "").lower()
    if status == "safe" and (resp or {}).get("is_safe_to_send", True) is not False:
        return "verified"
    if status == "catch_all":
        return "catch_all"
    return "miss"


def reoon_verify(email: str, *, key: str, timeout: int = 90) -> dict:
    """{'email', 'verdict', 'error'}. The key rides in Reoon's query string by
    their design, so the URL is never printed and errors never include it."""
    if not key:
        return {"email": email, "verdict": "not_checked", "error": ""}
    url = REOON_URL + "?" + urllib.parse.urlencode({"email": email, "key": key,
                                                    "mode": "power"})
    try:
        status, _h, data = http_request("GET", url, {"Accept": "application/json"},
                                        timeout=timeout)
    except Exception as exc:  # noqa: BLE001 - any failure is reported, never raised
        return {"email": email, "verdict": "not_checked",
                "error": f"reoon request failed ({type(exc).__name__})"}
    if status != 200 or not isinstance(data, dict):
        hint = " (check REOON_API_KEY or credits)" if status in (401, 402, 403) else ""
        return {"email": email, "verdict": "not_checked",
                "error": f"reoon returned HTTP {status}{hint}"}
    return {"email": email, "verdict": reoon_verdict(data), "error": ""}


# ---------------------------------------------------------------- TREG

class TregBudget:
    """Caps REPORTED TREG spend. Thread-safe. A call reserves its per-call ceiling
    up front, so concurrent calls can never jointly start past the cap."""

    def __init__(self, cap_usd: float):
        self.cap_micro = max(int(round(cap_usd * 1_000_000)), 0)
        self._spent = 0
        self._reserved = 0
        self._calls = 0
        self._lock = threading.Lock()

    def reserve(self, max_usd: float) -> int:
        with self._lock:
            remaining = self.cap_micro - self._spent - self._reserved
            ceiling = min(int(max_usd * 1_000_000), remaining)
            ceiling = (ceiling // 1000) * 1000  # whole tenths of a cent, rounded down
            if ceiling < 1000:
                raise TregBudgetExhausted(
                    f"TREG budget spent (${self.spent_usd_unlocked():.4f} of "
                    f"${self.cap_micro / 1_000_000:.2f}); raise --treg-budget for more")
            self._reserved += ceiling
            return ceiling

    def settle(self, reserved: int, cost_micro: int) -> None:
        with self._lock:
            self._reserved -= reserved
            self._spent += max(int(cost_micro), 0)
            self._calls += 1

    def release(self, reserved: int) -> None:
        with self._lock:
            self._reserved -= reserved

    def spent_usd_unlocked(self) -> float:
        return self._spent / 1_000_000

    @property
    def spent_usd(self) -> float:
        with self._lock:
            return self._spent / 1_000_000

    @property
    def calls(self) -> int:
        with self._lock:
            return self._calls


class TregClient:
    """treg.to routed calls. TREG_ORG is required: an identity token must say
    which team it is acting for."""

    def __init__(self, token: str, org: str, budget: TregBudget, *,
                 max_cost: float = TREG_ROUTE_MAX, timeout: int = 120):
        self.token = token
        self.org = org
        self.budget = budget
        self.max_cost = max_cost
        self.timeout = timeout
        self.stopped = ""
        self._lock = threading.Lock()

    def _stop(self, reason: str) -> TregStopped:
        with self._lock:
            if not self.stopped:
                self.stopped = reason
        return TregStopped(self.stopped)

    def call(self, endpoint: str, body: dict):
        """Output on a hit, None on a miss. Raises TregFieldError, TregStopped,
        TregBudgetExhausted or TregError."""
        if self.stopped:
            raise TregStopped(self.stopped)
        reserved = self.budget.reserve(self.max_cost)
        headers = {"X-Treg-Token": self.token, "X-Treg-Org": self.org,
                   "X-Treg-Route-Max-Cost": f"{reserved / 1_000_000:.3f}",
                   "Content-Type": "application/json", "Accept": "application/json"}
        try:
            status, hdrs, data = http_request("POST", f"{TREG_BASE}/{endpoint}", headers,
                                              json.dumps(body), timeout=self.timeout)
        except NetworkError as exc:
            self.budget.release(reserved)
            raise TregError(f"treg {endpoint}: {exc}") from None
        detail = json.dumps(data) if not isinstance(data, str) else data
        if 200 <= status < 300:
            meta = data.get("_treg") if isinstance(data, dict) else None
            cost = _header(hdrs, "X-Treg-Cost-Micro")
            try:
                cost_micro = int(float(cost)) if cost else int((meta or {}).get("charged_micro") or 0)
            except (TypeError, ValueError):
                cost_micro = 0
            self.budget.settle(reserved, cost_micro)
            out = data.get("output") if isinstance(data, dict) else None
            return out if out is not None else {}
        self.budget.release(reserved)
        if status == 422 or "identity_incomplete" in detail:
            raise TregFieldError(f"treg {endpoint} rejected the request fields (HTTP {status}); "
                                 "this is a bug in the request, not a miss")
        if status == 502 or "route_failed" in detail:
            return None
        if status in (401, 403):
            raise self._stop(f"treg refused the token {mask(self.token)} for org "
                             f"'{self.org}' (HTTP {status}); check TREG_TOKEN and TREG_ORG")
        if status == 402:
            raise self._stop("treg balance is too low (HTTP 402); top up at treg.to "
                             "or run with --no-treg")
        raise TregError(f"treg {endpoint} returned HTTP {status}: {_scrub(detail)}")


def person_from_search(output) -> dict | None:
    """Best person from treg.people.search output. Providers disagree on keys.
    Prefers an owner-type title; needs a first and last name."""
    people = output.get("people") if isinstance(output, dict) else output
    if not isinstance(people, list):
        return None
    candidates = []
    for p in people:
        if not isinstance(p, dict):
            continue
        first = p.get("first_name") or p.get("firstName") or ""
        last = p.get("last_name") or p.get("lastName") or ""
        name = (p.get("full_name") or p.get("name") or p.get("fullName")
                or f"{first} {last}").strip()
        if len(name.split()) < 2:
            continue
        f, la = name_parts(name)
        if not f:
            continue
        title = p.get("title") or p.get("job_title") or p.get("jobTitle") or ""
        email = (p.get("email") or p.get("work_email") or p.get("workEmail") or "")
        candidates.append({"name": name, "first": f, "last": la, "title": title,
                           "email": str(email).strip().lower()})
    if not candidates:
        return None
    for c in candidates:
        if any(t in c["title"].lower() for t in OWNER_TITLES):
            return c
    return candidates[0]


# ---------------------------------------------------------------- enrichment

class Notes:
    """Thread-safe, de-duplicated warnings for the end-of-run report."""

    def __init__(self):
        self._items: dict = {}
        self._lock = threading.Lock()

    def add(self, msg: str) -> None:
        with self._lock:
            self._items[msg] = self._items.get(msg, 0) + 1

    def items(self) -> list:
        with self._lock:
            return [m if n == 1 else f"{m} (x{n})" for m, n in self._items.items()]


RANK = {"verified": 3, "catch_all": 2, "not_checked": 1, "miss": 0}


def _check(email: str, reoon_key: str, notes: Notes) -> str:
    res = reoon_verify(email, key=reoon_key)
    if res["error"]:
        notes.add(res["error"])
    return res["verdict"]


def find_owner(row: dict, *, treg: TregClient | None, reoon_key: str, notes: Notes) -> dict:
    """Owner name + best email for one row, cheapest source first:
    1. TREG people.search for the owner's name (and an email if it has one)
    2. free email patterns, each checked with Reoon, stop at the first verified
    3. emails found on the website (--contacts), checked with Reoon
    4. TREG people.email.find, only if nothing verified yet
    """
    row = dict(row)
    domain = row.get("domain") or ""
    if not domain:
        row["verified"] = "skipped"
        return row

    best = {"email": "", "verdict": "miss"}

    def consider(email: str, verdict: str, prefer: bool = False) -> None:
        if not email or verdict == "miss":
            return
        if RANK[verdict] > RANK[best["verdict"]] or (
                prefer and RANK[verdict] == RANK[best["verdict"]]) or not best["email"]:
            best.update(email=email, verdict=verdict)

    def finish() -> dict:
        row["email"] = best["email"]
        row["verified"] = best["verdict"] if best["email"] else "miss"
        return row

    person, lookup_ran = None, False
    if treg is not None:
        try:
            out = treg.call("treg.people.search", {"company_domain": domain, "title": "Owner",
                                                   "location": row.get("location") or "",
                                                   "limit": 3})
            lookup_ran = True
            person = person_from_search(out) if out is not None else None
        except TregFieldError as exc:
            notes.add(str(exc))
        except TregError as exc:
            notes.add(str(exc))

    if person:
        row["owner_name"] = person["name"]
        if person["email"]:
            verdict = _check(person["email"], reoon_key, notes)
            consider(person["email"], verdict, prefer=True)
            if verdict in ("verified", "not_checked"):
                return finish()

    if not person:
        if best["email"]:
            return finish()
        row["verified"] = "miss" if lookup_ran else "skipped"
        return row

    guesses = email_patterns(person["first"], person["last"], domain)
    if guesses and reoon_key:
        verdicts = []
        for email in guesses:
            verdict = _check(email, reoon_key, notes)
            verdicts.append(verdict)
            if verdict == "verified":
                consider(email, verdict)
                return finish()
        if verdicts and set(verdicts) == {"catch_all"}:
            consider(guesses[0], "catch_all")
        elif verdicts and set(verdicts) == {"not_checked"}:
            consider(guesses[0], "not_checked")
    elif guesses:
        consider(guesses[0], "not_checked")

    if reoon_key:
        for email in row.get("site_emails") or []:
            if email in guesses or not email.endswith("@" + domain):
                continue
            verdict = _check(email, reoon_key, notes)
            if verdict == "verified":
                consider(email, verdict)
                return finish()

    if treg is not None and best["verdict"] != "verified":
        body = {"domain": domain, "first_name": person["first"], "last_name": person["last"]}
        if not person["last"]:
            body = {"domain": domain, "full_name": person["name"]}
        try:
            out = treg.call("treg.people.email.find", body)
            hit = ""
            if isinstance(out, dict):
                hit = str(out.get("email") or out.get("work_email") or "").strip().lower()
            if hit:
                verdict = _check(hit, reoon_key, notes)
                consider(hit, verdict, prefer=True)
        except TregError as exc:
            notes.add(str(exc))
    return finish()


def enrich(rows: list, *, treg: TregClient | None, reoon_key: str, notes: Notes,
           workers: int = 3) -> list:
    if not rows:
        return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        return list(pool.map(lambda r: find_owner(r, treg=treg, reoon_key=reoon_key,
                                                  notes=notes), rows))


# ---------------------------------------------------------------- output

def write_csv(rows: list, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_HEADER, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CSV_HEADER})


def estimate(args, keys: dict) -> dict:
    places = args.limit
    maps = places * (MAPS_PER_PLACE + (MAPS_CONTACTS_PER_PLACE if args.contacts else 0))
    fb = args.limit * FB_PER_AD if args.ads else 0.0
    treg_on = bool(keys["TREG_TOKEN"] and keys["TREG_ORG"]) and not args.no_treg
    treg = args.treg_budget if treg_on else 0.0
    reoon_on = bool(keys["REOON_API_KEY"]) and not args.no_verify
    rows = places + (args.limit if args.ads else 0)
    return {"maps": maps, "fb": fb, "treg": treg, "treg_on": treg_on, "reoon_on": reoon_on,
            "reoon_checks": rows * 9 if reoon_on else 0, "total": maps + fb + treg}


def print_estimate(args, keys: dict, est: dict) -> None:
    print("Spend estimate (upper bound, nothing has been charged yet):")
    print(f"  Google Maps via Apify    {args.limit} places x ${MAPS_PER_PLACE + (MAPS_CONTACTS_PER_PLACE if args.contacts else 0):.3f}"
          f"   = ${est['maps']:.4f}")
    if args.ads:
        print(f"  Facebook ads via Apify   {args.limit} ads x ${FB_PER_AD}"
              f"      = ${est['fb']:.4f}")
    else:
        print("  Facebook ads             off (--no-ads)")
    if est["treg_on"]:
        print(f"  TREG owner lookups       capped by --treg-budget = ${est['treg']:.4f}"
              "  (misses are free)")
    else:
        why = "--no-treg" if args.no_treg else "TREG_TOKEN or TREG_ORG missing"
        print(f"  TREG owner lookups       skipped ({why})")
    if est["reoon_on"]:
        print(f"  Reoon verification       up to {est['reoon_checks']} checks from your prepaid credits")
    else:
        why = "--no-verify" if args.no_verify else "REOON_API_KEY missing"
        print(f"  Reoon verification       skipped ({why}): emails will say not_checked")
    print(f"  Cash ceiling this run    ${est['total']:.2f}")


def _stdin_is_tty() -> bool:
    try:
        return sys.stdin.isatty()
    except (AttributeError, ValueError):
        return False


def _warn(msg: str) -> None:
    print("WARNING: " + msg, file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lead_finder.py",
        description="Find local businesses (Google Maps), flag the ones running Facebook "
                    "ads, find the owner's email, verify it, and write one CSV.",
        epilog='Example: python3 lead-finder/lead_finder.py --keyword roofers '
               '--location "Austin, TX" --limit 20')
    p.add_argument("--keyword", required=True, help='business type, e.g. "roofers"')
    p.add_argument("--location", required=True, help='city and state, e.g. "Austin, TX"')
    p.add_argument("--limit", type=int, default=20,
                   help="max Google Maps places, also the Facebook ads cap (1-200, default 20)")
    p.add_argument("--ads", action=argparse.BooleanOptionalAction, default=True,
                   help="check the Facebook Ad Library (default on; --no-ads to skip)")
    p.add_argument("--ads-only", action="store_true",
                   help="keep only businesses that are running ads (the layup list)")
    p.add_argument("--contacts", action="store_true",
                   help="also scrape emails from each website (+$0.002 per place)")
    p.add_argument("--treg-budget", type=float, default=0.25,
                   help="max USD to spend on TREG this run (default 0.25)")
    p.add_argument("--no-treg", action="store_true", help="skip TREG owner lookups")
    p.add_argument("--no-verify", action="store_true", help="skip Reoon verification")
    p.add_argument("--out", default="", help="CSV path (default output/leads-<search>-<date>.csv)")
    p.add_argument("--yes", "-y", action="store_true", help="skip the spend confirmation")
    p.add_argument("--dry-run", action="store_true",
                   help="print the plan and spend estimate, make no network calls")
    p.add_argument("--workers", type=int, default=3, help="parallel owner lookups (default 3)")
    p.add_argument("--env-file", default=".env", help="env file with your keys (default ./.env)")
    return p


def main(argv: list | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= 200:
        parser.error("--limit must be between 1 and 200")
    if args.treg_budget < 0:
        parser.error("--treg-budget cannot be negative")
    if args.ads_only:
        args.ads = True
    out_path = args.out or os.path.join(
        "output", f"leads-{_slug(args.keyword + ' ' + args.location)}-"
                  f"{datetime.date.today().isoformat()}.csv")

    keys = get_keys(args.env_file)
    print("Keys: " + "  ".join(
        f"{k}={keys[k] or '(missing)'}" if k == "TREG_ORG" else f"{k}={mask(keys[k])}"
        for k in KEY_NAMES), file=sys.stderr)

    est = estimate(args, keys)
    print_estimate(args, keys, est)
    if args.dry_run:
        print(f"Dry run: no network calls made. Would write {out_path}")
        if not keys["APIFY_TOKEN"]:
            _warn("APIFY_TOKEN is missing; a real run needs it (see lead-finder/README.md)")
        return 0

    if not keys["APIFY_TOKEN"]:
        print("ERROR: APIFY_TOKEN is missing. Add it to .env (see lead-finder/README.md).",
              file=sys.stderr)
        return 1
    if not args.yes:
        if not _stdin_is_tty():
            print("ERROR: this run spends money. Re-run with --yes to confirm, or "
                  "--dry-run to preview.", file=sys.stderr)
            return 2
        answer = input(f"Spend up to ${est['total']:.2f}? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Cancelled. Nothing was charged.", file=sys.stderr)
            return 2

    notes = Notes()
    print(f"[1/4] Google Maps: {args.keyword} in {args.location} ...", file=sys.stderr)
    try:
        maps_rows = maps_search(args.keyword, args.location, args.limit,
                                token=keys["APIFY_TOKEN"], contacts=args.contacts)
    except LeadFinderError as exc:
        print(f"ERROR: Google Maps stage failed: {exc}", file=sys.stderr)
        return 1
    print(f"      {len(maps_rows)} open businesses", file=sys.stderr)

    fb_pages: list = []
    if args.ads:
        print("[2/4] Facebook Ad Library ...", file=sys.stderr)
        try:
            fb_pages = fb_ads_search(args.keyword, args.location, args.limit,
                                     token=keys["APIFY_TOKEN"])
        except LeadFinderError as exc:
            notes.add(f"Facebook ads stage failed, ad_found is incomplete: {exc}")
        if not fb_pages:
            _warn("fb_ads=0: no active advertisers found for this search "
                  "(ad_found will be 'no' for every row)")
        else:
            print(f"      {len(fb_pages)} advertisers", file=sys.stderr)
    rows = join(maps_rows, fb_pages)
    if args.ads_only:
        rows = ads_only(rows)

    treg = None
    if args.no_treg:
        notes.add("TREG skipped (--no-treg): owner names come only from TREG, so most rows will say skipped")
    elif not (keys["TREG_TOKEN"] and keys["TREG_ORG"]):
        notes.add("TREG skipped: TREG_TOKEN or TREG_ORG missing in .env")
    else:
        treg = TregClient(keys["TREG_TOKEN"], keys["TREG_ORG"], TregBudget(args.treg_budget))
    reoon_key = "" if args.no_verify else keys["REOON_API_KEY"]
    if not reoon_key:
        notes.add("Reoon skipped: emails are unverified guesses (verified=not_checked)")

    print(f"[3/4] Owner name + email for {len(rows)} businesses ...", file=sys.stderr)
    rows = enrich(rows, treg=treg, reoon_key=reoon_key, notes=notes, workers=args.workers)

    print(f"[4/4] Writing {out_path}", file=sys.stderr)
    write_csv(rows, out_path)

    for msg in notes.items():
        _warn(msg)
    spent = treg.budget.spent_usd if treg else 0.0
    verified = sum(1 for r in rows if r.get("verified") == "verified")
    ads = sum(1 for r in rows if r.get("ad_found") == "yes")
    print(f"rows={len(rows)} verified={verified} ads_found={ads} treg_spent=${spent:.4f}")
    if not rows:
        _warn("0 rows written (header only). Nothing matched; widen --keyword or "
              "--location, or drop --ads-only.")
        return 3
    print(f"Saved: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
