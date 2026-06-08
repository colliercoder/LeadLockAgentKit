# Template: Privacy Policy & Terms - Required SMS Language

Reviewers visit your Privacy Policy and Terms URLs and check for specific language. Missing it gets you rejected even if everything else is perfect. Add the blocks below to your live pages **before** you submit.

> Both pages must be **publicly accessible** (not behind a login) and live at the exact URL you enter. See `../reference/consent-and-cta.md`.

---

## Privacy Policy - required mobile-data clause

Your privacy policy **must** explicitly state that mobile/SMS data is not shared with third parties for marketing. Add this (or equivalent):

```
Mobile Information & SMS: No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Text-messaging opt-in data and consent will not be shared with any third parties. {{brand_name}} uses your mobile number solely to send the messages you opted in to receive. You may opt out at any time by replying STOP.
```

**Critical:** if your privacy policy says anywhere that you share, sell, or disclose consumer data to third parties (even in an unrelated section), reviewers may flag the whole policy as non-compliant. The SMS carve-out above must be unambiguous.

---

## Terms of Service - required SMS section

Your Terms must cover opt-out, frequency, rates, and support. Add:

```
SMS Terms: By opting in, you agree to receive {{message_type}} text messages from {{brand_name}}. Message frequency varies (typically {{frequency}} per month). Message and data rates may apply. Reply STOP to any message to unsubscribe, or HELP for help. For support, contact {{support_email}}. Carriers are not liable for delayed or undelivered messages. Consent is not a condition of purchase.
```

---

## Footer links (put these on your landing page)

The opt-in page and your homepage footer should both link to all three:

```
Privacy Policy  ·  Terms of Service  ·  SMS Terms
{{website}}/privacy   {{website}}/terms   {{website}}/sms-terms
```

A missing footer link to Privacy/Terms was one of the original rejection causes. Make all three visible from the page that hosts the opt-in form.

## Placeholder key

| Placeholder | Example |
|---|---|
| `{{brand_name}}` | Acme Co |
| `{{website}}` | https://www.acme.com |
| `{{message_type}}` | marketing |
| `{{frequency}}` | 1-4 messages |
| `{{support_email}}` | support@acme.com |
