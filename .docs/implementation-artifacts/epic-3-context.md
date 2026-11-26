# Epic 3 Context: The couple sees the numbers and can trust them

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

The couple log in to an admin area, see how many households have answered, see the numbers Hardingasete asks for (arrivals, beds, meals, allergies, the Friday hike), open the people behind every count, and see a simple list of every household plus the allergy list. Automated tests prove that every count, total and allergy state equals the expected-results list worked out by hand, so the couple, the helpers and the examiner can trust the numbers. This is the last epic of the T1 usability-test build.

## Stories

- Story 3.1: The couple logs in
- Story 3.2: Answer progress and the summary
- Story 3.3: Every count opens the people behind it
- Story 3.4: The overview of every household and the allergy list
- Story 3.5: Tests prove the numbers match the expected-results list

## Requirements & Constraints

- Admin users log in with username and password; the couple have full access, helpers see everything and change nothing (the helper read-only mode itself is Epic 6). Accounts are made only by a management command; there is no self-registration.
- Quick tasks (seeing whether a household has answered, the summary, the allergy list) must work on a 360px phone: targets at least 44px, no horizontal scroll.
- Every count is the length of an id list returned by a pure rule function; the drill-down shows exactly those ids. A count of zero is plain text, not a link.
- Allergy data shows only for guests with stored consent; every coming guest has exactly one of three allergy states. Payment panels only show «not answered» and zero amounts until Epic 5.
- Security: passwords use Django's default hashing; the admin session cookie is scoped to `/admin/` and lasts 20 hours without use (renewed by every request); link codes never reach the logs, also on login redirects.
- The tests that assert the expected-results list use an explicit `now`; a deliberate change to that list is its own commit with the reason.
- Seed data: two fictional admin accounts (couple and helper) are test data and are replaced by `seed_testdata`; real accounts must survive it.

## Technical Decisions

- `wedding.User` has a `role` (`couple` or `helper`); `wedding/services/permissions.py` `require_couple(actor)` is the one write check. Guests are never users; guest views never read `request.user`.
- `dashboard/` holds admin views and templates under `/admin/` and never imports `guests` (and the reverse); shared templates live in `wedding/templates/wedding/`. `wedding/rsvp/` imports neither.
- Only `wedding/services/` writes; selectors load facts, rules decide counts and statuses and take `now` explicitly.
- Reserved first path segments (`admin`, `robots.txt`, `static`, `stil`) are routed above the catch-all `<str:code>/` and are listed in `NOT_LINK_CODES` of the log filter.
- Error pages are site-wide handlers; under `/admin/` they must be the couple's own, never the guest pages.
- Admin pages use flat page-green, straight-edged cream admin panels, the Admin nav (Oversikt, Gjester, Betalinger, Innstillinger, Logg ut; not sticky), denser 18px text and 44px targets; breakpoints are written in em.

## UX & Interaction Patterns

- Login (A1): states error, slowed (Epic 6) and expired; the expired text is «Du ble logget ut fordi du var borte en stund.»; no warning before expiry and no restore of unsaved input.
- Admin home (A2) comes after login; the attention list at the top is Epic 6.
- Status tags always use text plus icon, never colour alone; empty states have their own wording («Ingen husstander ennå.», «Ingen allergier registrert ennå.»).

## Cross-Story Dependencies

- Stories 3.2 to 3.4 all render inside the admin frame and login protection that Story 3.1 builds; 3.3 needs the rule id lists from 3.2; 3.5 needs the finished counts and the seed data (its Synne allergy note depends on Story 7.2 loading the withdrawal).
- Story 5.2/5.3 fill in the Betaling panel; Story 6.1 adds the helper read-only line; Story 6.6 adds login throttling; Story 4.4 mounts the RSVP form under `/admin/` and splits `wedding/rsvp/views.py` first.
