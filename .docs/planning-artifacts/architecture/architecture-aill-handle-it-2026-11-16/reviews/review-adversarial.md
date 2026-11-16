---
title: "Adversarial review: ARCHITECTURE-SPINE.md"
reviewed: ../ARCHITECTURE-SPINE.md (status draft, 2026-11-16)
rationale_read: ../.memlog.md
requirements_read: ../../../prds/prd-aill-handle-it-2026-11-07/prd.md, addendum.md, ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md
date: 2026-11-16
method: Pairs of stories that each obey every AD to the letter but build incompatibly
---

# Adversarial review: ARCHITECTURE-SPINE.md

## Verdict

The spine is sound at the level of layers (one monolith, pure rules, services as sole writers, stored facts only), but it leaves the **shape and lifecycle of the shared household data** undefined: what one "sent answer" is, what consent means on a re-send, which writes bump the revision and the "Changed" marker, how a guest-side "I have paid" relates to the couple's registrations, and how FR-63 reuses the guest form across the `guests`/`dashboard` import wall. Two stories can obey every AD and still lose a consented allergy, re-store a withdrawn one, show a guest numbers they must not see, or make a count disagree with its own drill-down. Fourteen holes are listed below; the first six should be closed with new or tightened ADs before epics and stories are written.

## How to read the findings

Each finding names two units one level down (a story or epic a developer agent would actually be handed), shows that both comply with the ADs as written, then shows how they diverge and what that costs. Severity:

- **Critical:** wrong data reaches Hardingasete's kitchen, consented data is lost, or withdrawn health data is kept.
- **High:** a wrong number on the admin home or the guest page, a privacy leak, or a test that fails on the examiner's machine.
- **Medium:** silent data loss for one guest or a recoverable inconsistency.

---

## Critical and high

### H1 (Critical) — A re-send by another household member wipes consented allergies; a stale draft re-stores withdrawn ones

**Unit A: "Change answer" story (FR-37, FR-38).** Prefills the form from the stored answer. FR-26 and CM-4 say the consent choice "starts unanswered" and is never pushed, and EXPERIENCE's Choice control says consent Ja/Nei starts unanswered. So the story renders consent unanswered for every person, also on a re-send.

**Unit B: "Send answer" service (FR-28, AD-8 *Without consent*).** "On send without consent, allergy data is dropped." It implements that literally per person on every send.

**Both comply.** AD-8 says what happens on send without consent; nothing says that a person who already has stored consent keeps it on a later send.

**Divergence.** Marie opens her own link two weeks later to change Filippa's days. Bestemor-style consents given earlier by Arild are not re-answered, so the send service drops every stored allergy in the household. Nothing in the conflict notice (AD-9) reports it, because the revision did not change. The kitchen never hears about the allergy: exactly SM-8.

**Mirror case (privacy).** Bestemor withdraws consent on her own link (FR-30, G11). Sigmund still has a draft cookie (AD-8) from before, holding bestemor's allergy note and consent "Ja". AD-9 only conflicts on the household revision, and nothing says a withdrawal bumps it. Sigmund sends, the service sees consent = yes in the payload and stores the allergy again with a fresh Consent row "given by another household member". A withdrawn Art. 9 consent is silently reversed by a stale device copy.

**Close with a new AD ("Consent state on re-send"):**

- Consent is per person and has three inputs on any send: *unchanged*, *given*, *refused*. A person with current consent whose consent field is unanswered on a re-send counts as *unchanged*, and their allergy rows stay.
- Only an explicit "Nei" on the form or a withdrawal (FR-30) deletes allergy data.
- A withdrawal is a household write: it bumps the revision (AD-9) and marks "Changed" (FR-39).
- A draft never carries a "Ja" across a revision change: when the draft's base revision differs from the current one, every consent in it is reset to unanswered and the conflict notice lists allergy differences per person.
- Test: seed household with consent → second member re-sends without touching allergies → allergy still in FR-58 list; withdraw → stale draft sent → allergy not stored.

### H2 (High) — "What is owed" and "refund" mean different things on the guest page and in admin; reports and refunds have no defined shape

**Unit A: Guest status block / FR-35 / FR-36 story.** Needs "what remains to pay", the pre-filled amount on "I have paid", and "the couple will refund the difference". AD-2 says payment status is computed by one function in `rules/` and never re-implemented, so the developer calls `payment_status(total, received, refunded)` from the guest view.

