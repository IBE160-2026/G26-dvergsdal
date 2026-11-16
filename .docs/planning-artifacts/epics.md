---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - prds/prd-aill-handle-it-2026-11-07/prd.md
  - prds/prd-aill-handle-it-2026-11-07/addendum.md
  - architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md
  - ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md
  - ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md
---

# AI'll handle it - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for AI'll handle it, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

Requirement IDs are the PRD's own (FR-n, NFR-n), so every story traces back to the PRD (NFR-9). Each FR carries its PRD priority tier (section 3.1a): **T1** usability-test build (27 November 2026), **T2** complete course version (10 December 2026), **T3** cut first, **[2027]** built before invitations, **[If time]** PRD 3.3. Only T1–T3 are in scope for v1 stories.

## Requirements Inventory

### Functional Requirements

**5.1 Personal links and access**

- FR-1 (T1): Each guest has their own personal link with a long random code that cannot be guessed; the link is the guest's only login (no accounts or passwords).
- FR-2 (T1): A link opens the guest's household and nothing else: the invitation, the household's answers, its total and its payment information.
- FR-3 (T1): Opening a link never changes anything; only a deliberate action (pressing a button) saves data.
- FR-4 (T1): Page titles and link previews are the same for everyone and contain no names.
- FR-5 (T1): Without a valid link (unknown, deactivated or bare address), the site shows only a friendly "private invitation, contact the couple" message with no names, phone numbers, date or place.
- FR-6 (T1): With a valid link, the couple's contact details are on every guest page, including error pages.

**5.2 Invitation and information pages**

- FR-7 (T1): The front page looks like an invitation; without scrolling on a phone it shows the couple's names, date and place, the invited household's names and the RSVP deadline, with "Svar" in a sticky menu button and as a link in the deadline line, both jumping to the RSVP button after the information and the child-free note.
- FR-8 (T1): Below the invitation, one entry each for Programme, Practical information and Our story (picture, one line, "Read more" to its own page), followed by the RSVP panel with child-free note, deadline and RSVP button.
- FR-9 (T1 page, full text T2): The programme shows the weekend day by day (incl. cabin ready/empty times), marks what costs money, says what to bring and that everything is voluntary; rebus, sauna/hot tub and yoga are information only.
- FR-10 (T1 page, full text T2): Practical information covers the ceremony in Strandebarm kirke with its time, address and directions, transport and parking, the venue and cabins, the area, dress code, house rules and what to bring.
- FR-11 (T1): Every information page has an obvious way back to the invitation.

**5.3 RSVP form**

- FR-12 (T1): The form shows "I am [name]", preset to the link's owner; the respondent can switch to another household member, and the choice records who answered.
- FR-13 (T1): The form goes step by step, one task per step, with a visible Back link and a progress indicator.
- FR-14 (T1): Step 1 marks each person "Coming"/"Not coming" with nothing preselected; step 2 asks whether everyone coming is there the whole weekend, and "No" lets the respondent choose days per person.
- FR-15 (T1): Later steps ask only about people who are coming and only for their days; a meal is offered only on days present, and Saturday breakfast only to those present from Friday.
- FR-16 (T1): Per coming person, yes/no to staying overnight; the form says a cabin is booked for the whole weekend and both nights are paid.
- FR-17 (T1): Each person present on Friday is asked about the Friday mountain hike: yes, no or maybe.
- FR-18: Removed 2026-11-11 (expected arrival).
- FR-19 (T2): "Read more" inside a step opens in place, so the respondent never leaves the form.
- FR-20 (T2): Leaving the form before sending shows a warning that the answer is not sent yet.
- FR-21 (T1): A check page says at the top that the answer is not sent yet, shows every answer per person and the household total with a "Change" link per part, shows skipped optional questions as "Not provided", and has the button "Send answer".
- FR-22 (T1): Errors appear next to the field with a fix hint; after a failed attempt, a summary at the top lists each error and links to its field.
- FR-23 (T1): After sending, a receipt confirms with a message for coming or not coming; "You can now safely close the invitation" appears with the payment choice, or straight away when nothing is owed.
- FR-24 (T1): Once answered, the invitation shows the household status: a sent line at the top with a link down, and a status block in the RSVP section's place (sent by whom and when, total, reported paid, deadline, "See or change answer").
- FR-70 (T1): Each day is shown with its date and what happens; the form stops contradicting answers (e.g. overnight while present only one day) and explains why.
- FR-78 (T1): An unsent answer is kept on the guest's own device across leaving, app switches and reloads, and is offered back on return through the link.

**5.4 Allergies and consent**

- FR-25 (T1): Per coming person, enter allergies/dietary needs (fixed categories gluten, lactose, nuts, shellfish, vegetarian, vegan, other, plus a short note; no diagnoses) or choose "No allergies or dietary needs"; the question is optional.
- FR-26 (T1): Allergy information, including "No allergies or dietary needs", is saved only with consent through a separate Yes/No choice that starts unanswered; the consent text states the purpose, who sees it, that names and allergies go to Hardingasete's kitchen, and that consent can be withdrawn through the link.
- FR-27 (T1): When entering allergies for others, the respondent confirms that those people know and agree.
- FR-28 (T1): The RSVP can always be sent without consent; if allergies are entered without consent, the form says before sending that they will not be saved and the guest can tell the couple directly.
- FR-29 (T1, moved from T2 on 2026-11-16, see the Epic List): Consent is stored per person: when, who gave it (the person, another household member or the couple) and which consent text version was shown.
- FR-30 (T2): Consent can be withdrawn through the personal link at any time, also after the deadline; withdrawal deletes that person's allergy information and marks the household "Changed".
- FR-31 (T3): The couple registers consent for a guest only after sending the consent text and getting a yes; the site records who registered it, the channel, the text version and when.

**5.5 Prices, total and payment for guests**

- FR-32 (T1): The price of each paid option (cabin for the whole weekend, Friday dinner, Saturday breakfast, Sunday breakfast) is shown before choosing, with a short note on why guests pay.
- FR-33 (T1): The household total is visible along the way, identical on check page and receipt, and always calculated from answers and current prices.
- FR-34 (T1): After sending, a household that owes something chooses "Pay now" (amount, Vipps number, account number, payment message) or "Pay later" (the link always shows what is owed).
- FR-35 (T2): The guest can report "I have paid" with amount (prefilled), method (Vipps or bank) and who paid if someone else; afterwards they see what and when they reported and can correct it.
- FR-36 (T2): If the total changes after a payment report, the guest sees what remains to pay, or that the couple has been told and will refund the difference.
- FR-71 (T1): Each household has its own payment message, "Bryllup" + the household's names; the couple can adjust it, and the site warns if two households would get the same message.

**5.6 Changing an answer, deadline and lock**

- FR-37 (T2): Before the deadline, once answered, the RSVP button becomes "See or change answer" and opens the form prefilled.
- FR-38 (T2): The form shows who last updated the answer and when; if someone else in the household sends after the respondent opened the form, the site shows that answer (who, when, what differs) before the respondent can send; no silent overwrite.
- FR-39 (T2): A household is marked "Changed" when a guest or the couple changes a sent answer, or consent is withdrawn; the first answer and payment reports don't count.
- FR-40 [2027]: Full change history per household; for allergies only that they changed, never the content.
- FR-41 (T1): The RSVP deadline is a date; guests can answer until 23:59 Norwegian time that day; shown with weekday, date and time next to the RSVP button and in the status; all times are Norwegian time.
- FR-42 (T2): After the deadline guests can't change attendance, days, meals, overnight, hike or allergies; the button says "See answer" with deadline text and contacts; payment info, "I have paid", info pages and consent withdrawal still work; never-answered households see the same message.

**5.7 Questions to the couple**

- FR-43, FR-44, FR-45: Removed 2026-11-15 ("Ask us" form).

**5.8 Admin access and roles**

- FR-46 (T1 couple login, T2 helper role): Admin users log in with username and password; the couple has full access, helpers see everything and change nothing.
- FR-47 (T1): Rikke creates admin accounts for the couple and helpers with a command; no self-registration.
- FR-48 (T1 basic responsive, beyond that T3): Quick tasks work well on a phone (find a guest, copy their link, see whether they answered); the full overview also works on a phone.

**5.9 Guest list and links**

- FR-49 (T2): The couple adds, edits and removes households and guests one by one; each guest has a name and optional phone and email.
- FR-50 (T3): The couple can move a guest to another household.
- FR-51 (T2): The couple can search for a guest by name, copy the guest's link and see contact details.
- FR-52 [2027]: Copy a warm, ready-to-send invitation message with the guest's name and link.
- FR-53 (T3): The couple can deactivate a guest's link and create a new one; only that guest's link changes.
- FR-76 [2027]: Record that the invitation was sent (date, channel) and each resend with a reason.

**5.10 Overview and "Needs attention"**

- FR-54 (T1): Below "Needs attention", the admin home shows "answered X of Y households" with a link to the full overview, then a summary in small groups: coming / not coming / not answered (people and households); whole weekend vs not, by day combination; who does not stay overnight and the number of beds; count per meal and per allergy category; coming guests without an allergy answer; households per payment status; hike interest with "maybe" separate.
- FR-55 (T1): Every count opens a list of the people behind it.
- FR-56 (T2): At the very top of the admin home, without scrolling, "Needs attention" lists households not answered, coming guests with nothing registered for allergies, "I have paid" reports without a matching payment (in red), refunds owed and households marked "Changed"; each item can be marked handled/seen and leaves the list; an empty list says so.
- FR-57 (T1 simple, T2 full): A full overview lists every household with who comes, the total and payment status, unanswered first; each household has its own page with every person's answers, contact details and notes; phone and email are tappable on a phone.
- FR-58 (T1): An allergy list shows names and categories for everyone who consented, ready for Hardingasete.
- FR-77 [2027]: Record when a household started; "Needs attention" also lists invitations not marked sent and households that haven't started weeks after sending.

**5.11 Payments**

- FR-59 (T2): The couple registers amounts received and refunds paid back per household; a registration can be corrected or undone.
- FR-60 (T2): Payment status is computed from received minus refunds versus total: nothing to pay, not paid, part paid (X missing), paid, refund owed (X); only admins see it.
- FR-61 (T2): An "I have paid" report matches when received minus refunds is at least the reported amount; a mismatch is marked red in the overview and listed under "Needs attention".
- FR-62 [2027]: One dated contact note per household, shown in the not-answered list and the payment overview.

**5.12 Overrides and settings**

- FR-63 (T2): The couple can fill in or change any household's answer, also after the deadline, with the same form as the guests, recorded with the admin as author.
- FR-64 (T2): The couple can change prices, deadline, contact details and payment details in admin (helpers cannot); a deadline change is repeated in words and confirmed, and a past or near deadline shows how many households would be locked out.
- FR-65 (T3): Changing prices after households have answered warns with the number of households whose total will change.

**5.13 Privacy functions**

- FR-66 (T2): A privacy page explains what is collected and why, who is responsible, the legal basis per kind of data, who can see it, when it is deleted, the guest's rights (incl. withdrawal and complaint to Datatilsynet) and how to contact the couple; linked from every page footer and from the consent question.
- FR-67 [2027]: The couple can delete all guest data in one operation after clear confirmation.

**5.14 Local setup and test data**

- FR-68 (T1): One documented command, separate from starting the app, fills the database with fictional test data: the people from UJ-1 to UJ-3 and households covering the expected-results list (declines entirely; Saturday only without cabin; paid; part paid; refund owed; report without matching payment; not answered; allergy with consent; allergy without consent; withdrawn consent), fictional contacts and a test link per guest, fictional prices/deadline/contacts and obviously invalid payment details, a test couple admin and a test helper.
- FR-69 (T1): An expected-results list is worked out by hand for the test data before the code it checks, committed to the repo, covering counts, totals, payment statuses and the deadline lock, and checked by automated tests.
- FR-72 (T1): Test data never reaches the real site; the seed command refuses to run in production, and test accounts and links exist only in test data.

**5.15 Rules for counts and totals**

- FR-73 (T1): Guests choose the paid meals (Friday dinner, Saturday breakfast, Sunday breakfast); everyone present on Saturday counts for Saturday lunch and dinner, which are not asked about; meals don't depend on staying overnight.
- FR-74 (T1): Each person is coming, not coming or not answered; a household is answered once an answer is sent and coming when at least one person comes.
- FR-75 (T1): When a person becomes not coming or a day is removed, the choices for that person or day are removed too and never count.

**If time (PRD 3.3, not in v1 stories):** envelope animation, Vipps QR code, print page for Hardingasete, speech sign-up, gift list, English version, wider PC layout.

### NonFunctional Requirements

