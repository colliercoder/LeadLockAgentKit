---
name: knowledge-base-builder
description: Build a knowledge base for an agent from URLs, FAQ documents, CSVs, or markdown — and attach it. Uses the platform's web crawler, FAQ generator, and table parser to assemble searchable Q&A blocks. Triggers on /knowledge-base-builder, build a KB, create a knowledge base, give my agent a knowledge base, add knowledge to my agent, attach FAQs, upload FAQs, give my agent documents, scrape FAQs from this URL, import this CSV as a KB, crawl [URL] into a knowledge base, add a pricing list, attach a service menu, give my agent reference material, set up RAG, search documents for my agent.
---

# Knowledge Base Builder

Stand up a searchable knowledge base for an agent and attach it. Sources can be a URL (crawled and chunked), an FAQ document (auto-generated into Q&A pairs), a CSV (parsed into rows), or raw markdown. All via the Leadlock API — no UI clicks.

## When to invoke

- "Build a KB for [agent]"
- "Give my agent these FAQs / this product catalog / this URL"
- "Crawl [URL] into a knowledge base"
- "Import this CSV as a price list / FAQ / service menu"
- Agent is answering off-prompt and needs deeper reference material

## Setup check

Confirm `./.env` has `LEADLOCK_API_KEY` and `LEADLOCK_API_URL`.

## Rules

1. **One KB per business domain.** Don't fragment "Plumbing FAQs", "HVAC FAQs", and "Electrical FAQs" into three KBs for one home-services agency — one KB with sources tagged.
2. **Q&A blocks beat blog prose.** The platform searches via xAI Search. Structured Q&A (or FAQ pairs) ranks better than long-form paragraphs. Prefer FAQ sources and rich text in Q&A format.
3. **Multiple phrasings per question.** Each FAQ block should start with 2-3 alternate phrasings of the same question so search recall is high.
4. **Don't dump everything.** A 200-Q FAQ that overlaps the system prompt creates contradiction risk. Curate to questions the prompt CANNOT answer well: technical specs, regulatory text, pricing matrices, rare scenarios.
5. **Attach to the agent and enable the tool.** After upload, PATCH the agent with `enable_collections_search=true`, `knowledge_base_ids=[<kb_id>]`, and add `search_knowledge_base` to `tools_enabled`.
6. **Branch discipline: stay on main.** No `git checkout -b`.

## Required inputs

- **KB name** (default: "<Business> KB" or derived from sources)
- **Source(s)** — one or more of:
  - URL → crawled via the platform's web crawler
  - FAQ text → auto-generated into Q&A pairs
  - Markdown / plain text → rich-text source
  - CSV file → parsed into table rows (good for price lists, service catalogs, locations)
- **Agent(s) to attach** — one or many. Optional; can attach later.

## Execution

### Step 0 — Resolve / create the KB

If the user names an existing KB, look it up:
```
GET /knowledge-bases
```

If creating new:
```
POST /knowledge-bases
{ "name": "<KB Name>" }
```

Save the returned `kb_id`.

### Step 1 — Add sources

For each source the user gave, choose the right endpoint.

#### URL → Web Crawler

```
POST /knowledge-bases/<kb_id>/web-crawlers
{
  "name": "<descriptive label, e.g. 'Acme Plumbing — main site'>",
  "root_url": "https://acmeplumbing.com",
  "schedule_interval": null
}
```

Optional: set `schedule_interval` to a number of hours for automatic re-crawls (e.g. `168` for weekly).

Re-trigger a manual crawl later:
```
POST /knowledge-bases/<kb_id>/web-crawlers/<source_id>/recrawl
```

#### FAQ text → auto-generated Q&A pairs

Two steps. First create the FAQ source:

```
POST /knowledge-bases/<kb_id>/faqs
{ "name": "<Source name, e.g. 'Battery FAQ from sales doc'>", "pairs": [] }
```

Save the returned `source_id`.

Then generate pairs from raw text content:

