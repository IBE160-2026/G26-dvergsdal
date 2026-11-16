# Review of epics.md (2026-11-16)

- **Content:** [`../epics.md`](../epics.md), the epics and stories document (class: docs that define behavior), reviewed before Story 1.1 starts.
- **Tool:** `bmad-review` with four lenses. Adversarial, edge-case-hunter and structure ran independently. Prose ran on top of the structure findings. Verification-gap was skipped because it applies only to code.
- **Machine-readable findings:** [`review-epics-2026-11-16.json`](review-epics-2026-11-16.json) holds the adversarial and edge-case findings. The editorial lenses use their own table shape, given below.
- **Status:** Findings only. Nothing has been changed in `epics.md` yet. The decisions on each finding are recorded in the session log.

| Lens | Findings |
|---|---|
| Adversarial | 30 (A1–A30) |
| Edge-case hunter | 46 (E1–E46) |
| Editorial structure | 11 rows + 2 minor |
| Editorial prose | 18 rows + 4 minor |

## Overlap between lenses

Several lenses found the same problems independently, which makes these findings more likely to be real:

- **Draft cookie path:** A1, E1. Confirmed by hand. Epics line 716 and spine line 135 scope the cookie to `/<code>/svar/`, so the front page `/<code>/` never receives it.
- **Seed re-run once payments exist:** A2, E25.
- **No deadline lock in the T1 build:** A6, E12.
- **Lock cases tied to the seeding date:** A5, E28.
- **Missing Settings row on a fresh database:** A14, E29.
- **Consent per person and the FR-27 confirmation:** A9, E6, E7.
- **Couple override and consent:** A7, E21.
- **Throttling locks out shared addresses:** A18, E46.
- **Removing or moving the sender, or the last person:** A23, E41, E42, E45.
- **Undefined day combinations for overnight stay:** A12, E3, E4.
- **Note field and the 4 KB cookie limit:** A10, E17.
- **SM-n and UJ-n used but never defined:** A30, structure row 7.
- **Story 2.4 AC has no Then:** structure row 10, prose row 4.
- **"For a while" has no tested value:** A19, prose row 15.
- **Template residue in Overview:** structure minor, prose row 7.


## Adversarial

**A1. Story 2.9 vs Story 2.1 / AD-8 (spine line 135)**
- Problem: Draft cookie is scoped to /&lt;code&gt;/svar/, but the front page /&lt;code&gt;/ must read it to show «Du har et svar som ikke er sendt ennå.»; browsers never send it there
- Fix: Scope the cookie to /&lt;code&gt;/ (still per guest, still excludes /admin/); update AD-8, Story 2.1 and 2.9; add AC: a test GETs /&lt;code&gt;/ with the draft cookie and sees the notice
- Consequence: The draft notice (UX-DR9/UX-DR26, FR-78) can never appear

**A2. Story 1.3 vs Stories 5.2, 6.5 / AD-3, AD-4**
- Problem: Seed re-run must delete households that hold non-voided payments from Epic 5 on, which AD-4 refuses; AD-3 says only services delete
- Fix: Add AC to 1.3: re-seeding uses a system-actor reset service (only when APP_ENV is local) that voids then deletes test data, tested after payments exist; or re-seed into a flushed DB
- Consequence: seed_testdata fails on the second run after Epic 5, or someone bypasses services; the examiner's README path breaks

**A3. Story 1.3 seed case 'withdrawn consent' and Story 3.5**
- Problem: withdraw_consent only exists in Story 7.2, so the seeded withdrawn-consent household cannot be produced before then
- Fix: Add AC to 7.2: seed_testdata applies the withdrawn consent through withdraw_consent; mark that expected.toml row as asserted from 7.2
- Consequence: Story 3.5 expected-results tests fail or are quietly weakened

**A4. Story 3.5 (every FR-54 count equals expected.toml)**
- Problem: FR-54 includes households per payment status, but payments are seeded only in 5.2
- Fix: Change AC to 'every FR-54 count except the Betaling panel; that panel is asserted in Story 5.3'
- Consequence: Story 3.5 cannot pass as written; the expected-results list gets edited without a reason

