# Template: Campaign Description

This is the field Twilio reviewers read first. It is a **compliance document, not a marketing pitch.** It must answer WHO sends, WHO receives, and WHY - in plain, specific language.

Replace every `{{placeholder}}`. Keep the structure; it is the version that passed after a 30886 rejection.

> Twilio limit: 40–4096 characters. See `../reference/campaign-registration-fields.md`.

---

## Marketing use case (promotional content ONLY)

Use this only if **every** message from this number is promotional. If you also send reminders/confirmations/alerts, use the Mixed version below instead.

```
This campaign sends marketing messages only. {{brand_name}} ({{legal_entity}}) sends promotional SMS to contacts who have explicitly opted in via an unchecked, optional consent checkbox on the {{where_optin_lives}} at {{website}}. The checkbox is not pre-selected and is not required to complete the form - users may proceed whether or not they opt in, and users who do not check the box receive no SMS. All messages sent through this campaign are marketing/promotional in nature: advertisements describing {{brand_name}}'s {{product_or_service}}, new-feature announcements, special offers, and promotional invitations. This campaign does NOT send transactional notifications, account alerts, appointment reminders, order confirmations, or customer-service messages. Message frequency varies, typically {{frequency}} messages per month. The complete opt-in flow - including a screenshot of the consent step, disclosure language, and opt-out instructions - is publicly documented at {{website}}/sms-terms. Privacy Policy and Terms of Service are linked in the footer of {{website}} and include all required SMS disclosures.
```

**Why this passed:** the original rejected version listed "follow-up messages after demo requests" and "appointment booking links," which the reviewer read as non-marketing → 30886. The fix is two explicit moves: (a) state **"marketing messages only,"** and (b) **enumerate what is NOT sent.** Keep both.

---

## Mixed / Low Volume Mixed use case (promotional + transactional)

Use this if you send a blend (e.g. promotions AND appointment reminders). It removes the self-contradiction that sinks a Marketing registration.

```
{{brand_name}} ({{legal_entity}}) sends a mix of marketing and transactional SMS to contacts who have explicitly opted in via an unchecked, optional consent checkbox on the {{where_optin_lives}} at {{website}}. The checkbox is not pre-selected and is not required to submit the form. Marketing messages include promotional offers and announcements about {{product_or_service}}. Transactional messages include appointment reminders, confirmations, and follow-ups related to services the contact requested. Message frequency varies, typically {{frequency}} per month. The full opt-in flow, including a screenshot of the consent step and opt-out instructions, is documented at {{website}}/sms-terms. Privacy Policy and Terms of Service are linked in the footer of {{website}}.
```

---

## Placeholder key

| Placeholder | Example |
|---|---|
| `{{brand_name}}` | Acme Co |
| `{{legal_entity}}` | a service of Acme Holdings Inc |
| `{{website}}` | https://www.acme.com |
| `{{where_optin_lives}}` | contact form / step 3 of the booking survey / footer signup |
| `{{product_or_service}}` | AI scheduling services |
| `{{frequency}}` | 1-4 |

Proofread the `{{website}}` value. A typo here caused a 30891 rejection (`https://https//...`). Twilio does not validate the URL on submit.
