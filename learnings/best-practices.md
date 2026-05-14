# Best practices

Patterns that worked well and are worth repeating. Concrete, not generic.

Each entry includes: date, tags, evidence link, rule, why, how to apply.

---

### Use `find_logo.py` to pull a prospect's logo with browser headers

Date: 2026-05-13
Tags: skill:prospect-demo, type:pattern, helper-script
Evidence: `.claude/skills/prospect-demo/find_logo.py`; verified working against `northernmistersparky.com` (Cloudflare-protected) — picked the 192×192 apple-touch-icon as avatar

**Rule:** When you need a prospect's logo, run `python3 .claude/skills/prospect-demo/find_logo.py <url> --download ./output/<slug>` instead of hand-grepping the HTML. The helper handles Cloudflare's basic block (browser User-Agent), parses `<link rel="apple-touch-icon">`, `<link rel="icon">`, og:image, and `<img class="logo">`, dedupes by URL, and returns two best-fit candidates — `avatar` (square) and `header` (rectangular).

**Why:** Logo extraction repeats across most demo builds. The bare `curl` pattern fails on Cloudflare sites without the right headers. Selecting "the right logo" depends on the slot (avatar wants square icons, header wants og:image), and that prioritization is non-obvious. Centralizing it in a small helper means each new build does it the same way and the priorities can be improved in one place.

