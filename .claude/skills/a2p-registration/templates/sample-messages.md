# Template: Sample Messages

Twilio requires **2-5** sample messages. They must match your use case, include your brand name in at least one, use `[Brackets]` for dynamic fields, include opt-out language in at least one, and use **full-domain URLs** (never bit.ly / tinyurl → instant 30892).

> Per-sample limit: 20–1024 characters. See `../reference/campaign-registration-fields.md`.

Replace every `{{placeholder}}`. These five are the approved Marketing set, genericized.

---

### Sample 1
```
Hi [First Name], this is {{sender_name}} from {{brand_name}}. We help businesses like yours with {{value_prop}}. Would you be open to a quick call this week? Book here: {{booking_link}} Reply STOP to opt out.
```

### Sample 2
```
{{brand_name}}: Hey [First Name], just following up. {{social_proof_line}}. Want to see a quick demo? {{website}} Msg & data rates apply. Reply STOP to unsubscribe.
```

### Sample 3
```
[First Name], we noticed your business could benefit from {{value_prop}}. {{brand_name}} clients are seeing {{result_metric}}. Interested? Reply YES or book a call: {{booking_link}} Reply STOP to opt out.
```

### Sample 4
```
Hi [First Name], last message from {{brand_name}}. If {{product_or_service}} isn't a priority right now, no worries. But if you'd like to see how it works: {{website}} Reply STOP to opt out.
```

### Sample 5
```
{{brand_name}}: Hey [First Name], {{sender_name}} here. We just launched {{new_thing}} for businesses like yours. Would that be useful? Reply YES to learn more or STOP to opt out.
```

---

## Rules these samples follow (don't break them)

- **Brand name present** in samples 1, 2, 3, 4, 5 (every one - at minimum one is required, more is safer).
- **STOP / opt-out** language in all five (at minimum one is required).
- **`[First Name]`** brackets show reviewers these are templated, not spam.
- **Full URLs only.** If you must shorten, use a **branded** short domain you own, never a public shortener.
- **Match the use case.** These are promotional → Marketing. If you registered Mixed, add one transactional sample (e.g. a reminder) so the set reflects the blend.
- **No SHAFT / restricted content.** See `../reference/prohibited-content-shaft.md`.

## Placeholder key

| Placeholder | Example |
|---|---|
| `{{sender_name}}` | Dan |
| `{{brand_name}}` | Acme Co |
| `{{value_prop}}` | automated appointment setting |
| `{{social_proof_line}}` | Our clients book 3x more appointments |
| `{{result_metric}}` | a 40% increase in booked appointments |
| `{{booking_link}}` | https://book.acme.com/intro (full domain, yours) |
| `{{website}}` | https://www.acme.com |
| `{{product_or_service}}` | AI appointment setting |
| `{{new_thing}}` | a 24/7 AI voice agent |