**Unit B: Admin payments story (FR-59–FR-61, A9).** Owns `payment_status`, built on registered `Payment` rows.

**Both comply.** AD-2 forbids a second implementation of "payment status". Nothing says the guest side has a *different* quantity.

**Divergence and cost.**

1. **Scope and privacy leak.** PRD 3.4 puts "payment confirmation to guests" out of scope, and FR-60 says only the couple and helpers see statuses. If the guest view reuses the admin function, the guest page shows "Betalt" or "300 kr mangler" based on the couple's private registrations.
2. **Wrong number.** The guest's "remaining" must be `total − reported`, the admin's "missing" is `total − (received − refunded)`. One function cannot be both.
3. **Report aggregation.** The ER diagram has `Household ||--o{ PaymentReport`. Story A appends a row on every correction (FR-35 "can correct"); the FR-61 match rule in story B sums the reports. Sigmund corrects 900 → 1 200: reported = 2 100, and the household turns red. Or two members each report the same Vipps payment: double. Or B takes the latest report and A meant reports to be additive (Arild paid the cabin, Marie paid the meals).
4. **Refund sign.** `Payment` covers "received or refunded". One story stores a refund as `amount=-200`, another as `kind=refund, amount=200`, and `received − refunds` subtracts a negative. AD-12 only says "int".
5. **Undo.** FR-59 "corrected or undone": hard delete in one story, a reversing row in another; the sums disagree with the "Registrert" list in A9.

**Close with a new AD ("Two money views"):**

- `rules/` has two named families: `guest_balance(total, reports)` for guest pages and `payment_status(total, received, refunded)` for admin. Guest views may not import or call the admin one (enforce with a test that greps `guests/`).
- `PaymentReport`: one *current* report per household (a correction replaces it; earlier versions kept only as history if needed), with amount, method, payer text, reported_at, reported_by. The FR-61 match uses the current report only.
- `Payment`: `kind ∈ {received, refunded}`, `amount > 0` always, `voided_at` for undo (rules ignore voided rows). Correction = void + new row.

### H3 (High) — FR-63 "same form as the guests" cannot be built across the import wall without breaking AD-8 or AD-10

**Unit A: Guest RSVP steps (AD-7, AD-8).** Forms and step views live in `guests/` (Structural Seed: "guests/ guest views, forms, templates"). Draft state is a cookie on path `/<code>/`.

**Unit B: Couple override story (FR-63, A7).** Lives in `dashboard/` under `/admin/`. The addendum says "the same form, not a second copy".

**Both comply, and are still incompatible.** The seed rule "guests and dashboard never import each other" forbids B from importing A's forms. B now has three legal-looking options, each breaking something:

- **Copy the forms into `dashboard/`** — obeys the import rule, violates FR-63 and the addendum, and the copy drifts (exactly what AD-7 tries to prevent).
- **Send the couple to the guest URL `/<code>/svar/`** — obeys AD-6, but AD-10 makes it a guest request: the author is recorded as the guest, not the admin (FR-63 broken), and the guest view's lock check (AD-11 "every lock check, in guest views...") refuses after the deadline, which is exactly when UJ-3 needs the override. Rikke's browser also gets a draft cookie with Synne's allergy note.
- **Carry multi-step state in the admin session** — the admin session is in the database (Django default), so unsent allergy data is written to `django_session` before consent, contradicting AD-8 *No early database write*.

**Close with a new AD ("One RSVP engine, two mounts"):**

- The step forms, the step order and the draft codec live in `wedding/rsvp/` (not `guests/`). `guests/` mounts them under `/<code>/svar/<step>/`, `dashboard/` under `/admin/husstand/<id>/svar/<step>/`.
- Every step and the send service take an explicit `actor`: `GuestActor(guest)` from the AD-6 resolver, or `CoupleActor(user)`. The author recorded is the actor. The lock is skipped only for `CoupleActor`, in the service, and the view asks the same service-level policy function instead of calling `is_locked` directly.
- The admin draft uses the same signed cookie, with path `/admin/husstand/<id>/`, cleared on send, on cancel and on logout. Nothing about an unsent answer is put in any session.
- The couple never uses guest URLs for writes.

### H4 (High) — "Household answered", counts and their drill-down lists can disagree

**Unit A: Admin summary story (FR-54).** Computes counts through `rules/` as AD-2 demands, from facts loaded by `selectors.py`.