- NFR-1 Reliability: links work from sending until deletion and the link format never changes after invitations; links are short and safe in SMS, Messenger and email; saving either succeeds and says so, or fails with a clear message and keeps what the guest entered; production availability and the PRD 3.2 operations rules apply in 2027.
- NFR-2 Correct numbers: all counts, totals and payment statuses are calculated from stored answers and payments, never stored; amounts are whole kroner; automated tests check admin counts and totals against the expected-results list.
- NFR-3 Privacy: GDPR applies and allergies are health data; Rikke and Valdemar are joint controllers; the legal basis table in the PRD applies; only necessary data; only fictional data in the repo, tests, screenshots, usability test and AI tools; real data only in EU/EEA production, deleted by 31 August 2028.
- NFR-4 Security: link codes ≥ 128 bits of randomness with no personal data; guest pages hidden from search engines and never leak the link; repeated wrong-link attempts slowed (T3); modern password hashing; admin sessions expire after inactivity; CSRF protection; repeated login attempts slowed; only logged-in admins see guest answers beyond a household's own; the server stops helpers from changing data; no secrets in the repo.
- NFR-5 Accessibility (WCAG 2.2 AA): text contrast ≥ 4.5:1; guest body text ≥ 18 px; works at 200% zoom and 320 px width; full keyboard use with visible focus; guest touch targets ≥ 44 × 44 px; every field labelled, errors per FR-22; don't ask for what the link knows; animation respects reduce motion and can be skipped.
- NFR-6 Ease of use: phone first for all ages (PC shows the phone layout); one obvious next step per screen; plain, warm Norwegian bokmål, also in errors; an older guest completes a household RSVP correctly and alone in under 10 minutes.
- NFR-7 Performance and size: pages load in under 3 seconds on an ordinary phone on 4G; sized for about 70 guests and 5 admin users.
- NFR-8 Runnability: runs locally on Windows, macOS or Linux by following the README, with no separate database server and none of Rikke's accounts or keys; install, start and tests take no more than 15–20 minutes.
- NFR-9 Maintainability: linter and formatter; all tests run with one command; settings that differ between local and production documented in `.env.example`; stories refer to PRD requirement IDs.

### Additional Requirements

From ARCHITECTURE-SPINE.md (AD = architecture decision). There is **no third-party starter template**: Epic 1 Story 1 sets up the project from `django-admin startproject` with uv, following the Structural Seed.

