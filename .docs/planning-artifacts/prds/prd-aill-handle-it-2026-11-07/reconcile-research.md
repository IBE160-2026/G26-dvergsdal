# Reconciliation: research.md against the PRD

- **Input:** `.docs/planning-artifacts/research/user-voice-wedding-website-pre-prd-2026-11-06/research.md` (user-voice, competitive, domain and technical research, 2026-11-06)
- **Checked against:** `prd.md`, `addendum.md` and `.memlog.md` in this folder. `pre-prd-discovery.md` was read only to resolve the C, D and Q IDs that the PRD cites.
- **Date:** 2026-11-07

**Result:** 18 gaps (0 high, 7 medium, 11 low), 1 contradiction without a record, 25 deliberate changes accounted for, and 23 items for architecture or UX.

The PRD carries most of the research well. These all trace cleanly to [R x.y]:

- consent separated from the RSVP (FR-26 to FR-30)
- answers per person per day (FR-14 to FR-17)
- the check page and receipt (FR-21, FR-23)
- the link handled as a secret (FR-3, FR-4, NFR-4)
- WCAG 2.2 AA (NFR-5)
- clone-and-run (NFR-8)
- EU storage (NFR-3)

The gaps cluster in three places:

- what the guest sees about payment and about sending
- the edges of the consent record
- readability for older guests

## 1. Gaps

### Medium

**G1. The status page does not show the guest's payment status**
- **Research:** Recommendation 4 [R 6] says the receipt or status page that the link always opens should show the amount, payment reference, account or Vipps number, *payment status* and deadline. In Tito, "Mark as paid" confirms the payment to the buyer and closes the payment link [R 1.7].
- **PRD:** FR-2 says a link opens the household's "payment status". FR-24 (what the link always opens after the household has answered) lists the answers, who last updated them and when, the total, how to pay and the deadline, but not the payment status.
  - FR-35 shows an "I have paid" report only to the couple, and FR-36 covers only a total that changes.
  - Nothing says what the guest sees after tapping "I have paid", or after the couple registers the money (FR-59, FR-60).
  - FR-24 ("the link always opens its status") also conflicts with FR-7 and FR-37, where the link opens the invitation with a "See or change answer" button.
- **Severity:** medium. The guest cannot tell whether the money arrived. That feeds CM-3 (payment mismatches) and the chasing the product is meant to remove.
- **Fix:**
  - Add payment status to FR-24, in guest wording based on FR-60: not paid; part paid, X kr left; paid; the couple owes you X kr.
  - Until the couple registers the money, show the pending "I have paid" report with its date.
  - When the household has paid in full, replace the "Pay now" details with a confirmation.
  - State where the status appears after answering, for example at the top of the front page.

**G2. The check page does not say that the answer is not sent yet**
- **Research:** Baymard: some users confuse the review page with the confirmation page. GOV.UK "Check answers": say that nothing is complete until the user confirms, and name the button after the action [R 1.7]. Older users miss vague messages and blame themselves [R 2.2].
- **PRD:** FR-21 lists what the check page contains: answers per person, the total, "Change" links and "Not provided". It does not say that the answer is not sent yet, and it does not name the button after the action. FR-20 only warns when the guest leaves the form, and phone browsers often show no warning when a tab or app is just closed.
- **Severity:** medium. If an older guest takes the check page for the receipt and closes it, the household shows as "not answered" while the guest believes they have answered.
- **Fix:** Add to FR-21: "The check page says clearly that the answer is not sent until the guest presses the send button. The button is named after the action, for example 'Send answer'."

**G3. Withdrawn allergy information can survive in the change history**
- **Research:** Consent can be withdrawn in the same place it was given, and the data is then deleted (EDPB paras 113–117). Storage must be limited in time (Art. 5(1)(e)) [R 3.2].
- **PRD:** FR-30 deletes the person's allergy information. But FR-40 keeps "the full history of each household's changes (who changed what, and when)", and the addendum asks for a data model that supports this history from the start. If the history stores the old values, withdrawn health data stays in it. FR-67 deletes "all guest data" but does not name the history, consent records, notes or questions.
- **Severity:** medium. FR-40 is marked [2027], but the data model is designed now.
- **Fix:**
  - FR-40: "The history records that allergy information changed, but never stores the allergy values." Alternatively, FR-30: withdrawal also removes the values from the history.
  - FR-67: name the history, consent records, contact notes and guest questions as part of "all guest data".

