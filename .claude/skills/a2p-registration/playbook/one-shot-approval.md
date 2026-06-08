# Playbook: One-Shot Approval

The field-by-field walkthrough for getting approved on the **first** submission. Work top to bottom. Each step links the reference or template that fills it.

The goal is zero rejections, because each rejection costs a vetting fee and 1-2 weeks. Everything below is preventable.

---

## Before you touch the Console

- [ ] **Decide the use case honestly.** List every kind of message you send from this number. Only promotional → Marketing. Any transactional mixed in → Mixed / Low Volume Mixed. (`../reference/campaign-use-cases.md`)
- [ ] **Build the opt-in checkbox** on your site: unchecked, optional, full disclosure language. (`../templates/consent-flow.md`)
- [ ] **Publish `/sms-terms`** with a screenshot of that checkbox. (`../templates/consent-flow.md`)
- [ ] **Add the SMS clauses** to your live Privacy Policy and Terms. (`../templates/privacy-policy-clause.md`)
- [ ] **Add footer links** to Privacy / Terms / SMS Terms on the page hosting the opt-in.

If any of those five aren't done, stop and do them. They are exactly what reviewers check, and skipping them is what causes the common rejections.

---

## Phase 1 - Customer Profile (business identity)

1. **Legal business name** - copy it **exactly** from your IRS CP-575 or 147c letter. Punctuation and "Inc/LLC" must match. (`../reference/brand-registration.md`)
2. **EIN / Tax ID** - exact match to IRS. Mismatch is the #1 brand failure (30795 / 18011).
3. **Business type** - LLC / Corporation / Sole Proprietor / Non-Profit / Government.
4. **Address** - registered business address on file with the IRS.
5. **Authorized representative** - a real person with a real business email.
6. **Website** - live, public, matches your brand.
7. Submit. Wait for the profile to verify.

## Phase 2 - Brand Registration

1. Choose **Standard** (have EIN) or **Sole Proprietor** (no EIN, lower throughput).
2. Submit the brand. Vetting runs in the background (days).
3. Optionally pay for **secondary vetting** to raise your trust score and throughput. Worth it if you send volume. (`../reference/throughput-and-trust-scores.md`)
4. If it fails → `rejection-recovery.md` brand section. It is almost always name/EIN/address.

## Phase 3 - Campaign Registration

Fill each field from the matching template:

1. **Use case** → the one you decided above.
2. **Campaign description** → `../templates/campaign-description.md`
   - State the message type explicitly. For Marketing, say "marketing messages only" and enumerate what is NOT sent.
3. **Sample messages (2-5)** → `../templates/sample-messages.md`
   - Brand name in at least one, STOP in at least one, full-domain URLs, `[brackets]` for variables.
4. **Message flow / "how do users consent?"** → `../templates/consent-flow.md`
   - The most scrutinized field. Describe the unchecked optional checkbox, the disclosure text, the confirmation reply, and link `/sms-terms`.
5. **Content attributes** → check only what's true. Links: usually yes. Phone numbers / age-gated / lending: usually no. (`../templates/keywords-and-autoreplies.md`)
6. **Opt-in keywords + confirmation** → `../templates/keywords-and-autoreplies.md`
7. **Opt-out keywords + confirmation** → same file.
8. **Help keywords + response** → same file.
9. **Privacy Policy URL** → must be live with the mobile-data clause. **Proofread the URL.** (30891)
10. **Terms URL** → must be live with the SMS section.

## Final gate

Run **every** item in `../pre-submission-checklist.md`. Then submit.

---

## The three things that decide it

If you do nothing else, get these right - they account for nearly every rejection:

1. **Use case matches your actual messages** (no transactional content in a Marketing campaign).
2. **Opt-in checkbox is unchecked + optional**, and the reviewer can verify it on a public page.
3. **Every URL is live and typo-free** (website, privacy, terms).