**Unit B: Drill-down story (FR-55, A3).** "Every count opens the people behind it." A selector filters in the ORM, e.g. `PersonAnswer.objects.filter(friday_dinner=True)`. AD-2 bans re-implementing *counts*; a filtered list is a "read query", which the seed hands to `selectors.py`.

**Divergence.**

- **Leftover choices (FR-75).** The step engine keeps Leone's Friday dinner in the draft when Arild toggles her to "not coming" (so it comes back if he toggles again). The send service stores what it receives. `rules/` ignores choices of non-coming people, so the summary says 11; the ORM drill-down lists 12 names. Same for a removed day.
- **"Answered" (FR-74).** Story A defines a household as answered when it has a revision ≥ 1; story C ("Needs attention: not answered") uses "any PersonAnswer exists". After the couple adds a person to an answered household (FR-49), or moves an answered guest into an unanswered household (FR-50), the two disagree: «Svart: 28 av 30» and the "Ikke svart" list no longer add up, and the new person is neither coming, not coming nor "not answered" anywhere.
- **Where the revision lives.** The ER diagram has no entity for "the household's sent answer"; `Guest ||--o| PersonAnswer` only. Who sent, when, and the revision (AD-9, FR-24, FR-38) have no home, so one story puts them on `Household`, another on each `PersonAnswer`.

**Close with a tightened AD-2 and AD-4:**

- Every count is returned by a rules function as the *list of subject ids*; the count is `len(list)` and the drill-down renders the same list. Selectors return unfiltered facts for a household set and never filter on answer content.
- The send service normalises before writing: it calls `rules.normalise_answer()` (FR-75), so stored answers never hold choices for absent people or days.
- Add a `HouseholdAnswer` entity (revision, sent_at, sent_by guest or admin, author kind) to the ER diagram; `PersonAnswer` rows belong to it. "Household answered" ⇔ revision ≥ 1. A guest in an answered household with no `PersonAnswer` is "person not answered" and puts the household on "Needs attention".
- Adding, removing or moving a guest is a household write that bumps the revision of every household it touches and marks them "Changed".

### H5 (High) — The "Changed" marker and "handled" marks are two stores of one fact, keyed too coarsely

**Unit A: Send / override / withdraw services (AD-3).** Set "the Changed marker" as a side effect, e.g. `household.changed = True`.

**Unit B: "Needs attention" story (FR-56, A2).** Stores "handled" as `AttentionMark(household, kind)` (ER: `Household ||--o{ AttentionMark`).

**Both comply with AD-4**, which lists both "the Changed marker" and "Needs attention handled marks" as stored facts.

**Divergence.**

- Rikke marks "Endret" as seen. Story B writes an AttentionMark; story A's boolean is still `True`, so A4's "Endret" tag stays while A2 hides it. Or story B clears the boolean instead, and then the two stores are one too many.
- Arild changes again after it was marked seen. If the mark is just `(household, 'changed')`, the new change stays hidden — the couple sends Hardingasete stale numbers. Same for "I have paid" not matching: marked handled, then the guest corrects the report upward; it should come back and does not.
- "Guest with nothing registered for allergies" is per **guest**, but the mark is per **household**: marking Marie handled also hides Filippa.
- Which writes count as a change is spread over stories: send (revision > 1), override, withdrawal, move/add/remove guest (H4), but not first answer, not "I have paid" (FR-39). Each story decides alone.

**Close with a new AD ("Attention items are derived, marks are versioned"):**

- Store `Household.changed_at` (last FR-39 change), set only by one service helper `mark_changed(household, actor)` that every qualifying service calls; list the qualifying services in the AD.
- An AttentionMark is `(kind, subject_type, subject_id, handled_at, handled_by, state_key)` where `state_key` is the fact it handled (changed_at, report id/amount, refund amount). A rules function shows an item iff its condition holds and no mark matches the current `state_key`. No stored "is changed" boolean.

### H6 (High) — Link codes are written to logs by default; guest requests can reach the database session

**Unit A: Logging and deployment story (AD-15 *Logs*).** "No names, link codes or allergy content are written to logs."

**Unit B: Any guest page story (AD-6 *URL*).** The code is in the path `/<code>/`, by design.

**Both comply, and the result breaks AD-15.** Django's `runserver` logs every request line, `django.request` logs every 404 (each unknown code, i.e. each guessing attempt, plus each deactivated code) with its path, and any production app server writes an access log with the path. Every guest link ends up in plain text in logs, which are not covered by the backup encryption in PRD 3.2. The links are the guests' only credential (FR-1).