**G4. Consent registered by the couple is neither informed nor tied to a text version**
- **Research:** Explicit consent must be informed. The person must be told about withdrawal before consenting (EDPB para 116). The record must show how and when consent was given and which text was shown (para 108) [R 3.2].
- **PRD:** FR-31 records only which admin registered the allergy and when.
  - Nothing requires the couple to tell the guest what FR-26 tells guests online: the purpose, who can see the information, that it goes to Hardingasete's kitchen, and that consent can be withdrawn through the link.
  - FR-29 stores "which version of the consent text was shown", but there is no equivalent for consent given by phone.
  - UJ-3 shows that this path serves the guests who are least likely to read the site themselves.
- **Severity:** medium.
- **Fix:** FR-31: "The admin form shows the FR-26 consent text for the couple to read out or send. The couple confirms that the guest was told it. The record stores the method (phone or message), the time, the admin and the text version."

**G5. The PRD does not say that consent is per person**
- **Research:** Recommendation 1 [R 6] asks for "its own unticked Yes/No consent per person". [R 5] insight 2 says consent should be "formulated and stored per person". Consent is the data subject's own statement [R 3.2].
- **PRD:** FR-26 has one consent choice, given by "the respondent", and FR-29 stores "who gave it". FR-30 assumes that consent is withdrawn per person ("deletes that person's allergy information"). But FR-26, FR-27 and FR-29 never say that the consent or the confirmation is recorded per person, so a single yes/no for the whole household would also fit the text.
- **Severity:** medium. This decides how the consent record is shaped in the data model.
- **Fix:** FR-26 and FR-29: "The consent (for the respondent) or the FR-27 confirmation (for others) is given and recorded per person whose allergy information is saved, with the time, the respondent and the text version."

**G6. Text on guest pages is not required to be large by default**
- **Research:** NN/g found that small text and buttons cause errors for users aged 65 and over [R 2.2]. Older guests want "large text, a clear way back, and a person to call" [R 2.3]. The brief also asked for "large readable text".
- **PRD:** NFR-5 requires 200 % zoom, touch targets of at least 44 × 44 px, visible focus and labels. NFR-6 says "phone first, for all ages". Nothing requires large body text by default, and relying on 200 % zoom assumes older guests know how to zoom.
- **Severity:** medium. Older guests are the main audience, and SM-3 depends on them.
- **Fix:** NFR-5 or NFR-6: "Guest pages use large, easy-to-read body text by default, so no one needs to zoom. The size is set in the UX spec."

**G7. The PRD does not say exactly when the deadline locks the form**
- **Research:** Joy closes the form automatically at midnight in the event's time zone, and shows the deadline next to the RSVP button [R 1.3].
- **PRD:** FR-41, FR-42 and FR-64 treat the deadline as a date. Nothing says whether the form locks at the start or the end of that day, or in which time zone. Production servers often run on UTC (international standard time, not Norwegian time), and a lock at 00:00 takes away the day guests were told they had.
- **Severity:** medium. It changes what guests see on the busiest day, and it changes the expected results of the deadline tests (UJ-6 step 6).
- **Fix:** FR-42: "Answers lock when the deadline day ends, at 23:59 Norwegian time. Guests can answer and change their answer throughout the deadline day."

### Low

