---
type: review
lens: reconcile spine against requirements source
target: ../ARCHITECTURE-SPINE.md (draft, 2026-11-16)
sources:
  - ../../../prds/prd-aill-handle-it-2026-11-07/prd.md
  - ../../../prds/prd-aill-handle-it-2026-11-07/addendum.md
  - ../.memlog.md (for rationale only)
date: 2026-11-16
---

# Review: spine reconciled against PRD and addendum

## Verdict

The spine covers the PRD's big structural calls well (stack, rules core, single writer, links, draft, revision check, deadline, money, roles, zero-config, privacy headers, oracle) and its Capability map covers every live FR. But it leaves one PRD requirement structurally unsolved (the couple using **the same form** as guests, FR-63), it does not say **which writes the deadline lock blocks** (FR-42, FR-30), it **contradicts the addendum on test link codes**, and several quiet data rules (actor, consent version, payment-report corrections, handled marks, "No allergies" without consent) are left for stories to decide independently. AD-8 also states a privacy premise that AD-7 makes false. None of this needs a redesign; most fixes are one or two lines in an existing AD.

Severity scale: **critical** (stories will build incompatible things, or the spine contradicts a binding requirement), **high**, **medium**, **low**.

## Findings

### F1 (high): "One form" for guests and couple (FR-63) is not placed, and the seed structure blocks it

- **PRD:** FR-63 "using the same form as the guests"; addendum *For architecture*: "One form (FR-63). The couple fills in and changes answers with the same form as the guests, not a second copy of it." Also FR-12 ("The choice records who answered"), FR-29 (consent "who gave it (the person, another household member or the couple)"), FR-31 (couple-registered consent with channel), FR-63 ("record the admin as the author").
- **What the spine says:** the RSVP steps live in `guests/` (Capability map, AD-7). `guests` and `dashboard` "never import each other". Every guest request goes through the AD-6 resolver at `/<code>/`; the admin area is under `/admin/`. The draft cookie is scoped to `/<code>/` (AD-8). AD-11 says couple overrides "skip the lock in the service, not in the view".
- **Why it matters:** with these rules, the dashboard story that builds FR-63 has three options, all incompatible with each other: (a) copy the step forms into `dashboard/` (violates the addendum), (b) import from `guests/` (violates the dependency rule), or (c) send the couple to `/<code>/svar/...` as if they were a guest (then AD-10 says the request is a guest request, the author is recorded as a guest, and the guest view's lock check blocks the override). The spine also has no single notion of *who acted* (link owner, chosen "I am" person, another household member, or an admin user), which FR-12, FR-24, FR-29, FR-31, FR-38, FR-39 and FR-63 all need to record the same way.
- **Suggested fix:** add to AD-7 (or a new AD) that the step forms, the step sequence and the step validation live in `wedding/` (for example `wedding/rsvp/`), and both `guests/` and `dashboard/` render them with their own templates/URLs. Define one actor value passed to every write service (for example `Actor(kind=guest|admin, guest_id|user_id)`), stored on the answer, consent and payment-report rows. State where the couple's in-progress override lives (Django session, not the guest's cookie) and that the override path bumps and checks the AD-9 revision just like `send_answer`, so a guest's open draft cannot silently overwrite the couple's change.

### F2 (high): the deadline lock's scope is not fixed, so a story could lock consent withdrawal or "I have paid"

- **PRD:** FR-42 lists what is locked (who is coming, days, meals, overnight, hike, allergies) and what still works after the deadline ("Payment information, 'I have paid', the information pages and consent withdrawal still work"; "Households that never answered see the same message"). FR-30: consent withdrawal "at any time, also after the deadline" (GDPR Art. 7(3)).
- **What the spine says:** AD-11 says every lock check calls one function, and couple overrides skip it. It never says which services check the lock and which must not.
- **Why it matters:** "every lock check calls that function" is consistent whether `withdraw_consent` and `report_payment` check the lock or not. A story that adds the check "to be safe" breaks a GDPR right. The draft cookie expiring at the deadline (AD-8) is also only one half of the boundary; the send service must reject a draft sent at 23:59:59 + 1 s.
- **Suggested fix:** add one rule to AD-11: "The lock applies only to services that change answer content (send answer, the guest side of FR-75). `withdraw_consent`, `report_payment`/`correct_payment_report` and all read pages never check it. Couple services (FR-63, FR-31, FR-59) never check it." Add the addendum's "tested at the boundary in both winter and summer time" to the rule (it is a test invariant, not story detail, because SM-11 depends on it).

### F3 (medium-high): AD-6 contradicts the addendum on test link codes, and AD-3 vs fixture loading is ambiguous

