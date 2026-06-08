# Template: Consent Flow ("How do end users consent to receive messages?")

This is the **most scrutinized field** in the whole registration. A weak answer here is the #1 cause of rejection (30896 / 30909). It must describe exactly where opt-in happens, what the checkbox says, that it is unchecked and optional, and what confirmation the user gets.

> Twilio limit: 40–2048 characters. See `../reference/consent-and-cta.md` for the full rules.

Replace every `{{placeholder}}`. This is the approved version (it passed after a 30896 rejection).

---

```
End users opt in to receive messages from {{brand_name}} by completing a consent form on {{where_optin_lives}} at {{website}}. The form includes an unchecked, optional checkbox that reads: '(Optional) I consent to receive {{message_type}} text messages from {{brand_name}} about {{topic}}. Message frequency varies. Message & data rates may apply. Reply HELP for help, STOP to opt out. Consent is not required to {{use_the_service}}. See our Privacy Policy and Terms of Service.' The checkbox is not pre-selected and is NOT required to complete the form submission - users may proceed whether or not they check the box. Users who do not check the box will not receive any SMS messages. A complete description of the opt-in flow, including a screenshot of the consent step, is publicly available at {{website}}/sms-terms. Privacy Policy and Terms of Service are linked in the site footer. After opting in, users receive a confirmation message identifying the brand, message frequency, data-rates disclosure, and opt-out instructions. Users can opt out at any time by replying STOP. Users may also text START to opt in.
```

---

## The checkbox itself (build this on your site before you submit)

The reviewer will visit `{{website}}` and try to find this. It must actually exist, and it must:

- Be **unchecked by default**
- Be **optional** - the form submits whether or not it is checked
- Have a label that **starts with "(Optional)"** and includes the words **"Consent is not required to {{use_the_service}}"**
- Contain: brand name, frequency, "Message & data rates may apply", STOP, HELP, a link to Privacy Policy, a link to Terms

Exact label text to put on the page:

```
(Optional) I consent to receive {{message_type}} text messages from {{brand_name}} about {{topic}}. Message frequency varies. Message & data rates may apply. Reply HELP for help, STOP to opt out. Consent is not required to {{use_the_service}}. See our Privacy Policy and Terms of Service.
```

## The /sms-terms proof page (strongly recommended)

The single highest-leverage move for one-shot approval: publish a public page at `{{website}}/sms-terms` with a **screenshot of the actual opt-in checkbox**, the disclosure language, and opt-out instructions. It lets the reviewer verify your flow without filling out your form, and it is what turned a repeat-rejection into an approval. Link it (plus Privacy and Terms) in your site footer.

## Placeholder key

| Placeholder | Example |
|---|---|
| `{{brand_name}}` | Acme Co |
| `{{website}}` | https://www.acme.com |
| `{{where_optin_lives}}` | the contact form / step 3 of the booking survey |
| `{{message_type}}` | marketing |
| `{{topic}}` | scheduling services |
| `{{use_the_service}}` | use the site / book a demo / get a quote |
