# Epic 1 Context: The guest opens their link and sees the invitation

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Lay the foundation of the wedding website and deliver the read-only guest experience. A guest (for example bestefar Sigmund, 78, on his phone) opens a personal link and sees a real invitation: the couple's names, date, place, his household, the deadline, the three topic pages (Programme, Practical information, Our story) and where to answer. A wrong link shows only a calm "private invitation" page that reveals nothing. The examiner must be able to install the app, run all tests and checks, seed fictional households and open their test links by following the README alone. This epic is part of the T1 usability-test build (27 November 2026) and sets up the structure, settings, data model, actors and test oracle that every later epic builds on.

## Stories

- Story 1.1: Runnable project with one command for tests and checks
- Story 1.2: Households, guests and personal links
- Story 1.3: Fictional test data and the hand-made expected-results list
- Story 1.4a: The invitation's colours, type, buttons and notices
- Story 1.4b: Paper, Rikke's images and the private-invitation page
- Story 1.4c: Guest pages stay private: headers, link previews and logs
- Story 1.5: The invitation front page
- Story 1.6: Practical information and Our story pages
- Story 1.7: The programme page
- Story 1.8: Error pages that still show how to reach the couple

## Requirements & Constraints

- **Personal links:** each guest has one unguessable link that is their only login; it opens their own household and nothing else.
- **Opening a link never writes** (chat apps and mail scanners open links automatically): no row is created or changed by any GET. This is proved twice: at the resolver (Story 1.2, before any guest view exists) and again over HTTP GET with Django's test client for `/<code>/` and every topic page (Story 1.5).
- **No valid link** (unknown code or bare `/`): only «Dette er en privat invitasjon» and «Virker ikke lenken din? Ta kontakt med brudeparet direkte.» No names, phone numbers, date, place, seal, nav bar or footer. Must render on an empty, migrated database.
- **Valid link:** the couple's phone numbers appear on every guest page, error pages included.
- **Privacy:** titles and link previews are the same for every guest and contain no names; guest pages stay out of search engines and logs.
- **Front page:** without scrolling on a phone it shows names, date, place, the household and the short deadline; «Svar» is reachable from the sticky nav and the deadline line. Info pages always have an obvious way back.
- **Accessibility (WCAG 2.2 AA):** text contrast ≥ 4.5:1, guest body text 20px (floor 18px), works at 320px width and 200% zoom (about 180 CSS px) with no horizontal scroll, full keyboard use with visible focus, touch targets ≥ 44 × 44px, reduced motion respected, forced-colours mode works.
- **Performance:** front page usable in under 3 seconds on throttled 4G on a phone.
- **Runnability:** runs on Windows, macOS or Linux by following the README, with SQLite, no `.env` and none of Rikke's accounts or keys; all tests run with one command.
- **Household size:** at most 8 people (confirmed by Rikke). This keeps a full RSVP draft inside the 4 KB cookie; no seed household may exceed it.
- **Test data:** only fictional people besides Rikke and Valdemar (`example.com` emails, impossible phone numbers, an account number with an invalid check digit). The seed command refuses unless `APP_ENV` is `local` (the default). The expected-results list is worked out by hand and committed in its own commit, with the method in the message, before any code that computes those numbers.
- **Payment status in the expected results:** a household that has not answered has no payment status and is listed as «Ikke svart», not «Ingenting å betale» (Rikke's decision while checking the list).
- **Traceability:** every rule function, service and test names the FR/NFR it implements in its docstring.

## Technical Decisions

- **Stack:** Python 3.14 (`.python-version`, `requires-python >=3.14,<3.15`), uv with `uv.lock`, Django 6.1.x, SQLite, pytest + pytest-django, Ruff (lint + format), djLint, WhiteNoise. Started from `django-admin startproject`, no third-party starter. Checks: `uv run pytest`, `uv run ruff check`, `uv run ruff format --check`, `uv run djlint --check .` (djLint needs the path; without it, it checks nothing and exits 2), run locally and by GitHub Actions on every push and PR.
- **Layout:** `config/` (settings, urls, middleware, logging filter), `wedding/` (`models.py` incl. custom User, `rules/`, `services/`, `rsvp/`, `selectors.py`, `actors.py`, `links.py`, `management/commands/`, `fixtures/`), `guests/`, `dashboard/`, `static/` (css, js, fonts, img), `tests/`. `guests` and `dashboard` never import each other.
- **Functional core:** `wedding/rules/` is pure Python with no Django or project imports, enforced by a test. Rules take plain values (and an explicit `now`).
- **Only services write:** functions in `wedding/services/` are the only code that calls `.save()`/`.delete()`; each is one transaction and takes an explicit actor, never the request. A guest service refuses any id outside the actor's household, with a test for the cross-household case.
- **Actors:** the guest actor (guest + household), admin actor (user + role) and system actor (seed command only) live in `wedding/actors.py`. `links.py` makes guest actors; views and the seed command make the others; services import the types from there rather than from `links.py` or `services/`.
- **Facts stored, derived values never:** no stored totals, counts or statuses. Money is whole kroner as `int`. The `is_test_data` marker on households and users is a stored fact.
- **User model:** `wedding.User(AbstractUser)` with `role` (`couple` | `helper`) is `AUTH_USER_MODEL` from the first migration. Guests are not Django users; guest views never read `request.user` or `request.session` and never use the messages framework.
- **Models in this epic:** `User` (1.1); `Household` (with `revision`, starting at 0), `Guest` (name, optional phone/email, link code) and a single-row `Settings` (contact names and phones, whole-kroner prices, deadline as a date, Vipps and account number) (1.2); `is_test_data` on `Household` and `User` (1.3). A data migration creates the `Settings` row with safe placeholders; guest views read it with `.get()` and never create it. Each later table comes with the story that needs it.
- **Link codes:** `secrets.token_urlsafe(16)` (22 URL-safe characters), stored plain, unique and indexed, no personal data. Only the seed command may set fixed codes in the same format. One resolver in `wedding/links.py` turns a code into a guest actor (unknown or wrong-length code → nothing); every guest view uses it. All guest pages live under `/<code>/`, and that format never changes.
- **Settings:** environment variables with safe local defaults, all listed in `.env.example`. `USE_TZ = True`, `TIME_ZONE = "Europe/Oslo"`, `LANGUAGE_CODE = "nb"`. SQLite: busy `timeout`, WAL via `init_command`, `transaction_mode: IMMEDIATE`, no `ATOMIC_REQUESTS`; ORM only, no raw SQL. With `APP_ENV=production` the app refuses to start if `DEBUG` is on, `SECRET_KEY` is the default or `ALLOWED_HOSTS` is empty.
- **Guest privacy:** `noindex` as meta tag and `X-Robots-Tag` middleware, `Referrer-Policy: same-origin` (never `no-referrer`, which breaks CSRF), `rel="noreferrer"` on external links, identical Open Graph tags for every code, self-hosted assets only, and a logging filter that masks codes in request paths.
- **Error pages** (404, 500, CSRF) under `/<code>/` show the couple's numbers when the code resolves and nothing personal otherwise; a failed lookup (for example a database error) falls back to the impersonal version.
- **Test oracle:** `wedding/fixtures/seed.toml` and `expected.toml`, read with `tomllib`. `seed_testdata` builds everything through services with the system actor, sets the deadline relative to today, prints a test link per guest, and creates a test couple and a test helper. Lock cases are offsets from the seeded deadline, never fixed dates. Changing the oracle is a deliberate commit with a reason.
- **Test-data marker and reset:** every household and admin user the system actor creates gets `is_test_data=True` (guests belong to their household). Before seeding, a reset service with the system actor deletes the marked households with everything in them (including guests added to them later) and the marked users, so the command is repeatable and never deletes anything it did not make; payments must be voided before a household is deleted. If a seed link code or username is already used by an unmarked row, the command stops before writing anything. `create_admin_user` is for the seed command only and always marks its accounts as test data; real admin accounts are made with `is_test_data=False` through their own path, never with the system actor.
- **Info-page text** lives in templates in v1, never in the database.
- **Server-rendered only:** every page is a Django template and works without JavaScript; no build step. User-facing text and URL paths are Norwegian bokmål; code is English. Browser checks that are not automated (viewport fit, reflow, forced colours, 4G timing) go in `docs/manual-test-plan.md`.

## UX & Interaction Patterns

- **Look:** a printed invitation: cream paper sheets (`panel-cream`, `ink` text) on a textured olive `page-green`. The sheet's texture, soft `edge-b3` edge and shadow sit on a `::before` layer behind the content, with a flat 5px-corner fallback and a 1px `CanvasText` border under forced colours. Light only (`color-scheme: light only`). Tokens, spacing and radii come from DESIGN.md as CSS custom properties in one stylesheet.
- **Type:** Imperial Script only for «Rikke & Valdemar» (hero `h1`, 48px, and the 40px signature on Vår historie); names stack instead of shrinking. Everything else is EB Garamond (regular, italic, 600), self-hosted WOFF2 with æ/ø/å, in `rem`, with lining figures. Small capitals only for the hero date and place and the info-page jump links. Cream text on the textured green must be ≥ 19px; the 18px nav words stand only on the flat nav bar.
- **Layout:** one centred column, at most 480px; gutters narrow below 340px and 260px. Check every build at 360 × 560, 320 × 568 and 180 × 320. The hero must fit above the fold.
- **Front page order:** sticky flat nav bar (Program · Praktisk · Vår historie + «Svar» button; never a hamburger; sticky only when the viewport is ≥ 400px tall) → hero sheet (seal over the top edge, whole illustration, names, invites line, gypsophila, date and place, «for <household>», «**Svar** innen <date>») → lead-in → «Alt om helgen» (lily garlands, three lace-framed topic rows with «Les mer» and an accessible name) → RSVP sheet (`#svar`, full deadline with weekday and «kl. 23:59») → footer band with `tel:` links ≥ 44px tall. «deg» for one invited person, «dere» for two or more.
- **Info pages:** «← Tilbake til invitasjonen» at the top, italic title with hairline, jump links in a `nav` labelled «Hopp til», one paper sheet per part, a back button at the bottom, the current nav word marked with `aria-current`. `scroll-padding-top` keeps jump targets and focus out from under the sticky bar. Programme events are an `ol` with `<time>`, alternating sides by CSS only and one-sided below about 260px.
- **Components:** 3px focus ring at 3px offset, coloured for its surface (never `outline: none`). The notice has four variants (icon + 4px rule + «Feil:»/«Obs:» prefix), never colour alone; guest notices never vanish by themselves. Smooth scrolling only under `prefers-reduced-motion: no-preference`. Decorative images get `alt=""`.
- **Assets:** Rikke's cut-out images (seal, gypsophila, lily garlands, lace frame, hero illustration 04, venue and couple photos, twelve programme icons) are in the UX design's `mockups/` folder; her originals are in `ux/egne-bilder/`. Use her images and never draw flowers, lace or icons in code. Approved renders: `front-page-3.html`, `info-praktisk.html`, `info-program.html`, `info-om-oss.html`, `privacy-1.html`. DESIGN.md and EXPERIENCE.md win over any render.

## Cross-Story Dependencies

- 1.1 comes first: structure, settings, custom User and CI. 1.2 depends on it, and 1.3 needs the services, actors and resolver from 1.2.
- 1.4a (tokens and components) and 1.4b (sheet, images, private page) come before the guest pages 1.5–1.8. 1.4c's privacy headers apply to every guest response, including the error pages in 1.8.
- 1.5 adds the first guest view, so it carries the HTTP-level FR-3 test that 1.2 could only do at the resolver. It also builds the info-page frame that 1.6 and 1.7 fill.
- The 8-person household cap is enforced when the couple saves a household (Story 6.4) and is what the 4 KB draft test uses (Story 2.4); Epic 1's models and seed must stay consistent with it.
- The test-data marker from 1.3 constrains Story 3.1: its `create_admin` command must not reuse `create_admin_user`, and a test there shows `seed_testdata` leaves real accounts alone. Story 5.2 repeats the reset test with payments seeded.
- The «Ikke svart» payment state in `expected.toml` is what `payment_status(answered, total, received, refunded)` in Stories 3.2 and 5.3 must reproduce.
- Later epics extend this one: the RSVP button and form (Story 2.1); answers, allergies, consents, payments and withdrawn consent added to the seed (2.6d, 5.2, 7.2); expected-results assertions (Epic 3); the «Personvern» link under the private page and the full info texts (Epic 7).
