---
name: sales-presentation
description: Turn a single fill-in template into a branded, client-facing sales deck that pitches an AI voice-agent system to any business in any industry. Produces one standalone dark-themed HTML page (single-scroll, not a slideshow) built from a reusable component library - hero with badges, numbered sections, stat grids, lead-journey flowcharts with branching paths, capability and compliance card grids, unit-economics stats, and a CTA footer. The agency owner gives a logo, two brand colors, the client name, and the use-case; the deck is rebranded in one place (the `:root` block) and the copy is rewritten for that industry. Triggers on /sales-presentation, build a sales deck, make a pitch deck, presentation for [client], pitch the AI to a client, client-facing deck, build a proposal deck, AI voice agent pitch deck, sales presentation for [industry], rebrand the deck for [client], make me a pitch for [business], deck to sell the AI system, proposal HTML for a prospect.
---

# Sales Presentation Builder

Turn one reusable template into a polished, branded sales deck that an agency owner hands to a client to pitch an AI voice-agent system. The output is a single standalone HTML file: a dark, single-scroll deck (not a slideshow) with a hero, numbered sections, and a library of visual components (stat grids, flowcharts with branches, card grids, tables, notes, pills).

The deck answers, for a specific client and industry: what the AI system is, how a lead flows through it, what the AI can do, how it stays compliant, what it costs, and what to do next.

## What it produces

A single `output/<client>-deck.html` file that:

- Renders standalone in any browser. No build step, no framework, no JavaScript beyond the Google Fonts link. Pure HTML and CSS.
- Carries the agency's brand: a logo at the top of the hero, plus a two-color accent scheme.
- Is written for one industry: every content section is rewritten for that vertical (call types, lead journey, capabilities, economics), while the component library and layout stay identical.

## When to invoke

- "Build a sales deck for [client] in [industry]"
- "Make me a pitch deck to sell the AI receptionist to a dental practice"
- "Rebrand this deck for my client and rewrite it for HVAC"
- "I need a client-facing proposal page for an AI voice agent"
- "Pitch the AI to a roofing company"

This is different from `prospect-demo` (which builds a live voice demo URL) and `talking-website` (which puts a voice agent on a live site). This skill builds a static **presentation** - a thing you send or screen-share to explain the system and sell it.

## The two things that change (and nothing else)

The whole design of this skill is one clean split:

1. **Branding lives in ONE place.** The `:root` block at the top of the CSS holds two color knobs (`--primary` and `--accent`), and there is a single logo `<img src>` in the hero. Change those, and the entire deck rebrands: gradients, borders, pills, stat numbers, flowchart highlights, every accent. You never hunt through the body for colors.
2. **Content is swapped per industry.** Every headline, stat, card, flowchart node, and table cell is rewritten for the client's vertical. The component classes (`.stats/.stat`, `.flow/.fnode/.arrow/.split/.branch`, `.grid/.card`, `.note`, `.pill`, tables) stay exactly as they are - you only change the words inside them.

Do not refactor the CSS, do not add a JS build, do not split branding across multiple selectors. Keep the split clean.

## Fill workflow

### (a) Gather the brand

Ask the user for, or infer from what they give you:

- **Logo URL** - a hosted image (PNG/SVG) for the hero. A horizontal logo on a transparent or dark background looks best, since the hero is dark. If the user has no logo, leave the placeholder and tell them where to swap it.
- **Two hex colors** - a primary and an accent. If the user gives none, default to Leadlock blue `#6298B6` (primary) and navy `#2C5570` (accent). If they give one, use it as primary and derive a complementary accent or ask.
- **Agency name and client name** - the agency is who is presenting; the client is who the deck is for. Both appear in copy (hero, footer, CTA).

### (b) Gather the industry and use-case

Ask what the AI system does for this client. Typical pieces:

- The **industry / vertical** (HVAC, dental, roofing, law firm, real estate, etc.).
- The **call types** the AI handles (inbound after-hours answering, missed-call text-back, outbound follow-up, appointment booking, lead qualification, reminders).
- The **conversion event** (booked appointment, scheduled estimate, captured lead, confirmed callback).
- Any **economics** the user wants shown (cost per lead, cost per booked job, monthly volume mix). If the user has no numbers, write realistic placeholder ranges and clearly mark them as estimates.

If anything is missing or contradictory, stop and ask using lettered options. A vague industry produces a vague deck.

### (c) Rewrite each section for the industry

Open `templates/deck-template.html`. For each `{{TOKEN}}` and each marked `PLACEHOLDER` section, rewrite the copy for the client's vertical. Keep:

