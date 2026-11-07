# Reconciliation: pre-PRD discovery vs PRD

- **Input checked:** `../../research/user-voice-wedding-website-pre-prd-2026-11-06/pre-prd-discovery.md` (updated 2026-11-07)
- **Checked against:** `prd.md`, `addendum.md` and `.memlog.md` in this folder. The brief was read only where pre-prd-discovery.md points to it (C2's residual risk, CSV export, cabin pricing).
- **Date:** 2026-11-07

**Result:** 17 gaps: 0 high, 4 medium and 13 low. The PRD contradicts no C, D or Q decision without a record. The memlog, PRD §9 or the addendum records 18 changes or decisions that the PRD made on purpose.

**How references work in this note:**

- FR, NFR, SM and UJ point to `prd.md`. A bare §n is a section of `prd.md`.
- PD §n is a section of pre-prd-discovery.md.
- memlog L38 is line 38 of `.memlog.md`.

## 1. Gaps

### Medium

**G1. D11 arrival choices (FR-18)**

- **Input:** D11 accepted the proposed fixed choices (Friday morning, Friday afternoon, Friday evening, Saturday morning) plus an optional comment. It also added "Don't know".
- **PRD:** FR-18 says only "fixed choices including 'Don't know'". The four choices and the optional comment are not in the PRD, the addendum or the brief. They survive only in the pre-PRD's proposal column and in the working extract.
- **Why it matters:** FR-54 counts "expected arrivals", and the expected-results list (FR-69) needs a fixed set of values. The list also doesn't fit per-day attendance (FR-14). Filippa (Saturday and Sunday) should not be offered Friday choices, and there is no Saturday-afternoon or Sunday choice.
- **Fix:** list the choices in FR-18, or in the addendum's For UX section, and decide whether to keep the optional comment. Offer only the choices that fit the person's first day, the same way FR-15 handles meals.

**G2. The expected-results list has no "guest only Saturday" (PD §7 topics 7–8, D2; FR-68)**

- **Input:** the test list should cover:
  - a couple who are both coming;
  - a family where one is not coming;
  - a single person with an allergy;
  - a guest who comes only on Saturday;
  - a household that has paid;
  - a household that hasn't answered.
- **PRD:** FR-68 covers all of these except the Saturday-only guest, and the drop is not recorded. Filippa (UJ-2) comes Saturday and Sunday. That tests the Friday rules, but no test person comes for the wedding day only, without a cabin and without paid meals (D2).
- **Why it matters:** such a household owes 0 kr. The addendum's payment-status table then matches two rows at once: "0 kr received → Not paid" and "Exactly the total → Paid". The same happens for households where nobody comes and for households that haven't answered.
- **Fix:**
  - Add a Saturday-only guest with no overnight stay to FR-68, for example by making Synne Saturday-only.
  - Define the status for a total of 0 kr, for example "Nothing to pay".
  - While editing FR-68, also cover the PRD's own new v1 states: part paid, refund owed, "I have paid" without a matching payment, "Changed", and consent given versus declined.

**G3. Large text for older guests (PD §4; NFR-5, NFR-6)**

- **Input:** older guests need large text, large buttons, a Back link, errors at the field, an error summary and the couple's phone number on every page. The brief also asks for "large, readable text".
- **PRD:** all of this is carried except large text. FR-6, FR-13, FR-22 and NFR-5's 44 × 44 px touch targets cover the rest. NFR-5 covers 200 % zoom and contrast, but not the default text size, and the change is not recorded.
- **Fix:** add to NFR-5 or NFR-6: "Guest pages use large body text by default." The UX phase sets the exact size, for example at least 18 px.

**G4. C1's consent rules when the couple registers consent (FR-31; compare FR-26 and FR-29)**

- **Input:** C1 requires that guests are told before they consent that they can withdraw it. It also requires storing the time and the version of the consent text.
- **PRD:** FR-31 is new (memlog L40). It lets the couple register allergies after a phone call and records who registered them and when. It does not require the couple to tell the guest what the consent covers: the purpose, who sees the data, that Hardingasete's kitchen gets it, and how to withdraw. FR-29 also stores "the version of the consent text shown", but on this path no text is shown.
- **Fix:** in FR-31, the couple confirms that they told the guest the same points as FR-26. Store the method (phone or message), the admin, the time and the consent-text version they used.

### Low

**G5. D2 is only implied (FR-15, FR-16)**

- **Input:** D2 says a guest can come without a cabin, for example only for the wedding day, and chooses meals independently of the cabin.
- **PRD:** this follows from FR-15 and FR-16. Overnight is a separate yes/no, and meals follow the days present. But no requirement states it.
- **Fix:** add one sentence to FR-16, tagged [D2].

**G6. When the lock starts on the deadline date (D4, D5; FR-41, FR-42, FR-64)**

- **PRD:** the deadline is a date setting, but the PRD doesn't say when on that date the form locks.
- **Why it matters:** guests will read "Svarfrist 1. april" as including 1 April. The tests and UJ-6 step 6 need a clear cut-off. The research (R 1.3) notes that Joy closes the form at midnight in the event's time zone.
- **Fix:** add to FR-42, for example: "The form locks at the end of the deadline date, Norwegian time."

**G7. C2's residual risk is not visible in the PRD (NFR-3, FR-27)**

- **Input:** C2 accepted that no source supports one adult consenting for another. The confirmation in FR-27 is therefore a safeguard without a legal source. The decision says the residual risk "is documented in the brief".
- **PRD:** the brief records the risk in its Data and Privacy section, but the PRD doesn't mention it. Choosing C2 closed PD §6's question to Datatilsynet. The accepted risk should still be visible in the document that now drives the work.
- **Fix:** add one sentence to NFR-3 that points to the brief and to R 3.2. This also gives context for Q8.

**G8. Details on the information pages (C3, PD §4, topic 5; FR-9, FR-10)**

- **Prices:** PD §4 says "prices visible before the form", but FR-9 only "marks what costs money", so guests first see prices inside the form. This is optional. FR-32 already meets C3, which asks for prices before the choices.
- **Optional parts:** topic 5 says the programme should mark what is optional. FR-9 doesn't.
- **Practical page:** PD §4 says it should be scannable, ordered by day and include the weather. FR-10 has neither the ordering nor the weather.
- **Fix:**
  - FR-9: "marks what is optional and what costs money, with the price".
  - FR-10: "ordered by day … and the weather to expect".

**G9. C4 and the If-time envelope's "first visit" (§3.3, addendum, FR-3)**

- **PRD:** the envelope opens "the first time a guest visits".
- **Risk:** suppose the server records the first visit when the page loads. That breaks FR-3, which says opening a link never changes anything. Messenger and WhatsApp would also use up the first visit when they fetch the link for a preview (the C4 finding), so the guest would never see the envelope.
- **Fix:** add a note to the addendum. Either the guest's browser remembers that the envelope has been seen, or the server saves it only when the guest acts, by opening or skipping the envelope.

**G10. Q1's price model: per person or per cabin? (§7, §8; FR-16, FR-32, FR-33)**

- **Input:** Q1 also asked whether cabins are allocated per person or per cabin, because that sets the price model.
- **PRD:** §7 marks Q1 as answered for capacity and moves cabin allocation out of scope. Q1 is then dropped from §8. The PRD assumes the cabin is priced per person for the whole weekend, as in the brief, but doesn't say this is an assumption. If Hardingasete prices per cabin, every total changes.
- **Fix:** add to the assumptions in §7: "The cabin is priced per person for the whole weekend; confirm with Q3."

**G11. Q7's second half and the envelope test (PD §3, §6; §8, §3.3)**

- **Q7:** PRD §8 keeps only the payment half. The other half, "What would you look for on the site?", is about how the site is organised, and it is dropped.
- **Envelope test:** PD §6 suggests testing the envelope prototype with one older relative. The PRD doesn't carry this; SM-3 tests the RSVP, not the envelope.
- **Fix:** extend the Q7 row in §8, and add the envelope check to the If-time item or to the usability test plan.

**G12. Scope ideas dropped without a record (PD §5)**

- **CSV export (If time):** PD §5 says it is "already in the brief", but the brief only has a printer-friendly page. The teacher's feedback says export isn't needed in v1.
- **Language preset per household (If time):** meant to come with the English version.
- **QR code with the personal link on a paper card:** outside the site, possible later.
- **PRD:** none of the three appears in the PRD or the addendum, not even as Out or rejected.
- **Fix:** add one line for each to §3.3, §3.4 or the addendum's Rejected alternatives.

**G13. Who sees speech sign-ups (PD §4, §5; §3.3 vs FR-46)**

- **PRD:** §3.3 says only the toastmaster sees the sign-ups. But FR-46 has just two roles: helpers "see everything", and the couple has full access. The research point was that sign-ups are hidden from the couple, so this needs a permission only the toastmaster has.
- **Fix:** decide who sees sign-ups. Add a note under For architecture in the addendum that this If-time item needs a toastmaster flag.

**G14. A "not answered" list with contact details (PD §4, §5; FR-55–FR-57, FR-62)**

- **PRD:** the content is there. FR-56 lists households that haven't answered, and in FR-57 the couple can tap a guest's phone number or email. But the not-answered list itself isn't said to show phone and email.
- **Naming:** FR-62 and UJ-5 refer to "the not-answered list" and "the payment overview", but neither view is defined anywhere else.
- **Fix:** in FR-56, show each member's phone and email on the not-answered item. Use one name for each view throughout.

**G15. Edge case: a household that splits up (topic 7; FR-50)**

- **PRD:** FR-50 lets the couple move a guest to another household. It doesn't say what moves with the guest: answers, allergy and consent records, the link or registered payments.
- **Why it matters:** after a move, the old household may suddenly show "refund owed" and the new one "not paid".
- **Fix:** add a rule to FR-50, for example:
  - the guest's answers, consent and link move with them;
  - payments stay with the household that paid;
  - both households are marked "Changed", and both totals are recalculated.

**G16. Edge case: changing your mind after paying, after the deadline (topic 7; FR-36, FR-60, FR-63, addendum "Needs attention")**

- **Before the deadline:** covered by UJ-2 and FR-36.
- **After the deadline:** when the couple lowers a total, the household automatically shows "refund owed" (FR-60). The PRD doesn't say whether a late cancellation is refunded once the numbers have gone to Hardingasete.
- **Mismatch:** the addendum clears "Refund owed" only when a refund is registered, while FR-56 says any item can be marked as handled.
- **Fix:** decide the rule. If late cancellations aren't always refunded, add a "no refund" option and make the addendum table match FR-56.

**G17. UX details not passed to the addendum's For UX section (D9, D10, topics 5 and 6)**

- **D10:** the proposed label "Allergies or dietary needs the kitchen must know about".
- **D9:** the suggested step order (attendance → options → allergies → arrival and hike → check) and the advice to keep the number of steps low.
- **Topic 6:** whether to write "du" or "dere", and whether error messages use humour. Rikke's receipt wording in the addendum uses "du/dere" without a rule.
- **Topic 5:** examples of what to bring, such as hiking boots and swimwear for the hot tub.
- **Fix:** add a short list of open UX questions from the pre-PRD discovery to the addendum.

## 2. Contradictions without a record

There are none: the PRD and the addendum contradict no C, D or Q decision without a record. These minor inconsistencies are for information only:

1. **Cabin rule.** Memlog L26 says the whole-weekend cabin rule is "still subject to Hardingasete confirmation (Q1)". D1 and the brief say Hardingasete has already confirmed it. FR-16 agrees with D1, so only the log note is out of date, and the PRD needs no change.
2. **CSV export.** PD §5 says CSV export is "already in the brief", but the brief only has a printer-friendly page. The PRD follows the brief (see G12).
3. **Number of admin users.** D13 and the research count four admin users. The PRD plans for five: the couple plus three helpers (NFR-7, memlog L80). That matches the roles in the brief, so it is the pre-PRD that needs updating (section 4).
4. **Conflicts inside the PRD.** Two come from pre-PRD items and are listed as gaps: G9 (the envelope's first visit vs FR-3) and G13 (toastmaster-only sign-ups vs FR-46).
5. **Misplaced table row.** In the addendum, the row "Saving an unfinished answer to continue later | Moved to If time" sits after the "Test data note" section. It is outside the Rejected alternatives table and won't display as part of it. Move it into the table.

## 3. Deliberate changes (accounted for)

- **C6:** "I am …" is pre-set to the link owner and can be changed (FR-12), because each guest has their own link. memlog L38; PRD §9 "Links"; addendum rejects "One link per household".
- **D1:** the first question asks whether everyone is coming the whole weekend, with nothing pre-selected, and then asks for exceptions (FR-14). memlog L27; addendum rejects "'Everyone is coming' ticked in advance".
- **D5 + C1:** after the deadline, guests can't add or change allergies, but they can still withdraw consent (FR-42, FR-30). memlog L39, L82.
- **D6, payment status:** the couple registers amounts received, and the site calculates the status: not paid, part paid, paid or refund owed (FR-59, FR-60). This replaces the two states. memlog L52, L55; PRD §9; addendum.
- **D6, "I have paid":** moved from optional into v1 (FR-35, FR-61). memlog L19; PRD §9.
- **D7:** "paid X, now owes Y" is now shown through the calculated status and registered refunds (FR-36, FR-59, FR-60). memlog L30, L55.
- **D9:** saving an unfinished answer moved to If time; a warning before leaving the form covers v1 (FR-20, §3.3). memlog L17; addendum (see note 5 in section 2).
- **D12:** decided. Text on the information pages lives in the code. Prices, the deadline, contact details and payment details are admin settings, with a warning when prices change (§5.12 note, FR-64, FR-65). memlog L63, L69.
- **D13:** helpers can see but not change; the brief had full access for all (FR-46). memlog L51; PRD §9.
- **C3 addition:** totals use the current prices, and the couple is warned when a price change affects households that have already answered (FR-33, FR-65). memlog L63.
- **Q1:** capacity is answered, so there is no bed limit, and the couple allocates cabins outside the site (§7, §3.4, addendum). memlog L59, L79.
- **Q6:** the activities are information only (FR-9, §3.4), but the Friday hike stays in the form and is asked only of guests present on Friday (FR-17). memlog L60, L81.
- **Q9:** the Vipps number is always shown (FR-34) and the QR code is If time (§3.3). Payment requests are Out (§3.4), and the Vipps terms are checked again before production (§3.2). memlog L20.
- **Contact details on every page (PD §4, §5):** shown only with a valid link. The page for an invalid link shows no contact details (FR-5, FR-6). memlog L85; addendum's Rejected alternatives.
- **"Regenerate a household's link" (PD §5):** now done per guest, and only that guest's link changes (FR-53). memlog L32, L38.
- **"Who's coming" list (PD §5, "Discuss"):** decided Out (§3.4). memlog L78.
- **Lost link (topic 7):** guests can't recover a link themselves. The couple copies and resends it, or deactivates it and creates a new one (UJ-3, FR-51, FR-53, §3.4). memlog L35, L43; addendum.
- **New: consent registered by the couple after a phone call (FR-31).** memlog L40. One C1 detail is missing; see G4.

## 4. Items in pre-prd-discovery.md to update

1. **Front matter or introduction.** Mark the note as used by the PRD on 2026-11-07 and link to `../../prds/prd-aill-handle-it-2026-11-07/prd.md`. Say that the PRD refers to its items as [C…], [D…] and [Q…].
2. **§1, C6 decision row.** Add: "PRD: pre-set to the link owner, since each guest has their own link (FR-12, PRD §9)."
3. **§2, D6 and D7 rows.** Add: "Replaced in the PRD: the couple registers amounts and the site calculates the status (FR-59, FR-60); 'I have paid' is in v1 (FR-35, FR-61); see PRD §9."
4. **§2, D11 row.** Point to FR-18, and record the final list of choices once G1 is fixed.
5. **§2, row "D12, D13 — Not decided yet. Taken into the PRD."** Replace it with:
   - D12 decided in the PRD on 2026-11-07: page text in the code; prices, deadline, contact details and payment details in admin (§5.12, FR-64, FR-65).
   - D13 changed in the PRD on 2026-11-07: helpers can see but not change (FR-46, PRD §9).
   - In D13's proposal, correct "4 trusted people" to five admin users (NFR-7).
6. **§2, D14–D16.** Add: "Tracked in PRD §8 and in the addendum's For architecture section; D16 also in PRD §3.2."
7. **§3, Q1.** Add: "Capacity answered 2026-11-07: far more beds than guests, so no bed limit; the couple allocates cabins outside the site (PRD §7, §3.4). The price model is still open (G10)."
8. **§3, Q2–Q4, Q7 and Q8.** Add: "Still open; tracked in PRD §7 and §8."
9. **§3, Q9.** Add: "Decided 2026-11-07: Vipps number always shown (FR-34), QR code If time (PRD §3.3), terms checked again before production (PRD §3.2)."
10. **§4, Helpers.** Change "shared admin" to "helpers can see but not change (FR-46)". For speech sign-ups, see G13.
11. **§5, scope table.** Add the PRD outcome to each row: FR-21; FR-23 and FR-24; FR-56; FR-63; FR-14; FR-6 and FR-5; FR-4; FR-53; FR-25; the §3.3 print page; FR-35; §3.4 for reminders; §3.4 for "who's coming"; the §3.3 envelope. Mark CSV export, the language preset and the paper-card QR code as not carried until G12 is resolved, and correct "CSV … already in the brief".
12. **§6, research topics.**
    - The household exemption: closed by PRD NFR-3.
    - The iMessage preview: handled by FR-3, FR-4 and NFR-1's test-send to an iPhone.
    - Hardingasete's numbers: Q1 is partly answered.
    - Confirming allergies for another adult: closed by choosing C2, with the residual risk accepted in the brief (see G7).
    - Older guests' reaction to the envelope: not carried (G11).
13. **§8, checklist.**
    - Tick "Start `bmad-prd` …": done 2026-11-07, with the path to the PRD.
    - Change the D1–D13 line to "D12–D13 decided in the PRD on 2026-11-07".
    - Change the Q1–Q4 line to "Q1 answered for capacity 2026-11-07; Q2–Q4 awaiting reply".
    - Optional: add "Brief change log updated with changes from the PRD phase". memlog L54 lists this as a to-do for the PRD's final step.

## Appendix: status of every item

| Item | Status | Where in the PRD |
|---|---|---|
| C1 | Carried, with a gap where the couple registers consent | FR-25, FR-26, FR-28–FR-30, FR-66; G4 |
| C2 | Carried; the residual risk is only in the brief | FR-25, FR-27, NFR-3; G7 |
| C3 | Carried | FR-32, FR-33, FR-65; Q7 in §8; G8 |
| C4 | Carried | FR-3, link tracking in §3.3; G9 |
| C5 | Carried | FR-24, FR-38, "Conflicts" in §3.4 |
| C6 | Changed, with a record | FR-12 |
| C7 | Carried | FR-4, FR-5 |
| D1 | Carried; the form's shape was refined, with a record | FR-14–FR-16, FR-54 |
| D2 | Carried by implication | FR-15, FR-16; G5, G2 |
| D3 | Carried through C1 and C2 | — |
| D4 | Carried: deadline shown next to the button and on the receipt | FR-7, FR-24, FR-41, FR-64, Q2 in §7; G6 |
| D5 | Carried | FR-42, FR-63, "Deadline rules" in §3.4; G6 |
| D6 | Changed, with a record | FR-35, FR-59, FR-60, NFR-2 (whole kroner) |
| D7 | Changed, with a record | FR-36, FR-60 |
| D8 | Carried: no household code, message "Bryllup Sigmund" | FR-34, "Payment code" in §3.4 |
| D9 | Carried | FR-13, FR-20, FR-21, FR-23, FR-24; G17 |
| D10 | Carried; the categories match exactly | FR-25, FR-54, FR-58; G17 (label) |
| D11 | Partly carried | FR-18; G1 |
| D12 | Decided in the PRD | §5.12 note, FR-64, FR-65 |
| D13 | Decided in the PRD (changed) | FR-46, §9 |
| D14 | Deferred to architecture | §8, addendum |
| D15 | Deferred to architecture | §8, addendum, NFR-8 |
| D16 | Deferred to 2027 | §3.2, §8, NFR-3 |
| Q1 | Capacity answered; price model open | §7, §3.4, addendum; G10 |
| Q2 | Open and tracked | §7, §8 |
| Q3 | Open and tracked | §7, §8, FR-64 |
| Q4 | Open and tracked | §7, §8 |
| Q5 | Answered and carried | FR-14 |
| Q6 | Answered and carried | FR-9, §3.4; FR-17 for the hike |
| Q7 | Open; only half tracked | §8; G11 |
| Q8 | Open and tracked | §8 |
| Q9 | Decided in the PRD | FR-34, §3.2–§3.4 |
| PD §4, guest needs | Carried, except large text and the practical-page details | FR-1, FR-6, FR-7, FR-13, FR-22–FR-24, FR-32, FR-33, NFR-5; G3, G8 |
| PD §4, couple needs | Carried; phone and email per guest make the not-answered follow-up possible | FR-49, FR-54–FR-57, FR-60, FR-63, §3.3; G12, G14 |
| PD §4, helper needs | Changed, with a record; gap on speech sign-ups | FR-46, §3.3; G13 |
| PD §5, scope table | Carried or changed with a record, except CSV export (the print page is carried), the language preset and the paper-card QR code | section 3; G12 |
| PD §6, research topics | Closed or carried, except the residual-risk note and the envelope test | NFR-1, NFR-3, FR-3, FR-4; G7, G11 |
| PD §7, topics 1–4 | Carried | UJ-1, UJ-2, UJ-4, FR-7, FR-32, FR-54, addendum |
| PD §7, topic 5 | Partly carried | FR-9; G8, G17 |
| PD §7, topic 6 | Partly carried | NFR-6, "Tone" in the addendum; G17 |
| PD §7, topic 7 | Lost link and simultaneous answers carried; the others are gaps | Lost link: UJ-3, FR-51, FR-53. Simultaneous answers: FR-38 [C5]. Household split: G15. Change of mind after the deadline: G16. Saturday only: G2 |
| PD §7, topic 8 | Partly carried | FR-68, FR-69; G2 |
| PD §8, checklist | Needs updating | section 4 |
