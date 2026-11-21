# Epic 1 Context: The guest opens their link and sees the invitation

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Lay the foundation of the wedding website and deliver the read-only guest experience. A guest (for example bestefar Sigmund, 78, on his phone) opens a personal link and sees a real invitation: the couple's names, date, place, his household, the deadline, the three topic pages (Programme, Practical information, Our story) and where to answer. A wrong link shows only a calm "private invitation" page that reveals nothing. The examiner must be able to install the app, run every test and check, seed fictional households and open their test links by following the README alone. The epic is part of the T1 usability-test build and sets up the structure, settings, data model, actors and test oracle that every later epic builds on.

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

- **Personal links:** one unguessable link per guest is their only login and opens only their own household.
- **Opening a link never writes** (chat apps and mail scanners open links): no GET creates or changes a row. Proved at the resolver, and again over HTTP for `/<code>/` and every topic page once the first guest view exists.
- **No valid link** (unknown code or bare `/`): only «Dette er en privat invitasjon» and «Virker ikke lenken din? Ta kontakt med brudeparet direkte.»; no names, phone numbers, date, place, seal, nav bar or footer. Must render on an empty, migrated database.
- **Valid link:** the couple's phone numbers appear on every guest page, error pages included; a failed lookup falls back to the impersonal page.
- **Privacy:** page titles and link previews are identical for every guest and name nobody; guest pages stay out of search engines and logs.
- **Accessibility (WCAG 2.2 AA):** contrast ≥ 4.5:1, guest body text 20px, no horizontal scroll at 320px and at 200% zoom (about 180 CSS px), full keyboard use with visible focus, touch targets ≥ 44 × 44px, reduced motion and forced colours respected.
- **Performance:** front page usable in under 3 seconds on throttled 4G on a phone.
- **Runnability:** SQLite, no `.env`, none of Rikke's accounts; all tests run with one command.
- **Test data:** fictional people only besides Rikke and Valdemar; households of at most 8 people. The seed command refuses unless `APP_ENV` is `local` (the default). The expected-results list is hand-worked and committed on its own, with the method in the message, before code that computes it. A household that has not answered has no payment status and shows as «Ikke svart».
- **Traceability:** every rule, service and test names the FR/NFR it implements in its docstring.

## Technical Decisions