- the component library (every CSS class) untouched,
- the section order and numbering,
- the `:root` branding mechanism - you swap only the two colors and the logo URL.

Every `{{TOKEN}}` in the template, and what to fill it with:

| Token | Fill with |
|---|---|
| `{{PRIMARY_COLOR}}` | Brand primary hex, in `:root` only (default `#6298B6`) |
| `{{ACCENT_COLOR}}` | Brand accent hex, in `:root` only (default `#2C5570`) |
| `{{LOGO_URL}}` | Hosted logo URL for the hero `<img src>` |
| `{{AGENCY_NAME}}` | The agency presenting the deck (hero `alt`, footer) |
| `{{CLIENT_NAME}}` | The business the deck is for (title, body, footer) |
| `{{INDUSTRY}}` | The vertical (HVAC, dental, roofing, etc.) |
| `{{HERO_HEADLINE}}` | First part of the hero H1 (plain text) |
| `{{HERO_HEADLINE_ACCENT}}` | Tail of the hero H1, rendered in the gradient accent `<span>` |
| `{{HERO_SUBHEAD}}` | One-paragraph pitch under the headline |
| `{{BADGE_1}}` through `{{BADGE_6}}` | Six short capability badges in the hero |
| `{{CTA_HEADLINE}}` | Closing call-to-action headline |
| `{{CTA_LINE}}` | One-sentence CTA supporting line |
| `{{CTA_BUTTON}}` | CTA button label |

Sections also contain inline `PLACEHOLDER` copy (no braces) inside stat values, cards, flowchart nodes, the note, and the economics table. Rewrite each of those for the industry too; the template's header comment marks them.

Replace the two default `:root` colors with the client's hex values, and set the logo `<img src>`. That is the entire branding change. Everything else is words.

See `templates/example-hvac-deck.html` for a fully worked example (fictional HVAC company "Summit Air") so you can see what a finished, industry-specific, rebranded deck looks like. Note it uses a different accent color than the default to prove the one-place rebrand works.

### (d) Save and open

Save the filled deck to `output/<client>-deck.html` (lowercase, hyphenated client name). The `output/` directory is created at fill time inside the skill folder; it is intentionally not committed. After saving, open it in the default browser so the user sees it immediately:

```bash
open "output/<client>-deck.html"
```

On non-macOS, use `xdg-open` (Linux) or tell the user the file path.

## Component library reference

The template ships these components. Reuse them; do not invent new ones unless the content truly needs it.

| Component | Classes | Use for |
|---|---|---|
| Hero | `.hero`, `.badges`, `.badge` | Title, one-paragraph pitch, a row of capability badges |
| Stat grid | `.stats`, `.stat` (`.v` value, `.l` label) | Quick numbers - speed, volume, cost, coverage |
| Card grid | `.grid.c2` / `.grid.c3`, `.card` (`.tag`, `h4`, `p`) | Capabilities, compliance rails, "what it is" pairs |
| Flowchart | `.flow`, `.fnode`, `.arrow`, `.split`, `.branch` | The lead journey, with branching outcomes |
| Node states | `.fnode.hl/.good/.warn/.stop` | Highlight, success, caution, terminal |
| Table | `table`, `th`, `td`, `td.dim` | Workflow lists, cadence schedules, economics rows |
| Note | `.note` | A callout / caveat under a section |
| Pill | `.pill.b/.g/.a/.r` | Inline status labels in cards and tables |

## Hard rules

1. **Branding is two colors plus one logo URL, in `:root` and the hero only.** Never scatter brand colors through the body.
2. **Never invent real client data.** No real phone numbers, real customer names, real prices the user did not give you, or anything tied to a specific real business. Placeholder economics must be marked as estimates.
3. **No em-dashes (U+2014) anywhere.** Use a hyphen, a colon, or rewrite the sentence. This is a hard style rule for every file this skill writes.
4. **The deck must render standalone.** No external JS. The only external resource is the Google Fonts (Poppins) link.
5. **Keep the dark aesthetic and the Poppins font.** The deck is designed to look premium on a dark background.
6. **Do not commit `output/` files.** They are per-client artifacts.

## Files in this skill

- `SKILL.md` - this file.
- `templates/deck-template.html` - the generalized deck with `{{PLACEHOLDER}}` tokens and industry-agnostic placeholder content that exercises every component.
- `templates/example-hvac-deck.html` - a fully filled worked example (fictional "Summit Air" HVAC) with a different accent color.
- `output/` - created at fill time; holds the generated `<client>-deck.html` files. Not committed.