**G8. The PRD does not record the remaining risk of answering for other adults**
- **Research:** No source supports one adult consenting for another adult. The confirmation box is a mitigation with no source behind it, and the remaining risk "must be described honestly" [R 3.2, R 5]. Recommendation 2 [R 6]: "(a) + (c), with the residual risk documented". [R 7] keeps it as an open question for Datatilsynet.
- **PRD:** FR-27 adopts the confirmation without any caveat. NFR-3, section 7 (Assumptions) and section 8 (Open questions) say nothing about the remaining risk. According to C2, it is documented only in the brief.
- **Severity:** low. It can be traced through C2, but the PRD reads as if FR-27 settles the matter.
- **Fix:** Add to section 7: "FR-27 is a practical mitigation, not proven valid consent for another adult. The remaining risk is accepted; see the brief." Optionally, add a question to section 8: ask Datatilsynet's advice line before the invitations go out in 2027.

**G9. The privacy page misses some of the points GDPR Art. 13 requires**
- **Research:** Art. 13 requires the privacy notice to cover:
  - who is responsible
  - the purpose and the legal basis
  - who receives the data
  - any transfer outside the EEA
  - how long the data is kept
  - the guest's rights, including withdrawal and complaints to Datatilsynet
  - whether giving the data is voluntary, and what happens if it is not given

  Hosting and email providers that store the data are processors [R 3.3].
- **PRD:** FR-66 covers what is collected and why, who can see it, the legal basis, deletion, rights and how to contact the couple. It misses four points:
  - that the couple are the ones responsible (the controllers)
  - that hosting and email providers also receive the data
  - that the data stays in the EU/EEA (NFR-3)
  - that allergy information is voluntary, and what happens if it is not given
- **Severity:** low.
- **Fix:** Add the four missing points to FR-66.

**G10. "Ask us" lets health information bypass the consent step**
- **Research:** Allergies are health data, and Datatilsynet reads health data broadly. Such data needs explicit, recorded consent and must be kept to a minimum [R 3.2].
- **PRD:** FR-28 tells guests who don't consent that they "can tell the couple directly". The obvious way to do that on the site is "Ask us". Its questions are always stored (FR-44) and emailed if an email key is set (FR-45), with no consent record and no deletion before 2028.
- **Severity:** low.
- **Fix:** Either change FR-28 to send guests to a phone call or message to the couple, who then use FR-31, or let the couple delete a question once it has been handled and add a short note on the "Ask us" form.

**G11. Religious diets are not treated as sensitive data**
- **Research:** Religious dietary needs may reveal religious belief, which is also sensitive data under Art. 9 [R 3.2].
- **PRD:** NFR-3 treats allergies as health data, and FR-26 requires consent for "allergy information". But FR-25 also collects dietary needs: vegetarian, vegan, "other" and a short note, which is where halal or kosher would be written.
- **Severity:** low.
- **Fix:** In NFR-3 or FR-26, state that the consent covers everything in FR-25 (allergies, dietary needs and the note), and that the consent text says "allergies and dietary needs".

**G12. The "not answered" list has no contact details**
- **Research:** Recommendation 7 [R 6] asks for a "not answered" list with contact details. The couple wants "to see exactly who is missing, with contact details" [R 2.3].
- **PRD:** FR-56 lists households that haven't answered, without contact details. The full overview in FR-57 has phone numbers and email addresses that can be tapped, so the information is one step away.
- **Severity:** low.
- **Fix:** FR-56: each household that hasn't answered shows its members' phone numbers and email addresses (tap to call or write), or links straight to them.

**G13. Admins cannot log out**
- **Research:** OWASP: logging out should end the session on the server [R 4.2].
- **PRD:** FR-46 covers logging in, and NFR-4 ends sessions after a period of inactivity, but there is no way to log out. Helpers can see health data, possibly on shared devices.
- **Severity:** low.
- **Fix:** FR-46 or NFR-4: "Admins can log out, and logging out ends the session on the server."

**G14. The research's warning against strict input formats was dropped**
- **Research:** Recommendation 10 [R 6]: "no time pickers or strict formats". NN/g found that strict formats, such as dates or phone numbers with hyphens, cause errors, and recommends accepting input in several forms [R 2.2].
- **PRD:** FR-18 rules out time pickers. Nothing says the site should accept common ways of writing what is typed into the fields that exist: phone numbers (FR-49), amounts (FR-59), prices and payment details (FR-64).
- **Severity:** low.
- **Fix:** NFR-6: "Fields accept common ways of writing things (spaces, +47, 'kr', thousand separators), and the site tidies them up."

