#!/usr/bin/env python3
"""Find a prospect's logo on their website.

Returns JSON with the best candidates for two slots:
- avatar  (square, ideal for the demo's call-screen avatar circle)
- header  (rectangular, ideal for landing-page hero / email banner)

Stdlib only. Handles Cloudflare-basic-protection with browser headers.

Usage:
    python3 find_logo.py https://acmeplumbing.com
    python3 find_logo.py https://acmeplumbing.com --download ./output/acme

Exit codes:
    0  found at least one candidate
    1  network or parse error
    2  page fetched but no logo candidates found
"""

import argparse
import io
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
}


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers.get_content_type(), r.read()


def absolutize(base, url):
    if not url:
        return None
    if url.startswith("data:"):
        return None
    return urllib.parse.urljoin(base, url)


def parse_size(s):
    """'192x192' -> 192. Returns 0 if unparseable."""
    if not s:
        return 0
    m = re.match(r"(\d+)\s*[x×]\s*(\d+)", s)
    if m:
        return min(int(m.group(1)), int(m.group(2)))
    m = re.match(r"(\d+)", s)
    return int(m.group(1)) if m else 0


def candidates_from_html(base_url, html):
    out = []

    # <link rel="apple-touch-icon" sizes="180x180" href="...">
    for m in re.finditer(
        r'<link\b[^>]*\brel=["\']([^"\']+)["\'][^>]*>',
        html, re.I,
    ):
        rel = m.group(1).lower()
        if not any(t in rel for t in ("apple-touch-icon", "icon", "shortcut")):
            continue
        tag = m.group(0)
        href = re.search(r'\bhref=["\']([^"\']+)["\']', tag, re.I)
        if not href:
            continue
        size = 0
        sm = re.search(r'\bsizes=["\']([^"\']+)["\']', tag, re.I)
        if sm:
            size = parse_size(sm.group(1))
        slot = "avatar" if "apple-touch-icon" in rel or size >= 96 else "favicon"
        out.append({
            "kind": "link-icon",
            "rel": rel,
            "size": size,
            "url": absolutize(base_url, href.group(1)),
            "slot_hint": slot,
        })

    # <meta property="og:image" content="...">
    for m in re.finditer(
        r'<meta\b[^>]*\bproperty=["\']og:image(?::secure_url)?["\'][^>]*\bcontent=["\']([^"\']+)["\']',
        html, re.I,
    ):
        out.append({
            "kind": "og-image",
            "size": 0,
            "url": absolutize(base_url, m.group(1)),
            "slot_hint": "header",
        })

    # <img class="...logo..."> or alt="...logo..."
    for m in re.finditer(r'<img\b[^>]+>', html, re.I):
        tag = m.group(0)
        src_m = re.search(r'\b(?:data-lazy-)?src=["\']([^"\']+)["\']', tag, re.I)
        if not src_m:
            continue
        src = src_m.group(1)
        if src.startswith("data:"):
            # try data-lazy-src as backup
            ds = re.search(r'\bdata-lazy-src=["\']([^"\']+)["\']', tag, re.I)
            if ds:
                src = ds.group(1)
            else:
                continue
        class_m = re.search(r'\bclass=["\']([^"\']+)["\']', tag, re.I) or re.search(
            r'\balt=["\']([^"\']+)["\']', tag, re.I)
        label = (class_m.group(1) if class_m else "").lower()
        if "logo" not in label and "logo" not in src.lower():
            continue
        out.append({
            "kind": "img-logo",
            "size": 0,
            "url": absolutize(base_url, src),
            "slot_hint": "header",
        })

    # <link rel="manifest"> — parse to find icons (often 512x512)
    # (not implemented here — most sites repeat their icons in <link rel> too)

    # Deduplicate by URL, prefer the largest-size candidate per URL
    by_url = {}
    for c in out:
        u = c.get("url")
        if not u:
            continue
        if u not in by_url or c.get("size", 0) > by_url[u].get("size", 0):
            by_url[u] = c
    return list(by_url.values())


def best_for_slot(cands, slot):
    """Pick the highest-priority candidate for the slot."""
    if slot == "avatar":
        # Prefer apple-touch-icon, then large square icons, then og:image, then any img-logo
        scored = []
        for c in cands:
            score = 0
            if c["kind"] == "link-icon":
                rel = c.get("rel", "")
                if "apple-touch-icon" in rel:
                    score = 100 + c.get("size", 0)
                elif "icon" in rel and c.get("size", 0) >= 96:
                    score = 80 + c.get("size", 0)
                elif "icon" in rel:
                    score = 40 + c.get("size", 0)
            elif c["kind"] == "og-image":
                score = 30
            elif c["kind"] == "img-logo":
                score = 20
            scored.append((score, c))
        scored.sort(key=lambda t: t[0], reverse=True)
        return scored[0][1] if scored else None
    elif slot == "header":
        scored = []
        for c in cands:
            score = 0
            if c["kind"] == "og-image":
                score = 100
            elif c["kind"] == "img-logo":
                score = 80
            elif c["kind"] == "link-icon" and c.get("size", 0) >= 180:
                score = 40
            scored.append((score, c))
        scored.sort(key=lambda t: t[0], reverse=True)
        return scored[0][1] if scored else None


def download(url, dest_dir):
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    name = url.split("/")[-1].split("?")[0] or "logo.bin"
    name = re.sub(r"[^\w.\-]", "_", name)[:80]
    path = Path(dest_dir) / name
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
            ctype = r.headers.get_content_type()
        path.write_bytes(data)
        return {"path": str(path), "bytes": len(data), "content_type": ctype}
    except Exception as e:
        return {"path": str(path), "error": f"{type(e).__name__}: {e}"}


def main():
    ap = argparse.ArgumentParser(description="Find a prospect's logo from their website.")
    ap.add_argument("url", help="Homepage URL")
    ap.add_argument("--download", help="If set, download the chosen avatar and header into this dir")
    ap.add_argument("--also-fetch", action="append", default=[],
                    help="Additional pages to scrape (about, contact, etc.). Repeatable.")
    args = ap.parse_args()

    pages = [args.url] + list(args.also_fetch)
    candidates = []

    for url in pages:
        try:
            code, ctype, body = fetch(url)
        except urllib.error.HTTPError as e:
            print(f"# warn: {url} -> HTTP {e.code}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"# warn: {url} -> {type(e).__name__}: {e}", file=sys.stderr)
            continue
        if ctype and not ctype.startswith("text"):
            continue
        try:
            html = body.decode(errors="ignore")
        except Exception:
            continue
        candidates.extend(candidates_from_html(url, html))

    # Dedup again across pages
    seen = {}
    for c in candidates:
        u = c.get("url")
        if u and (u not in seen or c.get("size", 0) > seen[u].get("size", 0)):
            seen[u] = c
    candidates = list(seen.values())

    avatar = best_for_slot(candidates, "avatar")
    header = best_for_slot(candidates, "header")

    result = {
        "source": args.url,
        "pages_scraped": pages,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "avatar": avatar,
        "header": header,
    }

    if args.download:
        if avatar and avatar.get("url"):
            result["avatar_download"] = download(avatar["url"], args.download)
        if header and header.get("url"):
            result["header_download"] = download(header["url"], args.download)

    print(json.dumps(result, indent=2))
    if not candidates:
        sys.exit(2)


if __name__ == "__main__":
    main()