**Second leak on the same seam.** AD-7 says each step redirects (PRG). A guest-step story that also redirects on a *failed* step must carry the typed input somewhere; the natural Django tools are `request.session` or `messages` with session storage. Both write to `django_session` in the database, which puts allergy notes there before consent (AD-8).

**Close with a tightened AD-15 and AD-8:**

- A logging filter replaces the first path segment of any guest URL with `<code>` on the `django.server` and `django.request` loggers; the production access-log format is configured the same way when hosting is chosen (add to Deferred constraints). Throttling keys on IP, never on the code.
- Guest views never touch `request.session`; `MESSAGE_STORAGE` is cookie-based or unused on guest pages. A failed step re-renders with status 200 and errors (no redirect); only a successful step redirects. The draft cookie is the only cross-request carrier for unsent input. Test: run the whole guest flow and assert `Session.objects.count() == 0`.

---

## Medium

### M1 — Seed command vs. expected-results tests vs. AD-6 and AD-10

**Unit A: Seed command (FR-68, AD-3, AD-14).** Must go through services (AD-3). The addendum requires README test links with *fixed* codes.

**Unit B: Expected-results tests (AD-16).** "Load the seed data and assert every count, total, payment status and the lock."

**Divergences.**

- AD-6 says every code comes from `secrets.token_urlsafe(16)`. Fixed codes need either a `code=` parameter on the create-guest service (then any caller, in production too, can set a guessable code; AD-14 only blocks the *command*) or a direct `.save()` (breaks AD-3). Same for `loaddata` of a fixture, which bypasses services.
- Services check the couple role (AD-10) and the lock (AD-11). The seed has no logged-in user; one story passes a fake admin user, another adds a `system=True` bypass flag that then exists in production code.
- The lock is part of the oracle. If the seed deadline is a fixed date, the "locked" expectation flips the day the examiner runs the tests after that date. If it is relative to today, the oracle file has to be relative too. And the rules need a `now` argument (AD-2 forbids Django imports, so `timezone.now()` cannot be called inside `rules/`); otherwise one story passes `now`, another calls `datetime.now()` without a timezone.
- The seed needs history: a household marked "Changed", a withdrawn consent, sent_at dates in the past. Through services with real "now", every row is dated today.

**Close with a new AD ("Seed is a declarative file applied through services"):** the seed is a data file in `wedding/fixtures/`; one command applies it through services with `actor=SeedActor` and an injected `now`; `SeedActor` and `links.fixed_code()` are refused unless `APP_ENV=local` (checked in the service, not only in the command); the deadline in seed and oracle is expressed as an offset from a fixed seed date, and the lock test injects `now` on both sides of the boundary, in winter and summer time; every `rules/` function that depends on time takes `now`.

### M2 — Draft cookie vs. new link (FR-53), moving a guest (FR-50), household edits (FR-49) and deadline changes (FR-64)

**Unit A: Draft cookie (AD-8).** Path `/<code>/`, expires at the deadline, holds everything entered, sized by a test on "the largest household".

**Units B: the admin stories that change what the draft refers to.**

- **New link.** The guest's real draft sits under the old path and is orphaned. Acceptable when the link leaked, but nobody decided it.
- **Move guest / add or remove person.** The draft keeps person ids from the old household. If the draft payload is trusted, `send_answer` writes PersonAnswers for guests that are no longer in the resolved household, which is a cross-household write. A signed cookie proves the server made it, not that it belongs to *this* household.
- **Larger household than the seed.** The 4 KB test runs on seed data; the couple can later add a fifth or sixth person with long notes. The browser silently drops an oversized cookie: the answer is lost without the guest knowing (NFR-1).
- **Deadline extended.** The cookie expiry was set from the old deadline; the couple extends it (common for stragglers); a draft made before the old deadline is gone during the extension.

**Close by tightening AD-8:** the draft payload carries `household_id`, `base_revision` and the guest id of the link owner; the signing salt includes the code; the server discards a draft whose household or member set does not match the resolver's; the send service checks every person id against the resolved household; the server enforces a maximum household size and note length derived from 4 KB (with a test at that maximum, not at the seed); the cookie's own expiry is generous, and the deadline is enforced server-side with `is_locked` when the draft is read.

### M3 — The admin session cookie is sent on guest pages; helpers are also guests

**Unit A: Guest RSVP story.** To pass an author to services, a developer reads `request.user` when it is authenticated ("couple is testing").