- **Stack:** Python 3.14, uv with `uv.lock`, Django 6.1.x, SQLite, pytest + pytest-django, Ruff (lint + format), djLint (`djlint --check .`, the path is required), WhiteNoise. Checks run locally and in GitHub Actions on every push and PR.
- **Layout:** `config/`, `wedding/` (models incl. custom User, `rules/`, `services/`, `rsvp/`, `selectors.py`, `actors.py`, `links.py`, `management/commands/`, `fixtures/`, `templates/wedding/`), `guests/`, `dashboard/`, `static/`, `tests/`. `guests` and `dashboard` never import each other, so `base.html` and shared includes (the notice) live in `wedding/templates/wedding/`, and every guest page, admin page and the RSVP form extends that base.
- **Functional core:** `wedding/rules/` is pure Python, no Django or project imports (enforced by a test), with `now` passed explicitly.
- **Only services write:** `wedding/services/` alone calls `.save()`/`.delete()`, one transaction per call, with an explicit actor (guest, admin or system, all defined in `wedding/actors.py`); a guest service refuses ids outside the actor's household.
- **Data:** facts stored, derived values never; money is whole kroner as `int`. Models here: `User(AbstractUser)` with `role` (`couple`/`helper`) as `AUTH_USER_MODEL` from the first migration; `Household` (`revision` from 0), `Guest`, single-row `Settings` (contacts, prices, deadline date, Vipps and account number) created by a data migration and only read with `.get()` by guest views; `is_test_data` on `Household` and `User`. Guests are not Django users; guest views never touch `request.user`, the session or the messages framework.
- **Link codes:** `secrets.token_urlsafe(16)` (22 characters), unique, indexed, no personal data. One resolver in `wedding/links.py`; all guest pages live under `/<code>/`: the front page, `program/`, `praktisk/` and `historie/`; `svar/` (RSVP form) and `personvern/` follow. `<str:code>/` matches any single segment, so reserved routes (`robots.txt`, later `admin/`) go above the guest include.
- **Settings:** env vars with safe local defaults, listed in `.env.example`; `USE_TZ`, `Europe/Oslo`, `nb`; SQLite busy timeout, WAL, `IMMEDIATE` transactions, no `ATOMIC_REQUESTS`. With `APP_ENV=production` the app refuses to start on `DEBUG`, the default `SECRET_KEY` or empty `ALLOWED_HOSTS`.
- **Guest privacy:** `noindex` meta tag and `X-Robots-Tag` middleware on every response, `Referrer-Policy: same-origin` (never `no-referrer`, which breaks CSRF), `rel="noreferrer"` on external links, identical Open Graph tags in `base.html` outside every block (`og:image` absolute from the request's own host, left out when a page renders without a request), `/robots.txt` that blocks nothing, self-hosted assets only, a logging filter that masks the first path segment.
- **Error pages:** 404, 500 and CSRF-failure pages under `/<code>/` show the couple's contact numbers when the code resolves and nothing personal otherwise; a failed lookup falls back to the impersonal page.
- **Test oracle:** `wedding/fixtures/seed.toml` and `expected.toml` via `tomllib`. `seed_testdata` builds through services with the system actor, sets the deadline relative to today and prints a test link per guest. Everything it creates is marked `is_test_data`; a reset service deletes only marked households (with everything in them) and users, and the command stops before writing if a seed code or username is taken by unmarked data. Real admin accounts never go through the system actor.
- **Info-page text lives in templates in v1**, never in the database. Every page is server-rendered and works without JavaScript; UI text and URL paths are Norwegian, code is English. Browser checks that are not automated go in `docs/manual-test-plan.md`.

## UX & Interaction Patterns

- **Look:** a printed invitation: cream paper sheets on a textured olive `page-green`; texture, `edge-b3` edge and shadow on a `::before` layer, flat 5px-corner fallback, 1px `CanvasText` border under forced colours. Light only. All DESIGN.md tokens, spacing and radii as custom properties in one stylesheet.
- **Type:** Imperial Script only for «Rikke & Valdemar» (names stack, never shrink); everything else EB Garamond, self-hosted WOFF2, `rem`, lining figures.
- **Layout:** one centred column, max 480px; check every build at 360 × 560, 320 × 568 and 180 × 320. The hero fits above the fold.
- **Front page:** sticky flat nav (Program · Praktisk · Vår historie + «Svar»; never a menu button; sticky only when the viewport is ≥ 400px tall and ≥ 20em wide) → hero sheet → lead-in → «Alt om helgen» (three lace-framed topic rows, «Les mer» with an accessible name) → RSVP sheet (`#svar`, full deadline with «kl. 23:59») → footer band with `tel:` links. «deg» for one invited person, «dere» for more.
- **Info pages:** back link at the top and back button at the bottom, italic title with hairline, «Hopp til» jump links, one paper sheet per part, `aria-current` on the nav word, `scroll-padding-top` on `html` alone (no `scroll-margin`) so targets clear the sticky bar. Programme events are an `ol` with `<time>` and Rikke's decorative icons, alternating sides by CSS, one-sided below about 260px.
- **Components:** 3px focus ring at 3px offset (never `outline: none`); notices in four variants with icon, 4px rule and «Feil:»/«Obs:» prefix, never vanishing on guest pages. Smooth scrolling only under `prefers-reduced-motion: no-preference`. Decorative images get `alt=""`.
- **Assets:** use Rikke's own images (seal, gypsophila, lily garlands, lace frame, hero illustration 04, venue and couple photos, twelve programme icons); never draw flowers, lace or icons in code. DESIGN.md and EXPERIENCE.md win over the approved mockups.
- **Programme and practical text:** a draft of the couple's real text and times now exists (`ux/innhold/programmet-og-praktisk.md`), with open gaps marked `[? …]`. Epic 1 still uses the mockup placeholders; the real text lands in Story 7.4. Its section order and headings match EXPERIENCE.md (programme days Fredag 26. mai, Lørdag 27. mai · bryllupsdagen, Søndag 28. mai; practical parts Vielsen through Området rundt). Prices are never written into page text: «Godt å vite» reads them from `Settings`, so the programme and the RSVP form cannot show different prices.

## Cross-Story Dependencies

- 1.1 comes first; 1.2 needs it; 1.3 needs the services, actors and resolver from 1.2.
- 1.4a (tokens, base template, components) and 1.4b (sheet, images, private page) come before the guest pages 1.5–1.8; 1.4c's headers apply to every guest response, including 1.8's error pages.
- 1.5 adds the first guest view (and the HTTP-level no-write test) and the info-page frame that 1.6 and 1.7 fill.
- Later epics extend this one: the RSVP button and form (2.1); answers, consents and payments added to the seed (2.6d, 5.2, 7.2); expected-results assertions (Epic 3); real admin accounts kept apart from test data (3.1); the «Personvern» link (7.1) and the full info texts, real programme times and the «Åpne veibeskrivelse i kart» button from the content draft (7.4). The 8-person cap is enforced in 6.4 and used by the draft-cookie test in 2.4.