**A5. Story 1.3 expected.toml lock cases; Stories 3.5, 4.3**
- Problem: Deadline is seeded relative to today, so absolute 'now' values go stale; and no story asserts the lock entries
- Fix: Store lock cases as offsets from the seeded deadline; add AC to 4.3 that the expected-results tests assert them
- Consequence: FR-69's claim that the deadline lock is tested is never checked

**A6. Stories 2.1, 2.6 (no deadline enforcement in Epics 1–3)**
- Problem: FR-41 is T1, but sends after the deadline are refused only in Story 4.3 (T2)
- Fix: Move the deadline function into 2.6 and add AC: a guest send after the deadline is refused with the FR-42 message; or record a deliberate T1 deviation in the PRD change log
- Consequence: The usability-test build accepts answers after the deadline

**A7. Story 4.4 (couple override) and the consent step**
- Problem: The override reuses the guest form, so the couple can tick consent «Ja» on a guest's behalf, bypassing FR-31 (Story 8.3)
- Fix: Add AC to 4.4: consent is read-only in the admin form; allergies only for people with stored consent; say who the respondent is for an admin actor (FR-12)
- Consequence: Health data stored without valid consent (GDPR Art. 9)

**A8. Story 4.4 vs FR-39 / AD-19**
- Problem: FR-39 marks 'Changed' when the guest or the couple changes a sent answer; 4.4 never mentions changed_at
- Fix: Add AC to 4.4: overriding a sent answer sets changed_at via the AD-19 helper; a first answer by the couple does not; tested both ways
- Consequence: Overrides vanish from «Trenger oppfølging» and the «Endret» tag

**A9. Story 2.4 (consent block, FR-27 confirmation)**
- Problem: Unclear whether consent is per person or per household, how the server shows the FR-27 confirmation without JS, and whether it is required
- Fix: One consent Ja/Nei per coming person inside their fieldset; FR-27 checkbox in every fieldset except the respondent's; field error if data entered for another person with Ja and the box unticked; tests for each
- Consequence: Household-level consent (breaks FR-29) or third-party allergy data without FR-27 confirmation

**A10. Story 2.4 (note field max length) and the 4 KB test**
- Problem: No number for the note's max length or the 'largest household', yet the 4 KB cookie test depends on both
- Fix: State e.g. 'note max 200 characters, server-validated with an FR-22 error' and the household size used as largest
- Consequence: Untestable AC; real drafts may exceed 4 KB and the browser silently drops the cookie

**A11. Story 2.1 (progress line «Steg 1 av m»)**
- Problem: m depends on who comes and which days, which are unknown at step 1
- Fix: Define m before step 1 is answered (e.g. maximum steps) and test it
- Consequence: Step count jumps and confuses older guests (NFR-6); AC not verifiable

**A12. Story 2.3 (overnight contradiction, FR-70)**
- Problem: Only 'present on one day' is blocked; Fri+Sun and other day sets are undefined for overnight
- Fix: List allowed day sets for overnight exhaustively in wedding/rules/ with a table-driven test; reject Fri+Sun or define it
- Consequence: Wrong bed and meal counts sent to Hardingasete (NFR-2)

**A13. Stories 1.2, 1.4, 8.2 ('deactivated code')**
- Problem: 1.4 tests a deactivated code, but the Guest model in 1.2 has no deactivation field; 8.2 doesn't say whether old codes are kept
- Fix: Remove 'deactivated' from 1.4 or add the field in 1.2; in 8.2, keep old codes as deactivated, never reissued, with a test
- Consequence: Untestable AC, and a later migration of the link model after invitations go out (NFR-1)

**A14. Story 1.2 (single Settings row) vs FR-3, Story 1.8**
- Problem: Nothing creates the Settings row on a fresh migrate; get_or_create on GET would break 'GET never writes'
- Fix: Add AC to 1.2: a data migration creates the row with safe defaults; guest views use .get(); a test on an empty migrated DB opens / and an error page
- Consequence: Front page and the 500 page crash before the couple configures settings