- **PRD:** addendum *Test data*: "The README's test links use fixed codes that exist only in the test data. Real links always come from the random generator." FR-68 (README lists a test link per guest), FR-72.
- **What the spine says:** AD-6: "each guest has one active code from `secrets.token_urlsafe(16)`". AD-3: management commands call services and never `.save()`. The seed lists `wedding/fixtures/` for "seed data", which reads like Django `loaddata` (which writes rows without services).
- **Why it matters:** the seed story will either generate random codes (README links break on every reseed, SM-5 fails) or bypass AD-6 with hand-written codes in a different format. A second story may load fixtures with `loaddata` and skip the "Changed"/revision/consent side effects that AD-3 says belong to the write, so the seeded state would not be one the app can produce, and the oracle (AD-16) would be checked against impossible data.
- **Suggested fix:** in AD-6, say "codes issued by services come from `token_urlsafe(16)`; the seed command alone may set fixed codes, which must have the same format (22 URL-safe characters) and are listed in the README". In AD-3 or AD-14, say whether seed data is built by calling services (recommended; fixtures then hold the *input*, not rows) or loaded as rows, and that the seed refuses to run in production (already in AD-14). Also carry the addendum's fake-data rules (`example.com` emails, unreal phone numbers, account number with invalid check digit) as a one-line invariant for the seed, since a wrong value here is a real-money or real-person risk, not a style choice.

### F4 (medium): AD-8 claims allergy data never reaches the server before consent, which AD-7 makes false

- **PRD:** FR-26 ("Allergy information is saved only if the respondent gives consent"), FR-28, FR-78, NFR-3 (allergies are health data). UX open question 6 was closed by Rikke on the premise, recorded in the memlog, that the draft "never leaves the device before 'Send answer'".
- **What the spine says:** AD-8 *Prevents:* "allergy data reaching the server before consent". But AD-7 POSTs every step to the server, and the draft cookie is sent back to the server on every request under `/<code>/`. A signed cookie is readable (signed, not encrypted).
- **Why it matters:** the requirement (not *saved* without consent) is met, but the spine's wording is wrong, and Rikke's privacy choice was made on that wording. Stories also get no rule about what the server may do with allergy data it receives in transit: Django's production error reports and any request logging can capture POST bodies and cookies.
- **Suggested fix:** reword AD-8 to "allergy data is not stored on the server before consent; it passes through the server in step POSTs and the cookie". Add: the draft cookie is `HttpOnly`, `SameSite=Lax`, and `Secure` in production; the allergy step and send views use `sensitive_post_parameters` (and the cookie is excluded from error reports). Tell Rikke the corrected premise so the UX Q6 decision stays informed (log it in the memlog).

### F5 (medium): quiet data rules left for stories to decide

AD-4 lists what is stored, but several stored facts the PRD needs are not named, and stories that store them differently will compute different numbers or lists:

| Gap | PRD reference | Risk if silent | Suggested rule |
|---|---|---|---|
| Who sent the answer and when; who last updated | FR-12, FR-24, FR-38, FR-63 | One story stores it on the household, another per person, a third only in the revision | Add "sent by (actor, F1) and sent at, per household revision" to AD-4 |
| Consent-text version | FR-29 | Decided in the memlog ("a constant in code bumped whenever the text changes") but not in the spine | Add to AD-4 or a consent AD |
| Correcting an "I have paid" report | FR-35 ("can correct it"), FR-61 | One story keeps all reports and sums them, another keeps the latest; the match result differs | State: a correction replaces the report (or: the latest report is the one compared) |
| Refunds and undoing a registration | FR-59, FR-60 | Refund as negative amount vs a kind flag; undo as delete vs reversal row | State the sign convention and whether undo deletes |
| Payment message | FR-71 ("The couple can adjust it") | Stored at creation (goes stale when names change) vs derived | Derived from names unless the couple has stored an override; the duplicate check runs on the effective message |
| "Needs attention" handled marks | addendum *"Needs attention" behaviour*, FR-56 | A boolean mark hides a household that changes again after being marked seen | Tie each handled mark to the occurrence it handles (for example the revision or a timestamp), so a new occurrence reappears |
| History-ready model, never allergy content | addendum *Change marker and history*: "The data model should allow it from the start"; "must never store allergy content"; FR-40 | The Deferred row keeps only "must go through services"; the allergy-content ban and the "plan the model now" note are lost | Copy both into the Deferred row (or AD-3) |

### F6 (medium): what counts as "answered the allergy question" without consent