- **Project setup (Story 1.1):** Python 3.14 pinned in `.python-version`, `requires-python = ">=3.14,<3.15"`, uv for dependencies (`pyproject.toml`, `uv.lock`), Django 6.1.x, pytest + pytest-django, Ruff (lint + format), djLint (templates), WhiteNoise; layout `config/`, `wedding/` (models, rules/, services/, rsvp/, selectors.py, links.py, management/commands/, fixtures/), `guests/`, `dashboard/`, `static/` (css, js, fonts, img), `tests/`.
- **CI:** a GitHub Actions workflow runs `uv run pytest`, Ruff and djLint on every push and pull request.
- **AD-1:** one server-rendered Django monolith; every page is a template; guest and admin pages work fully without JavaScript; scripts only enhance; the running-total fragment is the only non-page endpoint.
- **AD-2:** all rules (applicable questions, totals, counts, payment status, guest balance, allergy state, report match, lock state, derived payment message, `normalise_answer`) live only in `wedding/rules/` as pure functions with plain values and explicit `now`; counts are lists of ids; a test checks that `rules` imports nothing from Django or the project.
- **AD-3:** only `wedding/services/` writes; each service is one `transaction.atomic()` block with its side effects; each takes an explicit actor (guest, admin, system); guest services refuse ids outside the actor's household, with a cross-household test per write service.
- **AD-4:** facts stored, derived values never stored (see the spine's stored list); payments have kind `received`/`refunded`, positive integer amount, undo via `voided_at`, never deleted; households/guests with payments can't be deleted until voided.
- **AD-5:** SQLite everywhere through the ORM only (no raw SQL); busy `timeout`, WAL via `init_command`, `transaction_mode: IMMEDIATE`, no `ATOMIC_REQUESTS`.
- **AD-6:** link code from `secrets.token_urlsafe(16)` (22 chars), stored plain, unique, indexed; one resolver in `wedding/links.py` turns a code into a guest actor; URL `/<code>/`; unknown code or bare `/` shows the FR-5 page; GET never writes; codes and "Kopier lenke" rendered only for the couple; only the seed command sets fixed codes.
- **AD-7:** one RSVP form in `wedding/rsvp/`, mounted at `/<code>/svar/` and `/admin/husstand/<id>/svar/`; each step a plain POST with POST-redirect-GET (200 on errors); server renders the total on each step, and `POST …/svar/sum/` returns it as an HTML fragment for script enhancement; a price change between check page and send re-shows the check page; "Read more" is `<details>`.
- **AD-8:** the unsent answer lives only in a signed, compressed, HttpOnly, SameSite=Lax cookie scoped to the form path (Secure in production); nothing stored before "Send answer"; deleted on send and "Begynn på nytt"; guest views never touch `request.session` or the messages framework (tested); the largest household's draft fits 4 KB (tested).
- **AD-9:** `HouseholdAnswer.revision` increments on every send, override, consent withdrawal and guest add/move/remove; send compares the draft's revision in the same IMMEDIATE transaction and writes nothing on mismatch.
- **AD-10:** custom `wedding.User(AbstractUser)` with `role` (`couple`/`helper`) as `AUTH_USER_MODEL` from the first migration; guests are not users; every admin write service calls `require_couple(actor)`; admin session cookie scoped to `/admin/`; accounts only via a management command.
- **AD-11:** `USE_TZ = True`, `TIME_ZONE = "Europe/Oslo"`; one deadline function in `rules/` decides "after 23:59:59 Oslo time on the deadline date", tested on both sides and across a DST boundary; it locks only guest sends that change answer content.
- **AD-12:** all money is `int` whole kroner; `guest_balance(total, report)` is the only money function guest pages use; `payment_status(total, received, refunded)` is admin-only; guest views never read payment rows.
- **AD-13:** admin `SESSION_COOKIE_AGE` 20 hours with `SESSION_SAVE_EVERY_REQUEST`; no expiry warning; "Logg ut" on every admin page.
- **AD-14:** all settings from environment variables with safe local defaults (runs with no `.env`); `.env.example` lists every variable; `APP_ENV` local/production, and production refuses to start with DEBUG on, default SECRET_KEY or empty ALLOWED_HOSTS; seed refuses to run in production.
- **AD-15:** all assets self-hosted; every guest response sends `noindex` (meta + `X-Robots-Tag` middleware) and `Referrer-Policy: same-origin`, titles without names, external links `rel="noreferrer"` (tested); a logging filter masks link codes; guest form views use `sensitive_post_parameters`; 404/500/CSRF pages under `/<code>/` show the couple's numbers when the code resolves.
- **AD-16:** seed data and expected results are TOML files in `wedding/fixtures/` read with `tomllib`; expected results written by hand first; the seed command builds data via services with the system actor and sets the deadline relative to the seeding day; data obviously fake (`example.com`, impossible phone numbers, invalid account check digit); tests assert every count, total, status, allergy state and the lock with explicit `now`; changing the oracle is a deliberate commit with a reason.
- **AD-17:** info-page text lives in templates in v1 (editable plain text is [2027]).
- **AD-18:** allergy data and "Ingen allergier eller matbehov" stored only with consent; per send, consent per person is unchanged / given / refused (unanswered on re-send = unchanged); a draft never carries a consent "Ja" across a revision change; withdrawal deletes allergy data, bumps revision, marks changed; one rule gives each coming guest exactly one admin state: *Har allergier eller matbehov*, *Ingen allergier eller matbehov* or *Ingen allergiopplysninger lagret*.
- **AD-19:** `Household.changed_at` set by one helper, called only by changed-answer and consent-withdrawal services; attention items computed by rules with kind, subject and event time; handled marks store kind, subject, `handled_at`, and an item reappears when its event time is later.
- **AD-20:** confirmations are a preview POST that writes nothing, then a second POST calling the service; undo is a reversing service; every write form carries a one-time submission id; every write service records it in one `Submission` row under a unique constraint in the same transaction, checked before the AD-9 revision check, so repeats (also a double tap on a re-send) return the earlier result.
- **Conventions:** code and identifiers in English, everything user-facing in Norwegian bokmål (`LANGUAGE_CODE = "nb"`), Norwegian URL paths; naming (singular models, verb services, rule functions named for what they return); every rule function, service and test names its FR/NFR in the docstring; services raise their own exceptions shown per FR-22; one CSS file with DESIGN.md tokens as custom properties, small vanilla JS, self-hosted fonts, no build step.
- **Throttling:** one shared limiter on Django's database cache (`createcachetable`, set `MAX_ENTRIES`) for failed logins (T2) and unknown link codes (T3).
- **Manual test plan:** one real-browser form POST is in the manual test plan (Django's test client sends no browser headers).
- **Deferred to 2027 (not v1 stories):** hosting, domain, HTTPS, backups, monitoring, error reporting, update rules, device floor, Django 6.2 LTS upgrade (issue #13), FR-40, FR-67, FR-76, FR-77, editable info pages.

### UX Design Requirements

From DESIGN.md (visual) and EXPERIENCE.md (behaviour). Surface IDs (G1–G12, A1–A12) are EXPERIENCE.md's.

**Foundation and tokens**

- UX-DR1: Implement the DESIGN.md colour tokens (page-green, green-dark, green-dark-hover, panel-cream, ink, ink-muted, cream-on-green, field-surface, field-border, divider, focus-on-panel, focus-on-green, error, success, warning, scrim), spacing scale and radii as CSS custom properties in one stylesheet; light only with `<meta name="color-scheme" content="light only">`.
- UX-DR2: Self-host Imperial Script and EB Garamond (regular, italic, 600) as WOFF2 Latin subsets with æ/ø/å, keeping `lnum`/`tnum`; type built in `rem`; guest body 20px; lining figures for numbers and tabular in tables; non-breaking thousands space; `overflow-wrap: break-word` and `hyphens: auto` with `lang="nb"`; Imperial Script only for the names (48px hero, 40px signature).
- UX-DR3: Paper sheet surface: cream sheet with grain/fibre texture and the `edge-b3` SVG filter edge and shadow on a `::before` layer behind content; flat `panel-cream` with 5px radius fallback; 1px `CanvasText` border under forced colours. Textured page green with the calm grain; texture never shifts the average colour.
- UX-DR4: Prepare the image assets from Rikke's files (seal, gypsophila, lily garlands, lace frame, hero illustration 04, venue and couple photos, the twelve programme icons, favicon from the seal) in `static/img/`, all decorative ones with `alt=""`.
- UX-DR5: Page layout: one centred column max 480px; gutters 16px, 12px between 260–340px, 8px below 260px; no horizontal scroll at 320px or 200% zoom (180 CSS px); every image `max-width: 100%`.

**Guest components**

- UX-DR6: Nav bar: flat page-green, 64px, nav words Program · Praktisk · Vår historie (18px cream, current page underlined, `aria-current`), "Svar" button (green-dark, 1px cream border, ≥ 64×44px; 56px below 340px); sticky only when the viewport is ≥ 400px tall; tighter spacing below 340px; never a hamburger; `html { scroll-padding-top }` = bar height + 12px.
- UX-DR7: Hero sheet in the fixed order (seal over top edge, illustration whole, names as `h1`, invites line by the du/dere rule, gypsophila, date and place in small capitals, «for <household>», short deadline line with the "Svar" link), fitting above the fold at 360×560 and 320×568; names stack on three lines rather than shrink.
- UX-DR8: Lead-in line and «Alt om helgen» section on the green: lily garlands top and bottom, italic `h2` with cream hairline, three topic rows (lace-framed picture 136px left, `h3` title, italic line, «Les mer» outlined button on green with accessible names), stacking below ~300px.
- UX-DR9: RSVP sheet (`id="svar"`): heading, small gypsophila, «Barnefritt bryllup», full deadline «Svar innen <weekday date> kl. 23:59», primary button; warning notice above the button when a draft exists.
- UX-DR10: Status block (`id="status"`) replacing the RSVP sheet once answered, and the hero line «Svar sendt <date> · Se svaret»; nav "Svar" then targets the status block; after the deadline the button is «Se hele svaret»; never-answered after deadline shows «Svarfristen gikk ut … · Ring oss».
- UX-DR11: Footer band (green-dark): «Spørsmål? Send oss en melding:», each phone number its own ≥ 44px `tel:` row, «Personvern» link; on every valid-link guest page including error pages.
- UX-DR12: Info page frame: back link «← Tilbake til invitasjonen», italic centred title with hairline, jump links (`nav aria-label="Hopp til"`, small capitals, balanced lines, ≥ 44px, targets with `tabindex="-1"` and `scroll-margin-top`), one info sheet per part, bottom back button on green.
- UX-DR13: Programme timeline: one `ol` per day, alternating sides via CSS only, 6px dots on a centre line, icon 56px, `<time>` elements, «Godt å vite» list per day; one-sided below ~260px.
- UX-DR14: Story sheet for Vår historie: lace-framed photo, chapters with italic time · place `h2` lines, closing line, signature in Imperial Script.
- UX-DR15: Buttons: primary (green-dark, 52px, full width, "Sender …" busy state ignoring repeat taps), secondary (outlined, below primary in forms), outlined on green, destructive (rust outline, tier 3 only, placed apart); focus ring 3px/3px offset coloured by surface; never `outline: none`.
- UX-DR16: Form controls: text field (label above, italic hint below, error between label and field, `aria-describedby`, `aria-invalid`); choice control (26px box, whole row ≥ 44px, every group a `fieldset`/`legend`, group error under the legend as icon + «Feil: …»); forgiving amount input ("900", "900 kr", "1 450").
- UX-DR17: Notice component in four variants (success check, warning circle-!, error triangle-!, info "i") with 4px left rule, word prefixes «Feil:»/«Obs:»; never auto-dismiss on guest pages; live regions only for changes after load.
- UX-DR18: Error summary: focused on reload after a failed step, heading «For å gå videre må du rette opp følgende feil.», each item links to and focuses its field; `<title>` prefixed «Feil: ».
- UX-DR19: Form step layout: step question as `h1`, progress line «Steg n av m: <name>» (m changes only when who comes or which days change), respondent line «Jeg er <name> · Bytt» on every step (Bytt is a button with `aria-expanded`), one fieldset per person, running total on paid steps (`aria-live` polite), «Fortsett» above «Tilbake»; page title «Steg n av m: <name> – Invitasjon»; no nav bar in G4–G6.
- UX-DR20: Form step order: 1 who is coming → 2 whole weekend? / days per person → 3 overnight → 4 meals → 5 allergies and consent → 6 Friday hike (only if someone comes Friday) → check page; each step has its own address and the browser Back button is safe.
- UX-DR21: Allergy step: per person «Ingen allergier eller matbehov» exclusive with the categories (script clears the other; without script an inline error asks to choose one); consent block with purpose, recipients and withdrawal text before an unanswered Ja/Nei inside the fieldset; «Jeg bekrefter at <name> vet om dette og er enig» only when answering for others; «Personvern» link returns to the same step with answers kept.
- UX-DR22: Read-more disclosure as `<details>` with underlined «Les mer om …», chevron and divider left rule; never navigates away.
- UX-DR23: Check page: warning notice «Obs: Svaret er ikke sendt ennå.», `h1` «Se over svaret før du sender», one block per part with «Endre» (hidden context, returns to the check page after «Fortsett»), «Ikke oppgitt» for skipped optional answers, total, «Send svaret» above «Tilbake»; allergy-without-consent warning; conflict notice.
- UX-DR24: Receipt: success notice with `h1` «Svaret er sendt» and sent-by line, Rikke's coming/not-coming message by the du/dere rule, summary «Dette har dere svart», total, «Betal nå» above «Betal senere» with «Du kan nå trygt lukke invitasjonen.» directly below (or after the summary when nothing is owed).
- UX-DR25: Payment details sheet «Slik betaler du»: amount, Vipps number, account number and payment message as selectable text; «Kopier» buttons only when the clipboard is available, «Kopiert» in a polite live region, failure selects the value with «Trykk og hold for å kopiere»; «Jeg har betalt» below.
- UX-DR26: Draft offer and draft notice: G2 notice «Du har et svar som ikke er sendt ennå.»; opening the form by any route first shows «Vil du fortsette der du slapp?» with when it was started, «Ja, fortsett» and «Nei, begynn på nytt»; not offered after the deadline.
- UX-DR27: Leave warning: in-page links from G4–G5 open a dialog («Svaret er ikke sendt ennå. Det du har fylt ut, er tatt vare på på denne telefonen.» · «Bli og fullfør svaret» · «Gå uten å sende»), plus the browser's own `beforeunload` prompt where supported.
- UX-DR28: Last-updated info notice and conflict warning at the top of G4/G5 (who, when, what differs).
- UX-DR29: Dialog component: `role="alertdialog"`, labelled by heading, described by the consequence sentence, focus to the safe button (tier 2) or heading (tier 3), trapped; cancel returns focus to the trigger, confirm moves focus to a `role="status"` result message; Esc and scrim tap cancel; scrolls at 200% zoom; works without script as a server-rendered confirm page (AD-20).
- UX-DR30: G1 no-valid-link page: one paper sheet on green, «Dette er en privat invitasjon», gypsophila, «Virker ikke lenken din? Ta kontakt med brudeparet direkte.», a plain «Personvern» link below; no nav, no footer, no seal.
- UX-DR31: G12 privacy page in the info-page frame with parts Hva vi lagrer, og hvorfor · Hvem som ser det · Når det slettes · Rettighetene dine · Trekke samtykket; the last sheet lists each household member with stored allergy data and «Trekk samtykket for <name>» (or «Ingen allergiopplysninger lagret.»); from G1 only the general parts.
- UX-DR32: Consent withdrawal dialog: «Trekke samtykket for <name>?», «Allergiopplysningene til <name> slettes. …», «Avbryt» focused, primary «Slett allergiopplysningene»; afterwards «Allergiopplysningene til <name> er slettet.»; reachable from the answer view and the privacy page, also after the deadline.
- UX-DR33: G9 locked answer view: read-only answers, «Fristen gikk ut <weekday date> kl. 23:59» with contacts; payment, «Jeg har betalt», info and consent withdrawal still available.

**Admin components**

- UX-DR34: Admin frame: flat page-green (no texture), Admin nav (Oversikt · Gjester · Betalinger · Innstillinger · Logg ut, not sticky, `aria-current`), admin-panel (cream, straight edges, 12px padding, 8px gap), `admin-title` 28px cream titles, 18px admin body, 44px targets; no seal, illustration or script.
- UX-DR35: Helper read-only mode: action buttons hidden (not greyed), form values shown as text, the line «Du kan se alt, men ikke endre noe.» under the nav; no link codes or «Kopier lenke».
- UX-DR36: A1 login: username and password with paste and password managers allowed; plain error; slowed retries; «Du ble logget ut fordi du var borte en stund.» after expiry.
- UX-DR37: A2 attention panel: 5px green-dark top rule, `h2` «Trenger oppfølging (n)», as many items as fit while the answer progress stays on the first screen, then «Vis alle n»; payment mismatches first; items with reason (600 weight), household and detail and one action «Merk som håndtert»/«Merk som sett» with hidden context; empty state with check icon «Ingenting trenger oppfølging nå» and «Vis håndterte».
- UX-DR38: Undo in place: the handled row is replaced by «Merket som håndtert. Angre» with focus on «Angre», no timer; «Vis håndterte» filter to unmark later.
- UX-DR39: A2 answer progress: «Svart: X av Y husstander» (20px, 600), decorative bar (`aria-hidden`), Kommer / Kommer ikke / Ikke svart ennå rows (persons · households, each a link), «Se hva alle har svart» → A4.
- UX-DR40: A2 summary panels in order Når kommer de? · Overnatting · Mat · Allergier (med samtykke) · Fjelltur fredag · Betaling (husstander som kommer); each row label left, count right as a link to A3 (0 is plain text), lead and indented breakdown rows, «Én person kan ha flere allergier.» note; hike «5 kommer, 2 kanskje» with separate links.
- UX-DR41: A3 count drill-down: the people behind a count; zero not a link.
- UX-DR42: A4 Gjester: title, count «N husstander · M gjester», search «Finn en gjest» (on submit, polite live region «3 treff» / «Fant ingen med det navnet.»), «Legg til husstand», household rows (name link, status tag, one summary line), unanswered first, then needing follow-up, then by name; empty state «Ingen husstander ennå. Legg til den første.»; may become a table on PC.
- UX-DR43: A6 household page: back link «Alle gjester», panels Svar (sent by and when, per-person answers, tappable phone/email, «Endre svaret» → A7), Betaling (total, status tag, «Se betalingene»), Lenker («Kopier lenke» per person with «Kopiert», couple only), Husstanden («Endre navn og kontaktinfo», «Fjern husstanden» destructive and apart).
- UX-DR44: A6a add/edit household: one fieldset per person («Navn» required with hint «Slik navnet skal stå på invitasjonen.», «Telefon (valgfritt)», «E-post (valgfritt)»), «Legg til en person til» moves focus to the new name field, «Fjern <name> fra husstanden» (tier 3, hidden when one person left), «Lagre husstanden»/«Lagre endringene» (tier-2 dialog naming what changes, incl. payment message and duplicate warning), «Avbryt» link; input kept on errors.
- UX-DR45: A9 payments: list with «Til sammen» panel (Skal betales · Mottatt · Mangler · Skal betales tilbake) and household rows sorted stemmer ikke → skal ha tilbake → delbetalt → ikke betalt → betalt → ingenting å betale; household payment page with Status, Registrert (dated rows with «Angre»), Registrer betaling (Mottatt fra gjesten / Betalt tilbake til gjesten, Beløp, hint «Dagens dato settes selv.», tier-2 confirm naming the new status), Betalingsmelding (→ A10); after saving «Registrert: mottatt 300 kr.» with «Angre»; empty «Ingen betalinger registrert ennå.».
- UX-DR46: A10 payment message edit with duplicate warning before saving.
- UX-DR47: A12 settings: prices, deadline, contacts, Vipps/account; tier-2 confirm repeats the deadline in words and shows lock-out count, price-change count; helpers read only.
- UX-DR48: A5 allergy list: consented names and categories; empty «Ingen allergier registrert ennå.».
- UX-DR49: Status tags: outlined, text + icon, mapping Betalt → success; Ikke betalt, Delbetalt X mangler, Skal ha tilbake X, Ikke svart → warning; Stemmer ikke → error; Ingenting å betale, Endret → info; never colour alone.
- UX-DR50: Admin protection tiers: tier 1 no confirm + undo in place; tier 2 consequence dialog (payments, older-payment undo, household edit, new link, settings, price change, move guest, register consent); tier 3 typed «FJERN» (case and surrounding spaces ignored, `autocapitalize="off" autocorrect="off" spellcheck="false"`, button stays enabled, mismatch gives inline error).

**Cross-cutting**

- UX-DR51: Voice and tone: plain warm bokmål; the site calls itself «invitasjonen»; du when one person is invited, dere when two or more (receipt, lead-in, invites line, status block); every error says how to fix it; admin text neutral and brief. Use the decided microcopy from EXPERIENCE.md › Voice and Tone; proposals stay editable.
- UX-DR52: State patterns everywhere: saving ("Sender …"/"Lagrer …" with data kept), saved notice with what and when, save failed (what happened, nothing lost, «Prøv igjen», guest-side phone numbers, input kept also after an expired form token).
- UX-DR53: Accessibility floor checks: one `h1` per page, `lang="nb"`, page titles without names, decorative characters (· and ←) `aria-hidden`, focus never hidden under the sticky bar (2.4.11), forced-colours styles (blend off, choice marks visible, buttons outlined, panel borders), reflow checked at 360×560, 320×568 and 180×320.
- UX-DR54: Interaction limits: tap, scroll and type only (no swipe, long-press, drag, carousels, autoplay, hover-only controls, infinite scroll); smooth scroll only under `prefers-reduced-motion: no-preference`; no skeletons or spinners on guest pages.

### FR Coverage Map

| FR | Epic | Brief description |
|---|---|---|
| FR-1 | 1 | Personal link per guest, 128-bit code |
| FR-2 | 1 | Link opens only the guest's household |
| FR-3 | 1 | Opening a link never writes |
| FR-4 | 1 | Titles and previews without names |
| FR-5 | 1 | Friendly page without a valid link |
| FR-6 | 1 | Couple's contacts on every guest page |
| FR-7 | 1 | Invitation front page with "Svar" twice |
| FR-8 | 1 | Three topics and the RSVP panel |
| FR-9 | 1, 7 | Programme page (page in 1, full text in 7) |
| FR-10 | 1, 7 | Practical information (page in 1, full text in 7) |
| FR-11 | 1 | Way back to the invitation |
| FR-12 | 2 | "I am [name]", switchable |
| FR-13 | 2 | Step by step with progress and Back |
| FR-14 | 2 | Who is coming, then whole weekend / days |
| FR-15 | 2 | Only ask about coming people and their days |
| FR-16 | 2 | Overnight per person, cabin booked for both nights |
| FR-17 | 2 | Friday hike yes/no/maybe |
| FR-18 | — | Removed 2026-11-11 |
| FR-19 | 7 | "Read more" in place inside a step |
| FR-20 | 7 | Warning when leaving an unsent form |
| FR-21 | 2 | Check page |
| FR-22 | 2 | Field errors and error summary |
| FR-23 | 2 | Receipt with coming / not-coming message |
| FR-24 | 2 | Household status block once answered |
| FR-25 | 2 | Allergy categories or "No allergies" |
| FR-26 | 2 | Stored only with explicit consent |
| FR-27 | 2 | Confirm others know and agree |
| FR-28 | 2 | Sending works without consent, with warning |
| FR-29 | 2 | Consent record per person (pulled forward from T2, see Epic 2) |
| FR-30 | 7 | Withdraw consent, also after the deadline |
| FR-31 | 8 | Couple registers consent (T3) |
| FR-32 | 2 | Prices shown before choosing |
| FR-33 | 2 | Household total, always calculated |
| FR-34 | 2 | Pay now / pay later |
| FR-35 | 5 | "I have paid" report |
| FR-36 | 5 | Remaining amount or refund after a change |
| FR-37 | 4 | "See or change answer" |
| FR-38 | 4 | Last updated and no silent overwrite |
| FR-39 | 4 | "Changed" marker |
| FR-40 | [2027] | Full change history |
| FR-41 | 2 | Deadline 23:59 Oslo time, shown in full |
| FR-42 | 4 | Lock after the deadline |
| FR-43–45 | — | Removed 2026-11-15 |
| FR-46 | 3, 6 | Admin login (couple in 3, helper role in 6) |
| FR-47 | 3 | Admin accounts by command |
| FR-48 | 3, 8 | Phone-friendly admin (basic in 3, beyond in 8) |
| FR-49 | 6 | Add, edit, remove households and guests |
| FR-50 | 8 | Move a guest (T3) |
| FR-51 | 6 | Search, copy link, contact details |
| FR-52 | [2027] | Ready-to-send invitation message |
| FR-53 | 8 | Deactivate link and issue a new one (T3) |
| FR-54 | 3 | Answer progress and summary |
| FR-55 | 3 | Every count opens the people behind it |
| FR-56 | 6 | "Needs attention" |
| FR-57 | 3, 6 | Full overview (simple in 3, household pages in 6) |
| FR-58 | 3 | Allergy list for Hardingasete |
| FR-59 | 5 | Register received and refunded amounts |
| FR-60 | 5 | Computed payment status |
| FR-61 | 5 | Report match and mismatch in red |
| FR-62 | [2027] | Contact note |
| FR-63 | 4 | Couple override with the same form |
| FR-64 | 4 | Settings: prices, deadline, contacts, payment details |
| FR-65 | 8 | Price-change warning (T3) |
| FR-66 | 7 | Privacy page |
| FR-67 | [2027] | Delete all guest data |
| FR-68 | 1, 2, 5 | Seed command (households and links in 1, answers in 2, payments in 5) |
| FR-69 | 1, 3 | Expected-results list (written in 1, asserted by tests in 3) |
| FR-70 | 2 | Dates per day and no contradictions |
| FR-71 | 2, 5 | Payment message (shown in 2, adjusted by the couple in 5) |
| FR-72 | 1 | Test data never in production |
| FR-73 | 2 | Meal counting rule |
| FR-74 | 2 | People and household answer states |
| FR-75 | 2 | Removed choices never count |
| FR-76 | [2027] | Invitation sent record |
| FR-77 | [2027] | "Started" and unsent-invitation attention items |
| FR-78 | 2 | Unsent answer kept on the device |

## Epic List

The epics follow the PRD's priority tiers (section 3.1a). Epics 1–3 are the usability-test build (tier 1, 27 November 2026); the usability test in the first week of December is a real feedback point, so it is also an epic boundary. Epics 4–7 complete the course version (tier 2, 10 December 2026), in the PRD's tier-2 order. Epic 8 is tier 3, cut first; anything not done by 10 December moves to [2027] with the reason in the PRD change log. NFRs are cross-cutting and apply to every story; the NFR named under each epic is the one it first makes testable.

Epics 2, 4 and 7 all change the RSVP form in `wedding/rsvp/`. Merging them was considered and rejected: the usability test after Epic 3 may change the form, and the PRD's cut order puts Epic 7's parts last in tier 2. Each table is created by the first story that needs it: `User` (1.1), `Household`, `Guest`, `Settings` (1.2), `HouseholdAnswer`, `PersonAnswer`, `Allergy`, `Consent`, `Submission` (2.6), `PaymentReport` (5.1), `Payment` (5.2), `AttentionMark` (6.2), and the cache table for throttling (6.6).

### Epic 1: The guest opens their link and sees the invitation

Bestefar Sigmund opens his personal link on his phone and sees a real invitation: the names, date, place, his household and the deadline, the three topics and their pages, and the way to answer. A wrong link shows only a calm "private invitation" page. The examiner can install the app, fill it with fictional households and open their test links by following the README.

**FRs covered:** FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-9 (page), FR-10 (page), FR-11, FR-68 (households, guests, links, settings, admin test users), FR-69 (the expected-results list written by hand), FR-72
**Also delivers:** project setup and CI (Story 1.1), AD-1, AD-5, AD-6, AD-10 (custom User with role in the first migration), AD-14, AD-15, AD-16 (fixtures), AD-17; UX-DR1–UX-DR9, UX-DR11–UX-DR15, UX-DR30, UX-DR51, UX-DR53, UX-DR54; NFR-4 (link codes), NFR-5, NFR-8, NFR-9

### Epic 2: Guests answer for their household

Sigmund and Arild answer for everyone in their household on a phone: who is coming, which days, overnight stay, meals with prices, allergies with consent and the Friday hike. They see the running total, check everything before sending, get a receipt in Rikke's words, choose to pay now or later, and see their household's status on the invitation afterwards. An interrupted answer is offered back when they return.

**FRs covered:** FR-12, FR-13, FR-14, FR-15, FR-16, FR-17, FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-27, FR-28, FR-29, FR-32, FR-33, FR-34, FR-41, FR-70, FR-71 (derived message shown), FR-73, FR-74, FR-75, FR-78; FR-68 (seeded answers through the send service)
**Also delivers:** AD-2, AD-3, AD-4, AD-7, AD-8, AD-9 (revision introduced), AD-11 (deadline function), AD-12, AD-18, AD-20 (submission id); UX-DR10 (answered, before the deadline), UX-DR16–UX-DR21, UX-DR23–UX-DR26, UX-DR52; NFR-1, NFR-2, NFR-3, NFR-6
**Deviation from the PRD tiers:** FR-29 (consent record: who, when, text version) is pulled forward from tier 2. Consent is stored in this epic anyway, and AD-3 already makes every service record its actor; adding the record later would mean a second migration of the same model.

### Epic 3: The couple sees the numbers and can trust them

Rikke logs in and sees how many households have answered, the summary in small groups, the people behind every count, a simple overview of every household and the allergy list for Hardingasete. The automated tests prove that every count, total and payment status matches the expected-results list worked out by hand.

**FRs covered:** FR-46 (couple login), FR-47, FR-48 (basic responsive), FR-54, FR-55, FR-57 (simple overview), FR-58, FR-69 (tests assert the oracle)
**Also delivers:** AD-10, AD-13, AD-16 (oracle tests); UX-DR34, UX-DR36, UX-DR39, UX-DR40, UX-DR41, UX-DR42 (simple list), UX-DR48, UX-DR49; NFR-2, NFR-4 (password hashing, session expiry)

### Epic 4: Guests change their answer until the deadline locks it

Arild changes his household's answer before the deadline and sees who answered last; Marie never overwrites his answer without seeing it first. After the deadline guests can only see their answer, while the couple can still fill in or change any household's answer with the same form. The couple changes the deadline, prices and contact details in Settings, with a clear confirmation.

**FRs covered:** FR-37, FR-38, FR-39, FR-42, FR-63, FR-64
**Also delivers:** AD-9, AD-11 (lock), AD-19 (changed marker), AD-20 (confirm); UX-DR10 (locked states), UX-DR28, UX-DR29, UX-DR33, UX-DR47; SM-11

### Epic 5: Payments are reported, registered and matched

A guest reports "I have paid" and sees what remains or will be refunded if the total changes. The couple registers money received and refunds paid back, can undo a registration, sees each household's computed payment status, and sees mismatched reports in red. The couple can adjust a household's payment message, with a warning for duplicates.

**FRs covered:** FR-35, FR-36, FR-59, FR-60, FR-61, FR-71 (couple adjusts, duplicate warning); FR-68 (seeded payments and reports)
**Also delivers:** AD-4 (payment rows, `voided_at`), AD-12, AD-20 (confirm and undo); UX-DR45, UX-DR46, UX-DR49, UX-DR50 (tier 2); NFR-2

### Epic 6: The couple manages the guest list and follows up

Rikke sees "Needs attention" first when she logs in and marks items as handled. The couple adds, edits and removes households and guests, finds a guest by name and copies their link, and opens each household's own page. Helpers see everything and change nothing, and repeated login attempts are slowed down.

**FRs covered:** FR-46 (helper role), FR-49, FR-51, FR-56, FR-57 (household pages)
**Also delivers:** AD-10 (`require_couple`), AD-19 (attention items and handled marks), throttling on the database cache; UX-DR35, UX-DR37, UX-DR38, UX-DR42, UX-DR43, UX-DR44, UX-DR50 (tier 3 typed FJERN); NFR-4 (login throttling, server-side role checks)

### Epic 7: Guests understand their privacy and get a finished form

Guests can read a privacy page in plain words, withdraw allergy consent for a household member at any time, also after the deadline, open "Read more" inside a step without leaving the form, and get a warning before leaving an unsent answer. The programme and practical information pages get their full text.

**FRs covered:** FR-9 (full text), FR-10 (full text), FR-19, FR-20, FR-30, FR-66
**Also delivers:** AD-18 (withdrawal); UX-DR22, UX-DR27, UX-DR31, UX-DR32; NFR-3

### Epic 8: Cut-first extras (tier 3)

The couple can move a guest to another household, replace one guest's link, register consent given by phone, and is warned when a price change affects households that have answered. The admin pages use a PC screen better, and repeated wrong-link attempts are slowed down. Whatever is not done by 10 December moves to [2027], with the reason in the PRD change log.

**FRs covered:** FR-31, FR-48 (beyond basic responsive), FR-50, FR-53, FR-65
**Also delivers:** AD-6 (new link), AD-9 (revision on move), link-code throttling; UX-DR50 (tier 2 for move, new link and consent); NFR-4 (wrong-link throttling)

**Not in v1 stories:** FR-40, FR-52, FR-62, FR-67, FR-76, FR-77 [2027], and the If-time items in PRD section 3.3.

## Epic 1: The guest opens their link and sees the invitation

Bestefar Sigmund opens his personal link on his phone and sees a real invitation: the names, date, place, his household and the deadline, the three topics and their pages, and the way to answer. A wrong link shows only a calm "private invitation" page. The examiner can install the app, fill it with fictional households and open their test links by following the README.

### Story 1.1: Runnable project with one command for tests and checks

As Ingrid the examiner,
I want to install and start the app and run its tests with a few copyable commands,
So that I can assess it without asking Rikke anything.

**Covers:** NFR-8, NFR-9, AD-1, AD-5, AD-10, AD-11 (settings), AD-14, Structural Seed, Consistency Conventions

**Acceptance Criteria:**

**Given** a clean PC with uv installed and no `.env` file
**When** Ingrid runs `uv sync`, `uv run manage.py migrate` and `uv run manage.py runserver`
**Then** the app starts on localhost with SQLite and needs none of Rikke's accounts or keys
**And** `.python-version` is `3.14`, `requires-python` is `>=3.14,<3.15`, Django is 6.1.x, and every dependency is locked in `uv.lock`

**Given** the repository after this story
**When** the folders are listed
**Then** they follow the Structural Seed: `config/`, `wedding/` (with empty `rules/`, `services/` and `rsvp/` packages, `selectors.py`, `links.py`, `management/commands/`, `fixtures/`), `guests/`, `dashboard/`, `static/` and `tests/`

**Given** the first migration
**When** it is applied
**Then** `AUTH_USER_MODEL` is `wedding.User(AbstractUser)` with a `role` field that is `couple` or `helper` (AD-10)
**And** settings have `USE_TZ = True`, `TIME_ZONE = "Europe/Oslo"`, `LANGUAGE_CODE = "nb"` and the SQLite options from AD-5 (busy timeout, WAL, `transaction_mode: IMMEDIATE`, no `ATOMIC_REQUESTS`)

**Given** `APP_ENV=production`
**When** the app starts with `DEBUG` on, the default `SECRET_KEY` or an empty `ALLOWED_HOSTS`
**Then** it refuses to start with a message naming the problem, and a test proves each of the three cases (AD-14)

**Given** the test setup
**When** Ingrid runs `uv run pytest`
**Then** every test runs with that one command (NFR-9)
**And** one test checks that nothing under `wedding/rules/` imports Django or project modules (AD-2)

**Given** the code checks
**When** `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check` run, locally and in a GitHub Actions workflow on every push and pull request
**Then** all of them pass

**Given** the repository root
**When** Ingrid opens it
**Then** `.env.example` lists every setting with safe example values and no real ones, `.gitignore` keeps out `.env`, `db.sqlite3`, `.venv`, `__pycache__` and collected static files, and `docs/manual-test-plan.md` exists for checks that are not automated
**And** `README.md` describes the app, lists prerequisites with versions, gives the exact install, start and test commands, explains the settings, shows the folder structure and links to the planning documents

### Story 1.2: Households, guests and personal links

As the couple,
I want each guest to have their own unguessable personal link that belongs to their household,
So that the link is the guest's only login and opens nothing but their own household.

**Covers:** FR-1, FR-2, FR-3, NFR-4 (link codes), AD-3, AD-4, AD-6

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `Household`, `Guest` (name, optional phone and email, link code) and a single-row `Settings` (the couple's contact names and phone numbers, prices as whole-kroner integers, the RSVP deadline as a date, Vipps number and account number), and no other tables

**Given** a household is created through `wedding/services/` with an explicit actor
**When** its guests are saved
**Then** each guest gets a code from `secrets.token_urlsafe(16)`: 22 URL-safe characters, unique, indexed and containing no personal data (FR-1, AD-6)
**And** no code outside `wedding/services/` calls `.save()` or `.delete()` on these models (AD-3)

**Given** a code
**When** the one resolver in `wedding/links.py` is called
**Then** a known code returns a guest actor (the guest and their household) and an unknown code returns nothing
**And** tests cover a valid code, an unknown code and a code of the wrong length

**Given** any GET request with a valid code
**When** it is handled
**Then** no database row is created or changed (FR-3), and a test proves it

**Given** two households
**When** the resolver returns the guest actor for a guest in the first
**Then** nothing in the actor gives access to the second household (FR-2)

### Story 1.3: Fictional test data and the hand-made expected-results list

As Ingrid the examiner,
I want one command that fills the database with fictional households and lists a test link for each guest,
So that I can try the invitation as different guests, and the numbers can later be checked against a list worked out by hand.

**Covers:** FR-47 (test accounts), FR-68, FR-69, FR-72, NFR-3, AD-14, AD-16

**Acceptance Criteria:**

**Given** `wedding/fixtures/seed.toml`
**When** it is read
**Then** it describes the people from UJ-1 to UJ-3 (Sigmund and bestemor; Arild, Marie, Filippa and Leone; Synne) and households covering every case in FR-68: declines entirely, comes only on Saturday without a cabin, paid, part paid, owed a refund, an "I have paid" report without a matching payment, not answered, an allergy with consent, an allergy without consent, and a withdrawn consent
**And** each household's planned answers, allergies, consents, payment reports and payments are written as data in the file

**Given** `wedding/fixtures/expected.toml`
**When** it is committed, in its own commit before any code that computes these numbers
**Then** it holds the hand-worked results for the seed data: every FR-54 count, each household's total, payment status and allergy state, and which households are locked at stated `now` values (FR-69, AD-16)
**And** the commit message explains how the numbers were worked out

**Given** a local database
**When** Ingrid runs `uv run manage.py seed_testdata`
**Then** it creates the households and guests with fixed 22-character test codes, the settings (fictional prices, a deadline relative to today so the form is open, the couple's fictional contacts, a Vipps number and an account number with an invalid check digit), and a test couple admin and a test helper
**And** it creates everything by calling services with the system actor, and prints each guest's test link
**And** answers and payments in `seed.toml` are loaded by the stories that build their services (Epic 2 and Epic 5)

**Given** the command has already run
**When** it runs again
**Then** the old test data is replaced, so the result is always the same

**Given** `APP_ENV=production`
**When** the command runs
**Then** it refuses, says why and writes nothing (FR-72)

**Given** the seed data
**When** it is inspected
**Then** every person apart from Rikke and Valdemar is fictional, every email is on `example.com` and no phone number can belong to a real person (NFR-3)
**And** the README lists the command, a test link per guest and the test admin and helper logins

### Story 1.4: The invitation's look and the private-invitation page

As a guest,
I want every page to look like Rikke and Valdemar's printed invitation, and a wrong link to show only a calm "private invitation" page,
So that the invitation feels personal, and a stranger with a wrong link learns nothing about the wedding.

**Covers:** FR-4, FR-5, NFR-5, AD-15, UX-DR1, UX-DR2, UX-DR3, UX-DR4, UX-DR5, UX-DR15, UX-DR30, UX-DR53, UX-DR54

**Acceptance Criteria:**

**Given** the stylesheet
**When** it is loaded
**Then** one CSS file defines every DESIGN.md colour token, the spacing scale and the radii as custom properties, and every page declares `color-scheme: light only` (UX-DR1)
**And** Imperial Script and EB Garamond (regular, italic, 600) are served from `static/fonts/` as WOFF2 with æ, ø and å, type is set in `rem`, guest body text is 20px and numbers use lining figures (UX-DR2)

**Given** a guest content panel
**When** it is rendered
**Then** it is a paper sheet: cream with paper texture, the soft `edge-b3` edge and shadow on a `::before` layer behind the content, a flat `panel-cream` fallback with 5px corners, and a 1px `CanvasText` border under forced colours (UX-DR3)
**And** the page is the textured `page-green`, and the texture leaves the average colour unchanged

**Given** Rikke's images
**When** they are prepared
**Then** the seal, gypsophila, lily garlands, lace frame, hero illustration 04, venue and couple photos and the twelve programme icons are in `static/img/`, and the favicon is made from the seal (UX-DR4)

**Given** primary, secondary, outlined-on-green and destructive buttons
**When** they get keyboard focus or are pressed
**Then** a 3px focus ring at 3px offset shows in the colour for its surface, and no style uses `outline: none` (UX-DR15)

**Given** an unknown or deactivated code, or the bare address `/`
**When** the page opens
**Then** it shows one paper sheet on the green with «Dette er en privat invitasjon», the gypsophila and «Virker ikke lenken din? Ta kontakt med brudeparet direkte.», and no names, phone numbers, date, place, seal, nav bar or footer (FR-5, UX-DR30)
**And** the «Personvern» link under the sheet is added with the privacy page (Story 7.1)

**Given** any guest response, including this page
**When** its headers and HTML are inspected by a test
**Then** it sends `noindex` both as a meta tag and as `X-Robots-Tag`, `Referrer-Policy: same-origin`, a page title with no names, and loads nothing from other sites (FR-4, AD-15)
**And** a logging filter masks link codes in request paths, and a test proves no code is logged

**Given** the page at 360 × 560, 320 × 568 and 180 × 320 CSS px
**When** it is checked in a browser
**Then** there is no horizontal scroll, the gutters follow DESIGN.md › Layout & Spacing, and the check is recorded in the manual test plan (UX-DR5, UX-DR53)

### Story 1.5: The invitation front page

As bestefar Sigmund,
I want my link to open an invitation that shows at once who is getting married, when, where, that bestemor and I are invited and by when to answer,
So that I understand the invitation without scrolling and always see where to answer.

**Covers:** FR-2, FR-6, FR-7, FR-8, FR-11 (page frame), FR-41 (display), NFR-7, UX-DR6, UX-DR7, UX-DR8, UX-DR9, UX-DR11, UX-DR12 (frame), UX-DR51

**Acceptance Criteria:**

**Given** a valid personal link
**When** the guest opens `/<code>/`
**Then** the page shows the sticky nav bar (Program · Praktisk · Vår historie, and the "Svar" button), the hero sheet, the lead-in, «Alt om helgen», the RSVP sheet and the footer band, in that order (FR-7, FR-8)
**And** it shows only that guest's household and nothing from any other (FR-2)

**Given** the hero sheet
**When** it renders
**Then** it holds, in order, the seal over the top edge, the whole illustration, «Rikke & Valdemar» as the page's `h1`, the invites line, the gypsophila, the date and place in small capitals, «for <household names>» and «**Svar** innen <date>» (UX-DR7)
**And** it uses «deg» when one person is invited and «dere» when two or more are (UX-DR51)
**And** the whole hero fits above the fold at 360 × 560 and 320 × 568, the names stack instead of shrinking at narrower widths, and the measurement is recorded in the manual test plan

**Given** the nav "Svar" button or the "Svar" link in the deadline line
**When** the guest activates either, without JavaScript
**Then** the page jumps to the RSVP sheet (`#svar`), which is not hidden under the sticky bar (UX-DR6, UX-DR9)
**And** the nav bar is sticky only when the viewport is at least 400px tall, keeps the three words on one line at 320px, and never becomes a menu button

**Given** «Alt om helgen»
**When** it renders
**Then** it has the top and bottom lily garlands, the italic heading with its hairline, and three topic rows (Programmet, Praktisk informasjon, Vår historie), each with a lace-framed picture, an `h3`, one italic line and «Les mer» with an accessible name such as «Les mer om programmet» (UX-DR8)
**And** each «Les mer» and nav word opens that topic's page under `/<code>/`, which in this story has the info-page frame only: back link, italic title with hairline, the bottom back button, and the current nav word marked with `aria-current` (FR-11, UX-DR12)

**Given** the RSVP sheet
**When** it renders
**Then** it shows «Svar på invitasjonen», the small gypsophila, «Barnefritt bryllup» and the full deadline with weekday, date and «kl. 23:59» in Norwegian time (FR-41, UX-DR9)
**And** the RSVP button itself is added with the form (Story 2.1)

**Given** any page under a valid link
**When** the guest scrolls to the bottom
**Then** the footer band shows «Spørsmål? Send oss en melding:» and each of the couple's phone numbers from Settings as its own `tel:` link at least 44px tall (FR-6, UX-DR11)

**Given** the front page with its fonts and images
**When** it is loaded in a browser with a throttled 4G profile and a phone-sized window
**Then** it is usable in under 3 seconds, and the measurement is recorded in the manual test plan (NFR-7)

### Story 1.6: Practical information and Our story pages

As a guest,
I want to read how to get there, where we sleep, the house rules and the couple's own story,
So that I know what to expect from the weekend before I answer.

**Covers:** FR-10 (page), FR-11, AD-17, UX-DR12, UX-DR14

**Acceptance Criteria:**

**Given** the Practical information page
**When** the guest opens it
**Then** it shows the jump links (a `nav` labelled «Hopp til») and one info sheet per part in this order: Vielsen (Strandebarm kirke with its time), Hardingasete og hyttene, Hvordan komme seg dit, Husregler, Antrekk, Ta med, Området rundt (FR-10)
**And** the texts are the placeholders from `mockups/info-praktisk.html` until the couple's full text (Story 7.4), and they live in the templates, not in the database (AD-17)

**Given** a jump link
**When** the guest follows it, with keyboard or touch
**Then** focus moves to that part's section, and its heading is not hidden under the sticky bar (UX-DR12)

**Given** the Our story page
**When** the guest opens it
**Then** it shows one story sheet with the couple's photo in the lace frame, their own text in chapters each opened by an italic time · place line as `h2`, the closing line and «Rikke & Valdemar» as a signature in Imperial Script, with no jump links (UX-DR14)
**And** the middle dots and the back-link arrow are hidden from screen readers

**Given** either page
**When** the guest is done reading
**Then** «← Tilbake til invitasjonen» at the top and the button at the bottom both return to the front page (FR-11)

### Story 1.7: The programme page

As a guest,
I want to see the weekend day by day, with what costs money and what to bring,
So that I can decide which days to come before I answer.

**Covers:** FR-9 (page), UX-DR13

**Acceptance Criteria:**

**Given** the Programme page
**When** the guest opens it
**Then** it shows the jump links Fredag · Lørdag · Søndag, the line «Alt i programmet er frivillig. Bli med på det dere har lyst til.», and one paper sheet per day with its date line (FR-9)

**Given** a day sheet
**When** it renders
**Then** the events are an `ol` in time order, each with Rikke's icon (decorative), the time as a `<time>` element and a short name, alternating sides by CSS only, and «Godt å vite» below with what costs money, what to bring and who covers what (UX-DR13)
**And** the events and their order are those in EXPERIENCE.md (Friday: Fjelltur, Hyttene er klare, Middag, Rebus, Badstue, stamp og mingling; Saturday: Yoga, Frokost, Vi drar til kirka, Vielsen, Lunsj utenfor kirka, Middag og fest; Sunday: Frokost, Hyttene skal være tomme), with placeholder times until Story 7.4

**Given** a layout narrower than about 260px
**When** the page renders
**Then** the timeline becomes one-sided, with every event to the right of the line, and there is no horizontal scroll

### Story 1.8: Error pages that still show how to reach the couple

As a guest whose page fails,
I want the error page to tell me what happened and how to reach Rikke and Valdemar,
So that I am never stuck without a way to answer.

**Covers:** FR-5, FR-6, AD-15

**Acceptance Criteria:**

**Given** a valid code
**When** a page under `/<code>/` returns 404 or 500, or the form check fails (CSRF)
**Then** the error page explains in plain, warm Norwegian what happened and shows the couple's phone numbers in the footer band (FR-6)

**Given** an unknown code
**When** any of these errors happens
**Then** the page shows nothing personal: no names, phone numbers, date or place (FR-5)

**Given** the error pages
**When** a test requests each of them with a valid and with an unknown code
**Then** each shows the content described above and sends the guest headers from Story 1.4

## Epic 2: Guests answer for their household

Sigmund and Arild answer for everyone in their household on a phone: who is coming, which days, overnight stay, meals with prices, allergies with consent and the Friday hike. They see the running total, check everything before sending, get a receipt in Rikke's words, choose to pay now or later, and see their household's status on the invitation afterwards. An interrupted answer is offered back when they return.

Deviation from the PRD tiers: FR-29 is pulled forward from tier 2 into Story 2.6 (see the Epic List).

### Story 2.1: Start the answer: who is coming

As bestefar Sigmund,
I want to press the RSVP button and first mark who in my household is coming,
So that the rest of the form only asks about the people who come.

**Covers:** FR-12, FR-13, FR-14 (step 1), FR-22, NFR-5, NFR-6, AD-1, AD-7, AD-8, UX-DR16, UX-DR17, UX-DR18, UX-DR19, UX-DR20

**Acceptance Criteria:**

**Given** the RSVP sheet on the front page
**When** it renders for a household that has not answered
**Then** it has the primary button «Svar på invitasjonen», which opens the form at `/<code>/svar/`

**Given** the form's first step
**When** it opens
**Then** it shows the step question as `h1`, the progress line «Steg 1 av m: <name>» and the respondent line «Jeg er <link owner> · Bytt» (FR-12, FR-13, UX-DR19)
**And** each household member is a fieldset with «Kommer» and «Kommer ikke», and nothing is selected (FR-14)

**Given** the respondent presses «Bytt»
**When** they pick another household member
**Then** that person is recorded as the one answering, and nothing already filled in changes (FR-12)

**Given** step 1 sent with a person left unanswered
**When** the server validates it
**Then** the step re-renders with status 200, the error under that person's legend as icon and «Feil: …», and a focused error summary at the top whose links focus each field; the page title starts with «Feil: » (FR-22, UX-DR16, UX-DR18)

**Given** a valid step
**When** «Fortsett» is pressed
**Then** the server saves the step in the draft cookie (signed, compressed, `HttpOnly`, `SameSite=Lax`, scoped to `/<code>/svar/`) and redirects to the next step's own address (POST-redirect-GET), and nothing is stored in the database (AD-7, AD-8)
**And** «Tilbake» and the browser's Back button show the previous step with its answers, without a resubmit prompt (UX-DR20)

**Given** the whole guest flow
**When** a test runs it
**Then** no session rows are created and the messages framework is never used (AD-8)
**And** every step works without JavaScript (AD-1)

### Story 2.2: Which days each person comes

As onkel Arild,
I want to say whether everyone who comes is there the whole weekend, and otherwise choose the days for each person,
So that Filippa can come only Saturday and Sunday while the rest of us come all weekend.

**Covers:** FR-14 (step 2), FR-70 (dates), FR-75, AD-2

**Acceptance Criteria:**

**Given** step 2 after at least one person is marked «Kommer»
**When** it opens
**Then** it asks whether everyone who is coming is there the whole weekend, Friday to Sunday, and shows each day with its date and what happens that day (FR-14, FR-70)

**Given** the answer «Nei»
**When** the step continues
**Then** the respondent chooses the days for each coming person, and a coming person must have at least one day

**Given** nobody is marked «Kommer»
**When** step 1 is sent
**Then** the form goes straight to the check page and asks nothing more

**Given** a person changed to «Kommer ikke» or a day removed
**When** the draft is updated
**Then** `normalise_answer` in `wedding/rules/` removes that person's or day's later choices, so they never show or count (FR-75)

**Given** answers that change who comes or which days
**When** the progress line renders
**Then** the step count m changes; moving forward or back alone never changes it (UX-DR19)

**Given** the rule functions for applicable steps and days
**When** they are tested
**Then** the tests pass plain values and cover all household shapes in `seed.toml`

### Story 2.3: Overnight stay, meals and the running total

As bestefar Sigmund,
I want to choose overnight stay and meals for each coming person with the prices in front of me,
So that I know what we will pay before I decide.

**Covers:** FR-15, FR-16, FR-32, FR-33, FR-70 (contradictions), FR-73, NFR-2, AD-2, AD-7, AD-12, UX-DR19

**Acceptance Criteria:**

**Given** the overnight step
**When** it renders
**Then** each coming person gets yes or no to staying overnight, with the cabin price shown first and the line that a cabin is booked for the whole weekend and both nights are paid (FR-16, FR-32)

**Given** a person present on only one day
**When** the respondent chooses to stay overnight
**Then** the step is blocked with an explanation of why (FR-70)

**Given** the meals step
**When** it renders
**Then** each coming person is offered only the paid meals on their days (Friday dinner, Saturday breakfast only if present from Friday, Sunday breakfast), each with its price, and Saturday lunch and dinner are not asked about (FR-15, FR-73)
**And** a short, friendly note explains why guests pay (FR-32)

**Given** any paid step
**When** it renders, and after every change when JavaScript runs
**Then** «Totalt for husstanden: <amount>» is calculated by `household_total` in `wedding/rules/` from the answers and the current prices in Settings, as whole kroner (FR-33, AD-12)
**And** the script update uses `POST /<code>/svar/sum/`, which returns the same rule's result as server-rendered HTML, writes nothing and is announced politely (AD-7)

**Given** `household_total`
**When** it is tested
**Then** the tests cover every paid option, removed choices (FR-75), a household paying nothing and the Saturday-only guest without a cabin

### Story 2.4: Allergies and consent

As bestefar Sigmund,
I want to register bestemor's dietary needs, say that I have none, and give consent for it to be stored,
So that the kitchen can make safe food, and nothing is stored about our health without our consent.

**Covers:** FR-25, FR-26, FR-27, FR-28, NFR-3, AD-8, AD-18, UX-DR21

**Acceptance Criteria:**

**Given** the allergies step
**When** it renders
**Then** each coming person has «Ingen allergier eller matbehov» and the categories gluten, laktose, nøtter, skalldyr, vegetar, veganer and annet, plus a short note field with a maximum length (FR-25)
**And** the question is optional

**Given** «Ingen allergier eller matbehov» and a category are both ticked for one person
**When** JavaScript runs, ticking one clears the other; without it, the step comes back with an inline error asking to choose one (UX-DR21)

**Given** the consent block
**When** it renders
**Then** the text says what the information is for, who sees it (the couple, toastmaster, maid of honour and best man), that names and allergies go to Hardingasete's kitchen, and that consent can be withdrawn through the same link, before a Ja/Nei choice that starts unanswered (FR-26)
**And** «Jeg bekrefter at <name> vet om dette og er enig» appears only when information is entered for someone other than the respondent (FR-27)

**Given** allergies entered and consent not given
**When** the respondent continues
**Then** the step and later the check page say plainly that the allergy information will not be saved and that the guest can tell the couple directly, and continuing is still allowed (FR-28)

**Given** the draft for the largest household with every allergy field filled to its maximum
**When** a test measures the cookie
**Then** it fits in 4 KB (AD-8)

### Story 2.5: The Friday hike and the check page

As bestefar Sigmund,
I want to answer about the Friday hike and then see everything I have answered before I send it,
So that I can catch mistakes and know that nothing is sent yet.

**Covers:** FR-17, FR-21, FR-28, UX-DR23

**Acceptance Criteria:**

**Given** at least one person comes on Friday
**When** the hike step renders
**Then** each person present on Friday answers yes, no or maybe, and nobody else is asked (FR-17)
**And** when nobody comes on Friday, the step is skipped and not counted in the progress line

**Given** the last step is done
**When** the check page opens
**Then** «Obs: Svaret er ikke sendt ennå.» is at the top, followed by the `h1` «Se over svaret før du sender», one block per part (Hvem kommer · Dager · Overnatting · Måltider · Allergier og matbehov · Fjelltur fredag) with each person's answer, and the household total (FR-21)
**And** skipped optional answers show «Ikke oppgitt», and allergies entered without consent show the FR-28 warning

**Given** an «Endre» link on the check page
**When** the respondent uses it
**Then** it opens that step with the answers filled in, and «Fortsett» returns to the check page; each link has hidden context such as «Endre måltider» (UX-DR23)

**Given** the check page
**When** it renders
**Then** «Send svaret» is the primary button, above «Tilbake»

### Story 2.6: Send the answer

As bestefar Sigmund,
I want my answer saved safely when I press «Send svaret»,
So that the couple gets it, and I am told clearly if something went wrong.

**Covers:** FR-26, FR-29, FR-68 (answers), FR-74, NFR-1, NFR-2, AD-3, AD-4, AD-9, AD-18, AD-20, UX-DR52

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `HouseholdAnswer` (revision, sent by, sent at), `PersonAnswer`, `Allergy`, `Consent` (when, who gave it, the consent-text version) and `Submission` (submission id, kind, what was written; AD-20), and nothing derived such as totals (AD-4, FR-29)

**Given** «Send svaret» pressed on a valid draft
**When** `send_answer` runs with the guest actor
**Then** it writes the answer in one IMMEDIATE transaction, records the respondent as the sender, increases the revision and deletes the draft cookie (AD-3, AD-9)
**And** allergy data and «Ingen allergier eller matbehov» are stored only for people with consent, and each consent record stores when, by whom and the text version (FR-26, FR-29, AD-18)

**Given** a re-send where consent is left unanswered
**When** it is saved
**Then** existing consented data is kept unchanged; «Ja» gives consent, «Nei» refuses it (AD-18)

**Given** the total recalculated at send differs from the total on the check page
**When** the send is attempted
**Then** nothing is written and the check page is shown again with a notice about the new total (AD-7)

**Given** the same submission sent twice (double tap)
**When** the second POST arrives
**Then** the earlier result is returned and nothing is written twice; the submission id is checked in `Submission` before the revision check (AD-20)

**Given** a write that fails
**When** the guest is shown the result
**Then** the error notice says what happened, that nothing is lost, «Prøv igjen», and the couple's phone numbers, and every answer stays in the draft (NFR-1, UX-DR52)

**Given** `send_answer`
**When** tests run
**Then** a guest actor cannot write to another household (AD-3), and person and household states follow FR-74 (coming, not coming, not answered; a household is answered once sent)
**And** `seed_testdata` now loads the answers, allergies and consents in `seed.toml` through `send_answer`
**And** the manual test plan records one real-browser send, since Django's test client sends no browser headers

### Story 2.7: The receipt and how to pay

As bestefar Sigmund,
I want a clear thank-you that matches my answer, and to see what we owe and how to pay,
So that I know the answer arrived and can pay now or later.

**Covers:** FR-23, FR-34, FR-71 (derived message), AD-2, AD-12, UX-DR24, UX-DR25, UX-DR51

**Acceptance Criteria:**

**Given** a successful send
**When** the receipt opens
**Then** a success notice holds the `h1` «Svaret er sendt» and «Sendt av <name> <weekday date> kl. <time>.», then Rikke's message for coming (when at least one person comes) or not coming, by the du/dere rule, the summary «Dette har dere svart» and the total (FR-23, UX-DR24)

**Given** a household that owes money
**When** the receipt renders
**Then** «Betal nå» is above «Betal senere», and «Du kan nå trygt lukke invitasjonen.» stands directly below them (FR-23, FR-34)
**And** with nothing owed there are no payment buttons, and the closing line follows the summary

**Given** «Betal nå»
**When** the payment details open
**Then** they show the amount, the Vipps number, the account number and the payment message «Bryllup» + the household's names from the derived-message rule, all as selectable text (FR-34, FR-71)
**And** «Kopier» buttons appear only when the clipboard is available, «Kopiert» is announced politely, and a failed copy selects the value with «Trykk og hold for å kopiere» (UX-DR25)

**Given** «Betal senere»
**When** it is chosen
**Then** the guest is told that the same link always shows what is owed and how to pay (FR-34)

**Given** guest pages showing money
**When** they get an amount
**Then** they use only `guest_balance(total, report)` and never read payment rows (AD-12)

### Story 2.8: The household's status on the invitation

As tante Marie,
I want my own link to show that Arild has already answered for us, and when,
So that I don't answer again or wonder whether it was done.

**Covers:** FR-24, FR-41, UX-DR10

**Acceptance Criteria:**

**Given** a household that has answered
**When** any member opens their link
**Then** the hero's deadline line reads «Svar sendt <date> · Se svaret», and the RSVP sheet's place holds the status block (`id="status"`): «Svaret er sendt», the small gypsophila, «Barnefritt bryllup», «Sendt av <name> <weekday date> kl. <time>.», «Totalt for husstanden: …» and «Dere kan endre svaret fram til <weekday date> kl. 23:59.» (FR-24, FR-41, UX-DR10)
**And** the line «Meldt betalt: …» is added with payment reports (Story 5.1), and «Se eller endre svar» with changing answers (Story 4.1)

**Given** the answered front page
**When** the guest uses the nav "Svar" or «Se svaret»
**Then** the page jumps to the status block and focus lands on its heading

### Story 2.9: An interrupted answer is kept on the phone

As bestefar Sigmund,
I want my half-finished answer to be waiting when the phone rings and Messenger reloads the page,
So that I don't have to start again.

**Covers:** FR-41 (deadline rule), FR-78, AD-8, AD-11, UX-DR26

**Acceptance Criteria:**

**Given** a draft cookie from an earlier visit
**When** the guest opens their link
**Then** the RSVP sheet shows «Du har et svar som ikke er sendt ennå.» (UX-DR26)

**Given** a draft
**When** the form is opened by any route (either "Svar", the RSVP button, or reloading a step)
**Then** the draft offer comes first: «Vil du fortsette der du slapp?», when the answer was started, «Ja, fortsett» and «Nei, begynn på nytt» (FR-78)
**And** «Ja, fortsett» opens the step they left with all answers filled in; «Nei, begynn på nytt» deletes the draft and starts from the sent answer or empty

**Given** the deadline function in `wedding/rules/`
**When** it is given the deadline date and `now`
**Then** it says whether `now` is after 23:59:59 Oslo time on that date, and tests cover both sides of the boundary and a winter/summer time change (FR-41, AD-11)
**And** a draft is not offered after the deadline

## Epic 3: The couple sees the numbers and can trust them

Rikke logs in and sees how many households have answered, the summary in small groups, the people behind every count, a simple overview of every household and the allergy list for Hardingasete. The automated tests prove that every count, total and payment status matches the expected-results list worked out by hand.

### Story 3.1: The couple logs in

As Rikke,
I want to log in with a username and password, also on my phone,
So that only we can see the guests' answers.

**Covers:** FR-46 (couple), FR-47, NFR-4, AD-10, AD-13, UX-DR34, UX-DR36

**Acceptance Criteria:**

**Given** `uv run manage.py create_admin <username> --role couple|helper`
**When** Rikke runs it
**Then** it creates an admin user with that role and asks for the password; there is no self-registration (FR-47, AD-10)

**Given** the login page under `/admin/`
**When** Rikke logs in with the right username and password
**Then** she reaches the admin home; with wrong details she sees a plain error in Norwegian; paste and password managers work (UX-DR36)
**And** passwords are stored with Django's default password hashing (NFR-4)
**And** Django's built-in admin site is not mounted at `/admin/`, so the couple's admin area owns that path

**Given** any admin page
**When** it renders
**Then** it has the flat green admin frame, the Admin nav (Oversikt · Gjester · Betalinger · Innstillinger) and «Logg ut» (UX-DR34, AD-13)
**And** an admin page opened without login redirects to the login page

**Given** a logged-in admin
**When** 20 hours pass without a request
**Then** the session expires, every request renews it, the session cookie is scoped to `/admin/`, and the login page says «Du ble logget ut fordi du var borte en stund.» (AD-13, UX-DR36)

### Story 3.2: Answer progress and the summary

As Rikke,
I want to see at once how many households have answered and the numbers Hardingasete will ask for,
So that I can plan the weekend without counting by hand.

**Covers:** FR-48 (basic), FR-54, FR-73, FR-74, NFR-2, AD-2, AD-12, AD-18, UX-DR39, UX-DR40, UX-DR49

**Acceptance Criteria:**

**Given** the admin home
**When** it renders
**Then** the Svar panel shows «Svart: X av Y husstander», a decorative bar (`aria-hidden`), the rows Kommer / Kommer ikke / Ikke svart ennå with persons and households, and «Se hva alle har svart» (FR-54, UX-DR39)
**And** a place at the top is kept for «Trenger oppfølging» (Story 6.2)

**Given** the summary panels
**When** they render
**Then** they come in this order: Når kommer de? (whole weekend; not the whole weekend by day combination) · Overnatting (does not stay overnight; total beds) · Mat (one count per meal, Saturday lunch and dinner counting everyone present on Saturday) · Allergier (med samtykke) (per category, Ingen allergier eller matbehov, Ingen allergiopplysninger lagret) · Fjelltur fredag («n kommer, n kanskje», never added together) · Betaling (husstander som kommer) (FR-54, FR-73, UX-DR40)

**Given** every count
**When** it is computed
**Then** it is the length of a list of guest or household ids returned by a rule function in `wedding/rules/`; selectors load facts and never filter on answer content (AD-2)
**And** `allergy_state` gives each coming guest exactly one of the three AD-18 states, and `payment_status(total, received, refunded)` covers all five FR-60 statuses as a pure function, with received and refunded at 0 until payments exist (Story 5.2)

**Given** the admin home on a 360px phone
**When** it is used
**Then** every target is at least 44px and there is no horizontal scroll (FR-48)

### Story 3.3: Every count opens the people behind it

As Rikke,
I want to tap «Fredag middag 12» and see who the 12 are,
So that I can trust the numbers I send to Hardingasete.

**Covers:** FR-55, UX-DR41

**Acceptance Criteria:**

**Given** a count above zero on the admin home
**When** Rikke taps it
**Then** a page lists exactly the people or households in that rule's id list, with the count as its heading (FR-55)

**Given** a count of zero
**When** it renders
**Then** it shows «0» as plain text, not a link (UX-DR41)

**Given** each count on the admin home
**When** a test opens its drill-down
**Then** the number of rows equals the count

### Story 3.4: The overview of every household and the allergy list

As Rikke,
I want one list of all households with who is coming, and a list of allergies I can pass to the kitchen,
So that I can check any household and send Hardingasete the allergy names and counts.

**Covers:** FR-48 (basic), FR-57 (simple), FR-58, UX-DR42 (list), UX-DR48, UX-DR49

**Acceptance Criteria:**

**Given** the Gjester page
**When** it renders
**Then** it shows «N husstander · M gjester» and one row per household with the name, a status tag (text and icon, never colour alone) and one line with who comes and the total; households that have not answered come first and carry «Ikke svart» (FR-57, UX-DR42, UX-DR49)
**And** with no households it says «Ingen husstander ennå.»

**Given** the allergy list
**When** it renders
**Then** it lists the name and categories of every guest with consented allergy data, plus their notes, and nothing for guests without consent (FR-58)
**And** with nobody on it, it says «Ingen allergier registrert ennå.» (UX-DR48)

**Given** both pages on a 360px phone
**When** they are used
**Then** the rows stack with visible labels, targets are at least 44px and there is no horizontal scroll (FR-48)

### Story 3.5: Tests prove the numbers match the expected-results list

As Rikke,
I want automated tests that compare the admin numbers with the list we worked out by hand,
So that I, the examiner and the couple can trust that the numbers are right.

**Covers:** FR-69, NFR-2, SM-2, AD-16

**Acceptance Criteria:**

**Given** the seed data loaded by `seed_testdata`
**When** `uv run pytest` runs the expected-results tests
**Then** every FR-54 count, each household's total and each guest's allergy state equals `wedding/fixtures/expected.toml`, with `now` passed explicitly (FR-69, AD-16)
**And** payment statuses and report matches are asserted from Story 5.3, when payments are seeded

**Given** a deliberate change to the expected-results list
**When** it is committed
**Then** it is its own commit with the reason in the message (AD-16)

**Given** the README
**When** Ingrid reads the test section
**Then** it says what the expected-results tests check and where the hand-worked list is

## Epic 4: Guests change their answer until the deadline locks it

Arild changes his household's answer before the deadline and sees who answered last; Marie never overwrites his answer without seeing it first. After the deadline guests can only see their answer, while the couple can still fill in or change any household's answer with the same form. The couple changes the deadline, prices and contact details in Settings, with a clear confirmation.

### Story 4.1: See or change the answer before the deadline

As onkel Arild,
I want to open our sent answer, see who answered last and change it,
So that a change of plans is easy to register.

**Covers:** FR-37, FR-38 (last updated), FR-39, AD-19, UX-DR28

**Acceptance Criteria:**

**Given** a household that has answered, before the deadline
**When** a member opens the status block
**Then** it has the primary button «Se eller endre svar», which opens the form with the sent answers filled in (FR-37)
**And** the top of the form shows the info notice «Sist endret av <name>, <date> kl. <time>» (FR-38, UX-DR28)

**Given** a changed answer is sent
**When** `send_answer` saves it
**Then** the household's `changed_at` is set by the one helper in AD-19, and the first answer and payment reports never set it (FR-39)

**Given** the total changed by the new answer
**When** the receipt and status block render
**Then** they show the new total

**Given** a changed answer sent twice (double tap)
**When** the second POST arrives
**Then** the receipt from the first is shown, not a conflict notice about the respondent's own answer, and the revision rises only once (AD-9, AD-20)

### Story 4.2: No answer is overwritten without anyone seeing it

As tante Marie,
I want to see Arild's newer answer before mine is sent,
So that I don't wipe out his changes without knowing.

**Covers:** FR-38, AD-9, AD-18, UX-DR28

**Acceptance Criteria:**

**Given** Marie's draft started at revision n
**When** Arild sends an answer (revision n+1) and Marie then presses «Send svaret»
**Then** nothing is written, and Marie sees a warning notice with who sent, when and what differs from her draft (FR-38, AD-9)
**And** she can review and send again, and that second send is saved

**Given** a draft with a consent «Ja»
**When** the revision has changed
**Then** the consent «Ja» is not carried across, and the respondent must answer consent again (AD-18)

**Given** the conflict check
**When** tests run
**Then** they cover two members sending in sequence and a draft started before a couple override

### Story 4.3: The answer locks at the deadline

As the couple,
I want guests' answers to lock at 23:59 on the deadline day,
So that the numbers we give Hardingasete stay fixed.

**Covers:** FR-42, SM-11, AD-11, UX-DR10 (locked), UX-DR33

**Acceptance Criteria:**

**Given** a guest send that changes answer content after the deadline
**When** it reaches the service
**Then** it is refused, using the one deadline function (AD-11)
**And** consent withdrawal and "I have paid" reports are never refused because of the deadline

**Given** an answered household after the deadline
**When** a member opens their link
**Then** the status block has «Se hele svaret», which opens the read-only answer view with «Fristen gikk ut <weekday date> kl. 23:59» and the couple's phone numbers (FR-42, UX-DR33)

**Given** a household that never answered, after the deadline
**When** a member opens their link
**Then** the hero line reads «Svarfristen gikk ut <date> · Ring oss», and the RSVP sheet's place shows the deadline message and contacts instead of the RSVP button (UX-DR10)

**Given** the lock
**When** tests run with `now` just before and just after the deadline
**Then** both sides behave as described (SM-11)

### Story 4.4: The couple fills in or changes any household's answer

As Rikke,
I want to fill in or change a household's answer with the same form the guests use, also after the deadline,
So that I can help Synne when she calls.

**Covers:** FR-63, AD-3, AD-7, AD-10

**Acceptance Criteria:**

**Given** a household's row in Gjester (its household page from Story 6.3 links here too)
**When** Rikke chooses «Endre svaret»
**Then** the same form from `wedding/rsvp/` opens at `/admin/husstand/<id>/svar/`, with the household's answers filled in (FR-63, AD-7)

**Given** the deadline has passed
**When** Rikke sends the answer
**Then** it is saved, and the admin is recorded as the author (FR-63, AD-3)

**Given** any admin write service
**When** it is called
**Then** it calls `require_couple(actor)`, and a test proves a helper actor is refused (AD-10)

### Story 4.5: The couple changes the deadline, prices and contact details

As Rikke,
I want to change the deadline, prices, our phone numbers and the payment details in the admin area,
So that real values can be set without changing code.

**Covers:** FR-64, AD-20, UX-DR29, UX-DR47, UX-DR50 (tier 2)

**Acceptance Criteria:**

**Given** the Innstillinger page
**When** Rikke saves a change
**Then** a confirmation step (a first POST that writes nothing) shows the change; the second POST saves it (AD-20)
**And** with JavaScript the confirmation is a dialog with `role="alertdialog"`, focus on the safe button, Esc to cancel and focus back to the trigger; without it, a confirm page (UX-DR29)

**Given** a new deadline
**When** the confirmation shows
**Then** it repeats the new deadline in words, and a deadline in the past or within two weeks also says how many households would be locked out (FR-64, UX-DR47)

**Given** a helper
**When** they open Innstillinger
**Then** values show as text without save buttons, and the service refuses any write (FR-64, AD-10)

**Given** the examiner moves the deadline to yesterday
**When** a guest link is opened
**Then** the answer is locked for the guest, and the couple can still change it (UJ-6)

## Epic 5: Payments are reported, registered and matched

A guest reports "I have paid" and sees what remains or will be refunded if the total changes. The couple registers money received and refunds paid back, can undo a registration, sees each household's computed payment status, and sees mismatched reports in red. The couple can adjust a household's payment message, with a warning for duplicates.

### Story 5.1: The guest reports "I have paid"

As bestefar Sigmund,
I want to tell the couple that I have paid, how much and how,
So that they know to look for the money.

**Covers:** FR-35, AD-4, AD-11, AD-12

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `PaymentReport`, one current report per household (AD-4)

**Given** «Jeg har betalt» on the payment details or status block
**When** the guest opens it
**Then** the amount is prefilled with what is owed, the method is Vipps or bank, and an optional field says who paid if it was someone else (FR-35)
**And** amounts accept «900», «900 kr» and «1 450», and errors follow FR-22

**Given** a saved report
**When** the guest returns
**Then** they see what they reported and when, can correct it (the correction replaces it), and the status block shows «Meldt betalt: <amount>, <date>.»

**Given** the deadline has passed
**When** a guest reports or corrects a payment
**Then** it is still accepted (AD-11)

### Story 5.2: The couple registers money received and refunded

As Rikke,
I want to register each amount received and each refund, and undo a mistake,
So that the site knows who has paid.

**Covers:** FR-59, FR-68 (payments), AD-3, AD-4, AD-12, AD-20, UX-DR45 (household page), UX-DR50 (tier 2)

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `Payment` with kind `received` or `refunded`, a positive whole-kroner amount, who registered it and `voided_at` (AD-4)

**Given** a household's payment page
**When** Rikke registers «Mottatt fra gjesten» or «Betalt tilbake til gjesten» with an amount
**Then** a tier-2 confirmation names the new status, and after saving the page shows «Registrert: mottatt <amount>.» with «Angre» (FR-59, UX-DR45)

**Given** «Angre» on a registration
**When** it is used
**Then** the payment is voided by setting `voided_at`, never deleted; undoing an older entry asks for confirmation first (AD-4, AD-20)

**Given** a household or guest with payments that are not voided
**When** someone tries to delete it
**Then** the delete is refused with an explanation (AD-4)

**Given** `seed_testdata`
**When** it runs
**Then** it now loads the payments and payment reports in `seed.toml` through the services

### Story 5.3: Payment status and the payments list

As Rikke,
I want each household's payment status worked out from the money, and mismatches marked,
So that I know who to remind and who to pay back.

**Covers:** FR-60, FR-61, NFR-2, AD-2, UX-DR45 (list), UX-DR49

**Acceptance Criteria:**

**Given** a household's total, received and refunded amounts
**When** `payment_status` is computed
**Then** it is nothing to pay, not paid, part paid (X missing), paid or refund owed (X), shown only to admins (FR-60)

**Given** an "I have paid" report
**When** received minus refunds is lower than the reported amount
**Then** the household gets the «Stemmer ikke» tag (error icon and word) in the overview and on the payments list (FR-61, UX-DR49)

**Given** the Betalinger page
**When** it renders
**Then** it shows «Til sammen» (Skal betales · Mottatt · Mangler · Skal betales tilbake) and one row per coming household, sorted stemmer ikke → skal ha tilbake → delbetalt → ikke betalt → betalt → ingenting å betale (UX-DR45)
**And** with no payments it says «Ingen betalinger registrert ennå.»

**Given** the seed data with payments
**When** the expected-results tests run
**Then** every payment status, report match and the Betaling summary panel equal `expected.toml`

### Story 5.4: The guest sees what remains or will be refunded

As onkel Arild,
I want to see what is left to pay, or that the couple will pay me back, after I change our answer,
So that I always know where we stand.

**Covers:** FR-36, AD-12

**Acceptance Criteria:**

**Given** a payment report and a total that has gone up
**When** the guest sees the status block, receipt or payment details
**Then** they read «Du har <amount> igjen å betale» (FR-36)

**Given** a total that has gone down below the reported amount
**When** the guest sees them
**Then** they read «Rikke og Valdemar har fått beskjed og betaler tilbake <amount>» (FR-36)

**Given** these guest pages
**When** they compute the amounts
**Then** they use only `guest_balance`, never the couple's registered payments (AD-12)

### Story 5.5: The couple adjusts a payment message

As Rikke,
I want to change a household's payment message and be warned if two households would share one,
So that every payment can be matched to the right household.

**Covers:** FR-71, AD-4, UX-DR46

**Acceptance Criteria:**

**Given** «Endre betalingsmeldingen» on a household's payment page
**When** Rikke saves a new message
**Then** it is stored only because it was adjusted; otherwise the message is derived from the household's names (AD-4)

**Given** a message identical to another household's (derived or adjusted)
**When** Rikke tries to save it
**Then** she is warned before saving, and the warning names the other household (FR-71, UX-DR46)

## Epic 6: The couple manages the guest list and follows up

Rikke sees "Needs attention" first when she logs in and marks items as handled. The couple adds, edits and removes households and guests, finds a guest by name and copies their link, and opens each household's own page. Helpers see everything and change nothing, and repeated login attempts are slowed down.

### Story 6.1: Helpers see everything and change nothing

As the toastmaster,
I want to see the same overview as the couple without any buttons that change things,
So that I can help with planning without risk of mistakes.

**Covers:** FR-46 (helpers), NFR-4, AD-6, AD-10, UX-DR35

**Acceptance Criteria:**

**Given** a helper logged in
**When** they open any admin page
**Then** they see the same information as the couple, action buttons are hidden (not greyed), form values show as text, and the line «Du kan se alt, men ikke endre noe.» stands under the Admin nav (UX-DR35)
**And** no link codes and no «Kopier lenke» are rendered for them (AD-6)

**Given** a forged POST from a helper to any admin write
**When** it reaches the service
**Then** `require_couple` refuses it, and a test covers every admin write service (NFR-4, AD-10)

### Story 6.2: "Needs attention" at the top

As Rikke,
I want the things I must follow up listed first when I log in,
So that nothing slips.

**Covers:** FR-56, AD-19, UX-DR37, UX-DR38

**Acceptance Criteria:**

**Given** the admin home
**When** it renders
**Then** «Trenger oppfølging (n)» is the first panel, visible without scrolling, listing households that have not answered, coming guests with no allergy information stored, "I have paid" mismatches (first, with «Stemmer ikke»), refunds owed and households marked «Endret» (FR-56, UX-DR37)
**And** it shows as many items as fit while «Svart: X av Y» stays on the first screen, then «Vis alle n»

**Given** an item
**When** Rikke presses «Merk som håndtert» (or «Merk som sett» for «Endret»)
**Then** the row is replaced in place by «Merket som håndtert. Angre», with focus on «Angre» and no timer, and the item leaves the list when the page is left (UX-DR38)

**Given** this story's migration
**When** it is applied
**Then** it creates `AttentionMark` (kind, subject, `handled_at`), and attention items are computed by rules with kind, subject and event time (AD-19)

**Given** a handled item whose event happens again later (for example a new change)
**When** the list is computed
**Then** the item shows again (AD-19)
**And** «Vis håndterte» lists handled items and lets Rikke unmark them

**Given** nothing needs attention
**When** the panel renders
**Then** it reads «Ingenting trenger oppfølging nå» with a check icon, and «Vis håndterte» below

### Story 6.3: Find a guest and copy their link

As Rikke,
I want to find Synne by name on my phone and copy her link,
So that I can send it again when she has lost it.

**Covers:** FR-51, FR-57 (household pages), FR-48, UX-DR42, UX-DR43

**Acceptance Criteria:**

**Given** the Gjester page
**When** Rikke searches «Finn en gjest» with part of a name
**Then** matching guests are listed and a polite message says «3 treff» or «Fant ingen med det navnet.» (FR-51, UX-DR42)

**Given** a household page
**When** it opens
**Then** it shows the panels Svar (who sent and when, each person's answers, tappable phone and email, «Endre svaret»), Betaling (total, status tag, «Se betalingene»), Lenker («Kopier lenke» per person with «Kopiert») and Husstanden (FR-57, UX-DR43)

**Given** «Kopier lenke»
**When** the clipboard is unavailable or copying fails
**Then** the link is shown as selectable text with «Trykk og hold for å kopiere»

**Given** Rikke on a 360px phone
**When** she finds a guest, copies the link and checks whether they have answered
**Then** each task fits one screen (FR-48)

### Story 6.4: Add and edit households

As Rikke,
I want to add a household with its people and change names and contact details,
So that the guest list is right before invitations go out.

**Covers:** FR-49 (add, edit), AD-3, AD-9, AD-20, UX-DR44

**Acceptance Criteria:**

**Given** «Legg til husstand»
**When** Rikke fills in one fieldset per person («Navn» required, «Telefon (valgfritt)», «E-post (valgfritt)») and presses «Lagre husstanden»
**Then** the household and guests are created, and each guest gets their own link (FR-49, UX-DR44)
**And** «Legg til en person til» adds a fieldset and moves focus to its name field

**Given** «Endre navn og kontaktinfo»
**When** Rikke presses «Lagre endringene»
**Then** a tier-2 confirmation names what changes, including that the payment message changes, with the FR-71 duplicate warning
**And** adding a person raises the household's revision (AD-9)

**Given** a missing name or an invalid email
**When** the form is sent
**Then** the error summary and field errors appear, and everything typed is kept

### Story 6.5: Remove a household or a person

As Rikke,
I want to remove a household or one person, with a confirmation that is hard to do by mistake,
So that people who are no longer invited disappear from the numbers.

**Covers:** FR-49 (remove), AD-4, AD-9, UX-DR50 (tier 3)

**Acceptance Criteria:**

**Given** «Fjern husstanden» or «Fjern <name> fra husstanden»
**When** Rikke chooses it
**Then** a dialog asks her to type FJERN; matching ignores case and surrounding spaces, the field has `autocapitalize="off" autocorrect="off" spellcheck="false"`, and a wrong word gives an inline error (UX-DR50)

**Given** the removal is confirmed
**When** the service runs
**Then** the guest's answers, allergies and consent records are deleted with them, the household's revision is raised, and the result message is announced at the top of Gjester (AD-4, AD-9)
**And** «Fjern <name> fra husstanden» is hidden when only one person is left

**Given** a household or guest with payments that are not voided
**When** removal is attempted
**Then** it is refused with an explanation (AD-4)

### Story 6.6: Slow down repeated login attempts

As the couple,
I want repeated wrong logins to be slowed down,
So that nobody can guess our passwords.

**Covers:** NFR-4

**Acceptance Criteria:**

**Given** several failed logins for one username or from one address
**When** the limit is reached
**Then** further attempts are refused for a while with a plain Norwegian message (NFR-4)
**And** the limiter is one shared helper on Django's database cache (`createcachetable`, a set `MAX_ENTRIES`), so it can be reused for link codes (Story 8.6)

**Given** a successful login after the wait
**When** it happens
**Then** it works normally, and tests cover both sides of the limit

## Epic 7: Guests understand their privacy and get a finished form

Guests can read a privacy page in plain words, withdraw allergy consent for a household member at any time, also after the deadline, open "Read more" inside a step without leaving the form, and get a warning before leaving an unsent answer. The programme and practical information pages get their full text.

### Story 7.1: The privacy page

As a guest,
I want to read in plain words what is stored about us, why, who sees it and when it is deleted,
So that I can trust the invitation with our information.

**Covers:** FR-66, NFR-3, UX-DR31

**Acceptance Criteria:**

**Given** «Personvern» in the footer of every guest page, under the sheet on the private-invitation page, and in the consent text
**When** the guest opens it
**Then** the page uses the info-page frame with the parts Hva vi lagrer, og hvorfor · Hvem som ser det · Når det slettes · Rettighetene dine · Trekke samtykket (FR-66, UX-DR31)

**Given** the page content
**When** it is read
**Then** it covers what is collected and why (including the phone numbers and emails the couple enters), that Rikke and Valdemar are jointly responsible, the legal basis per kind of information from NFR-3, who can see it (and for allergies Hardingasete's kitchen), when it is deleted, the guest's rights including withdrawing consent and complaining to Datatilsynet, and how to contact the couple

**Given** the page opened from the private-invitation page (no valid link)
**When** it renders
**Then** it shows only the general parts, without names or a withdrawal list

**Given** the «Personvern» link in the consent block
**When** the guest returns with «Tilbake»
**Then** they are back on the same step with their answers kept

### Story 7.2: Withdraw consent

As bestemor,
I want to withdraw my consent and have my allergy information deleted, also after the deadline,
So that I decide over my own health information.

**Covers:** FR-30, AD-3, AD-9, AD-11, AD-18, AD-19, UX-DR32

**Acceptance Criteria:**

**Given** the last part of the privacy page, and the answer view next to the allergies
**When** a household member opens it
**Then** it lists each person with allergy data stored and «Trekk samtykket for <name>», or «Ingen allergiopplysninger lagret.» (UX-DR31, UX-DR32)

**Given** «Trekk samtykket for bestemor»
**When** the guest confirms in the dialog («Trekke samtykket for bestemor?», «Avbryt» focused, «Slett allergiopplysningene»)
**Then** `withdraw_consent` deletes that person's allergy data, records the withdrawal, raises the revision and marks the household changed, and the page says «Allergiopplysningene til bestemor er slettet.» (FR-30, AD-18, AD-19)

**Given** the deadline has passed
**When** consent is withdrawn
**Then** it works (AD-11)

**Given** the withdrawal
**When** the admin pages are opened
**Then** the person is in «Ingen allergiopplysninger lagret», the household is tagged «Endret», and an old draft can never store the withdrawn allergy again (AD-18)

### Story 7.3: "Read more" inside the form and the leave warning

As bestefar Sigmund,
I want to read about the cabins without leaving the form, and to be warned if I am about to leave without sending,
So that I don't lose my place or think I have answered when I haven't.

**Covers:** FR-19, FR-20, AD-7, UX-DR22, UX-DR27

**Acceptance Criteria:**

**Given** a step with more context, such as the cabins and their price
**When** the guest opens «Les mer om hyttene»
**Then** it expands in place as a `<details>` element and never navigates away (FR-19, UX-DR22)

**Given** a guest in the form or on the check page with an unsent answer
**When** they follow an in-page link that leaves the form
**Then** a dialog says «Svaret er ikke sendt ennå. Det du har fylt ut, er tatt vare på på denne telefonen.» with «Bli og fullfør svaret» and «Gå uten å sende» (FR-20, UX-DR27)
**And** where the browser supports it, its own leave prompt shows when the tab is closed or reloaded

### Story 7.4: The full text of the programme and practical information

As a guest,
I want the real times, prices and practical details,
So that I can plan the weekend.

**Covers:** FR-9, FR-10

**Acceptance Criteria:**

**Given** the couple's final texts and times
**When** the Programme and Practical information pages render
**Then** the placeholders are replaced, the programme marks what costs money and what to bring, and practical information covers every FR-10 topic (FR-9, FR-10)

**Given** the full text
**When** the pages are checked at 360 × 560, 320 × 568 and 180 × 320
**Then** there is no horizontal scroll and the check is recorded in the manual test plan

## Epic 8: Cut-first extras (tier 3)

The couple can move a guest to another household, replace one guest's link, register consent given by phone, and is warned when a price change affects households that have answered. The admin pages use a PC screen better, and repeated wrong-link attempts are slowed down. Whatever is not done by 10 December moves to [2027], with the reason in the PRD change log.

### Story 8.1: Move a guest to another household

As Rikke,
I want to move a guest to another household,
So that the households match how people actually answer.

**Covers:** FR-50, AD-9, UX-DR50 (tier 2)

**Acceptance Criteria:**

**Given** a guest on a household page
**When** Rikke moves them to another household and confirms the tier-2 dialog
**Then** the guest keeps their link, both households' revisions are raised, and both totals and counts follow the move (FR-50, AD-9)

### Story 8.2: A new link for one guest

As Rikke,
I want to deactivate a link that has gone astray and create a new one,
So that only the right person can open the invitation.

**Covers:** FR-53, AD-6, UX-DR50 (tier 2)

**Acceptance Criteria:**

**Given** a guest on a household page
**When** Rikke confirms the tier-2 dialog («<name>s gamle lenke slutter å virke. De andre i husstanden beholder sine.»)
**Then** only that guest gets a new code, the rest of the household keeps theirs, and the old code shows the private-invitation page (FR-53, AD-6)

### Story 8.3: The couple registers consent given by phone

As Rikke,
I want to register that Synne said yes to the consent text I sent her,
So that her allergy can be stored correctly.

**Covers:** FR-31, FR-29, UX-DR50 (tier 2)

**Acceptance Criteria:**

**Given** a person on a household page
**When** Rikke registers consent with the channel and confirms
**Then** the consent record stores who registered it, the channel, the consent-text version and when, and the person's allergies can then be stored (FR-31)

### Story 8.4: Warning when prices change after households have answered

As Rikke,
I want to know how many households' totals change before I save new prices,
So that I can warn them.

**Covers:** FR-65, AD-20

**Acceptance Criteria:**

**Given** households that have answered
**When** Rikke saves new prices in Innstillinger
**Then** the confirmation says how many households' totals will change, computed by rules without writing anything (FR-65, AD-20)

### Story 8.5: The admin pages on a PC screen

As Rikke,
I want the household list and the payments to use the wider screen on my PC,
So that I can see more at once when I go through everything.

**Covers:** FR-48 (beyond basic)

**Acceptance Criteria:**

**Given** a PC-width screen
**When** Gjester or Betalinger render
**Then** the rows may become a real `<table>` with a header row, while the phone layout is unchanged (FR-48)

### Story 8.6: Slow down guessing of link codes

As the couple,
I want repeated attempts with wrong links to be slowed down,
So that nobody can find a guest's invitation by trying codes.

**Covers:** NFR-4, AD-6

**Acceptance Criteria:**

**Given** many unknown link codes from one address
**When** the limit is reached
**Then** further attempts get the private-invitation page without looking up the code for a while, using the shared limiter from Story 6.6 (NFR-4)
**And** a valid link from another address is not affected
