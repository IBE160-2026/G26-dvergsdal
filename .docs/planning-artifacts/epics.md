---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - prds/prd-aill-handle-it-2026-11-07/prd.md
  - prds/prd-aill-handle-it-2026-11-07/addendum.md
  - architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md
  - ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md
  - ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md
---

# AI'll handle it – Epic Breakdown

## Overview

This document breaks the requirements in the PRD, the UX design (DESIGN.md, EXPERIENCE.md) and the architecture spine into epics and stories that can be built one at a time.

**How to read it**

- Requirement IDs are the PRD's own (FR-n, NFR-n), so every story traces back to the PRD (NFR-9). Each story's **Covers:** line lists what it builds, and [Requirements Inventory (reference)](#requirements-inventory-reference) at the end lists every FR with the stories that build it.
- Priority tiers come from PRD section 3.1a: **T1** usability-test build (27 November 2026), **T2** complete course version (10 December 2026), **T3** cut first. Only T1–T3 are in v1. *Protection tier* 1–3 is something else: how hard an admin action is to do by mistake (UX-DR50).
- **AD-n** are architecture decisions in ARCHITECTURE-SPINE.md, where *Structural Seed* and *Consistency Conventions* are also sections. **UX-DRn** are UX design requirements from DESIGN.md and EXPERIENCE.md; the surface IDs G1–G12 (guest pages) and A1–A12 (admin pages) are EXPERIENCE.md's. **SM-n** are the PRD's success measures (section 2), for example SM-2 "the admin counts match the expected-results list" and SM-11 "answers lock at the deadline while the couple can still change them". **UJ-n** are the PRD's user journeys (section 4).
- «…» is exact Norwegian interface text. Straight quotes are English descriptions, such as "Needs attention" or "I have paid".
- The people in the stories are the PRD's: bestefar Sigmund and bestemor (UJ-1); onkel Arild, tante Marie and their adult daughters Filippa and Leone (UJ-2); Synne, who has lost her link (UJ-3); Ingrid the examiner (UJ-6); Rikke and Valdemar, the couple.
- A story's **Not in this story:** line names work that belongs to a later story, so it is not built early.

**Not in v1**

- **[2027]**, built before the invitations go out: FR-40, FR-52, FR-62, FR-67, FR-76, FR-77.
- **[If time]**, the extras listed in PRD section 3.3: envelope animation, Vipps QR code, print page for Hardingasete, speech sign-up, gift list, English version, wider PC layout.
- **Deferred in the architecture to 2027:** hosting, domain, HTTPS, backups, monitoring, error reporting, update rules, device floor, the Django 6.2 LTS upgrade ([issue #13](https://github.com/IBE160-2026/G26-dvergsdal/issues/13)) and editable info pages.

**Standing acceptance criteria for every story with a write service** (from Story 2.6c, which creates `Submission`):

- The form carries a one-time submission id, recorded in `Submission` in the same transaction (AD-20).
- A guest service has a test proving that an id from another household is refused (AD-3).
- An admin service calls `require_couple(actor)`, and a test proves that a helper is refused (AD-10).

## Epic List

The epics follow the PRD's priority tiers. Epics 1–3 are the T1 usability-test build (27 November 2026); the usability test in the first week of December is a real feedback point, so it is also an epic boundary. It runs locally on Rikke's machine, not on a public address (Rikke, 2026-11-23). Epics 4–7 complete the course version (T2, 10 December 2026), in the PRD's T2 order. Epic 8 is T3, cut first; anything not done by 10 December moves to [2027] with the reason in the PRD change log. NFRs are cross-cutting and apply to every story; the NFRs named under each epic are the ones it first makes testable.

**Decision: three epics change the RSVP form.** Epics 2, 4 and 7 all change the form in `wedding/rsvp/`. Merging them was considered and rejected: the usability test after Epic 3 may change the form, and the PRD's cut order puts Epic 7's parts last in T2.

**Migrations by story.** Each table is created by the first story that needs it:

- `User` (1.1)
- `Household` with `revision`, `Guest`, and `Settings` with its one row (1.2)
- `HouseholdAnswer` and `PersonAnswer` (2.6a)
- `Allergy` and `Consent` (2.6b)
- `Submission` (2.6c)
- `PaymentReport` (5.1)
- `Payment` (5.2)
- `AttentionMark` (6.2)
- the cache table for throttling (6.6)
- deactivated link codes (8.2)

### Epic 1: The guest opens their link and sees the invitation (T1)

**FRs covered:** FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-9 (page), FR-10 (page), FR-11, FR-68 (households, guests, links, settings, admin test users), FR-69 (the expected-results list written by hand), FR-72
**Also delivers:** project setup and CI (Story 1.1), AD-1, AD-5, AD-6, AD-9 (revision field), AD-10 (custom User with role in the first migration), AD-14, AD-15, AD-16 (fixtures), AD-17; UX-DR1–UX-DR9, UX-DR11–UX-DR15, UX-DR17, UX-DR30, UX-DR51, UX-DR53, UX-DR54; NFR-4 (link codes), NFR-5, NFR-8, NFR-9

### Epic 2: Guests answer for their household (T1)

**FRs covered:** FR-12, FR-13, FR-14, FR-15, FR-16, FR-17, FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-27, FR-28, FR-29, FR-32, FR-33, FR-34, FR-41, FR-70, FR-71 (derived message shown), FR-73, FR-74, FR-75, FR-78; FR-68 (seeded answers through the send service)
**Also delivers:** AD-2, AD-3, AD-4, AD-7, AD-8, AD-9 (revision checked), AD-11 (deadline function), AD-12, AD-18, AD-20 (submission id); UX-DR10 (answered, before the deadline), UX-DR16, UX-DR18–UX-DR21, UX-DR23–UX-DR26, UX-DR52; NFR-1, NFR-2, NFR-3, NFR-6
**Deviation from the PRD tiers:** FR-29 (consent record: who, when, text version) is pulled forward from T2 into Story 2.6b. Consent is stored in this epic anyway, and AD-3 already makes every service record its actor; adding the record later would mean a second migration of the same model.

### Epic 3: The couple sees the numbers and can trust them (T1)

**FRs covered:** FR-46 (couple login), FR-47, FR-48 (basic responsive), FR-54, FR-55, FR-57 (simple overview), FR-58, FR-69 (tests assert the expected-results list)
**Also delivers:** AD-10, AD-13, AD-16 (expected-results tests); UX-DR34, UX-DR36, UX-DR39, UX-DR40, UX-DR41, UX-DR42 (simple list), UX-DR48, UX-DR49; NFR-2, NFR-4 (password hashing, session expiry)

### Epic 4: Guests change their answer until the deadline locks it (T2)

**FRs covered:** FR-37, FR-38, FR-39, FR-42, FR-63, FR-64
**Also delivers:** AD-9, AD-11 (lock), AD-19 (changed marker), AD-20 (confirm); UX-DR10 (locked states), UX-DR28, UX-DR29, UX-DR33, UX-DR47; SM-11

### Epic 5: Payments are reported, registered and matched (T2)

**FRs covered:** FR-35, FR-36, FR-59, FR-60, FR-61, FR-71 (couple adjusts, duplicate warning); FR-68 (seeded payments and reports)
**Also delivers:** AD-4 (payment rows, `voided_at`), AD-12, AD-20 (confirm and undo); UX-DR45, UX-DR46, UX-DR49, UX-DR50 (protection tier 2); NFR-2

### Epic 6: The couple manages the guest list and follows up (T2)

**FRs covered:** FR-46 (helper role), FR-49, FR-51, FR-56, FR-57 (household pages)
**Also delivers:** AD-10 (`require_couple`), AD-19 (attention items and handled marks), throttling on the database cache; UX-DR35, UX-DR37, UX-DR38, UX-DR42, UX-DR43, UX-DR44, UX-DR50 (protection tier 3, typed FJERN); NFR-4 (login throttling, server-side role checks)

### Epic 7: Guests understand their privacy and get a finished form (T2)

**FRs covered:** FR-9 (full text), FR-10 (full text), FR-19, FR-20, FR-30, FR-66
**Also delivers:** AD-18 (withdrawal); UX-DR22, UX-DR27, UX-DR31, UX-DR32; NFR-3

### Epic 8: Cut-first extras (T3)

**FRs covered:** FR-31, FR-48 (beyond basic responsive), FR-50, FR-53, FR-65
**Also delivers:** AD-6 (new link), AD-9 (revision on move), link-code throttling; UX-DR50 (protection tier 2 for move, new link and consent); NFR-4 (wrong-link throttling)

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
**When** `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, locally and in a GitHub Actions workflow on every push and pull request
**Then** all of them pass

**Given** the repository root
**When** Ingrid opens it
**Then** `.env.example` lists every setting with safe example values and no real ones, `.gitignore` keeps out `.env`, `db.sqlite3`, `.venv`, `__pycache__` and collected static files, and `docs/manual-test-plan.md` exists for checks that are not automated
**And** `README.md` describes the app, lists prerequisites with versions, gives the exact install, start and test commands, explains the settings, shows the folder structure and links to the planning documents

### Story 1.2: Households, guests and personal links

As the couple,
I want each guest to have their own unguessable personal link that belongs to their household,
So that the link is the guest's only login and opens nothing but their own household.

**Covers:** FR-1, FR-2, FR-3, NFR-4 (link codes), AD-3, AD-4, AD-6, AD-9 (revision field)

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `Household` (with `revision`, starting at 0; AD-9), `Guest` (name, optional phone and email, link code) and a single-row `Settings` (the couple's contact names and phone numbers, prices as whole-kroner integers, the RSVP deadline as a date, Vipps number and account number), and no other tables
**And** a data migration creates the one `Settings` row with safe placeholder values, so a fresh `migrate` without test data already has settings; guest views read it with `.get()` and never create it, so FR-3 holds

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
**Then** no database row is created or changed (FR-3), and a test proves it at the resolver; the same test over an HTTP GET follows in Story 1.5, which adds the first guest view

**Given** two households
**When** the resolver returns the guest actor for a guest in the first
**Then** nothing in the actor gives access to the second household (FR-2)

### Story 1.3: Fictional test data and the hand-made expected-results list

As Ingrid the examiner,
I want one command that fills the database with fictional households and lists a test link for each guest,
So that I can try the invitation as different guests, and the numbers can later be checked against a list worked out by hand.

**Covers:** FR-47 (test accounts), FR-68, FR-69, FR-72, NFR-3, AD-14, AD-16
**Not in this story:** loading answers, allergies and consents (Story 2.6d), payment reports and payments (Story 5.2) and the withdrawn consent (Story 7.2) from `seed.toml`

**Acceptance Criteria:**

**Given** `wedding/fixtures/seed.toml`
**When** it is read
**Then** it describes the people from UJ-1 to UJ-3 (Sigmund and bestemor; Arild, Marie, Filippa and Leone; Synne) and households covering every case in FR-68: declines entirely, comes only on Saturday without a cabin, paid, part paid, owed a refund, an "I have paid" report without a matching payment, not answered, an allergy with consent, an allergy without consent, and a withdrawn consent
**And** each household's planned answers, allergies, consents, payment reports and payments are written as data in the file

**Given** `wedding/fixtures/expected.toml`
**When** it is committed, in its own commit before any code that computes these numbers
**Then** it holds the hand-worked results for the seed data: every FR-54 count, each household's total, payment status and allergy state, and the lock cases written as offsets from the seeded deadline (for example: 23:59:59 on the deadline date is open, one second later is locked), so they do not depend on the day the tests run (FR-69, AD-16)
**And** the commit message explains how the numbers were worked out

**Given** a local database
**When** Ingrid runs `uv run manage.py seed_testdata`
**Then** it creates the households and guests with fixed 22-character test codes, the settings (fictional prices, a deadline relative to today so the form is open, the couple's fictional contacts, a Vipps number and an account number with an invalid check digit), and a test couple admin and a test helper
**And** it creates everything by calling services with the system actor, and prints each guest's test link

**Given** the command has already run
**When** it runs again
**Then** the old test data is replaced, so the result is always the same
**And** the replacing is done by a reset service with the system actor that removes only rows the seed command created; once payments exist it voids them before removing (AD-4), and Story 5.2 repeats this test with payments seeded
**And** if a username or link code in `seed.toml` is already used by data the seed did not create, the command stops with a clear message and writes nothing

**Given** `APP_ENV` set to any value other than `local` (the default when it is not set)
**When** the command runs
**Then** it refuses, says why and writes nothing, and tests cover `production` and a misspelled value (FR-72, AD-14)

**Given** the seed data
**When** it is inspected
**Then** every person apart from Rikke and Valdemar is fictional, every email is on `example.com` and no phone number can belong to a real person (NFR-3)
**And** the README lists the command, a test link per guest and the test admin and helper logins

### Story 1.4a: The invitation's colours, type, buttons and notices

As a guest,
I want the invitation's colours, letters and buttons to look like Rikke and Valdemar's printed invitation and to be easy to read and use,
So that every page feels personal and works for me, also with the keyboard or high-contrast settings.

**Covers:** NFR-5, UX-DR1, UX-DR2, UX-DR15, UX-DR17, UX-DR53 (forced colours, focus), UX-DR54

**Acceptance Criteria:**

**Given** the stylesheet
**When** it is loaded
**Then** one CSS file defines every DESIGN.md colour token, the spacing scale and the radii as custom properties, and every page declares `color-scheme: light only` (UX-DR1)
**And** Imperial Script and EB Garamond (regular, italic, 600) are served from `static/fonts/` as WOFF2 with æ, ø and å, type is set in `rem`, guest body text is 20px and numbers use lining figures (UX-DR2)

**Given** primary, secondary, outlined-on-green and destructive buttons
**When** they get keyboard focus or are pressed
**Then** a 3px focus ring at 3px offset shows in the colour for its surface, and no style uses `outline: none` (UX-DR15)

**Given** the notice component
**When** it renders in its four variants
**Then** success, warning, error and info each have their icon, a 4px left rule and the word prefix («Feil:», «Obs:») where EXPERIENCE.md gives one; guest notices never disappear by themselves, and only notices added after the page has loaded use a live region (UX-DR17)

**Given** forced colours (for example Windows high contrast)
**When** buttons and notices render
**Then** button outlines, notice rules and the focus ring stay visible, and the check is recorded in the manual test plan (UX-DR53)

**Given** `prefers-reduced-motion: reduce`
**When** a link jumps within a page
**Then** it jumps without smooth scrolling; smooth scrolling is set only under `prefers-reduced-motion: no-preference`, and nothing on the page moves by itself (UX-DR54)

### Story 1.4b: Paper, Rikke's images and the private-invitation page

As a guest,
I want the pages to be paper sheets on the green with Rikke's own pictures, and a wrong link to show only a calm "private invitation" page,
So that the invitation feels real, and a stranger with a wrong link learns nothing about the wedding.

**Covers:** FR-5, NFR-5, UX-DR3, UX-DR4, UX-DR5, UX-DR30, UX-DR53 (reflow)
**Not in this story:** the «Personvern» link under the sheet (Story 7.1)

**Acceptance Criteria:**

**Given** a guest content panel
**When** it is rendered
**Then** it is a paper sheet: cream with paper texture, the soft `edge-b3` edge and shadow on a `::before` layer behind the content, a flat `panel-cream` fallback with 5px corners, and a 1px `CanvasText` border under forced colours (UX-DR3)
**And** the page is the textured `page-green`, and the texture leaves the average colour unchanged

**Given** Rikke's images
**When** they are prepared
**Then** the seal, gypsophila, lily garlands, lace frame, hero illustration 04, venue and couple photos and the twelve programme icons are in `static/img/`, and the favicon is made from the seal (UX-DR4)
**And** every decorative image has `alt=""`

**Given** an unknown code or the bare address `/`
**When** the page opens
**Then** it shows one paper sheet on the green with «Dette er en privat invitasjon», the gypsophila and «Virker ikke lenken din? Ta kontakt med brudeparet direkte.», and no names, phone numbers, date, place, seal, nav bar or footer (FR-5, UX-DR30)
**And** with an empty, migrated database and no test data, the page still renders (a test proves it)

**Given** the private-invitation page at 360 × 560, 320 × 568 and 180 × 320 CSS px
**When** it is checked in a browser
**Then** there is no horizontal scroll, the gutters follow DESIGN.md › Layout & Spacing, and the check is recorded in the manual test plan (UX-DR5, UX-DR53)

### Story 1.4c: Guest pages stay private: headers, link previews and logs

As a guest,
I want my link and my name to stay out of search engines, link previews and the server's logs,
So that nobody learns about the wedding or about me from a link that is shared.

**Covers:** FR-4, NFR-4, AD-15

**Acceptance Criteria:**

**Given** any guest response, including the private-invitation page
**When** its headers and HTML are inspected by a test
**Then** it sends `noindex` both as a meta tag and as `X-Robots-Tag`, `Referrer-Policy: same-origin`, a page title with no names, and loads nothing from other sites (FR-4, AD-15)
**And** external links have `rel="noreferrer"`

**Given** a guest link pasted into Messenger, SMS or email
**When** the preview is built from the page
**Then** the preview title, description and image (Open Graph tags) are the same for every code and contain no names, and a test compares the previews for two different codes (FR-4)

**Given** a request to a guest page
**When** it is logged
**Then** a logging filter masks the link code in the request path, and a test proves no code is logged (AD-15)

### Story 1.5: The invitation front page

As bestefar Sigmund,
I want my link to open an invitation that shows at once who is getting married, when, where, that bestemor and I are invited and by when to answer,
So that I understand the invitation without scrolling and always see where to answer.

**Covers:** FR-2, FR-3 (over HTTP), FR-6, FR-7, FR-8, FR-11 (page frame), FR-41 (display), NFR-7, UX-DR6, UX-DR7, UX-DR8, UX-DR9, UX-DR11, UX-DR12 (frame), UX-DR51
**Not in this story:** the RSVP button (Story 2.1)

**Acceptance Criteria:**

**Given** a valid personal link
**When** the guest opens `/<code>/`
**Then** the page shows the sticky nav bar (Program · Praktisk · Vår historie, and the «Svar» button), the hero sheet, the lead-in, «Alt om helgen», the RSVP sheet and the footer band, in that order (FR-7, FR-8)
**And** it shows only that guest's household and nothing from any other (FR-2)

**Given** the hero sheet
**When** it renders
**Then** it holds, in order, the seal over the top edge, the whole illustration, «Rikke & Valdemar» as the page's `h1`, the invites line, the gypsophila, the date and place in small capitals, «for <household names>» and «**Svar** innen <date>» (UX-DR7)
**And** it uses «deg» when one person is invited and «dere» when two or more are (UX-DR51)
**And** the whole hero fits above the fold at 360 × 560 and 320 × 568, the names stack instead of shrinking at narrower widths, and the measurement is recorded in the manual test plan

**Given** the nav «Svar» button or the «Svar» link in the deadline line
**When** the guest activates either, without JavaScript
**Then** the page jumps to the RSVP sheet (`#svar`), which is not hidden under the sticky bar (UX-DR6, UX-DR9)
**And** the nav bar is sticky only when the viewport is at least 400px tall and at least 20em wide *(width condition added 2026-11-23 after the Epic 1 retrospective, R1: Story 1.5 built it, approved by Rikke)*, keeps the three words on one line at 320px, and never becomes a menu button

**Given** «Alt om helgen»
**When** it renders
**Then** it has the top and bottom lily garlands, the italic heading with its hairline, and three topic rows (Programmet, Praktisk informasjon, Vår historie), each with a lace-framed picture, an `h3`, one italic line and «Les mer» with an accessible name such as «Les mer om programmet» (UX-DR8)
**And** each «Les mer» and nav word opens that topic's page under `/<code>/`, which in this story has the info-page frame only: back link, italic title with hairline, the bottom back button, and the current nav word marked with `aria-current` (FR-11, UX-DR12)

**Given** the RSVP sheet
**When** it renders
**Then** it shows «Svar på invitasjonen», the small gypsophila, «Barnefritt bryllup» and the full deadline with weekday, date and «kl. 23:59» in Norwegian time (FR-41, UX-DR9)

**Given** any page under a valid link
**When** the guest scrolls to the bottom
**Then** the footer band shows «Spørsmål? Send oss en melding:» and each of the couple's phone numbers from Settings as its own `tel:` link at least 44px tall (FR-6, UX-DR11)

**Given** a valid personal link
**When** the guest opens `/<code>/` and each topic page under it with a GET request
**Then** no database row is created or changed, and a test proves it over HTTP with Django's test client (FR-3; Story 1.2 tested the resolver on its own)

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

**Given** a 500 caused by a database failure
**When** the error page tries to resolve the code
**Then** a failed lookup falls back to the page without names, so the error page itself never fails (FR-5)

**Given** the error pages
**When** a test requests each of them with a valid and with an unknown code, and with an empty, migrated database
**Then** each shows the content described above and sends the guest headers from Story 1.4c

## Epic 2: Guests answer for their household

Sigmund and Arild answer for everyone in their household on a phone: who is coming, which days, overnight stay, meals with prices, allergies with consent and the Friday hike. They see the running total, check everything before sending, get a receipt in Rikke's words, choose to pay now or later, and see their household's status on the invitation afterwards. An interrupted answer is offered back when they return.

Deviation from the PRD tiers: FR-29 is pulled forward from T2 into Story 2.6b (see the Epic List).

### Story 2.1: Start the answer: who is coming

As bestefar Sigmund,
I want to press the RSVP button and first mark who in my household is coming,
So that the rest of the form only asks about the people who come.

**Covers:** FR-12, FR-13, FR-14 (step 1), FR-22, FR-41 (deadline rule), NFR-5, NFR-6, AD-1, AD-7, AD-8, AD-11, UX-DR16, UX-DR17, UX-DR18, UX-DR19, UX-DR20, UX-DR52 (form check)
**Not in this story:** the locked views after the deadline (Story 4.3)

**Acceptance Criteria:**

**Given** the RSVP sheet on the front page
**When** it renders for a household that has not answered
**Then** it has the primary button «Svar på invitasjonen», which opens the form at `/<code>/svar/`

**Given** the deadline function in `wedding/rules/`
**When** it is given the deadline date and `now`
**Then** it says the deadline has passed from 00:00:00 Oslo time on the day after the deadline date, so 23:59:59.999 is still open, and tests cover both sides of the boundary and a winter/summer time change (FR-41, AD-11)
**And** after the deadline the form does not open; the guest sees the deadline with weekday and date and the couple's phone numbers instead

**Given** the form's first step
**When** it opens
**Then** it shows the step question as `h1`, the progress line «Steg 1 av m: <name>» and the respondent line «Jeg er <link owner>» (FR-12, FR-13, UX-DR19)
**And** before step 1 is answered, m counts every step as if everyone comes the whole weekend; from then on it follows the answers (UX-DR19)
**And** each household member is a fieldset with «Kommer» and «Kommer ikke», and nothing is selected (FR-14)
**And** form steps have no nav bar (UX-DR19)

**Given** a household with more than one person
**When** a step renders
**Then** the respondent line ends with «· Bytt»; for a household of one, «Bytt» is not shown

**Given** the respondent presses «Bytt»
**When** they pick another household member
**Then** that person is recorded as the one answering, and nothing already filled in changes (FR-12)

**Given** step 1 sent with a person left unanswered
**When** the server validates it
**Then** the step re-renders with status 200, the error under that person's legend as icon and «Feil: …», and a focused error summary at the top whose links focus each field; the page title starts with «Feil: » (FR-22, UX-DR16, UX-DR18)

**Given** a valid step
**When** «Fortsett» is pressed
**Then** the server saves the step in the draft cookie (signed, compressed, `HttpOnly`, `SameSite=Lax`, scoped to `/<code>/`) and redirects to the next step's own address (POST-redirect-GET), and nothing is stored in the database (AD-7, AD-8)
**And** «Tilbake» and the browser's Back button show the previous step with its answers, without a resubmit prompt (UX-DR20)

**Given** the whole guest flow
**When** a test runs it
**Then** no session rows are created and the messages framework is never used (AD-8)
**And** every step works without JavaScript (AD-1)

**Given** a draft cookie with a bad signature, that fails to decompress, or in an old format
**When** any step opens
**Then** the cookie is deleted and the form starts empty, and a test proves there is no server error (AD-8)

**Given** a form step whose form check fails (CSRF)
**When** the guest sees the result
**Then** the same step is shown again with what they typed filled in, nothing is saved, and a notice says what happened and «Prøv igjen» (UX-DR52)

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
**And** a person's days must follow each other (one day, Friday–Saturday, Saturday–Sunday or all three); Friday and Sunday without Saturday gives a field error that explains why (FR-14, FR-70)

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
**Then** the tests pass plain values, cover all household shapes in `seed.toml`, and list every day combination in one table, including the refused Friday and Sunday

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
**And** overnight stay is offered for two or three days in a row; a table-driven test in `wedding/rules/` covers every allowed day combination

**Given** a person who stays overnight
**When** their days are later changed to one day, for example through «Endre» on the check page
**Then** `normalise_answer` removes the overnight stay, so it never shows or counts (FR-75)

**Given** the meals step
**When** it renders
**Then** each coming person is offered only the paid meals on their days (Friday dinner, Saturday breakfast only if present on both Friday and Saturday, Sunday breakfast), each with its price, and Saturday lunch and dinner are not asked about (FR-15, FR-73)
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
**Then** each coming person has «Ingen allergier eller matbehov» and the categories gluten, laktose, nøtter, skalldyr, vegetar, veganer and annet, plus a short note field of at most 200 characters, checked by the server with an FR-22 error (FR-25, AD-8)
**And** the question is optional

**Given** one person's «Ingen allergier eller matbehov» and a category
**When** the respondent ticks both
**Then** with JavaScript, ticking one clears the other; without JavaScript, the step comes back with an inline error asking them to choose one (UX-DR21)

**Given** the consent block
**When** it renders
**Then** the text says what the information is for, who sees it (the couple, toastmaster, maid of honour and best man), that names and allergies go to Hardingasete's kitchen, and that consent can be withdrawn through the same link (FR-26)
**And** inside each coming person's fieldset there is that person's own Ja/Nei consent choice, which starts unanswered, so consent is given or refused per person (FR-26, FR-29, UX-DR21)
**And** every fieldset except the respondent's has «Jeg bekrefter at <name> vet om dette og er enig» (FR-27)

**Given** consent «Ja» for someone other than the respondent, with allergy information entered for them
**When** the confirmation is not ticked
**Then** the step comes back with a field error on the confirmation (FR-22, FR-27), and a test covers it

**Given** allergies entered and consent not given
**When** the respondent continues
**Then** the step and later the check page say plainly that the allergy information will not be saved and that the guest can tell the couple directly, and continuing is still allowed (FR-28)

**Given** the draft for a household of 8 people with every field filled to its maximum
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

**Given** nobody comes on Friday
**When** the respondent finishes the previous step
**Then** the hike step is skipped and not counted in the progress line

**Given** the last step is done
**When** the check page opens
**Then** «Obs: Svaret er ikke sendt ennå.» is at the top, followed by the `h1` «Se over svaret før du sender», one block per part (Hvem kommer · Dager · Overnatting · Måltider · Allergier og matbehov · Fjelltur fredag) with each person's answer, and the household total (FR-21)
**And** skipped optional answers show «Ikke oppgitt», and allergies entered without consent show the FR-28 warning

**Given** an «Endre» link on the check page
**When** the respondent uses it
**Then** it opens that step with the answers filled in, and «Fortsett» returns to the check page; each link has hidden context such as «Endre måltider» (UX-DR23)
**And** if the change adds a person or a day, «Fortsett» goes to the first later step with questions for them, and the check page comes after that step, so nobody is sent without answers

**Given** the check page
**When** it renders
**Then** «Send svaret» is the primary button, above «Tilbake»

### Story 2.6a: Send the answer

As bestefar Sigmund,
I want my answer saved when I press «Send svaret»,
So that the couple gets it.

**Covers:** FR-41 (sends refused after the deadline), FR-74, NFR-2, AD-3, AD-4, AD-9, UX-DR15 (busy state)

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `HouseholdAnswer` (sent by, with the sender's name kept as text; sent at) and `PersonAnswer`, and nothing derived such as totals (AD-4)

**Given** «Send svaret» pressed on a valid draft
**When** `send_answer` runs with the guest actor
**Then** it writes the answer in one IMMEDIATE transaction, records the respondent as the sender, raises `Household.revision` and deletes the draft cookie (AD-3, AD-9)
**And** the button shows «Sender …» while the send is under way and ignores more taps (UX-DR15)

**Given** a guest send after the deadline
**When** it reaches `send_answer`
**Then** it is refused using the deadline function from Story 2.1, nothing is written, and the guest sees the deadline and the couple's phone numbers (FR-41)

**Given** `send_answer`
**When** tests run
**Then** a guest actor cannot write to another household (AD-3), and person and household states follow FR-74 (coming, not coming, not answered; a household is answered once sent)

### Story 2.6b: Allergies are stored only with consent

As bestemor,
I want my allergy information stored only when I have said yes, and deleted when I say no,
So that nothing about my health is kept without my consent.

**Covers:** FR-26, FR-28, FR-29, NFR-3, AD-18

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `Allergy` and `Consent`; each consent row records one event per person (given, refused or withdrawn), when, who gave it (the actor and their name as text) and the consent-text version from `CONSENT_TEXT_VERSION`, so withdrawal in Story 7.2 adds a row without a new migration (FR-29, AD-18)

**Given** a send
**When** `send_answer` stores the allergy step
**Then** allergy data and «Ingen allergier eller matbehov» are stored only for people whose consent is «Ja», and each consent is recorded per person (FR-26, FR-29, AD-18)

**Given** a re-send
**When** a person's consent is left unanswered
**Then** that person's stored allergy data is kept unchanged (AD-18)
**And** if the allergy fields were changed, the check page says before sending that the changes are not saved without a consent answer (FR-28)

**Given** a re-send
**When** a person's consent is «Nei» and allergy data was stored for them
**Then** that data is deleted and the refusal is recorded (AD-18)

**Given** the consent rules
**When** tests run
**Then** they cover «Ja», «Nei» and unanswered, on a first send and on a re-send, for the respondent and for another household member

### Story 2.6c: A send that fails or repeats is safe

As bestefar Sigmund,
I want a double tap, a changed price or a failed save never to lose or double my answer,
So that I can trust what I sent, and I am told clearly if something went wrong.

**Covers:** NFR-1, AD-7, AD-9, AD-20, UX-DR52

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `Submission` (submission id, unique; kind; what was written) (AD-20)

**Given** the same submission sent twice (double tap)
**When** the second POST arrives
**Then** the earlier result is returned and nothing is written twice; the submission id is checked in `Submission` before the revision check (AD-20)

**Given** a draft started at an older revision than the household's
**When** it is sent
**Then** nothing is written and the check page is shown again with a notice that the answer has changed (AD-9)

**Given** the total recalculated at send differs from the total on the check page
**When** the send is attempted
**Then** nothing is written and the check page is shown again with a notice about the new total (AD-7)

**Given** a refused send (older revision, changed total or the deadline)
**When** the guest sends again
**Then** it is handled as a new send, because a refused send records no `Submission` (AD-20)

**Given** a write that fails
**When** the guest is shown the result
**Then** the error notice says what happened, that nothing is lost, «Prøv igjen», and the couple's phone numbers, and every answer stays in the draft (NFR-1, UX-DR52)

### Story 2.6d: Test data with answers, and a real-browser send

As Ingrid the examiner,
I want the test households to have their answers, allergies and consents after seeding,
So that the admin numbers have something to count and can be checked against the expected-results list.

**Covers:** FR-68 (answers), AD-16

**Acceptance Criteria:**

**Given** `seed_testdata`
**When** it runs
**Then** it loads the answers, allergies and consents in `seed.toml` through `send_answer` with the system actor, and the result matches the households described in the file

**Given** the manual test plan
**When** this story is done
**Then** it records one real-browser send, since Django's test client sends no browser headers

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

**Covers:** FR-24, FR-34 (pay later), UX-DR10
**Not in this story:** «Meldt betalt: …» (Story 5.1); «Dere kan endre svaret fram til <weekday date> kl. 23:59.» and «Se eller endre svar» (Story 4.1), so the page never promises a change it cannot make

**Acceptance Criteria:**

**Given** a household that has answered
**When** any member opens their link
**Then** the hero's deadline line reads «Svar sendt <date> · Se svaret», and the RSVP sheet's place holds the status block (`id="status"`): «Svaret er sendt», the small gypsophila, «Barnefritt bryllup», «Sendt av <name> <weekday date> kl. <time>.» and «Totalt for husstanden: …» (FR-24, UX-DR10)

**Given** a household that has answered and owes money
**When** the status block renders
**Then** it has a link to «Slik betaler du» with the same payment details as the receipt, so «Betal senere» keeps its promise (FR-34)

**Given** the answered front page
**When** the guest uses the nav «Svar» or «Se svaret»
**Then** the page jumps to the status block and focus lands on its heading

**Given** a household that has answered
**When** a member opens `/<code>/svar/` directly
**Then** they are sent to the status block, so the answer cannot be overwritten before changing an answer is built (Story 4.1 lifts this)

### Story 2.9: An interrupted answer is kept on the phone

As bestefar Sigmund,
I want my half-finished answer to be waiting when the phone rings and Messenger reloads the page,
So that I don't have to start again.

**Covers:** FR-78, AD-8, AD-11, UX-DR26

**Acceptance Criteria:**

**Given** a draft cookie from an earlier visit
**When** the guest opens their link
**Then** the RSVP sheet shows «Du har et svar som ikke er sendt ennå.» (UX-DR26)
**And** a test sends a GET to `/<code>/` with the draft cookie set at the path the form uses and sees the notice (AD-8)

**Given** a draft
**When** the form is opened by any route (the nav «Svar», the RSVP button or reloading a step)
**Then** the draft offer comes first: «Vil du fortsette der du slapp?», when the answer was started, «Ja, fortsett» and «Nei, begynn på nytt» (FR-78)
**And** «Ja, fortsett» opens the step they left with all answers filled in; «Nei, begynn på nytt» deletes the draft and starts from the sent answer or empty

**Given** a draft whose household has changed since it was started (a person added, removed or moved)
**When** «Ja, fortsett» is chosen
**Then** answers for people no longer in the household are dropped, and the form opens at step 1 so everyone in the household is asked (AD-8)

**Given** a draft cookie after the deadline
**When** the guest opens their link
**Then** no draft notice or offer is shown, and the cookie is deleted, using the deadline function from Story 2.1 (AD-11)

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
**And** an existing username or a role other than `couple` or `helper` is refused with a message, the `role` field has no blank value, and a user without a valid role gets no admin access
**And** the command creates real accounts with `is_test_data=False` through its own path, never the system actor: `create_admin_user` is for the seed command only and marks every account it makes as test data (AD-16), and a test shows that `seed_testdata` leaves accounts made by `create_admin` alone

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
**And** `allergy_state` gives each coming guest exactly one of the three AD-18 states, and `payment_status(answered, total, received, refunded)` covers all five FR-60 statuses and «not answered» for a household that has not answered, as a pure function, with received and refunded at 0 until payments exist (Story 5.2)

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
**Not in this story:** the Betaling panel, payment statuses and report matches (Story 5.3); the withdrawn-consent household (Story 7.2); the lock cases (Story 4.3)

**Acceptance Criteria:**

**Given** the seed data loaded by `seed_testdata`
**When** `uv run pytest` runs the expected-results tests
**Then** every FR-54 count except the Betaling panel, each household's total and each guest's allergy state equals `wedding/fixtures/expected.toml`, with `now` passed explicitly (FR-69, AD-16)

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

**Covers:** FR-37, FR-38 (last updated), FR-39, FR-41 (change window), AD-19, UX-DR10, UX-DR28

**Acceptance Criteria:**

**Given** a household that has answered, before the deadline
**When** a member opens the status block
**Then** it has the line «Dere kan endre svaret fram til <weekday date> kl. 23:59.» and the primary button «Se eller endre svar», which opens the form with the sent answers filled in (FR-37, FR-41, UX-DR10)
**And** the top of the form shows the info notice «Sist endret av <name>, <date> kl. <time>» (FR-38, UX-DR28)

**Given** a changed answer is sent
**When** `send_answer` saves it
**Then** the household's `changed_at` is set by the one helper in AD-19, and the first answer and payment reports never set it (FR-39)
**And** a re-send whose content, after `normalise_answer`, is the same as the stored answer does not set `changed_at`

**Given** a household that has answered, before the deadline
**When** a member opens `/<code>/svar/`
**Then** the form opens with the sent answers filled in, instead of the redirect to the status block from Story 2.8

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
**Not in this story:** a draft started before a couple override (Story 4.4, which builds the override)

**Acceptance Criteria:**

**Given** Marie's draft started at revision n
**When** Arild sends an answer (revision n+1) and Marie then presses «Send svaret»
**Then** nothing is written, and Marie sees a warning notice with who sent, when and what differs from her draft (FR-38, AD-9), replacing the simple notice from Story 2.6c
**And** she can review and send again, and that second send is saved

**Given** a draft with a consent «Ja»
**When** the revision has changed
**Then** the consent «Ja» is not carried across, and the respondent must answer consent again (AD-18)

**Given** the conflict check
**When** tests run
**Then** they cover two members sending in sequence

### Story 4.3: The answer locks at the deadline

As the couple,
I want guests' answers to lock at 23:59 on the deadline day,
So that the numbers we give Hardingasete stay fixed.

**Covers:** FR-42, SM-11, AD-11, UX-DR10 (locked), UX-DR33

**Acceptance Criteria:**

**Given** a guest send that changes answer content after the deadline
**When** it reaches the service
**Then** it is refused, using the one deadline function (AD-11), and the guest sees the read-only answer view with the deadline text and the couple's phone numbers; the draft is deleted

**Given** a consent withdrawal or an "I have paid" report after the deadline
**When** it reaches its service
**Then** it is accepted (AD-11)

**Given** an answered household after the deadline
**When** a member opens their link
**Then** the status block has «Se hele svaret», which opens the read-only answer view with «Fristen gikk ut <weekday date> kl. 23:59» and the couple's phone numbers (FR-42, UX-DR33)

**Given** a household that never answered, after the deadline
**When** a member opens their link
**Then** the hero line reads «Svarfristen gikk ut <date> · Ring oss», and the RSVP sheet's place shows the deadline message and contacts instead of the RSVP button (UX-DR10)

**Given** the lock
**When** tests run with `now` just before and just after the deadline
**Then** both sides behave as described (SM-11)
**And** the expected-results tests assert the lock cases in `expected.toml` (FR-69)

### Story 4.4: The couple fills in or changes any household's answer

As Rikke,
I want to fill in or change a household's answer with the same form the guests use, also after the deadline,
So that I can help Synne when she calls.

**Covers:** FR-39, FR-63, AD-3, AD-7, AD-9, AD-10, AD-18, AD-19

**Acceptance Criteria:**

**Given** a household's row in Gjester (its household page from Story 6.3 links here too)
**When** Rikke chooses «Endre svaret»
**Then** the same form from `wedding/rsvp/` opens at `/admin/husstand/<id>/svar/`, with the household's answers filled in (FR-63, AD-7)

**Given** the deadline has passed
**When** Rikke sends the answer
**Then** it is saved, and the admin is recorded as the author (FR-63, AD-3)

**Given** the form opened by the couple
**When** it renders
**Then** the respondent line reads «Jeg er Rikke og Valdemar» without «Bytt», and the guest pages show «Sendt av Rikke og Valdemar», never an admin username (FR-12, FR-24)
**And** on the allergy step every person's consent is shown as read-only and kept as it is; the couple can enter allergies only for people with stored consent, and registering new consent is Story 8.3 (FR-31, AD-18)

**Given** the couple overrides an answer that was already sent
**When** it is saved
**Then** `changed_at` is set by the AD-19 helper; a first answer filled in by the couple does not set it, and tests cover both (FR-39)

**Given** a guest send that arrives while the couple has the form open
**When** the couple sends
**Then** nothing is written and the couple sees the Story 4.2 conflict notice, and a test proves it (FR-38, AD-9)

**Given** a guest draft started before the couple's override
**When** the guest presses «Send svaret»
**Then** nothing is written and the guest sees the Story 4.2 conflict notice naming the admin as the sender, and a test proves it (FR-38, AD-9)

**Given** any admin write service
**When** it is called
**Then** it calls `require_couple(actor)`, and a test proves a helper actor is refused (AD-10)

### Story 4.5: The couple changes the deadline, prices and contact details

As Rikke,
I want to change the deadline, prices, our phone numbers and the payment details in the admin area,
So that real values can be set without changing code.

**Covers:** FR-64, AD-20, UX-DR29, UX-DR47, UX-DR50 (protection tier 2)

**Acceptance Criteria:**

**Given** the Innstillinger page
**When** Rikke saves a change
**Then** a confirmation step (a first POST that writes nothing) shows the change; the second POST saves it (AD-20)
**And** with JavaScript the confirmation is a dialog with `role="alertdialog"`, focus on the safe button, Esc to cancel and focus back to the trigger; without it, a confirm page (UX-DR29)

**Given** a price that is negative or not a whole number, or an empty deadline
**When** Rikke saves
**Then** the field errors from FR-22 show before any confirmation, and nothing is saved

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
**And** amounts accept «900», «900 kr» and «1 450»; zero, negative amounts and øre («1 450,50») are refused with FR-22 errors
**And** «Jeg har betalt» is not shown when the household owes nothing

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

**Covers:** FR-59, FR-68 (payments), AD-3, AD-4, AD-12, AD-20, UX-DR45 (household page), UX-DR50 (protection tier 2)

**Acceptance Criteria:**

**Given** this story's migration
**When** it is applied
**Then** it creates `Payment` with kind `received` or `refunded`, a positive whole-kroner amount, who registered it and `voided_at` (AD-4)

**Given** a household's payment page
**When** Rikke registers «Mottatt fra gjesten» or «Betalt tilbake til gjesten» with an amount
**Then** a protection-tier-2 confirmation names the new status, and after saving the page shows «Registrert: mottatt <amount>.» with «Angre» (FR-59, UX-DR45)

**Given** «Angre» on a registration
**When** it is used
**Then** the payment is voided by setting `voided_at`, never deleted; undoing an older entry asks for confirmation first (AD-4, AD-20)

**Given** a refund larger than received minus earlier refunds
**When** Rikke registers it
**Then** it is refused with an explanation, and a test covers it

**Given** `seed_testdata`
**When** it runs
**Then** it now loads the payments and payment reports in `seed.toml` through the services
**And** running it a second time still gives the same result, because the reset voids seeded payments before removing test data (Story 1.3)

### Story 5.3: Payment status and the payments list

As Rikke,
I want each household's payment status worked out from the money, and mismatches marked,
So that I know who to remind and who to pay back.

**Covers:** FR-60, FR-61, NFR-2, AD-2, UX-DR45 (list), UX-DR49

**Acceptance Criteria:**

**Given** a household's total, received and refunded amounts
**When** `payment_status` is computed
**Then** it is nothing to pay, not paid, part paid (X missing), paid or refund owed (X), shown only to admins (FR-60)
**And** a household that has not answered has no payment status and shows «Ikke svart», so `payment_status` is also told whether the household has answered (FR-60)

**Given** an "I have paid" report
**When** received minus refunds is lower than the reported amount
**Then** the household gets the «Stemmer ikke» tag (error icon and word) in the overview and on the payments list (FR-61, UX-DR49)

**Given** the Betalinger page
**When** it renders
**Then** it shows «Til sammen» (Skal betales · Mottatt · Mangler · Skal betales tilbake) and one row per household that owes something or has payments that are not voided (so a household that paid and then stopped coming is listed), sorted stemmer ikke → skal ha tilbake → delbetalt → ikke betalt → betalt → ingenting å betale (UX-DR45)
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

**Given** a payment report lower than the household's total, for any reason
**When** the guest sees the status block, receipt or payment details
**Then** they read «Du har <amount> igjen å betale» (FR-36)

**Given** a payment report higher than the household's total
**When** the guest sees the status block, receipt or payment details
**Then** they read «Rikke og Valdemar har fått beskjed og betaler tilbake <amount>» (FR-36), and the couple has a matching item under «Trenger oppfølging» (Story 6.2)

**Given** a payment report equal to the total
**When** the guest sees these pages
**Then** no remaining amount or refund is shown, and `guest_balance` has a test for all three cases

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
**Then** the adjusted message is stored; a message nobody has adjusted is derived from the household's names and never stored (AD-4)
**And** saving an empty message removes the adjustment, so the derived message is used again

**Given** a message identical to another household's (derived or adjusted)
**When** Rikke tries to save it
**Then** she is warned before saving, and the warning names the other household (FR-71, UX-DR46)
**And** the same duplicate check runs when a household is added (Story 6.4) and when the seed command runs

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
**And** it shows the first 2 items and then «Vis alle n», so «Svart: X av Y» stays on the first screen at 360 × 560; the number is checked in the manual test plan and may be changed after measuring (EXPERIENCE.md › A2)
**And** «refunds owed» includes households whose "I have paid" report is higher than their new total, even before the couple has registered the payment (FR-36)

**Given** an item
**When** Rikke presses «Merk som håndtert» (or «Merk som sett» for «Endret»)
**Then** the row is replaced in place by «Merket som håndtert. Angre», with focus on «Angre» and no timer, and the item disappears from the list when Rikke leaves the page (UX-DR38)

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
**And** the search ignores upper and lower case also for æ, ø and å («øystein» finds «Øystein»), which SQLite's `LIKE` does not do on its own, and a test covers it

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
**And** a household has at most 8 people, so its draft fits the 4 KB cookie (AD-8)

**Given** a person added to a household that has already answered
**When** the household is saved
**Then** the new person is «Ikke svart», and the household is listed under «Trenger oppfølging» until someone answers for them

**Given** «Endre navn og kontaktinfo»
**When** Rikke presses «Lagre endringene»
**Then** a protection-tier-2 confirmation names what changes, including that the payment message changes, with the FR-71 duplicate warning
**And** adding a person raises the household's revision (AD-9)

**Given** a missing name or an invalid email
**When** the form is sent
**Then** the error summary and field errors appear, and everything typed is kept

### Story 6.5: Remove a household or a person

As Rikke,
I want to remove a household or one person, with a confirmation that is hard to do by mistake,
So that people who are no longer invited disappear from the numbers.

**Covers:** FR-49 (remove), AD-4, AD-9, UX-DR50 (protection tier 3)

**Acceptance Criteria:**

**Given** «Fjern husstanden» or «Fjern <name> fra husstanden»
**When** Rikke chooses it
**Then** a dialog asks her to type FJERN; matching ignores case and surrounding spaces, the field has `autocapitalize="off" autocorrect="off" spellcheck="false"`, and a wrong word gives an inline error (UX-DR50)

**Given** the removal is confirmed
**When** the service runs
**Then** the guest's answers, allergies and consent records are deleted with them, the household's revision is raised, and the result message is announced at the top of Gjester (AD-4, AD-9)
**And** if the removed person sent the household's answer or gave consent for others, the answer and the others' consent records are kept, with the name kept as text; a test covers it

**Given** a household with one person left
**When** its edit form renders
**Then** «Fjern <name> fra husstanden» is hidden, and the service refuses to remove the last person and suggests removing the household instead

**Given** a household or guest with payments that are not voided
**When** removal is attempted
**Then** it is refused with an explanation (AD-4)

### Story 6.6: Slow down repeated login attempts

As the couple,
I want repeated wrong logins to be slowed down,
So that nobody can guess our passwords.

**Covers:** NFR-4

**Acceptance Criteria:**

**Given** 5 failed logins for one username, or 20 from one address, within 15 minutes
**When** the limit is reached
**Then** further attempts for that username or from that address are refused for 15 minutes with a plain Norwegian message (NFR-4)
**And** the limiter is one shared helper on Django's database cache (`createcachetable`, a set `MAX_ENTRIES`), so it can be reused for link codes (Story 8.6)

**Given** a successful login after the wait
**When** it happens
**Then** it works normally, and tests cover both sides of the limit

**Given** the README
**When** Ingrid follows the install steps on a clean machine
**Then** they include `uv run manage.py createcachetable` (or a migration creates the cache table), and the clean-machine run is repeated and recorded

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

**Given** «Personvern» in the consent block
**When** the guest uses it
**Then** it is a button that first saves what is typed on the step to the draft (without checking it) and then opens the privacy page
**And** «Tilbake» from the privacy page returns to the same step with everything kept (UX-DR21)

### Story 7.2: Withdraw consent

As bestemor,
I want to withdraw my consent and have my allergy information deleted, also after the deadline,
So that I decide over my own health information.

**Covers:** FR-30, AD-3, AD-9, AD-11, AD-18, AD-19, UX-DR32

**Acceptance Criteria:**

**Given** the last part of the privacy page, and the answer view next to the allergies
**When** a household member opens either
**Then** it lists each person with anything stored on the strength of consent, also «Ingen allergier eller matbehov», with «Trekk samtykket for <name>», or «Ingen allergiopplysninger lagret.» (UX-DR31, UX-DR32)

**Given** «Trekk samtykket for bestemor»
**When** the guest confirms in the dialog («Trekke samtykket for bestemor?», «Avbryt» focused, «Slett allergiopplysningene»)
**Then** `withdraw_consent` deletes that person's allergy data, adds a consent row of kind «withdrawn», raises the revision and marks the household changed, and the page says «Allergiopplysningene til bestemor er slettet.» (FR-30, AD-18, AD-19)
**And** a person id from another household is refused, and a test proves it (AD-3)

**Given** the deadline has passed
**When** consent is withdrawn
**Then** it works (AD-11)

**Given** the withdrawal
**When** the admin pages are opened
**Then** the person is in «Ingen allergiopplysninger lagret», the household is tagged «Endret», and an old draft can never store the withdrawn allergy again (AD-18)

**Given** `seed_testdata`
**When** it runs
**Then** it now applies the withdrawn consent in `seed.toml` through `withdraw_consent`, and the expected-results tests assert that household

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
**And** where the browser supports it, its own leave prompt shows when the tab is closed

**Given** a step's own «Fortsett» or «Tilbake», a reload, or «Personvern» from the consent block
**When** the guest uses it
**Then** no leave warning is shown, since the answer is kept (FR-78)
**And** the manual test plan records the warning on iOS Safari and in Messenger's in-app browser

### Story 7.4: The full text of the programme and practical information

As a guest,
I want the real times, prices and practical details,
So that I can plan the weekend.

**Covers:** FR-9, FR-10

**Acceptance Criteria:**

**Given** the couple's final texts and times, delivered by Rikke and Valdemar before this story starts
**When** the Programme and Practical information pages render
**Then** the placeholders are replaced, the programme marks what costs money and what to bring, and practical information covers every FR-10 topic (FR-9, FR-10)

**Given** the full text
**When** the pages are checked at 360 × 560, 320 × 568 and 180 × 320
**Then** there is no horizontal scroll and the check is recorded in the manual test plan

**Given** times that are not final by 10 December 2026 (Hardingasete's final times come in early 2028)
**When** the story is done
**Then** the best-known times are used and each open item is listed in the PRD change log

**Given** the real address of Hardingasete
**When** «Hvordan komme seg dit» renders
**Then** it has the outlined button «Åpne veibeskrivelse i kart», a link to a chosen map service with the address filled in, with `rel="noreferrer"` (AD-15), and the privacy page (Story 7.1) says that the link leaves the site for that service

**Given** the guest pages after the full text is in
**When** the tests run
**Then** a test fails if any guest page still contains a square-bracket placeholder such as «[14:00]» or «[adresse]», so no placeholder reaches a guest
**And** the one exception is «[stilling]» on Vår historie, which the test allows until Rikke's job title is decided *(added 2026-11-23: Rikke decided the placeholder stays through the course submission, since the title is not decided before then; see `deferred-work.md`)*

*(Changed 2026-11-20 in Story 1.6: the map button from `mockups/info-praktisk.html` moved here, since there is no real address yet and no map service decided; the placeholder test was added so the placeholders that Story 1.6 keeps on Praktisk informasjon cannot be forgotten. See `deferred-work.md`.)*

## Epic 8: Cut-first extras (T3)

The couple can move a guest to another household, replace one guest's link, register consent given by phone, and is warned when a price change affects households that have answered. The admin pages use a PC screen better, and repeated wrong-link attempts are slowed down. Whatever is not done by 10 December moves to [2027], with the reason in the PRD change log.

### Story 8.1: Move a guest to another household

As Rikke,
I want to move a guest to another household,
So that the households match how people actually answer.

**Covers:** FR-50, AD-9, UX-DR50 (protection tier 2)

**Acceptance Criteria:**

**Given** a guest on a household page
**When** Rikke moves them to another household and confirms the protection-tier-2 dialog
**Then** the guest keeps their link, both households' revisions are raised, and both totals and counts follow the move (FR-50, AD-9)
**And** the guest's attendance answers are removed, so they are «Ikke svart» in the new household; their consent and allergy data stay with them, since they belong to the person
**And** both households' payment messages are checked for duplicates (FR-71)

**Given** the last person in a household
**When** Rikke tries to move them
**Then** the move is refused, and she is told to remove or edit the household instead

### Story 8.2: A new link for one guest

As Rikke,
I want to deactivate a link that has gone astray and create a new one,
So that only the right person can open the invitation.

**Covers:** FR-53, AD-6, UX-DR50 (protection tier 2)

**Acceptance Criteria:**

**Given** a guest on a household page
**When** Rikke confirms the protection-tier-2 dialog («<name>s gamle lenke slutter å virke. De andre i husstanden beholder sine.»)
**Then** only that guest gets a new code, the rest of the household keeps theirs, and the old code shows the private-invitation page (FR-53, AD-6)
**And** the old code is kept as deactivated and never issued again, and a test proves the old link shows the private-invitation page

### Story 8.3: The couple registers consent given by phone

As Rikke,
I want to register that Synne said yes to the consent text I sent her,
So that her allergy can be stored correctly.

**Covers:** FR-31, FR-29, UX-DR50 (protection tier 2)

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
**Then** the rows are shown as a `<table>` with a header row, while the phone layout is unchanged (FR-48)

### Story 8.6: Slow down guessing of link codes

As the couple,
I want repeated attempts with wrong links to be slowed down,
So that nobody can find a guest's invitation by trying codes.

**Covers:** NFR-4, AD-6

**Acceptance Criteria:**

**Given** 20 unknown link codes from one address within 15 minutes
**When** the limit is reached
**Then** for the next 15 minutes every request with a link code from that address is answered only after a delay of 1 second, using the shared limiter from Story 6.6, so guessing is slowed (NFR-4)
**And** a valid code still opens its invitation from a limited address, only later, so a family on shared Wi-Fi is never locked out; a test covers it

## Requirements Inventory (reference)

The requirements as the stories use them, summarised from the PRD, which wins on any difference. Each FR ends with the stories that build it.

### Functional Requirements

**5.1 Personal links and access**

- FR-1 (T1): Each guest has their own personal link with a long random code that cannot be guessed; the link is the guest's only login (no accounts or passwords). → Story 1.2
- FR-2 (T1): A link opens the guest's household and nothing else: the invitation, the household's answers, its total and its payment information. → Stories 1.2, 1.5
- FR-3 (T1): Opening a link never changes anything; only a deliberate action (pressing a button) saves data. → Stories 1.2, 1.5
- FR-4 (T1): Page titles and link previews are the same for everyone and contain no names. → Story 1.4c
- FR-5 (T1): Without a valid link (unknown, deactivated or bare address), the site shows only a friendly "private invitation, contact the couple" message with no names, phone numbers, date or place. → Stories 1.4b, 1.8
- FR-6 (T1): With a valid link, the couple's contact details are on every guest page, including error pages. → Stories 1.5, 1.8

**5.2 Invitation and information pages**

- FR-7 (T1): The front page looks like an invitation; without scrolling on a phone it shows the couple's names, date and place, the invited household's names and the RSVP deadline, with «Svar» in a sticky menu button and as a link in the deadline line. Both jump to the RSVP button, which comes after the information and the child-free note. → Story 1.5
- FR-8 (T1): Below the invitation, one entry each for Programme, Practical information and Our story (picture, one line, "Read more" to its own page), followed by the RSVP panel with child-free note, deadline and RSVP button. → Story 1.5
- FR-9 (T1 page, full text T2): The programme shows the weekend day by day (including when the cabins are ready and must be empty), marks what costs money, says what to bring and that everything is voluntary; rebus, sauna/hot tub and yoga are information only. → Stories 1.7, 7.4
- FR-10 (T1 page, full text T2): Practical information covers the ceremony in Strandebarm kirke with its time, address and directions, transport and parking, the venue and cabins, the area, dress code, house rules and what to bring. → Stories 1.6, 7.4
- FR-11 (T1): Every information page has an obvious way back to the invitation. → Stories 1.5, 1.6

**5.3 RSVP form**

- FR-12 (T1): The form shows "I am [name]", preset to the link's owner; the respondent can switch to another household member, and the choice records who answered. → Story 2.1
- FR-13 (T1): The form goes step by step, one task per step, with a visible Back link and a progress indicator. → Story 2.1
- FR-14 (T1): In step 1 the respondent marks each person "Coming" or "Not coming", with nothing preselected; step 2 asks whether everyone coming is there the whole weekend, and "No" lets the respondent choose days per person; a person's days must follow each other, so Friday and Sunday without Saturday is not possible. → Stories 2.1, 2.2
- FR-15 (T1): Later steps ask only about people who are coming and only for their days; a meal is offered only on days present, and Saturday breakfast only to those present on both Friday and Saturday. → Story 2.3
- FR-16 (T1): Per coming person, yes/no to staying overnight; the form says a cabin is booked for the whole weekend and both nights are paid. → Story 2.3
- FR-17 (T1): Each person present on Friday is asked about the Friday mountain hike: yes, no or maybe. → Story 2.5
- FR-18: Removed 2026-11-11 (expected arrival).
- FR-19 (T2): "Read more" inside a step opens in place, so the respondent never leaves the form. → Story 7.3
- FR-20 (T2): Leaving the form before sending shows a warning that the answer is not sent yet. → Story 7.3
- FR-21 (T1): A check page says at the top that the answer is not sent yet, shows every answer per person and the household total with a "Change" link per part, shows skipped optional questions as "Not provided", and has the button "Send answer". → Story 2.5
- FR-22 (T1): Errors appear next to the field with a fix hint; after a failed attempt, a summary at the top lists each error and links to its field. → Story 2.1
- FR-23 (T1): After sending, a receipt confirms with a message for coming or not coming; "You can now safely close the invitation" appears with the payment choice, or straight away when nothing is owed. → Story 2.7
- FR-24 (T1): Once answered, the invitation shows the household status: a sent line at the top with a link down, and a status block in the RSVP section's place (sent by whom and when, total, reported paid, deadline, "See or change answer"). → Story 2.8
- FR-70 (T1): Each day is shown with its date and what happens; the form stops contradicting answers (for example, overnight while present only one day, or Friday and Sunday without Saturday) and explains why. → Stories 2.2, 2.3
- FR-78 (T1): An unsent answer is kept on the guest's own device across leaving, app switches and reloads, and is offered back on return through the link. → Story 2.9

**5.4 Allergies and consent**

- FR-25 (T1): Per coming person, enter allergies or dietary needs (fixed categories gluten, lactose, nuts, shellfish, vegetarian, vegan, other, plus a short note; no diagnoses) or choose "No allergies or dietary needs"; the question is optional. → Story 2.4
- FR-26 (T1): Allergy information, including "No allergies or dietary needs", is saved only with consent through a separate Yes/No choice that starts unanswered; the consent text states the purpose, who sees it, that names and allergies go to Hardingasete's kitchen, and that consent can be withdrawn through the link. → Stories 2.4, 2.6b
- FR-27 (T1): When entering allergies for others, the respondent confirms that those people know and agree. → Story 2.4
- FR-28 (T1): The RSVP can always be sent without consent; if allergies are entered without consent, the form says before sending that they will not be saved and the guest can tell the couple directly. → Stories 2.4, 2.5, 2.6b
- FR-29 (T1, moved from T2 on 2026-11-16, see Epic 2 in the Epic List): Consent is stored per person: when, who gave it (the person, another household member or the couple) and which consent text version was shown. → Stories 2.6b, 8.3
- FR-30 (T2): Consent can be withdrawn through the personal link at any time, also after the deadline; withdrawal deletes that person's allergy information and marks the household "Changed". → Story 7.2
- FR-31 (T3): The couple registers consent for a guest only after sending the consent text and getting a yes; the site records who registered it, the channel, the text version and when. → Story 8.3

**5.5 Prices, total and payment for guests**

- FR-32 (T1): The price of each paid option (cabin for the whole weekend, Friday dinner, Saturday breakfast, Sunday breakfast) is shown before choosing, with a short note on why guests pay. → Story 2.3
- FR-33 (T1): The household total is visible along the way, identical on check page and receipt, and always calculated from answers and current prices. → Story 2.3
- FR-34 (T1): After sending, a household that owes something chooses "Pay now" (amount, Vipps number, account number, payment message) or "Pay later" (the link always shows what is owed). → Stories 2.7, 2.8
- FR-35 (T2): The guest can report "I have paid" with amount (prefilled), method (Vipps or bank) and who paid if someone else; afterwards they see what and when they reported and can correct it. → Story 5.1
- FR-36 (T2): If the total changes after a payment report, the guest sees what remains to pay, or that the couple has been told and will refund the difference. → Story 5.4
- FR-71 (T1): Each household has its own payment message, "Bryllup" + the household's names; the couple can adjust it, and the site warns if two households would get the same message. → Stories 2.7, 5.5

**5.6 Changing an answer, deadline and lock**

- FR-37 (T2): Before the deadline, once answered, the RSVP button becomes "See or change answer" and opens the form prefilled. → Story 4.1
- FR-38 (T2): The form shows who last updated the answer and when; if someone else in the household sends after the respondent opened the form, the site shows that answer (who, when, what differs) before the respondent can send; no silent overwrite. → Stories 4.1, 4.2
- FR-39 (T2): A household is marked "Changed" when a guest or the couple changes a sent answer, or consent is withdrawn; the first answer and payment reports don't count. → Stories 4.1, 4.4
- FR-40 [2027]: Full change history per household; for allergies only that they changed, never the content. → not in v1
- FR-41 (T1): The RSVP deadline is a date; guests can answer until 23:59 Norwegian time that day; shown with weekday, date and time next to the RSVP button and in the status; all times are Norwegian time. → Stories 1.5, 2.1, 2.6a, 4.1
- FR-42 (T2): After the deadline guests can't change attendance, days, meals, overnight, hike or allergies; the button says "See answer" with deadline text and contacts; payment info, "I have paid", info pages and consent withdrawal still work; never-answered households see the same message. → Story 4.3

**5.7 Questions to the couple**

- FR-43, FR-44, FR-45: Removed 2026-11-15 ("Ask us" form).

**5.8 Admin access and roles**

- FR-46 (T1 couple login, T2 helper role): Admin users log in with username and password; the couple has full access, helpers see everything and change nothing. → Stories 3.1, 6.1
- FR-47 (T1): Rikke creates admin accounts for the couple and helpers with a command; no self-registration. → Stories 1.3, 3.1
- FR-48 (T1 basic responsive, beyond that T3): Quick tasks work well on a phone (find a guest, copy their link, see whether they answered); the full overview also works on a phone. → Stories 3.2, 3.4, 6.3, 8.5

**5.9 Guest list and links**

- FR-49 (T2): The couple adds, edits and removes households and guests one by one; each guest has a name and optional phone and email. → Stories 6.4, 6.5
- FR-50 (T3): The couple can move a guest to another household. → Story 8.1
- FR-51 (T2): The couple can search for a guest by name, copy the guest's link and see contact details. → Story 6.3
- FR-52 [2027]: Copy a warm, ready-to-send invitation message with the guest's name and link. → not in v1
- FR-53 (T3): The couple can deactivate a guest's link and create a new one; only that guest's link changes. → Story 8.2
- FR-76 [2027]: Record that the invitation was sent (date, channel) and each resend with a reason. → not in v1

**5.10 Overview and "Needs attention"**

- FR-54 (T1): Below "Needs attention", the admin home shows "answered X of Y households" with a link to the full overview, then a summary in small groups: coming / not coming / not answered (people and households); whole weekend or not, by day combination; who does not stay overnight and the number of beds; count per meal and per allergy category; coming guests without an allergy answer; households per payment status; hike interest with "maybe" separate. → Story 3.2
- FR-55 (T1): Every count opens a list of the people behind it. → Story 3.3
- FR-56 (T2): At the very top of the admin home, without scrolling, "Needs attention" lists households not answered, coming guests with nothing registered for allergies, "I have paid" reports without a matching payment (in red), refunds owed and households marked "Changed"; each item can be marked handled or seen and leaves the list; an empty list says so. → Story 6.2
- FR-57 (T1 simple, T2 full): A full overview lists every household with who comes, the total and payment status, unanswered first; each household has its own page with every person's answers, contact details and notes; phone and email are tappable on a phone. → Stories 3.4, 6.3
- FR-58 (T1): An allergy list shows names and categories for everyone who consented, ready for Hardingasete. → Story 3.4
- FR-77 [2027]: Record when a household started; "Needs attention" also lists invitations not marked sent and households that haven't started weeks after sending. → not in v1

**5.11 Payments**

- FR-59 (T2): The couple registers amounts received and refunds paid back per household; a registration can be corrected or undone. → Story 5.2
- FR-60 (T2): Payment status is computed from received minus refunds versus total: nothing to pay, not paid, part paid (X missing), paid, refund owed (X); a household that has not answered has no status and shows «Ikke svart»; only admins see it. → Story 5.3
- FR-61 (T2): An "I have paid" report matches when received minus refunds is at least the reported amount; a mismatch is marked red in the overview and listed under "Needs attention". → Story 5.3
- FR-62 [2027]: One dated contact note per household, shown in the not-answered list and the payment overview. → not in v1

**5.12 Overrides and settings**

- FR-63 (T2): The couple can fill in or change any household's answer, also after the deadline, with the same form as the guests, recorded with the admin as author. → Story 4.4
- FR-64 (T2): The couple can change prices, deadline, contact details and payment details in admin (helpers cannot); a deadline change is repeated in words and confirmed, and a past or near deadline shows how many households would be locked out. → Story 4.5
- FR-65 (T3): Changing prices after households have answered warns with the number of households whose total will change. → Story 8.4

**5.13 Privacy functions**

- FR-66 (T2): A privacy page explains what is collected and why, who is responsible, the legal basis per kind of data, who can see it, when it is deleted, the guest's rights (including withdrawal and complaint to Datatilsynet) and how to contact the couple; linked from every page footer and from the consent question. → Story 7.1
- FR-67 [2027]: The couple can delete all guest data in one operation after clear confirmation. → not in v1

**5.14 Local setup and test data**

- FR-68 (T1): One documented command, separate from starting the app, fills the database with fictional test data: the people from UJ-1 to UJ-3 and households covering the expected-results list (declines entirely; Saturday only without cabin; paid; part paid; refund owed; report without matching payment; not answered; allergy with consent; allergy without consent; withdrawn consent), fictional contacts and a test link per guest, fictional prices, deadline and contacts and obviously invalid payment details, a test couple admin and a test helper. → Stories 1.3, 2.6d, 5.2
- FR-69 (T1): An expected-results list is worked out by hand for the test data before the code it checks, committed to the repo, covering counts, totals, payment statuses and the deadline lock, and checked by automated tests. → Stories 1.3, 3.5
- FR-72 (T1): Test data never reaches the real site; the seed command refuses to run in production, and test accounts and links exist only in test data. → Story 1.3

**5.15 Rules for counts and totals**

- FR-73 (T1): Guests choose the paid meals (Friday dinner, Saturday breakfast, Sunday breakfast); everyone present on Saturday counts for Saturday lunch and dinner, which are not asked about; meals don't depend on staying overnight. → Stories 2.3, 3.2
- FR-74 (T1): Each person is coming, not coming or not answered; a household is answered once an answer is sent and coming when at least one person comes. → Stories 2.6a, 3.2
- FR-75 (T1): When a person becomes not coming or a day is removed, the choices for that person or day are removed too and never count. → Story 2.2

### Non-functional Requirements

- NFR-1 Reliability: links work from sending until deletion and the link format never changes after invitations; links are short and safe in SMS, Messenger and email; saving either succeeds and says so, or fails with a clear message and keeps what the guest entered; production availability and the PRD 3.2 operations rules apply in 2027.
- NFR-2 Correct numbers: all counts, totals and payment statuses are calculated from stored answers and payments, never stored; amounts are whole kroner; automated tests check admin counts and totals against the expected-results list.
- NFR-3 Privacy: GDPR applies and allergies are health data; Rikke and Valdemar are joint controllers; the legal basis table in the PRD applies; only necessary data; only fictional data in the repo, tests, screenshots, usability test and AI tools; real data only in EU/EEA production, deleted by 31 August 2028.
- NFR-4 Security: link codes ≥ 128 bits of randomness with no personal data; guest pages hidden from search engines and never leak the link; repeated wrong-link attempts slowed (T3); modern password hashing; admin sessions expire after inactivity; CSRF protection; repeated login attempts slowed; only logged-in admins see guest answers beyond a household's own; the server stops helpers from changing data; no secrets in the repo.
- NFR-5 Accessibility (WCAG 2.2 AA): text contrast ≥ 4.5:1; guest body text ≥ 18 px; works at 200% zoom and 320 px width; full keyboard use with visible focus; guest touch targets ≥ 44 × 44 px; every field labelled, errors per FR-22; don't ask for what the link knows; animation respects reduce motion and can be skipped.
- NFR-6 Ease of use: phone first for all ages (PC shows the phone layout); one obvious next step per screen; plain, warm Norwegian bokmål, also in errors; an older guest completes a household RSVP correctly and alone in under 10 minutes.
- NFR-7 Performance and size: pages load in under 3 seconds on an ordinary phone on 4G; sized for about 70 guests and 5 admin users.
- NFR-8 Runnability: runs locally on Windows, macOS or Linux by following the README, with no separate database server and none of Rikke's accounts or keys; install, start and tests take no more than 15–20 minutes.
- NFR-9 Maintainability: linter and formatter; all tests run with one command; settings that differ between local and production documented in `.env.example`; stories refer to PRD requirement IDs.

### Architecture Decisions

One line per decision. The full rules and their reasons are in [ARCHITECTURE-SPINE.md](architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md); the stories repeat the values they depend on. There is **no third-party starter template**: Story 1.1 sets up the project from `django-admin startproject` with uv, following the spine's Structural Seed.

- **Project setup (Story 1.1):** Python 3.14 pinned in `.python-version`, `requires-python = ">=3.14,<3.15"`, uv for dependencies (`pyproject.toml`, `uv.lock`), Django 6.1.x, pytest + pytest-django, Ruff (lint + format), djLint (templates), WhiteNoise; layout `config/`, `wedding/` (models, rules/, services/, rsvp/, selectors.py, links.py, management/commands/, fixtures/), `guests/`, `dashboard/`, `static/` (css, js, fonts, img), `tests/`.
- **CI:** a GitHub Actions workflow runs `uv run pytest`, Ruff and djLint on every push and pull request.
- **AD-1:** one server-rendered Django monolith; everything works without JavaScript.
- **AD-2:** all rules are pure functions in `wedding/rules/`, with plain values and explicit `now`.
- **AD-3:** only `wedding/services/` writes, one transaction per service, with an explicit actor.
- **AD-4:** facts are stored, derived values never; payments are voided, never deleted.
- **AD-5:** SQLite everywhere, through the ORM only, with WAL and IMMEDIATE transactions.
- **AD-6:** a 22-character random link code per guest, resolved in one place; GET never writes.
- **AD-7:** one RSVP form in `wedding/rsvp/`, mounted for guests and for the couple's override.
- **AD-8:** the unsent answer lives only in a signed draft cookie scoped to `/<code>/`.
- **AD-9:** `Household.revision` stops one send from silently overwriting another.
- **AD-10:** a custom `User` with role `couple` or `helper`; only the couple writes.
- **AD-11:** times in Oslo time; one deadline function decides the lock.
- **AD-12:** money is whole kroner; guest pages use only `guest_balance`.
- **AD-13:** admin sessions last 20 hours and are renewed by every request.
- **AD-14:** settings from environment variables with safe local defaults; seed runs only locally.
- **AD-15:** guest pages are hidden from search engines and never leak the link.
- **AD-16:** seed data and hand-worked expected results are TOML files, checked by tests.
- **AD-17:** information-page text lives in templates in v1.
- **AD-18:** allergy data is stored only with consent, recorded per person and per event.
- **AD-19:** one helper sets the "Changed" marker; attention items are computed by rules.
- **AD-20:** confirmations are a preview POST; every write is protected against repeats.
- **Conventions:** code and identifiers in English, everything user-facing in Norwegian bokmål (`LANGUAGE_CODE = "nb"`), Norwegian URL paths; naming (singular models, verb services, rule functions named for what they return); every rule function, service and test names its FR or NFR in the docstring; services raise their own exceptions, shown per FR-22; one CSS file with DESIGN.md tokens as custom properties, small vanilla JavaScript, self-hosted fonts, no build step.
- **Throttling:** one shared limiter on Django's database cache for failed logins (T2, Story 6.6) and unknown link codes (T3, Story 8.6).
- **Manual test plan:** one real-browser form POST is in the manual test plan, because Django's test client sends no browser headers.

### UX Design Requirements

One line per requirement. The full specification is in [DESIGN.md](ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md) (how it looks) and [EXPERIENCE.md](ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md) (how it behaves); the stories repeat the details they depend on.

**Foundation and tokens**

- UX-DR1: colour tokens, spacing scale and radii as CSS custom properties; light only.
- UX-DR2: self-hosted Imperial Script and EB Garamond; type in `rem`, guest body text 20px.
- UX-DR3: the paper sheet surface on textured page green, with fallbacks.
- UX-DR4: image assets prepared from Rikke's files in `static/img/`.
- UX-DR5: one centred column, at most 480px; no horizontal scroll at 320px or 200% zoom.

**Guest components**

- UX-DR6: nav bar with the «Svar» button.
- UX-DR7: hero sheet in a fixed order, above the fold on a phone.
- UX-DR8: lead-in line and «Alt om helgen» with three topic rows.
- UX-DR9: RSVP sheet with the full deadline and the draft notice.
- UX-DR10: status block once answered, and the locked states.
- UX-DR11: footer band with the couple's phone numbers and «Personvern».
- UX-DR12: information-page frame with back link and jump links.
- UX-DR13: programme timeline, one list per day.
- UX-DR14: story sheet for «Vår historie».
- UX-DR15: buttons, focus ring and the «Sender …» busy state.
- UX-DR16: text fields and choice controls with labels, hints and errors.
- UX-DR17: notice component in four variants.
- UX-DR18: error summary after a failed step.
- UX-DR19: form step layout: progress line, respondent line, one fieldset per person; no nav bar.
- UX-DR20: form step order, each step with its own address.
- UX-DR21: allergy step with consent per person.
- UX-DR22: «Les mer» disclosure inside a step.
- UX-DR23: check page.
- UX-DR24: receipt.
- UX-DR25: payment details sheet «Slik betaler du».
- UX-DR26: draft notice and draft offer.
- UX-DR27: leave warning.
- UX-DR28: last-updated notice and conflict warning.
- UX-DR29: dialog component, with a confirm page without JavaScript.
- UX-DR30: G1, the page without a valid link.
- UX-DR31: G12, the privacy page.
- UX-DR32: consent withdrawal dialog.
- UX-DR33: G9, the locked answer view.

**Admin components**

- UX-DR34: admin frame and Admin nav.
- UX-DR35: helpers' read-only mode.
- UX-DR36: A1, login.
- UX-DR37: A2, the attention panel «Trenger oppfølging».
- UX-DR38: undo in place for handled items.
- UX-DR39: A2, answer progress «Svart: X av Y husstander».
- UX-DR40: A2, summary panels in a fixed order.
- UX-DR41: A3, the people behind a count.
- UX-DR42: A4, Gjester: search, household rows and empty state.
- UX-DR43: A6, the household page.
- UX-DR44: A6a, add or edit a household.
- UX-DR45: A9, payments list and household payment page.
- UX-DR46: A10, editing the payment message.
- UX-DR47: A12, settings.
- UX-DR48: A5, the allergy list.
- UX-DR49: status tags, never colour alone.
- UX-DR50: admin protection tiers 1–3.

**Cross-cutting**

- UX-DR51: voice and tone; du for one person, dere for two or more.
- UX-DR52: saving, saved and save-failed states.
- UX-DR53: accessibility floor checks.
- UX-DR54: interaction limits; reduced motion respected.

## Change log

| Date | Change |
|---|---|
| 2026-11-16 | First version, made with `bmad-create-epics-and-stories`: 8 epics and 48 stories. |
| 2026-11-16 | After the review in [reviews/review-epics-2026-11-16.md](reviews/review-epics-2026-11-16.md) (adversarial, edge-case, structure and prose lenses). **Rikke decided:** a person's days must follow each other, so Friday and Sunday without Saturday is not possible (also in PRD FR-14, FR-15 and FR-70). **Claude decided, as technical fixes Rikke asked for:** the draft cookie is scoped to `/<code>/` (it could not reach the front page), and the revision moved to `Household` (both also in the architecture); deadline enforcement moved into T1 (Story 2.1 and 2.6a), since FR-41 is T1; consent is per person with the FR-27 confirmation enforced; numbers for the note length, household size, the attention list and throttling; link-code throttling slows instead of blocking, so a family on shared Wi-Fi is never locked out. Story 1.4 is split into 1.4a–1.4c and Story 2.6 into 2.6a–2.6d, so each can be reviewed on its own. Structure: the Epic List comes first, the requirement inventories are shortened to one line each and moved to the end with links to their sources, each FR lists the stories that build it (replacing the FR coverage map), and deferred work in the ACs moved to **Not in this story:** lines. |
| 2026-11-16 | Story 1.1: the djLint command is `uv run djlint --check .` (with a path). djLint 1.50 needs a path: `djlint --check` alone exits with code 2 and checks nothing, so the AC could never pass as written. Found while writing the Story 1.1 spec; `pyproject.toml` sets `allow_empty_input = true` until Story 1.4a adds the first template, and excludes `.docs/`, whose HTML mockups are not app templates. |
| 2026-11-16 | **Rikke confirmed** the household limit of 8 people (Claude's technical choice from the epics review): no household on the guest list is larger. Confirmed before Story 1.2, which builds households. |
| 2026-11-16 | **Claude decided** (technical; in the Story 1.2 spec Rikke approved): FR-3 is tested at the resolver in Story 1.2, because no guest view exists until Story 1.5. Story 1.5 gets an AC that repeats the test over an HTTP GET, and FR-3 now lists both stories. Found while writing the Story 1.2 spec. |
| 2026-11-16 | **Rikke decided** while checking `expected.toml` in Story 1.3: a household that has not answered has no payment status and shows «Ikke svart», not «Ingenting å betale» (PRD FR-60, commit 9360654). Story 3.5 and Story 5.3 and the FR-60 line now say so, and `payment_status` is told whether the household has answered. |
| 2026-11-16 | **Claude decided** (technical, from the Story 1.3 review): Story 3.1's `create_admin` makes real accounts with `is_test_data=False` through its own path and never uses the system actor. Story 1.3's `create_admin_user` is system-only and marks every account as test data, so reusing it would let the next `seed_testdata` delete Rikke's real accounts. Also in AD-16. |
| 2026-11-21 | **Rikke confirmed** the numbers Claude chose in the 2026-11-16 review: «Trenger oppfølging» shows the first 2 items before «Vis alle n» (Story 3.2; still re-measured in the manual test plan), and login throttling after 5 failed logins for one username or 20 from one address within 15 minutes (Story 6.6), with link-code throttling that slows and never blocks (Story 8.6). No change to the stories. |
| 2026-11-23 | **Rikke approved** reconciling the plan with Epic 1 (retrospective action 2, R1): the Story 1.5 AC now says the nav bar is sticky only when the viewport is at least 400px tall **and at least 20em wide**, as built and as in DESIGN.md. PRD FR-6, FR-7, FR-10 and FR-60 were reconciled the same day. |
