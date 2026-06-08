# Playbook: Rejection Recovery

You got rejected. Find your error code, apply the fix, **edit the existing campaign** (do not delete and recreate - recreating triggers a fresh vetting fee), and resubmit.

The one exception: **30897 (disallowed content) cannot be resubmitted.** The content itself is prohibited; you must change what you send, not how you describe it.

Full code reference: `../reference/error-codes.md`. This file is the fast triage + the lessons from a campaign that was rejected three times before approval.

---

## Triage table

| Error | Means | Fix |
|---|---|---|
| **30886** | Invalid campaign description | Description mixes message types or is too vague. For Marketing, write "marketing messages only" and enumerate what is NOT sent. Use `../templates/campaign-description.md`. |
| **30887** | Opt-out error | Add/clarify STOP handling and opt-out confirmation. `../templates/keywords-and-autoreplies.md`. |
| **30888** | Age gate not present/acceptable | Only if you have age-gated content; add a real DOB age gate or remove the attribute. |
| **30889** | Embedded phone number | A sample contains a phone number but the attribute wasn't set (or vice versa). Align the checkbox with the samples. |
| **30890** | Subscriber help | Add proper HELP keyword + help response. |
| **30891** | Invalid / unreachable website | URL typo or site not public. **Proofread the URL field** (Twilio doesn't validate it), make the site live and login-free. |
| **30892** | Invalid sample / URL shortener | Remove bit.ly/tinyurl; use full-domain URLs you own. |
| **30893** | Sample ↔ use-case mismatch | Samples don't match the registered use case. Either fix the samples or change the use case. |
| **30894** | Invalid brand info | Brand data problem; see brand section below. |
| **30895** | Direct lending / content mismatch | Lending content without the right attributes, or attributes without matching content. |
| **30896** | Opt-in / consent error | The big one. Checkbox must be unchecked + optional; consent flow must be fully described and publicly verifiable. `../templates/consent-flow.md`. |
| **30897** | Disallowed content | **Cannot resubmit.** Content violates SHAFT/restricted rules. `../reference/prohibited-content-shaft.md`. |
| **30898** | Excessive EIN | Too many brands/campaigns under one EIN, or duplicate. Consolidate. |
| **30909** | Message flow / CTA incomplete | Consent description doesn't fully document the opt-in. Expand it with every required disclosure. `../templates/consent-flow.md`. |
| **30910** | Not in English | Submit registration fields in English. |

### Brand-level failures

| Error | Means | Fix |
|---|---|---|
| **30703** | Duplicate record | A brand with this EIN already exists. Use the existing one. |
| **30795** | Tax ID mismatch | EIN doesn't match IRS records. Verify against your CP-575/147c; if recently issued, the EIN may not have propagated (allow 30-90 days). |
| **18011** | Business name mismatch | Legal name doesn't match IRS exactly. Copy it character-for-character from the IRS letter. |

---

## The real rejection history (learn from these three)

This skill's templates exist because a Marketing campaign was rejected three times. Each one teaches a reusable lesson:

### Rejection 1 - 30896 (Opt-in Error)
**What was wrong:** the consent checkbox was **required** to submit the form (violated the "must be optional" rule), the landing page had **no Privacy/Terms links** in the footer, and there was no public proof of the opt-in flow.
**Fix:** made the checkbox truly optional and prefixed its label with "(Optional)"; added a compliance footer linking Privacy, Terms, and SMS Terms; published a public `/sms-terms` page with a **screenshot of the opt-in step** so reviewers could verify without filling out the form.
**Lesson:** the reviewer must be able to *see* your unchecked, optional checkbox on a public page. Give them a screenshot page.

### Rejection 2 - 30886 (Invalid Campaign Description)
**What was wrong:** the Marketing description listed "follow-up messages after demo requests" and "appointment booking links" - the reviewer read those as **transactional**, which a Marketing use case doesn't permit.
**Fix:** rewrote the description to (a) state **"marketing messages only"** and (b) **enumerate what is NOT sent** (no reminders, confirmations, alerts).
**Lesson:** Marketing means marketing. If your description hints at transactional content, either purge it from the description or switch to a Mixed use case.

### Rejection 2 (same round) - 30891 (Unverifiable Website)
**What was wrong:** the Website field had a typo: `https://https//brand.ai` (double "https", missing colon). Twilio's console does not validate the URL format on submit, so it sailed through to the reviewer and failed.
**Fix:** corrected to the canonical `https://www.brand.ai` (chosen over the bare domain to skip a 301 redirect).
**Lesson:** **proofread every URL field by hand.** Prefer the canonical `www` form that returns 200 directly with no redirect.

---

## After you fix it

1. **Edit** the rejected campaign in place (don't recreate).
2. Re-run `../pre-submission-checklist.md` end to end.
3. Resubmit. If it's a brand issue, the brand must clear before the campaign can.