- **PRD:** FR-25 (an explicit "No allergies or dietary needs" per person), FR-26 (allergy information saved only with consent), FR-28, FR-30 (withdrawal deletes the allergy information), FR-54 and FR-56 (coming guests "who haven't answered the allergy question" / "have nothing registered"), FR-68 (test cases "entered an allergy but didn't consent" and "withdrew consent").
- **What the spine says:** nothing beyond AD-8's "allergy data is dropped".
- **Why it matters:** is "No allergies" itself health data that needs consent? Does a guest who entered allergies without consent, or who withdrew, count as "not answered" in FR-54/FR-56? The send story, the summary story and the hand-written oracle (AD-16) must agree, and the oracle is written first.
- **Suggested fix:** one rule (in AD-4 or AD-8): "'No allergies' is stored without consent / needs consent [pick one]. A guest whose allergies were dropped (no consent) or deleted (withdrawal) has nothing registered and counts as not answered in FR-54/FR-56." This one touches privacy, so Rikke should choose; record it in the PRD addendum too.

### F7 (medium): error pages and link previews (FR-4, FR-5, FR-6)

- **PRD:** FR-6 (contact details on every guest page "including error messages"), UJ-3 step 6, FR-5 (pages without a valid link show no names, phone numbers, date or place), FR-4 ("Page titles and link previews are the same for everyone and contain no names").
- **What the spine says:** AD-6 covers the FR-5 page; AD-15 covers the title. Nothing on 404/500 handlers or preview metadata.
- **Why it matters:** contacts live in the `Settings` row in the database, so a 500 page caused by a database fault cannot read them; a 404 *inside* a valid `/<code>/` must show contacts while a 404 elsewhere must not. Chat apps build previews from `og:*` and `meta description`, not only `<title>`.
- **Suggested fix:** add to AD-15 (or AD-6): custom `handler404`/`handler500`; under a resolvable code they render the guest base template with contacts; otherwise the FR-5 page; the 500 template must render without database access (best effort for contacts). And: `og:title`, `og:description`, `og:image` and `meta description` are fixed, identical for every link, and contain no names.

### F8 (low): smaller gaps

- **PRD 3.2 update rules are not carried into Deferred.** The Deferred backup row names the backup constraints, but not the *Updates* rule (all tests pass, backup right before every update, post-update check that a real guest link opens the right household and the admin counts are unchanged, no updates in the last two weeks before the deadline except guest-flow fixes) or the *Device floor* (works in Messenger's and Facebook's in-app browsers on a real old device). Add both as constraints on the 2027 hosting/backup row; the post-update check is a natural reuse of the AD-16 oracle idea.
- **Production access logs.** AD-15 bans link codes in logs, but every web server and host logs request paths, and the code *is* the path. Add to the hosting Deferred row: access logs must drop or truncate paths under `/<code>/`, or have short retention, and the record of processing (PRD 3.2 *Privacy in operation*) must mention them.
- **NFR-5, NFR-6 and NFR-7 have no AD.** The front matter says the spine binds NFR-1 to NFR-9, but accessibility, tone and performance appear only through the Assets and Language conventions. One line would do: "DESIGN.md tokens and EXPERIENCE.md rules are binding for every template (NFR-5: 18 px body, 44 px targets, 320 px, 200% zoom, visible focus)". For NFR-6, set `LANGUAGE_CODE = "nb"` and `TIME_ZONE = "Europe/Oslo"` in the convention, and say that Django's built-in validation messages are replaced by the project's own warm wording (Django's defaults are formal).
- **"A GET request never writes" (AD-6) is broader than FR-3.** The unknown-code limiter (Deferred) writes to the database cache on GET, and admin GETs renew the session row (AD-13). Reword to "a GET never changes guest data" so a reviewer does not flag the limiter as a violation.
- **Lost or reissued link and the draft.** FR-53 replaces a code; a draft cookie on the old path is orphaned and an open form under the old code will fail. Fine as behaviour, but say that the send service resolves the code again at send time and fails with the FR-5 page, so the failure is clear (NFR-1).
- **Capability map:** every live FR (FR-1 to FR-78, except the removed FR-18 and FR-43 to FR-45) is mapped. A row for "Deadline lock and boundary tests (SM-11)" would be optional. NFR-1 to NFR-9 are bound only through ADs, not map rows; consider a short NFR row group or a note that NFRs are bound per AD.

## What is correctly deferred

Hosting, backup tooling and monitoring, Django 6.2 LTS, FR-40, FR-67, editable info pages (AD-17), throttling details and browser tests are all listed under Deferred with their constraints, and none needs more now except the additions in F5 (FR-40 constraints) and F8 (update rules, device floor, access logs).

## Suggested order of fixes

1. F1 and F2: decide in the spine before any tier 1 story for the form or the lock is written (FR-63 is tier 2, but the step forms are tier 1 and must be placed in `wedding/` from the start).
2. F3: before the seed/oracle story, which tier 1 builds first.
3. F6: ask Rikke (privacy) before the oracle is written.
4. F4, F5, F7: one-line additions to existing ADs.
5. F8: as convenient; the 2027 items can wait for the hosting story.
