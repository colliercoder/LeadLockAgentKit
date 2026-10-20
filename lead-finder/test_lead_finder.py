"""Tests for lead_finder.py. Every network call is mocked through the one seam,
`http_request`, so nothing here ever reaches Apify, TREG or Reoon.

Run from the kit root:
    python3 -m pytest lead-finder -q
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
KIT_ROOT = HERE.parent
SCRIPT = HERE / "lead_finder.py"

_spec = importlib.util.spec_from_file_location("lead_finder", SCRIPT)
lf = importlib.util.module_from_spec(_spec)
sys.modules["lead_finder"] = lf
_spec.loader.exec_module(lf)

HEADER = "business,website,phone,owner_name,email,verified,source,ad_found"


# ---------------------------------------------------------------- fake HTTP

class FakeHTTP:
    """Routes a request to the first handler whose substring is in the URL.

    A handler is either a (status, headers, data) tuple or a callable taking
    (method, url, headers, body) and returning one. Every call is recorded.
    """

    def __init__(self, routes=None):
        self.routes = list(routes or [])
        self.calls = []

    def add(self, needle, response):
        self.routes.append((needle, response))
        return self

    def __call__(self, method, url, headers=None, body=None, timeout=60):
        self.calls.append({"method": method, "url": url, "headers": dict(headers or {}),
                           "body": body})
        for needle, resp in self.routes:
            if needle in url:
                return resp(method, url, headers or {}, body) if callable(resp) else resp
        raise AssertionError("unexpected HTTP call to " + url.split("?")[0])

    def to(self, needle):
        return [c for c in self.calls if needle in c["url"]]


def _boom(*_a, **_k):
    raise AssertionError("network must not be touched")


@pytest.fixture
def fake(monkeypatch):
    f = FakeHTTP()
    monkeypatch.setattr(lf, "http_request", f)
    return f


def reoon_by_email(table, default="invalid"):
    """Reoon handler: answers each address from `table`."""
    def handler(method, url, headers, body):
        email = re.search(r"email=([^&]+)", url).group(1).replace("%40", "@")
        return 200, {}, {"email": email, "status": table.get(email, default)}
    return handler


def treg_by_endpoint(table):
    """TREG handler: `table` maps endpoint name to (status, headers, data)."""
    def handler(method, url, headers, body):
        endpoint = url.rsplit("/", 1)[-1]
        return table[endpoint]
    return handler


MAPS_ITEMS = [
    {"title": "Summit Roofing LLC", "website": "https://www.summitroofing.com/contact",
     "phone": "(512) 555-0101", "address": "1 Main St", "city": "Austin", "state": "Texas",
     "placeId": "p1", "url": "https://maps.example/p1", "categoryName": "Roofing contractor"},
    {"title": "Lone Star Roof Co.", "website": "", "phone": "(512) 555-0102",
     "city": "Austin", "state": "Texas", "placeId": "p2", "categoryName": "Roofer"},
    {"title": "Closed Roofing", "website": "https://closed.example", "phone": "1",
     "placeId": "p3", "permanentlyClosed": True},
]

FB_ITEMS = [
    {"pageId": "111", "snapshot": {"pageName": "Summit Roofing", "caption": "SUMMITROOFING.COM",
                                   "pageProfileUri": "https://facebook.com/summit"}},
    {"pageId": "111", "snapshot": {"pageName": "Summit Roofing", "caption": "summitroofing.com"}},
    {"pageId": "222", "snapshot": {"pageName": "Lone Star Roof Co LLC"}},
    {"pageId": "333", "snapshot": {"pageName": "Hill Country Gutters",
                                   "linkUrl": "https://hcgutters.com/offer?x=1"}},
    {"page_id": "444", "pageName": "No Snapshot Roofing"},
    {"snapshot": None},
]


# ---------------------------------------------------------------- CLI basics

def test_help_subprocess():
    out = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True,
                         text=True, cwd=str(KIT_ROOT))
    assert out.returncode == 0
    assert "--keyword" in out.stdout
    assert "--dry-run" in out.stdout


def test_bogus_flag_nonzero_no_http(monkeypatch):
    monkeypatch.setattr(lf, "http_request", _boom)
    with pytest.raises(SystemExit) as exc:
        lf.main(["--keyword", "roofers", "--location", "Austin, TX", "--dry-run", "--bogus-flag"])
    assert exc.value.code != 0


def test_missing_keyword_nonzero(monkeypatch):
    monkeypatch.setattr(lf, "http_request", _boom)
    with pytest.raises(SystemExit) as exc:
        lf.main(["--location", "Austin, TX", "--dry-run"])
    assert exc.value.code != 0


def test_dry_run_zero_network(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(lf, "http_request", _boom)
    for k in ("APIFY_TOKEN", "TREG_TOKEN", "TREG_ORG", "REOON_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    env = tmp_path / ".env"
    env.write_text("APIFY_TOKEN=abcd1234efgh5678\nREOON_API_KEY=rkey00001111\n")
    rc = lf.main(["--keyword", "roofers", "--location", "Austin, TX", "--limit", "5",
                  "--dry-run", "--env-file", str(env), "--out", str(tmp_path / "x.csv")])
    out = capsys.readouterr()
    text = out.out + out.err
    assert rc == 0
    assert "estimate" in text.lower()
    assert "abcd1234efgh5678" not in text
    assert "rkey00001111" not in text
    assert not (tmp_path / "x.csv").exists()


def test_non_tty_without_yes_exits_2_no_http(monkeypatch, tmp_path):
    monkeypatch.setattr(lf, "http_request", _boom)
    monkeypatch.setattr(lf, "_stdin_is_tty", lambda: False)
    monkeypatch.setenv("APIFY_TOKEN", "abcd1234efgh5678")
    rc = lf.main(["--keyword", "roofers", "--location", "Austin, TX",
                  "--env-file", str(tmp_path / "none.env"), "--out", str(tmp_path / "x.csv")])
    assert rc == 2


def test_missing_apify_token_fails_before_network(monkeypatch, tmp_path):
    monkeypatch.setattr(lf, "http_request", _boom)
    monkeypatch.delenv("APIFY_TOKEN", raising=False)
    rc = lf.main(["--keyword", "roofers", "--location", "Austin, TX", "--yes",
                  "--env-file", str(tmp_path / "none.env"), "--out", str(tmp_path / "x.csv")])
    assert rc == 1


# ---------------------------------------------------------------- env + masking

def test_load_env_partition_and_quotes(tmp_path):
    p = tmp_path / ".env"
    p.write_text("# comment\n\nAPIFY_TOKEN=\"abc=def\"\nTREG_ORG='my-team'\n"
                 "REOON_API_KEY = spaced \nnot a pair\n")
    env = lf.load_env(str(p))
    assert env["APIFY_TOKEN"] == "abc=def"
    assert env["TREG_ORG"] == "my-team"
    assert env["REOON_API_KEY"] == "spaced"
    assert lf.load_env(str(tmp_path / "missing.env")) == {}


def test_real_env_wins_and_placeholders_are_missing(tmp_path, monkeypatch):
    p = tmp_path / ".env"
    p.write_text("APIFY_TOKEN=from_file_1234\nTREG_TOKEN=paste_your_treg_token_here\n"
                 "TREG_ORG=your-team-slug\n")
    monkeypatch.setenv("APIFY_TOKEN", "from_env_9999")
    monkeypatch.delenv("TREG_TOKEN", raising=False)
    monkeypatch.delenv("TREG_ORG", raising=False)
    monkeypatch.delenv("REOON_API_KEY", raising=False)
    keys = lf.get_keys(str(p))
    assert keys["APIFY_TOKEN"] == "from_env_9999"
    assert keys["TREG_TOKEN"] == ""
    assert keys["TREG_ORG"] == ""
    assert keys["REOON_API_KEY"] == ""


def test_mask_never_shows_full_key():
    key = "abcdefghijklmnopqrstuvwxyz"
    m = lf.mask(key)
    assert key not in m
    assert m.startswith("abcd") and m.endswith("wxyz")
    assert lf.mask("") == "(missing)"
    assert "short" not in lf.mask("short")


# ---------------------------------------------------------------- Google Maps

def test_parse_maps_fields():
    rows = lf.parse_maps(MAPS_ITEMS)
    assert [r["business"] for r in rows] == ["Summit Roofing LLC", "Lone Star Roof Co."]
    r = rows[0]
    assert r["website"] == "https://www.summitroofing.com/contact"
    assert r["phone"] == "(512) 555-0101"
    assert r["source"] == "google_maps"
    assert r["ad_found"] == "no"
    assert r["domain"] == "summitroofing.com"
    assert r["location"] == "Austin, Texas"


def test_parse_maps_dedupes_place_id():
    rows = lf.parse_maps([MAPS_ITEMS[0], dict(MAPS_ITEMS[0])])
    assert len(rows) == 1


def test_maps_empty_raises(fake):
    fake.add("crawler-google-places", (201, {}, []))
    with pytest.raises(lf.EmptyRunError) as exc:
        lf.maps_search("roofers", "Austin, TX", 5, token="tok_secret_123")
    assert "input" in str(exc.value).lower()


def test_maps_auth_header_not_in_url(fake):
    fake.add("crawler-google-places", (201, {}, MAPS_ITEMS))
    rows = lf.maps_search("roofers", "Austin, TX", 5, token="tok_secret_123")
    assert len(rows) == 2
    call = fake.calls[0]
    assert call["method"] == "POST"
    assert "tok_secret_123" not in call["url"]
    assert call["headers"]["Authorization"] == "Bearer tok_secret_123"
    body = json.loads(call["body"])
    assert body["searchStringsArray"] == ["roofers"]
    assert body["locationQuery"] == "Austin, TX"
    assert body["maxCrawledPlacesPerSearch"] == 5
    assert body["scrapeContacts"] is False


def test_maps_http_error_raises_without_token(fake):
    fake.add("crawler-google-places", (401, {}, {"error": {"message": "bad token"}}))
    with pytest.raises(lf.ApifyError) as exc:
        lf.maps_search("roofers", "Austin, TX", 5, token="tok_secret_123")
    assert "tok_secret_123" not in str(exc.value)
    assert "401" in str(exc.value)


# ---------------------------------------------------------------- Facebook ads

def test_parse_fb_ads_defensive_fields_and_collapse():
    pages = lf.parse_fb_ads(FB_ITEMS)
    by_id = {p["page_id"]: p for p in pages}
    assert sorted(by_id) == ["111", "222", "333", "444"]
    assert by_id["111"]["ads"] == 2
    assert by_id["111"]["domain"] == "summitroofing.com"
    assert by_id["333"]["domain"] == "hcgutters.com"
    assert by_id["444"]["name"] == "No Snapshot Roofing"
    assert by_id["222"]["domain"] == ""


def test_fb_link_to_facebook_is_not_a_website():
    pages = lf.parse_fb_ads([{"pageId": "9", "snapshot": {
        "pageName": "X", "linkUrl": "https://www.facebook.com/x", "caption": "fb.me/x"}}])
    assert pages[0]["domain"] == ""


def test_fb_search_url_and_empty_is_warning(fake):
    fake.add("facebook-ads-scraper", (201, {}, []))
    pages = lf.fb_ads_search("roofers", "Austin, TX", 5, token="tok_secret_123")
    assert pages == []
    body = json.loads(fake.calls[0]["body"])
    url = body["startUrls"][0]["url"]
    assert "country=US" in url
    assert "q=roofers+Austin" in url
    assert body["resultsLimit"] == 5
    assert "tok_secret_123" not in fake.calls[0]["url"]


# ---------------------------------------------------------------- join

def test_join_ad_found_by_domain():
    maps = lf.parse_maps(MAPS_ITEMS)
    fb = lf.parse_fb_ads(FB_ITEMS[:2])
    rows = lf.join(maps, fb)
    summit = [r for r in rows if r["business"].startswith("Summit")]
    assert len(summit) == 1
    assert summit[0]["ad_found"] == "yes"
    assert summit[0]["source"] == "both"


def test_join_ad_found_by_name():
    maps = lf.parse_maps(MAPS_ITEMS)
    fb = lf.parse_fb_ads([FB_ITEMS[2]])
    rows = lf.join(maps, fb)
    lone = [r for r in rows if "Lone Star" in r["business"]]
    assert len(lone) == 1
    assert lone[0]["ad_found"] == "yes"
    assert lone[0]["source"] == "both"


def test_norm_name_strips_only_legal_suffixes():
    assert lf.norm_name("Lone Star Roof Co.") == lf.norm_name("Lone Star Roof, Inc")
    assert lf.norm_name("A & B Roofing LLC") == "a and b roofing"
    assert lf.norm_name("Roofing Company") == "roofing company"


def test_fb_only_rows_source_facebook_ads():
    maps = lf.parse_maps(MAPS_ITEMS)
    fb = lf.parse_fb_ads(FB_ITEMS)
    rows = lf.join(maps, fb)
    hc = [r for r in rows if r["business"] == "Hill Country Gutters"][0]
    assert hc["source"] == "facebook_ads"
    assert hc["ad_found"] == "yes"
    assert hc["domain"] == "hcgutters.com"
    plain = [r for r in rows if r["source"] == "google_maps"]
    assert all(r["ad_found"] == "no" for r in plain)


def test_ads_only_filter():
    rows = lf.join(lf.parse_maps(MAPS_ITEMS), lf.parse_fb_ads(FB_ITEMS[:2]))
    kept = lf.ads_only(rows)
    assert kept and all(r["ad_found"] == "yes" for r in kept)


# ---------------------------------------------------------------- email patterns

def test_email_patterns_order_and_cleaning():
    got = lf.email_patterns("Jo-hn", "O'Brien", "Summitroofing.com")
    assert got == [
        "john@summitroofing.com",
        "john.obrien@summitroofing.com",
        "johnobrien@summitroofing.com",
        "jobrien@summitroofing.com",
        "johno@summitroofing.com",
        "john_obrien@summitroofing.com",
        "obrien@summitroofing.com",
    ]


def test_email_patterns_empty_inputs():
    assert lf.email_patterns("", "Smith", "x.com") == []
    assert lf.email_patterns("John", "Smith", "") == []
    assert lf.email_patterns("John", "", "x.com") == ["john@x.com"]


def test_name_parts_drops_noise():
    assert lf.name_parts("Mr. John Q. Smith Jr.") == ("john", "smith")
    assert lf.name_parts("Blaine Y.") == ("blaine", "")


# ---------------------------------------------------------------- Reoon

@pytest.mark.parametrize("status,expected", [
    ("safe", "verified"), ("catch_all", "catch_all"), ("invalid", "miss"),
    ("disposable", "miss"), ("unknown", "miss"),
])
def test_reoon_verdicts(fake, status, expected):
    fake.add("reoon", (200, {}, {"status": status}))
    assert lf.reoon_verify("a@b.com", key="rk_123")["verdict"] == expected
    assert "mode=power" in fake.calls[0]["url"]


def test_reoon_safe_but_not_safe_to_send_is_miss():
    assert lf.reoon_verdict({"status": "safe", "is_safe_to_send": False}) == "miss"


def test_reoon_no_key_is_not_checked(monkeypatch):
    monkeypatch.setattr(lf, "http_request", _boom)
    assert lf.reoon_verify("a@b.com", key="")["verdict"] == "not_checked"


def test_reoon_key_not_in_error_message(monkeypatch):
    def leaky(method, url, headers=None, body=None, timeout=60):
        raise OSError("failed to open " + url)
    monkeypatch.setattr(lf, "http_request", leaky)
    res = lf.reoon_verify("a@b.com", key="SUPERSECRETKEY99")
    assert res["verdict"] == "not_checked"
    assert "SUPERSECRETKEY99" not in json.dumps(res)


# ---------------------------------------------------------------- TREG

def _treg(budget=1.0, org="my-team"):
    return lf.TregClient("treg_tok_abcdef123456", org, lf.TregBudget(budget))


def test_treg_200_charges_budget_from_header(fake):
    fake.add("treg.to", (200, {"X-Treg-Cost-Micro": "22600"},
                         {"output": {"email": "a@b.com"}, "_treg": {"charged_micro": 1}}))
    c = _treg()
    out = c.call("treg.people.email.find", {"domain": "b.com", "first_name": "a"})
    assert out == {"email": "a@b.com"}
    assert abs(c.budget.spent_usd - 0.0226) < 1e-9


def test_treg_charge_falls_back_to_body(fake):
    fake.add("treg.to", (200, {}, {"output": {}, "_treg": {"charged_micro": 5000}}))
    c = _treg()
    c.call("treg.people.search", {"company_domain": "b.com"})
    assert abs(c.budget.spent_usd - 0.005) < 1e-9


def test_treg_422_is_field_error_not_miss(fake):
    fake.add("treg.to", (422, {}, {"error": "identity_incomplete"}))
    c = _treg()
    with pytest.raises(lf.TregFieldError):
        c.call("treg.people.search", {"bad": 1})
    assert c.budget.spent_usd == 0


def test_treg_identity_incomplete_on_other_status_is_field_error(fake):
    fake.add("treg.to", (400, {}, {"error": "identity_incomplete: need q"}))
    with pytest.raises(lf.TregFieldError):
        _treg().call("treg.people.search", {"bad": 1})


def test_treg_502_is_miss(fake):
    fake.add("treg.to", (502, {}, {"error": "route_failed"}))
    c = _treg()
    assert c.call("treg.people.email.find", {"domain": "b.com"}) is None
    assert c.budget.spent_usd == 0


def test_treg_401_auth_error_masks_token(fake):
    fake.add("treg.to", (401, {}, {"error": "bad token"}))
    c = _treg()
    with pytest.raises(lf.TregStopped) as exc:
        c.call("treg.people.search", {"company_domain": "b.com"})
    assert "treg_tok_abcdef123456" not in str(exc.value)
    with pytest.raises(lf.TregStopped):
        c.call("treg.people.search", {"company_domain": "b.com"})
    assert len(fake.calls) == 1


def test_treg_budget_stops_calls(fake):
    fake.add("treg.to", (200, {"X-Treg-Cost-Micro": "30000"}, {"output": {"email": "x@y.com"}}))
    c = _treg(budget=0.05)
    c.call("treg.people.email.find", {"domain": "y.com"})
    c.call("treg.people.email.find", {"domain": "y.com"})
    n = len(fake.calls)
    assert n == 2
    with pytest.raises(lf.TregBudgetExhausted):
        c.call("treg.people.email.find", {"domain": "y.com"})
    assert len(fake.calls) == n


def test_treg_route_ceiling_never_exceeds_remaining(fake):
    fake.add("treg.to", (200, {"X-Treg-Cost-Micro": "20000"}, {"output": {}}))
    c = _treg(budget=0.03)
    c.call("treg.people.search", {"company_domain": "b.com"})
    c.call("treg.people.search", {"company_domain": "b.com"})
    second = float(fake.calls[1]["headers"]["X-Treg-Route-Max-Cost"])
    assert second <= 0.01 + 1e-9


def test_treg_sends_org_header_from_env(fake, monkeypatch, tmp_path):
    fake.add("treg.to", (200, {}, {"output": {}}))
    monkeypatch.setenv("TREG_TOKEN", "treg_tok_abcdef123456")
    monkeypatch.setenv("TREG_ORG", "acme-agency")
    keys = lf.get_keys(str(tmp_path / "none.env"))
    c = lf.TregClient(keys["TREG_TOKEN"], keys["TREG_ORG"], lf.TregBudget(1.0))
    c.call("treg.people.search", {"company_domain": "b.com"})
    h = fake.calls[0]["headers"]
    assert h["X-Treg-Org"] == "acme-agency"
    assert h["X-Treg-Token"] == "treg_tok_abcdef123456"
    assert fake.calls[0]["url"] == "https://treg.to/call/treg.people.search"


def test_person_from_search_varied_keys():
    out = {"people": [
        {"name": "Solo"},
        {"firstName": "Amy", "lastName": "Lee", "jobTitle": "Estimator"},
        {"first_name": "Bob", "last_name": "Ray", "job_title": "Owner & President",
         "work_email": " Bob@X.com "},
    ]}
    p = lf.person_from_search(out)
    assert p["name"] == "Bob Ray"
    assert p["email"] == "bob@x.com"
    p2 = lf.person_from_search([{"full_name": "Cara Diaz", "title": "Manager"}])
    assert p2["first"] == "cara" and p2["last"] == "diaz"
    assert lf.person_from_search({"people": []}) is None
    assert lf.person_from_search(None) is None


# ---------------------------------------------------------------- find_owner

def _row(domain="summitroofing.com"):
    return {"business": "Summit Roofing", "website": "https://" + domain, "phone": "",
            "owner_name": "", "email": "", "verified": "", "source": "google_maps",
            "ad_found": "no", "domain": domain, "location": "Austin, TX", "site_emails": []}


def test_find_owner_pattern_hit_skips_treg_email_find(fake):
    fake.add("treg.to", treg_by_endpoint({
        "treg.people.search": (200, {"X-Treg-Cost-Micro": "10000"},
                               {"output": {"people": [{"name": "John Smith", "title": "Owner"}]}}),
    }))
    fake.add("reoon", reoon_by_email({"john.smith@summitroofing.com": "safe"}))
    row = lf.find_owner(_row(), treg=_treg(), reoon_key="rk", notes=lf.Notes())
    assert row["owner_name"] == "John Smith"
    assert row["email"] == "john.smith@summitroofing.com"
    assert row["verified"] == "verified"
    assert not [c for c in fake.calls if c["url"].endswith("treg.people.email.find")]
    reoon_emails = [re.search(r"email=([^&]+)", c["url"]).group(1) for c in fake.to("reoon")]
    assert reoon_emails[0].startswith("john%40")
    assert len(reoon_emails) == 2


def test_find_owner_catch_all_falls_to_treg(fake):
    fake.add("treg.to", treg_by_endpoint({
        "treg.people.search": (200, {}, {"output": {"people": [{"name": "John Smith"}]}}),
        "treg.people.email.find": (200, {"X-Treg-Cost-Micro": "22600"},
                                   {"output": {"email": "jsmith@summitroofing.com"}}),
    }))
    fake.add("reoon", reoon_by_email({}, default="catch_all"))
    row = lf.find_owner(_row(), treg=_treg(), reoon_key="rk", notes=lf.Notes())
    order = [c["url"].rsplit("/", 1)[-1] if "treg.to" in c["url"] else "reoon"
             for c in fake.calls]
    assert order[0] == "treg.people.search"
    assert "treg.people.email.find" in order
    assert order.index("treg.people.email.find") > order.index("reoon")
    assert row["email"] == "jsmith@summitroofing.com"
    assert row["verified"] == "catch_all"
    body = json.loads(fake.to("treg.people.email.find")[0]["body"])
    assert body == {"domain": "summitroofing.com", "first_name": "john", "last_name": "smith"}


def test_find_owner_search_email_verified_stops(fake):
    fake.add("treg.to", treg_by_endpoint({
        "treg.people.search": (200, {}, {"output": {"people": [
            {"name": "Jane Roe", "email": "jane@summitroofing.com"}]}}),
    }))
    fake.add("reoon", reoon_by_email({"jane@summitroofing.com": "safe"}))
    row = lf.find_owner(_row(), treg=_treg(), reoon_key="rk", notes=lf.Notes())
    assert row["email"] == "jane@summitroofing.com"
    assert row["verified"] == "verified"
    assert len(fake.to("reoon")) == 1


def test_find_owner_no_domain_skipped(monkeypatch):
    monkeypatch.setattr(lf, "http_request", _boom)
    row = lf.find_owner(_row(domain=""), treg=_treg(), reoon_key="rk", notes=lf.Notes())
    assert row["verified"] == "skipped"
    assert row["email"] == ""


def test_find_owner_no_treg_no_name_is_skipped(monkeypatch):
    monkeypatch.setattr(lf, "http_request", _boom)
    row = lf.find_owner(_row(), treg=None, reoon_key="rk", notes=lf.Notes())
    assert row["verified"] == "skipped"


def test_find_owner_field_error_is_reported_not_a_miss(fake):
    fake.add("treg.to", (422, {}, {"error": "identity_incomplete"}))
    notes = lf.Notes()
    row = lf.find_owner(_row(), treg=_treg(), reoon_key="rk", notes=notes)
    assert row["verified"] == "skipped"
    assert any("field" in n.lower() for n in notes.items())


# ---------------------------------------------------------------- CSV + end to end

def test_csv_exact_header(tmp_path):
    out = tmp_path / "sub" / "leads.csv"
    row = _row()
    row.update(owner_name="John Smith", email="john@summitroofing.com", verified="verified")
    lf.write_csv([row], str(out))
    lines = out.read_text().splitlines()
    assert lines[0] == HEADER
    rec = next(csv.DictReader(io.StringIO(out.read_text())))
    assert rec["email"] == "john@summitroofing.com"
    assert set(rec) == set(HEADER.split(","))


def test_csv_empty_writes_header_and_exit_3(fake, monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("APIFY_TOKEN", "apify_tok_1234567890")
    for k in ("TREG_TOKEN", "TREG_ORG", "REOON_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    fake.add("crawler-google-places", (201, {}, MAPS_ITEMS[:1]))
    fake.add("facebook-ads-scraper", (201, {}, []))
    out = tmp_path / "leads.csv"
    rc = lf.main(["--keyword", "roofers", "--location", "Austin, TX", "--limit", "5",
                  "--ads-only", "--yes", "--env-file", str(tmp_path / "none.env"),
                  "--out", str(out)])
    cap = capsys.readouterr()
    assert rc == 3
    assert out.read_text().splitlines() == [HEADER]
    assert "rows=0" in cap.out
    assert "WARNING" in cap.err


def test_maps_empty_run_exit_1(fake, monkeypatch, tmp_path):
    monkeypatch.setenv("APIFY_TOKEN", "apify_tok_1234567890")
    fake.add("crawler-google-places", (201, {}, []))
    rc = lf.main(["--keyword", "roofers", "--location", "Austin, TX", "--yes", "--no-ads",
                  "--env-file", str(tmp_path / "none.env"), "--out", str(tmp_path / "x.csv")])
    assert rc == 1


def test_end_to_end_mocked(fake, monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("APIFY_TOKEN", "apify_tok_1234567890")
    monkeypatch.setenv("TREG_TOKEN", "treg_tok_abcdef123456")
    monkeypatch.setenv("TREG_ORG", "acme-agency")
    monkeypatch.setenv("REOON_API_KEY", "reoon_key_0987654321")
    fake.add("crawler-google-places", (201, {}, MAPS_ITEMS))
    fake.add("facebook-ads-scraper", (201, {}, FB_ITEMS))

    def treg(method, url, headers, body):
        endpoint = url.rsplit("/", 1)[-1]
        req = json.loads(body)
        if endpoint == "treg.people.search" and req["company_domain"] == "summitroofing.com":
            return 200, {"X-Treg-Cost-Micro": "10000"}, {"output": {"people": [
                {"first_name": "John", "last_name": "Smith", "title": "Owner"}]}}
        if endpoint == "treg.people.search":
            return 502, {}, {"error": "route_failed"}
        return 502, {}, {"error": "route_failed"}
    fake.add("treg.to", treg)
    fake.add("reoon", reoon_by_email({"john@summitroofing.com": "safe"}))

    out = tmp_path / "leads.csv"
    rc = lf.main(["--keyword", "roofers", "--location", "Austin, TX", "--limit", "5",
                  "--yes", "--env-file", str(tmp_path / "none.env"), "--out", str(out)])
    cap = capsys.readouterr()
    assert rc == 0, cap.err
    recs = list(csv.DictReader(io.StringIO(out.read_text())))
    assert out.read_text().splitlines()[0] == HEADER
    by = {r["business"]: r for r in recs}
    assert by["Summit Roofing LLC"]["email"] == "john@summitroofing.com"
    assert by["Summit Roofing LLC"]["verified"] == "verified"
    assert by["Summit Roofing LLC"]["source"] == "both"
    assert by["Lone Star Roof Co."]["verified"] == "skipped"
    assert by["Hill Country Gutters"]["source"] == "facebook_ads"
    assert re.search(r"^rows=4 verified=1 ads_found=4 treg_spent=\$0\.01", cap.out, re.M)
    blob = cap.out + cap.err + out.read_text()
    for secret in ("apify_tok_1234567890", "treg_tok_abcdef123456", "reoon_key_0987654321"):
        assert secret not in blob


# ---------------------------------------------------------------- hygiene

# Built by concatenation so this file never matches its own patterns.
SECRET_PATTERNS = [
    re.compile("sk" + "_live"),
    re.compile("sk" + "_test"),
    re.compile("apify" + "_api_" + "[A-Za-z0-9]"),
    re.compile("pit" + "-[0-9a-f]{6}"),
    re.compile("131" + "31"),
]
COMPETITORS = ["va" + "pi", "ret" + "ell", "synth" + "flow", "assist" + "able", "bla" + "nd"]
COMPETITOR_RE = re.compile(r"\b(" + "|".join(COMPETITORS) + r")\b", re.I)
EMDASH = chr(0x2014)
# Private names (clients, the maintainer's org slug) are checked by hash so the
# public repo never spells them out. sha256 of the lowercased word or bigram.
PRIVATE_HASHES = {
    "ec97539d3d5027454675e89f7ac05814ab8cfef8f4567492616ffb1266b92253",
    "4d4ed4fc67d404c4d83262fd160f450be345f0e8094e5bc38be924cbe8b278a2",
    "1a47d5f99b6c94ce8553382f2f48f8de329af5d809d52cafbf719f3c08d817a8",
    "4db5e6d7b9b80519031075716f34a6bf87ac5e0cbb78a1e5425252e710b0d4e3",
    "9a79c62e37ef77119c5a1d2ac8d5814e7f42e6593f27b3eee4be812283eccbe8",
    "fd981b1671690481a18bac14c716a36dd465e25e02797f4cc106275ce71134ac",
    "f46c981c68cd9e611d20398d5507d692f5949dabc83086e1e486e1aed877ef84",
    "1baf4973347bf18e85a4008a6eebe7157e95ef21943adf8afd47b2c53698ae05",
    "945da698fa19ab476ba5e1d1900f5cd4a5d312cffcd042a641d69839876e0f32",
    "1855f8fe0e94e2f8a0b09707b3159acc0be5a9f6bb1b8fc0c2e75b662398e050",
    "37e5f3943a284e92b1f154c32d0702342c1deefb8feaf5e5b6cff5683f3511e3",
    "af2947970bdf3bc80d7ecd9d2ab5afeb4d2851e2aed6a5c488334c01089f8942",
}


def _private_hashes():
    return set(PRIVATE_HASHES)


def _tokens(text):
    words = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())
    grams = set(words)
    grams.update(a + " " + b for a, b in zip(words, words[1:]))
    return grams


def scan(text, hashes=None):
    hashes = _private_hashes() if hashes is None else hashes
    hits = [p.pattern for p in SECRET_PATTERNS if p.search(text)]
    if EMDASH in text:
        hits.append("em-dash")
    hits += ["competitor:" + m.group(1).lower() for m in COMPETITOR_RE.finditer(text)]
    for tok in _tokens(text):
        if hashlib.sha256(tok.encode()).hexdigest() in hashes:
            hits.append("private-name")
    return hits


def _new_files():
    files = [p for p in HERE.rglob("*") if p.is_file() and p.suffix in (".py", ".md")
             and p.name != Path(__file__).name and "__pycache__" not in p.parts]
    files.append(KIT_ROOT / ".claude" / "skills" / "lead-finder" / "SKILL.md")
    return files


def test_hygiene_positive_control():
    planted_hash = hashlib.sha256(b"zebracorn").hexdigest()
    planted = ("key " + "sk" + "_live_abc " + "apify" + "_api_X1 " + "pit" + "-abc123 "
               + EMDASH + " we beat " + "Va" + "pi and zebracorn")
    hits = scan(planted, hashes={planted_hash})
    assert "em-dash" in hits
    assert "competitor:" + "va" + "pi" in hits
    assert "private-name" in hits
    assert len([h for h in hits if not h.startswith(("em-dash", "competitor", "private"))]) == 3
    assert scan("Roofers in Austin, TX. Call after hours.", hashes={planted_hash}) == []


def test_hygiene_scan_new_files():
    files = _new_files()
    assert (HERE / "lead_finder.py") in files and (HERE / "README.md") in files
    for f in files:
        assert f.exists(), f
        assert scan(f.read_text()) == [], f