**How to apply:** Step 1.5 of `prospect-demo/SKILL.md` calls this helper. When building any future demo-creation skill, reuse the pattern (don't duplicate the helper — point at the file). Then upload the chosen avatar to the demo via `POST /demos/{demo_id}/upload-image` and wire it through `phone_caller_image` — see `[[best-practices#phone-demo-per-prospect-branding-works-today]]`.

---

### Phone demo per-prospect branding works today

Date: 2026-05-13
Tags: skill:prospect-demo, type:pattern, channel:phone, surface:public-demo-page
Evidence: deployed bundle `https://app.leadlock.ai/assets/_slug_-DnMHePt3.js` reads `(t.config)?.phone_caller_image` and `(t.config)?.phone_accent_color`; passes them as `callerImage` / `accentColor` to `PhoneDemoView`

**Rule:** Phone-channel demos accept two per-demo branding knobs in `demo.config`. Set them via `PATCH /demos/{demo_id}`:
- `phone_caller_image` — URL to the avatar image (PNG/JPG, square). Replaces the agent-initials fallback.
- `phone_accent_color` — hex color string (e.g. `"#FFC72C"`). Drives the call-arc ring color, the accept-button glow, and other accents. Defaults to `#3b82f6` (blue) when absent.

Recipe (Northern Mister Sparky example):
```bash
# 1. Find and download the logo
python3 .claude/skills/prospect-demo/find_logo.py https://prospect.com --download ./output/<slug>

# 2. Upload to the demo, get back a Supabase URL
curl -X POST $API_URL/demos/$DEMO_ID/upload-image \
  -H "X-API-Key: $KEY" \
  -F "file=@./output/<slug>/<avatar>.png"
# → { "url": "https://<project>.supabase.co/storage/v1/object/public/.../avatar.png" }

# 3. Wire it into the demo config (plus accent color)
curl -X PATCH $API_URL/demos/$DEMO_ID \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"config": {
        "phone_caller_image": "<url from step 2>",
        "phone_accent_color": "#FFC72C",
        "display_name": "Northern Mister Sparky",
        "landing_heading": "Talk to Maya — Northern Mister Sparky",
        "landing_subheading": "Tap to call: ...",
        "landing_instructions": "..."
      }}'
```

**Why:** These keys are undocumented — they don't appear in `openapi-spec.json`/`LEADLOCKDOCS.json` because `demo.config` is `additionalProperties: true`. Found them by reading the deployed `/d/<slug>` route chunk (`_slug_-DnMHePt3.js`), which destructures the keys directly from `t.config`. The prior "platform-gap" entry was a probing error — see `[[platform-gaps#demo-page-avatar-cannot-be-overridden-via-api]]` (retracted).

**How to apply:** Add this to every phone-channel demo build by default. The logo-finder already stages the right image. The accent color should match the prospect's brand (pull from `og:image` ambient color, or pick from the brand palette manually). If the prospect doesn't have an obvious brand color, leave `phone_accent_color` off and accept the blue default. Verify after PATCH by re-fetching the demo and confirming both keys are stored — then load the page and confirm the avatar circle shows the image, not initials.

---

### Transparent iframe surround for demo embeds

Date: 2026-05-13
Tags: skill:prospect-demo, type:pattern, surface:iframe-embed
Evidence: deployed bundle `_slug_-DnMHePt3.js` lines (post-mount useEffect): `if(z||w||A){ document.documentElement.style.background="transparent"; document.body.style.background="transparent"; #root.style.background="transparent"; }` where `z=h.get("embed")==="true"`, `w=h.get("mode")==="phone"`, `A=window.self!==window.top`

**Rule:** Embedded demo iframes get transparent backgrounds automatically when ANY of these conditions hit:
1. The iframe URL includes `?embed=true`
2. The iframe URL includes `?mode=phone`
3. The page is loaded inside an iframe at all (`window.self !== window.top` — auto-detect)

This means: the parent page's background bleeds through. White GHL page → white surround. Whatever color the user puts behind the iframe wins.

**Why:** The surround color is controlled by the parent, not the demo. Old approach was to file a feature request for a per-demo theme override — unnecessary. Just embed the iframe on the GHL section with the right background.

**How to apply:** Always include `?embed=true` on iframe sources for safety (it's idempotent with the iframe auto-detect, but explicit is better). The iframe template in `prospect-demo/SKILL.md` should look like:

```html
<iframe
  src="https://app.leadlock.ai/d/<slug>?embed=true"
  width="100%"
  height="780"
  style="border:0; border-radius:12px; max-width:480px; background:transparent;"
  allow="microphone; autoplay"
  loading="lazy"
  title="<Business> — <Agent> (Phone Demo)"
></iframe>
```

Tell the prospect to drop it on whatever GHL section color they want. If they want white surround, the section background needs to be white. Note: the *phone mockup itself* keeps its dark bezel — that's the iPhone-style frame design, not the page background. Only the area around the bezel inherits from the parent.

---

### Read deployed JS chunks to find undocumented config keys

Date: 2026-05-13
Tags: type:debug-pattern, source:deployed-bundle
Evidence: discovered `phone_caller_image`, `phone_accent_color`, `embed=true` query handling by reading `_slug_-DnMHePt3.js`; none of these strings appear in openapi-spec or LEADLOCKDOCS

**Rule:** When the openapi spec marks a field as `additionalProperties: true` (typical for `demo.config`, `agent.tool_instructions`, etc.) and a user claims undocumented behavior, don't argue from the spec — read the deployed JS chunk that renders the relevant surface.

Recipe:
```bash
# 1. Get the HTML for the surface in question
curl -s -H "User-Agent: Mozilla/5.0" https://app.leadlock.ai/d/<some-existing-slug> > /tmp/page.html

# 2. Find the JS bundles referenced
grep -oE '/assets/[A-Za-z0-9_\-]+\.js' /tmp/page.html

# 3. Grab the main bundle, find route lazy-loads
curl -s https://app.leadlock.ai/assets/index-<hash>.js | grep -oE '[A-Za-z]+(_[A-Za-z]+)*-[A-Za-z0-9]{8,}\.js' | sort -u
# Look for chunk names matching the surface (e.g. _slug_-*.js for /d/[slug], PhoneDemoView-*.js)

# 4. Grep that chunk for snake_case property accesses (config keys are usually snake_case)
curl -s https://app.leadlock.ai/assets/_slug_-<hash>.js | grep -oE '\.[a-z][a-z_]{4,30}' | sort -u | grep _

# 5. For each key, find the usage context to understand what it controls
```

**Why:** The platform's openapi schema is the formal contract for typed fields. For `additionalProperties: true` fields like `demo.config`, the schema doesn't enumerate accepted keys — they're discoverable only from the renderer. Doing this discovery in 60 seconds saves a feature-request round-trip and prevents publishing wrong "platform gap" entries.

**How to apply:** Whenever you're about to write "the API doesn't support X" for a feature that lives in a free-form config object, run this audit first. If the JS chunk contains the snake_case key, the feature exists — try it. If it doesn't, then it's a real gap. Document the audit result either way.