**A15. Story 2.8 (status block) vs Story 2.7 («Betal senere»)**
- Problem: 2.7 promises the link always shows how to pay, but the status block shows only the total until Story 5.1
- Fix: Add AC to 2.8: when something is owed, the status block links to «Slik betaler du»
- Consequence: In the usability test a guest who chose «Betal senere» cannot find payment details (FR-34, T1)

**A16. Story 5.4 («… har fått beskjed og betaler tilbake»)**
- Problem: The guest message is computed from total vs report, but the couple's attention item (6.2) comes from registered payments
- Fix: Add an attention item 'report exceeds new total' in 6.2/5.3, or reword the guest message
- Consequence: Guests owed refunds that the couple never sees

**A17. Story 7.3 (beforeunload) vs FR-78, Story 7.1**
- Problem: beforeunload fires on reload, on every step POST unless excluded, and on the «Personvern» link inside the consent block
- Fix: Add ACs: no prompt on step submits or «Personvern»; only on links leaving the form; manual test on iOS Safari and Messenger's browser
- Consequence: A warning on every step, or the privacy link is blocked

**A18. Story 8.6 (link-code throttling per address)**
- Problem: Throttling per IP locks out whole families or the venue Wi-Fi after one mistyped link
- Fix: Always resolve valid codes; throttle only unknown codes; give concrete numbers
- Consequence: Real guests cannot open their invitation

**A19. Stories 6.6, 8.6 ('several failed logins', 'for a while')**
- Problem: Thresholds and lockout duration are not given, so 'tests on both sides of the limit' cannot be written
- Fix: State numbers (e.g. 5 per username or 20 per IP in 15 min, locked 15 min) and whether counts are per username, IP or both
- Consequence: Implementer invents undocumented values; weakens criterion 1

**A20. Stories 6.6, 1.1 (README install)**
- Problem: 6.6 adds a database cache table, but migrate doesn't create it and no story updates the README
- Fix: Add AC to 6.6: README includes 'uv run manage.py createcachetable' (or a migration runs it); repeat a clean-machine README run
- Consequence: Examiner gets 'no such table' on the login page (criterion 6)

**A21. Story 5.2 delete guard vs Story 6.5**
- Problem: No delete operation exists in Epic 5, so 5.2's 'deletion is refused' AC cannot be tested there
- Fix: Keep the AC only in 6.5, or say 5.2 tests it at the model/service-guard level
- Consequence: An early delete service built only to satisfy the AC, or an AC marked done without a test

**A22. Stories 5.1, 5.2, 5.5, 6.2, 6.4, 6.5, 7.2, 8.1–8.3 (write services)**
- Problem: AD-3 cross-household tests and AD-20 submission ids are stated only in 2.6 and 4.1; 7.2 lets a guest post a person id
- Fix: Standing AC in each write story: submission id (AD-20); for guest services a test that another household's id is refused (AD-3); explicit in 7.2
- Consequence: A guest can delete another household's allergy data; double taps create duplicate rows

**A23. Story 6.5 (remove person), Story 8.1 (move guest)**
- Problem: Removing/moving the guest recorded as sent_by is undefined; 8.1 doesn't say what happens to the moved guest's answers and consent
- Fix: sent_by keeps a name snapshot or SET_NULL; removing the sender never deletes the answer; in 8.1 decide whether answers move or reset, consent follows the person, payment messages re-checked
- Consequence: Data loss on an ordinary admin action; counts no longer match the expected-results list

**A24. Story 2.6 (size)**
- Problem: One story holds five tables, the send service, consent semantics, idempotency, price-change detection, failure UX, cross-household tests, seeding and a manual test
- Fix: Split into 2.6a models + happy-path send; 2.6b consent semantics; 2.6c idempotency, price re-check, failure UX; 2.6d seeding through the service
- Consequence: One huge PR that cannot be reviewed meaningfully (criteria 1 and 3)