**G15. Payment details are not checked before they are saved**
- **Research:** Norwegian account numbers have 11 digits. Private persons use a free-text message, not a KID reference [R 3.4].
- **PRD:** FR-64 lets the couple change the Vipps number and the account number without any check. One typo would send every guest's payment to the wrong account.
- **Severity:** low.
- **Fix:** FR-64: "Before saving, the site checks that the account number has 11 digits and that the Vipps number has the right format, and shows the details back for confirmation."

**G16. No rule against claims about tax or Vipps**
- **Research:** Recommendation 14 [R 6]: the site should not claim anything about tax or Vipps beyond showing the number or QR code [R 3.4].
- **PRD:** Section 3.4 excludes Vipps payment requests, but nothing limits what the payment text may claim, for example "free with Vipps" or "not taxable".
- **Severity:** low.
- **Fix:** Add a constraint to section 7, or to FR-34: "The payment text shows only the amount, the Vipps number (and QR code, if time), the account number and the message. It makes no claims about fees or tax."

**G17. The legal points are not re-checked before invitations go out**
- **Research:** The research's list of what goes stale [R 9] says that prices, the Vipps terms and the legal points (consent and the household exemption) must be checked again before production in 2027.
- **PRD:** Section 3.2 includes "A fresh check of Vipps terms and prices" but not the legal points that the consent model rests on. Several of them were taken from search excerpts, because datatilsynet.no could not be reached.
- **Severity:** low.
- **Fix:** Add to section 3.2: "Check the consent model and Datatilsynet's guidance again (R 3.1–3.2) before invitations are sent."

**G18. CSV/Excel export is neither planned nor ruled out**
- **Research:** git-hitched and Greenvelope export guest data to CSV or Excel [R 1.4].
- **PRD:** Only the print page is listed, under If time (section 3.3). CSV export appears nowhere, not even as out of scope, although the teacher's feedback on the brief left file export out of v1.
- **Severity:** low.
- **Fix:** Add CSV export either to section 3.3 (If time) or to section 3.4 (Out), with a reason, so the choice is on record.

## 2. Contradictions without a record

**X1. Changing a price after guests have answered changes their total**
- **Research:** Adding costs after guests have answered is seen as improper [R 2.2]. An unexpected change in the total makes users stop recognising their order [R 1.7]. C3 accepted "a total that doesn't change unexpectedly".
- **PRD:** FR-33 always calculates totals from the *current* prices. FR-64 lets the couple change prices after households have answered, and FR-65 warns only the couple. Guests affected see a new total, or "what remains to pay" (FR-36), with no reason given. The memlog records the warning to the couple, but not the trade-off against C3.
- **Severity:** low. Real prices are entered before invitations go out (section 3.2), so this rarely happens.
- **Fix:** Decide and record one of these:
  - each household keeps the prices that applied when it answered, or
  - guests affected see a short explanation on their status page.

  Log the choice in the memlog, and add the option not chosen to Rejected alternatives.

## 3. Deliberate changes (accounted for)

These differ from the research, but the memlog, PRD section 9, the scope lists or the addendum's Rejected alternatives show they were chosen on purpose.

