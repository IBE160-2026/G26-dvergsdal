---
stepsCompleted: [1, 2]
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
- FR-29 (T2): Consent is stored per person: when, who gave it (the person, another household member or the couple) and which consent text version was shown.
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
- **AD-20:** confirmations are a preview POST that writes nothing, then a second POST calling the service; undo is a reversing service; every write form carries a one-time submission id stored under a unique constraint so repeats return the earlier result.
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