**A25. Story 1.4 (size and Covers)**
- Problem: Tokens, fonts, paper texture, assets, buttons, G1 page, headers and log filter in one story; Covers lists UX-DR53/54 with no AC
- Fix: Split into 1.4a tokens/fonts/buttons, 1.4b paper/assets, 1.4c G1/headers/log masking; add ACs for UX-DR53/54 or drop them from Covers
- Consequence: False traceability: claimed requirements never built

**A26. Covers vs ACs: UX-DR15, UX-DR19, UX-DR17, FR-4**
- Problem: Busy state «Sender …», no nav bar on form steps, the four notice variants and identical link previews have no AC anywhere
- Fix: One AC each: 2.6 busy state, 2.1 no nav bar, 1.4 notice component, 1.4 OG tags identical for every code with no names
- Consequence: Skipped in implementation while the coverage map claims them

**A27. Story 6.2 ('as many items as fit')**
- Problem: Viewport fit cannot be computed on the server, and no number is given; conflicts with AD-1 (works without JS)
- Fix: Show a fixed number (e.g. 3) then «Vis alle n»; check at 360×560 in the manual test plan
- Consequence: JS-only layout logic, or the rule is ignored

**A28. Story 7.4 (final texts)**
- Problem: Acceptance depends on the couple's final texts and times, with no owner or date; Hardingasete's times come early 2028
- Fix: Add a precondition and fallback: texts by a date, else ship best-known times and record open items in the PRD change log
- Consequence: Story blocks T2 completion or is marked done with placeholders

**A29. Story 7.2 (withdrawal record) vs Story 2.6 Consent fields**
- Problem: 2.6's Consent has no state or withdrawn_at, so 7.2 needs a second migration of the same model
- Fix: Add state (given/refused/withdrawn) and withdrawn_at in 2.6, or model withdrawal as a new Consent row
- Consequence: Undermines the stated reason FR-29 was pulled forward

**A30. General (identifiers SM-2, SM-11, UJ-6)**
- Problem: Cited in Covers and ACs (3.5, 4.3, 4.5) but not defined in this document
- Fix: Add a short 'Success measures and journeys referenced' list under Requirements Inventory
- Consequence: Traceability gaps; a build agent guesses what SM-11 requires

## Edge-case hunter