- One personal link per guest, not per household (Rec. 3, [R 5]). Recorded in the memlog, PRD section 9 and Rejected alternatives.
- The last save wins, and the form shows "last updated by X at Y". No version check or conflict message ([R 4.5]). Recorded in C5 and PRD section 3.4 "Conflicts".
- Payment status is calculated from the amounts registered (not paid, part paid, paid, refund owed), instead of two states (Rec. 6, [R 1.7]). Recorded in the memlog, PRD section 9 and Rejected alternatives. Undo is kept in FR-59.
- The guest's "I have paid" report is in v1 instead of optional. Recorded in PRD section 9.
- Helpers can only read, they don't get full access ([R 2.1] limited roles, D13). Recorded in the memlog and PRD section 9.
- No household code in the payment; the message is "Bryllup" plus a name (Rec. 4 "payment reference"). Recorded in D8 and PRD section 3.4 "Payment code".
- No grace period after the deadline ([R 1.3] Joy). Recorded in D5 and PRD section 3.4.
- The site sends no invitations or reminders ([R 1.3] Joy's reminders, [R 2.1] chasing). Recorded in PRD section 3.4 "Sending" and the memlog.
- No summary or change emails to the couple ([R 1.3]). Recorded in PRD sections 3.4 and 9, and Rejected alternatives.
- Link tracking counts only households that have done something, and is If time (Rec. 13, [R 4.1]). Recorded in C4 and PRD section 3.3.
- Guests' phone numbers and email addresses are stored, despite the data-minimisation advice ([R 3.2], Art. 5(1)(c)). Recorded in the memlog, PRD section 9 and Rejected alternatives.
- Guests cannot get a lost link sent to themselves ([R 2.2] lost links). Recorded in PRD section 3.4, Rejected alternatives and the memlog.
- Allergies for other adults are handled by the respondent's confirmation plus fixed categories (options a + c), not by each adult confirming their own (option b) (Rec. 2). Recorded in C2 and FR-27. The note about the remaining risk is G8.
- No import of the guest list ([R 1.4] CSV import). Recorded in Rejected alternatives.
- The print page for Hardingasete is If time, not v1 ([R 1.4]). Recorded in PRD section 3.3. CSV export itself is not recorded; see G18.
- No online payment and no Vipps payment requests ([R 1.5] Stripe; Rec. 14, [R 3.4]). Recorded in PRD section 3.4 "Payment".
- Speech sign-up is If time, and only the toastmaster sees it ([R 1.6]). Recorded in PRD section 3.3.
- The envelope animation is If time, can be skipped and respects "reduce motion" ([R 2.2]: no evidence on how older guests react). Recorded in PRD section 3.3 and the memlog.
- The English version with a language button is If time ([R 2.2]). Recorded in PRD section 3.3.
- Saving an unfinished answer is If time; v1 warns before leaving. Recorded in the memlog and Rejected alternatives. In addendum.md, that table row has ended up below the "Test data note" section.
- The form asks per event only about days, meals, overnight stay and the hike; the activities are information only ([R 1.2] multi-event). Recorded in Q6 and PRD section 3.4.
- No children and no child prices ([R 1.4] adult/child counts). Recorded in PRD section 3.4 "Children".
- The form uses fewer, task-sized steps instead of strictly one question per page ([R 2.2] GOV.UK). Recorded in D9, cited in FR-13.
- Guests pay the couple rather than a third party such as Hardingasete ([R 2.2]). Kept open as Q4 (PRD sections 7–8).
- Paper or phone for the oldest guests ([R 2.2] hybrid). The phone route is covered by FR-63 and UJ-3. The assumptions in section 7 say links are sent digitally, and the pre-PRD discovery (section 5) leaves a paper card outside the site.

## 4. Items that belong in architecture or UX rather than the PRD

### Architecture (bmad-architecture)

| # | Item | Research | Does the addendum point to it? |
|---|---|---|---|
| A1 | Link codes come from a cryptographically secure random generator, with at least 128 bits (OWASP prefers 160+), are short and safe in links (NFR-1), and are stored hashed or plain (D14) | [R 4.1] | Yes (D14) |
| A2 | Keep link codes out of server and proxy logs, analytics and error reports | [R 4.1] | No; add to the D14 note |
| A3 | Guest pages send `Referrer-Policy: no-referrer` and say noindex in a meta tag or header, because Meta may bypass robots.txt and Slack ignores it; `<title>` and `og:` tags are generic | [R 4.1] | Indirectly (NFR-4 and FR-4 cite [R 4.1]) |
| A4 | Every change goes through a POST (FR-3). That includes "pressed Start" for link tracking (If time) and the envelope's "first visit" (section 3.3). "First visit" must be remembered on the device or after a guest action, because chat apps and email scanners often open the link before the guest does | [R 4.1] | No; add a note on the envelope and link tracking |
| A5 | Rate limiting slows down wrong links (NFR-4) but must never block a valid link (NFR-1). Mobile networks share IP addresses between many users, and Zola's lockout is a cited failure | [R 4.1], [R 1.1] | No |
| A6 | Admin login: Argon2id settings, HttpOnly, Secure and SameSite cookies, a new session ID at login, 15–30 minutes' idle timeout, logout that ends the session on the server (G13), the framework's CSRF protection, about 5 login attempts per minute | [R 4.2] | Yes |
| A7 | Data model: attendance per person per day, with a "not answered" state (git-hitched's Event/RSVP pattern, not one true/false field per event); options stored on the person, not as separate rows (the Eventbrite mistake); whole kroner; totals and statuses calculated; consent records per person with the text version (G5) | [R 1.2], [R 1.5], [R 1.7], [R 3.2] | Partly (calculated values, room for history); no pointer to [R 1.2] or [R 1.7] |
| A8 | Check the deadline in Norwegian time (Europe/Oslo), whatever time zone the server uses (G7) | [R 1.3] | No |
| A9 | SQLite and a separate seeding step. If Django is chosen, its built-in admin is an internal tool, not the couple's overview. Laravel needs PHP, Composer and npm, which affects the 15–20 minutes in SM-5 | [R 4.4] | Yes (D15) |
| A10 | Email: console output or Mailpit locally. The production provider must *store* data in the EU; Resend keeps account data and logs in the US | [R 4.3] | Partly (PRD D16 and section 3.2); no pointer to [R 4.3] |
| A11 | Hosting in 2027: free plans that sleep (Render's web services after 15 minutes) or expire (Render's free Postgres after 30 days) would break NFR-1 | [R 4.6] | No |
| A12 | Roles: FR-46 has two roles, but the speech sign-up (If time) is for the toastmaster only, and in the research example the couple can't see it. Leave room for visibility per feature | [R 1.6] | No (only "Two admin roles") |
| A13 | Daily backups (NFR-1) keep withdrawn allergy information. Set how long backups are kept, and include them in the deletion by 31 August 2028 | [R 3.2], Art. 5(1)(e) | No |
| A14 | Version check on saving (optimistic locking) was not adopted (C5); `updated_at` is enough for the display in FR-38 | [R 4.5] | Not needed |

### UX (bmad-ux)

| # | Item | Research |
|---|---|---|
| U1 | Check page: a title that says what to do, "Change" links with hidden text for screen readers, and a button named after the action (the PRD part is G2) | [R 1.7] |
| U2 | Error summary: shown only after an attempt to continue, focus moves to it, and it links to each field. Designsystemet's standard heading, "For å gå videre må du rette opp følgende feil.", is formal; reconcile it with the warm tone in NFR-6 | [R 3.5] |
| U3 | Receipt: what was received, what happens next and when, and that the link is the guest's record to bookmark | [R 1.7], [R 2.2] |
| U4 | Exact text size and spacing for older guests (after G6); check sage green on soft white at 4.5:1 contrast | [R 2.2], [R 3.5] |
| U5 | Practical details first, for the half of guests who only want those: times, address, parking, dress code, what to bring | [R 2.2], [R 2.3] |
| U6 | Wording about money (Q7): a friendly reason, optional choices priced up front, and who the guest pays, all shown before they commit | [R 2.2], [R 2.3] |
| U7 | Language button (English, If time): easy to see, with text rather than flags | [R 2.2] |
| U8 | Envelope animation (If time): try it with an older relative before keeping it | [R 2.2], [R 7] |
| U9 | Payment details: the account number grouped so it is easy to read, the Vipps number, and the exact message text; no claims about fees or tax (G16) | [R 3.4] |