**Unit B: Admin roles story (AD-10).** Services refuse writes unless the user has the `couple` role.

**Divergence.** The toastmaster, maid of honour and best man are guests with their own links *and* helper accounts. Django's session cookie path is `/` by default, so on their own guest link the request carries their helper session. Story A passes the helper user to `send_answer`; story B's role check refuses it: a helper cannot RSVP for their own household. The reverse also happens: Rikke testing a guest link while logged in writes as "couple" and skips the lock. AD-13's sliding renewal also renews admin sessions on every guest page view.

**Close by tightening AD-10:** guest views never read `request.user`; the actor for guest writes comes only from the resolver; `SESSION_COOKIE_PATH = "/admin/"` (and the CSRF cookie stays site-wide so guest forms work).

### M4 — Prices change between the check page and "Send answer"

The check page and the receipt both compute the total from current prices (AD-4, FR-33). If the couple changes a price in between (FR-64), the guest sends and the receipt shows a different total from the one they confirmed, without warning. Small in practice because prices are set before invitations (PRD 3.2), but the FR-65 warning only protects the couple's side. **Close:** the check page posts the total it showed; the send service recomputes and, if it differs, returns to the check page with a notice instead of writing.

### M5 — Removing a household or person deletes money and consent records

Tier-3 "delete household" (EXPERIENCE) with default `on_delete=CASCADE` deletes `Payment`, `PaymentReport` and `Consent` rows. Payments then vanish from A9's "Til sammen", and the proof of consent (NFR-3, Art. 7(1)) disappears outside the FR-67 operation the PRD designed for that. **Close:** an AD that removal of a household with payments is refused (or archived) until its balance is zero, and that `Consent` rows are deleted only by FR-67 or the retention date.

### M6 — Payment message: derived or stored

FR-71 says "Bryllup" + the household's names, *and* the couple can adjust it. One story derives it on each render; another stores it on household creation. Renaming a person after the household has paid changes the derived message, so the couple can no longer match the old bank transfer. **Close:** store the message on household creation as a fact (AD-4 list), regenerate only on explicit couple action, and run the duplicate check (FR-71) in the service.

---

## Lower priority (note only)

- **L1.** AD-11 says the deadline is a *date*; FR-64's "how many households would be locked out" must use the same `is_locked`, with the new date and the current `now`. State it, so the settings story does not count with `date < today`.
- **L2.** AD-9 does not say whether "I have paid" or a couple payment registration bumps the household revision. If one story does, every payment produces a false conflict notice for a guest mid-draft. State that only answer, allergy, consent and membership writes bump it.
- **L3.** FR-12 "I am [name]" records who answered, but the actor (whose link) and the chosen respondent can differ. Store both, so FR-38's "who" and the FR-40 history in 2027 agree.
- **L4.** `Settings` as a single row: two settings forms (prices vs. contacts) saving the whole row can overwrite each other's fields. Each settings service should update only its own fields.

---

## Proposed changes to the spine (summary)

| # | New or tightened AD | Closes |
|---|---|---|
| 1 | New: consent state on re-send (unchanged / given / refused); withdrawal bumps revision; drafts never carry "Ja" across a revision change | H1 |
| 2 | New: two money views (`guest_balance` vs `payment_status`); one current report; `Payment.kind` + positive amounts + `voided_at` | H2 |
| 3 | New: one RSVP engine in `wedding/rsvp/`, two mounts, explicit `actor`, admin draft cookie on `/admin/husstand/<id>/` | H3, M3 |
| 4 | Tighten AD-2/AD-4: counts are lists, selectors do not filter on answers, `normalise_answer` before write, `HouseholdAnswer` entity, membership changes bump revision | H4 |
| 5 | New: `changed_at` + versioned AttentionMarks keyed by subject and state | H5 |
| 6 | Tighten AD-15/AD-8: path scrubbing in logs, no guest sessions, failed step re-renders | H6 |
| 7 | New: declarative seed through services with `SeedActor`, injected `now`, local-only fixed codes | M1 |
| 8 | Tighten AD-8: draft bound to household and revision, size limits enforced from the model, server-side expiry | M2 |
| 9 | Tighten AD-10: guest views never read `request.user`; `SESSION_COOKIE_PATH = "/admin/"` | M3 |

Each new AD should name its FRs in **Binds**, as the existing ones do, and get a line in `.memlog.md` with the reason.