| # | Location | Trigger | Guard | Consequence |
|---|---|---|---|---|
| E1 | epics.md:951-953 | Front page /&lt;code&gt;/ reads draft cookie scoped to path /&lt;code&gt;/svar/ | Add a small unsigned has-draft marker cookie scoped to /&lt;code&gt;/, or widen the draft cookie path to /&lt;code&gt;/ | «Du har et svar som ikke er sendt ennå.» notice can never appear (UX-DR26, FR-78) |
| E2 | epics.md:841-843 | «Endre» on step 1/2 adds a person or day, then «Fortsett» returns to check page | After an Endre save, if applicable_steps(answer) has unanswered required items, route to the first incomplete step before the check page | New person/day never asked overnight, meals, allergies or hike; incomplete answer sent |
| E3 | epics.md:772-774 | Days reduced to one via «Endre» after overnight=yes, skipping the overnight step | normalise_answer clears overnight when len(days) &lt; 2, or check page validates the FR-70 contradiction before Send | Contradictory overnight for a one-day guest is sent and charged a cabin |
| E4 | epics.md:738-740 | Non-consecutive days chosen, e.g. Friday and Sunday only | Define in rules: either forbid Fri+Sun without Sat, or state overnight and Saturday-breakfast eligibility for it, with a test | Undefined overnight and breakfast offers; totals and counts disagree with the expected-results list |
| E5 | epics.md:776-778 | Person present Friday but not Saturday; Saturday breakfast rule says 'present from Friday' | offer_saturday_breakfast = 'fri' in days and 'sat' in days | Saturday breakfast offered and charged to someone absent on Saturday |
| E6 | epics.md:808-811 | Consent block wording is singular; consent is per person (FR-26, FR-29) | State one Ja/Nei consent per coming person inside that person's fieldset, plus per-person FR-27 confirmation | One household-level Ja is stored as consent for every member |
| E7 | epics.md:811 | Consent Ja for another person but FR-27 confirmation left unticked | if consent == 'ja' and person != respondent and not confirmed: field error per FR-22 (or treat as no consent and warn per FR-28) | Allergies for others stored without the confirmation FR-27 requires |
| E8 | epics.md:868-870 | Re-send with «Nei» where allergy data was previously stored with consent | On refused consent: delete that person's Allergy rows, record refusal, set changed_at as with withdrawal (AD-18) | Health data stays stored after the guest refused consent |
| E9 | epics.md:868-870 | Re-send edits allergies but leaves consent unanswered | Define: unanswered consent with changed allergy fields either requires a consent answer (field error) or shows FR-28 warning that edits are not saved | Guest's allergy edits silently dropped; old data kept without the guest knowing |
| E10 | epics.md:859-866 | Revision bump (guest add/remove/move) on household with no HouseholdAnswer row yet | Create HouseholdAnswer(revision=0) with the household, or keep revision on Household, and define the draft's 'no answer yet' revision value | Revision bump has nowhere to live; never-answered drafts skip the conflict check |
| E11 | epics.md:876-878 | Send rejected (revision conflict or price change) then resent with same submission id | Record a Submission row only when the write commits; rejected sends issue a fresh submission id on the re-shown page | Second send after conflict returns the stored rejection forever; Story 4.2 send never saves |
| E12 | epics.md:681-963 | Epic 2 (T1) send after deadline; lock refusal arrives only in Story 4.3 (T2) | send_answer in Story 2.6 calls is_after_deadline(settings.deadline, now) and refuses guest sends; RSVP button hidden after deadline | Usability-test build accepts answers after the FR-41 deadline |
| E13 | epics.md:932-935 | Answered household opens /&lt;code&gt;/svar/ directly before Story 4.1 exists | In Epic 2 the form view redirects answered households to the status block until Story 4.1 enables changes | Second send overwrites the answer with no Changed marker or last-updated info |
| E14 | epics.md:951-963 | Draft cookie still present after the deadline | if is_after_deadline(...): suppress draft notice and delete the draft cookie on next guest response | Front page keeps saying an unsent answer exists that can never be sent |
| E15 | epics.md:955-958 | Draft references a guest since removed/moved, or lacks a newly added guest | On «Ja, fortsett» drop unknown guest ids and route to step 1 when household membership differs from the draft | Steps render or crash on missing guests; added person never asked |
| E16 | epics.md:714-717 | Draft cookie with bad signature, failed decompression or old schema | try: signing.loads(...) except (BadSignature, ValueError): delete cookie and start empty | Every form step returns 500 for that guest |
| E17 | epics.md:817-819 | Real household larger than the largest seed household pushes draft over 4 KB | Before set_cookie, if len(value) &gt; 4000: show FR-22-style error / cap household size in Story 6.4 | Browser silently drops the cookie; answers vanish between steps |
| E18 | epics.md:960-963 | now between 23:59:59.000 and 23:59:59.999 on the deadline date | locked = now &gt;= datetime.combine(deadline + 1 day, time(0), tz=Oslo) | Answers locked up to one second early; boundary test passes inconsistently |
| E19 | epics.md:1159-1162 | Draft started before deadline, sent just after 23:59 | On lock refusal render the locked answer view with deadline text and contacts, and delete the draft | Guest sees an unhandled error or a form that silently does nothing |
| E20 | epics.md:701-708 | Household with one person; «Bytt» has nobody to switch to | Render «· Bytt» only when household.guests.count() &gt; 1 | Dead control shown on every step for single guests |
| E21 | epics.md:1186-1192 | Admin override reaches allergy/consent step and respondent line | Define admin path: respondent line shows admin, consent Ja not offered to admin until FR-31 (Story 8.3), existing consents kept | Admin records guest consent without the FR-31 safeguards, or allergy data lost |
| E22 | epics.md:1194-1196 | Admin override draft collides with a guest send or a second admin | Apply the AD-9 revision check and Story 4.2 conflict notice on the admin path too, with a test | Admin silently overwrites a newer guest answer |
| E23 | epics.md:932-935 | Status block or receipt «Sendt av &lt;name&gt;» when sender is an admin user | sent_by_display = guest.name if guest else 'Rikke og Valdemar' (never the admin username) | Guest sees an admin username, or template fails on null guest |
| E24 | epics.md:1114-1116 | Re-send with content identical to the stored answer | if normalise_answer(new) == stored: skip changed_at (and revision bump) or document that it counts | Household tagged «Endret» in Needs attention with nothing changed |
| E25 | epics.md:509-511 | Seed re-run must delete households holding non-voided payments (Story 5.2 refuses) | Seed teardown voids payments via service or uses a seed-only reset path before deleting | Second seed_testdata run fails once Epic 5 seeds payments |
| E26 | epics.md:509-511 | Local DB also holds couple-created households or admin users with same usernames | Delete only rows marked as seed data; on username or code clash, stop with a clear message | Re-run wipes local work or crashes on unique constraint |
| E27 | epics.md:513-515 | APP_ENV unset or misspelled on the production server | seed runs only if APP_ENV == 'local'; any other value refuses (allowlist, not denylist) | Test data and fixed codes written into the real database |
| E28 | epics.md:498-505 | Deadline seeded relative to today, while expected.toml lock cases use stated now values | Express expected lock cases as offsets from the seeded deadline, or let tests seed with an explicit deadline | Lock assertions in expected-results tests fail depending on run date |
| E29 | epics.md:461-463 | Fresh migrate with no seed: Settings row absent or deadline/contacts empty | Data migration creates the single Settings row with safe defaults; templates handle empty deadline and phone list | Front page, totals and footer fail before the couple configures settings |
| E30 | epics.md:669-671 | 500 caused by database failure; error page resolves the code via the database | Wrap resolver in the 500 handler in try/except and fall back to the no-names page | Error handler raises again; guest gets a bare server error |
| E31 | epics.md:669-671 | CSRF failure on a form step POST | CSRF page links back to the same step; state that the current step's unsaved input is lost, or re-render it from POST | UX-DR52 promise 'input kept after expired token' broken for the current step |
| E32 | epics.md:979-981 | create_admin with an existing username, bad role, or createsuperuser used instead | Refuse duplicate usernames with a message; role field has no blank default; require_couple rejects role not in {couple, helper} | Account with empty role gets undefined access |
| E33 | epics.md:1212-1219 | Settings saved with negative, zero or non-numeric prices or empty deadline | Validate prices as int &gt;= 0 and deadline required, with FR-22 errors before the confirm step | Negative totals or crashes in deadline function on guest pages |
| E34 | epics.md:1247-1254 | Payment report amount 0, negative, decimal («1 450,50») or when nothing is owed | parse_amount accepts only positive whole kroner; hide «Jeg har betalt» when total == 0 | Zero or fractional reports stored; spurious «Stemmer ikke» items |
| E35 | epics.md:1300-1302 | Refunded total exceeds received (received - refunded &lt; 0) | register_payment refuses refunds above received minus earlier refunds; payment_status test covers the case | payment_status gets an undefined net-negative input; wrong status shown |
| E36 | epics.md:1308-1311 | Household paid, then changed to not coming; refund owed | List rows for every household with total &gt; 0 or non-voided payments, not only coming households | Refund-owed household missing from Betalinger and its sums |
| E37 | epics.md:1327-1333 | Report below total with no change, or total lowered but still above report | Branch on guest_balance: total &gt; reported -&gt; remaining; total &lt; reported -&gt; refund; equal -&gt; paid | No message shown for common partial-report states |
| E38 | epics.md:1349-1355 | Adjusted payment message saved empty, or duplicate created by «Legg til husstand» | Empty adjusted message reverts to derived; run duplicate check on household add and in seed | Blank payment message, or two households share one unseen |
| E39 | epics.md:1422-1424 | Search for names with æ/ø/å in different case on SQLite | Store a casefolded search_name column, or filter in Python with str.casefold() | «øystein» does not find «Øystein»; SQLite LIKE folds ASCII only |
| E40 | epics.md:1448-1456 | Person added to a household that already sent its answer | Define new person as not answered; Needs attention lists answered households with not-answered persons | New guest never answered and never surfaced for follow-up |
| E41 | epics.md:1476-1479 | Removed person is the answer's sender, payment reporter or giver of others' consent | Use on_delete=SET_NULL with a stored name snapshot for sent_by and consent given_by; test cascade scope | Cascade deletes household answer or other members' consent records |
| E42 | epics.md:1476-1479 | Forged POST removes the last person of a household | remove_guest service raises if household.guests.count() == 1; suggest removing the household | Empty household breaks du/dere rule, counts and payment message |
| E43 | epics.md:1530-1532 | «Personvern» followed after filling the current step but before «Fortsett» | Open privacy in place via &lt;details&gt;/new view that saves the step first, or warn per Story 7.3 | Current step's input lost despite 'answers kept' |
| E44 | epics.md:1544-1546 | Person has only consented «Ingen allergier eller matbehov» stored | Withdrawal list includes any person with a Consent-backed record, including the no-needs choice | Guest cannot withdraw consent for stored data; admin state inconsistent |
| E45 | epics.md:1611-1613 | Move the only member out of a household, or into an answered/unanswered household | Refuse moving the last member; define moved person's answer state in target household and drop source answers | Empty source household; moved person's answers counted twice or lost |
| E46 | epics.md:1681-1684 | Legitimate guest with valid code shares an address that hit the limit | Look up the code first; apply the limit only to failed lookups, letting valid codes through | Family on shared Wi-Fi locked out of their own invitations |