```
POST /knowledge-bases/<kb_id>/faqs/<source_id>/generate
{
  "content": "<paste the raw FAQ text or document content here>",
  "num_pairs": 25
}
```

The platform extracts question/answer pairs from the content automatically.

Or add hand-curated pairs:

```
POST /knowledge-bases/<kb_id>/faqs/<source_id>/pairs
[
  {
    "question": "<canonical question — include alternate phrasings>",
    "answer": "<concise answer, 2-4 sentences>"
  },
  ...
]
```

#### Markdown / plain text → rich-text source

```
POST /knowledge-bases/<kb_id>/rich-text
{
  "name": "<Source label>",
  "content": "<markdown body>"
}
```

#### CSV → table source

If the user gave a CSV file path, parse it first:

```
POST /knowledge-bases/<kb_id>/tables/parse-csv
<multipart upload with the CSV file>
```

Returns the parsed headers and rows.

Then create the table source:

```
POST /knowledge-bases/<kb_id>/tables
{
  "name": "<Source name, e.g. 'Pricing matrix'>",
  "headers": ["<col1>", "<col2>", ...],
  "table_data": [
    ["<row1col1>", "<row1col2>", ...],
    ...
  ]
}
```

### Step 2 — Verify the KB

```
GET /knowledge-bases/<kb_id>/stats
```

Returns document count, source count, total bytes, and ingestion status.

```
GET /knowledge-bases/<kb_id>/sources
```

Lists all sources with their state (`ready`, `processing`, `failed`).

Wait until all sources are `ready` before attaching to an agent.

### Step 3 — Attach to agent(s)

For each agent:

```
PATCH /agents/<agent_id>
{
  "enable_collections_search": true,
  "knowledge_base_ids": ["<kb_id>"],
  "tools_enabled": ["end_call", "book_appointment", "check_availability", "collect_contact", "search_knowledge_base"]
}
```

(Preserve whatever else was in `tools_enabled` — just add `search_knowledge_base` if it's not already there.)

### Step 4 — Update the agent's prompt to use the KB

In the agent's `## Tools` section, the prompt must mention `search_knowledge_base` so the model knows when to call it. If missing, PATCH the system_prompt to add this entry:

```
- **search_knowledge_base**: For specific technical questions, regulatory details, pricing matrices, or anything this prompt doesn't directly answer. Pass the caller's question as the search query.
```

Also tighten in-prompt objection responses for topics the KB covers, so the model is nudged toward KB usage on follow-ups. Long in-prompt answers crowd out KB calls.

### Step 5 — Test with a call

The user should run a test call asking a deep technical question only the KB would know. Check the transcript for a `search_knowledge_base` tool call. If the agent answers from prompt content instead, the prompt's objection responses for that topic are too detailed; trim them.

### Step 6 — Report back

```
✓ Knowledge base "<KB Name>" ready
  KB id: <kb_id>
  Sources: <count> (<url_count> URLs, <faq_count> FAQ sets, <table_count> tables, <rich_text_count> rich texts)
  Total Q&A pairs: <pairs>
  Status: all sources ready

Attached to:
  <count> agents — search_knowledge_base tool enabled on each
```

## Gotchas

- **Web crawls take time.** Source state is `processing` until done. Don't attach to an agent until `ready`, or the agent will get empty results.
- **`gemini_voice` defaults can cause confusion.** Unrelated, but a reminder to verify with explicit fields per the prospect-demo gotchas.
- **FAQ generation is AI-driven and lossy.** If the source content is critical (legal text, exact pricing), hand-curate pairs instead of using `/generate`.
- **CSV with many rows can be slow to ingest.** Split very large product catalogs (5000+ rows) into themed sub-tables.
- **The `search_knowledge_base` tool is provider-agnostic.** All four voice providers (ElevenLabs, OpenAI, Gemini, Grok) can call it. The KB runs on xAI Search regardless of voice provider.
- **Don't list every URL on a site as a separate web crawler.** One root URL with the platform's auto-crawl is enough. Save sources for genuinely different docs.

## Rule capture

<!-- Append new rules here. -->
