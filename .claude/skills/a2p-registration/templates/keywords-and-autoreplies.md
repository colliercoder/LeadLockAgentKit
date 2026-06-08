# Template: Keywords & Auto-Reply Messages

Carriers (CTIA) require you to honor **STOP**, **HELP**, and **START** and to send the right confirmation replies. Fill these in the campaign registration exactly.

> Confirmation messages: 20–320 characters each. Keyword fields: 255 alphanumeric chars max. See `../reference/campaign-registration-fields.md`.

Replace every `{{placeholder}}`.

---

## Opt-In Keywords
```
START, SUBSCRIBE, YES
```

## Opt-In Confirmation Message (auto-reply when someone opts in)
```
{{brand_name}}: You are now opted in to receive {{message_type}} messages about {{topic}}. Msg frequency varies. Msg & data rates apply. Reply HELP for help, STOP to opt out.
```

---

## Opt-Out Keywords
```
STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, QUIT
```

## Opt-Out Confirmation Message
```
You have been unsubscribed from {{brand_name}} messages and will receive no further texts. Reply START to re-subscribe.
```

---

## Help Keywords
```
HELP, INFO
```

## Help Response Message
```
{{brand_name}}: For support visit {{website}}/support or email {{support_email}}. Msg & data rates may apply. To opt out, reply STOP.
```

---

## Message content attributes (checkboxes)

Check **only** what is truthfully in your messages:

- [ ] Messages include embedded links - *check this if any sample has a URL (most do)*
- [ ] Messages include embedded phone numbers - *check only if you put a phone number in the text*
- [ ] Messages include age-gated content - *almost always NO*
- [ ] Direct lending or loan arrangement - *NO unless you are a lender; this triggers extra scrutiny (30895)*
- [ ] Affiliate marketing - *NO unless applicable*

## Placeholder key

| Placeholder | Example |
|---|---|
| `{{brand_name}}` | Acme Co |
| `{{message_type}}` | marketing |
| `{{topic}}` | AI scheduling services |
| `{{website}}` | https://www.acme.com |
| `{{support_email}}` | support@acme.com |