## Editorial structure

**Purpose read:** This document helps the developer and the AI build workflow implement one story at a time. It also lets the examiner trace each requirement (FR, NFR, AD, UX-DR) to an epic, a story and then to code.
**Structure model:** Reference/Database, with the Overview and Epic List acting as a summary. The document has 18,853 words. The Requirements Inventory plus the FR Coverage Map account for 7,080 of them (38 %).

| # | Original | Recommendation | Why |
|---|---|---|---|
| 1 | §Epic List (1,048 words) placed after the Requirements Inventory and FR Coverage Map (7,080 words) | MOVE §Epic List directly after §Overview. Move the inventory and the coverage map after the last epic, as a reference section. | The plan (8 epics, tiers, order) is the headline but comes after about 7,200 words. First check that BMAD tooling finds sections by heading, not by position. |
| 2 | §UX Design Requirements UX-DR1–54 (2,317 words) | CONDENSE to an ID index pointing at the DESIGN.md or EXPERIENCE.md surface | The detail exists three times: in the UX docs, in this inventory and in the ACs. That is where versions drift apart. Saves about 1,700 words. |
| 3 | §Additional Requirements AD-1–AD-20 (1,101 words) | CONDENSE to one line per AD, pointing at ARCHITECTURE-SPINE.md. Keep the Story 1.1 setup bullet in full. | Same pattern as row 2. Saves about 650 words. |
| 4 | §FR Coverage Map (889 words) | MERGE the target into each FR inventory line (for example "FR-14 → Epic 2, Stories 2.1–2.2"), then cut the table | The mapping appears three times, and the FR-to-*story* trace the examiner needs is missing. Saves about 740 words. Check whether BMAD expects the heading. |
| 5 | Each epic's narrative appears word for word in §Epic List and in §Epic N | MERGE: keep it in §Epic N only | 8 identical paragraphs. Editing one leaves the other stale. Saves about 455 words. |
| 6 | Forward/deferral "And …" clauses inside ACs (1.3, 1.4, 1.5, 2.8, 3.2, 3.5, 4.2, 6.6) | MOVE to a per-story field "**Not in this story:**" | A build agent treats every AC as something to implement. |
| 7 | SM-2, SM-11, UJ-1–3, UJ-6, "Structural Seed", "Consistency Conventions" and personas are used but never defined | Add a short paragraph in §Overview defining them | Every other ID family is defined before it is used. |
| 8 | "Not in v1" is spread over four places | MERGE into one block under §Overview | One place answers "is this in scope?". |
| 9 | Epic List intro paragraph 2 hides the table-creation schedule | Split it into a "Migrations by story" list | The schedule is build-critical sequencing. |
| 10 | Story 2.4 AC with no **Then** | Rewrite as Given/When/Then (wording in prose row 4) | It is the only AC that breaks the schema. |
| 11 | Per-story schema and the Epic 2 deviation rationale | PRESERVE | Random access works because of the schema, and the deviation is a decision record the grading guide asks for. |

Minor: template residue ("UX Design if it exists") in §Overview, and the FR-29 pointers are inconsistent ("see the Epic List" vs "see Epic 2").
**Net reduction if all rows are accepted:** about 3,500 words (19 %). The trade-off: the builder must open DESIGN.md, EXPERIENCE.md or the spine for details that the ACs do not repeat.

## Editorial prose

Kept as written: British spelling, Norwegian kinship titles and Norwegian microcopy in «».

| # | Original | Revised | Why |
|---|---|---|---|
| 1 | "tier 2/3" used both for PRD priority and for admin protection level | Use T1/T2/T3 for priority and "protection tier 2/3" for confirmations | Term clash: Epic 6 delivers "UX-DR50 (tier 3 typed FJERN)" while Epic 8 *is* tier 3 |
| 2 | Norwegian copy in straight quotes ("Svar", "Kopier lenke", "Logg ut", "Sender …"); AD-8 "Begynn på nytt" | Use «» for all Norwegian copy; change AD-8 to «Nei, begynn på nytt» | The convention breaks, and AD-8 does not match UX-DR26 or Story 2.9 |
| 3 | Stories 2.5, 4.3 and 6.5: an **And** that contradicts its own **Given** | Make each one its own Given/When/Then | Not readable as one testable case |
| 4 | Story 2.4 "When JavaScript runs, ticking one clears the other; without it …" | "**Given** one person's «Ingen allergier…» and a category **When** the respondent ticks both **Then** with JavaScript … without JavaScript …" | Adds the missing Then |
| 5 | Story 5.5 "it is stored only because it was adjusted" | "the adjusted message is stored; a message nobody has adjusted is derived … and never stored" | States the rule directly |
| 6 | "oracle" (AD-16, Epic 3) | "expected-results list" | Undefined jargon; the rest of the document uses the other term |
| 7 | Overview "UX Design if it exists"; "[If time] PRD 3.3." | "the UX design (DESIGN.md, EXPERIENCE.md) and the architecture spine"; "extras listed in PRD section 3.3" | Template residue and an unclear reference |
| 8 | "the NFR named under each epic is the one" | "the NFRs … are the ones" | Each epic lists several NFRs |
| 9 | FR-7 "both jumping to the RSVP button after the information" | Split into two sentences | "After" reads as a time, not a position |
| 10 | Story 5.4 "the guest sees them"; Story 7.2 "opens it" | Name the antecedent | Unclear reference |
| 11 | Story 3.5 "asserted from Story 5.3" | "asserted starting in Story 5.3, once payments are seeded" | Ambiguous |
| 12 | Story 2.9 "(either "Svar", the RSVP button, or reloading a step)" | "(the nav «Svar», the RSVP button or reloading a step)" | "Either" with three items |
| 13 | FR-14 "Step 1 marks each person" | "In step 1 the respondent marks each person" | The step does not do the marking |
| 14 | Story 8.5 / UX-DR42 "may become a table" | Make it required or remove it | "May" in an AC is unclear |
| 15 | Stories 6.6, 8.6 "for a while" | Name the period | Cannot be tested |
| 16 | "e.g.", "incl.", "vs", "22 chars" | "for example", "including", "or", "22 characters" | Microsoft style guide |
| 17 | Story 6.2 "leaves the list when the page is left" | "disappears from the list when Rikke leaves the page" | Echo, and the verb lacks a subject |
| 18 | "### NonFunctional Requirements" | "### Non-functional Requirements" | Hyphenation |

Minor: slashes such as "allergies/dietary needs"; a hyphen instead of an en dash in the title; Story 1.4 "the page at 360 × 560" without saying which page; Story 2.9's draft-after-deadline clause is loosely tied to its Given.
