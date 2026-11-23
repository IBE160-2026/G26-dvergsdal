# Deferred work

Findings from build reviews that belong to a later story. Each entry names the spec that found it.

- source_spec: `.docs/implementation-artifacts/spec-1-4a-the-invitation-s-colours-type-buttons-and-notices.md`
  summary: A notice inserted after page load with `live=True` arrives with its text already inside the new `role="status"`/`role="alert"` element, which some screen readers do not announce; the story that first inserts notices with JavaScript should keep an empty live region in the page at load and put only the text into it.
  evidence: maybe-false, would be medium. Nothing inserts notices with JavaScript yet (all of 1.4a is server-rendered and JS-free), so it cannot be observed now. It is settled by testing the first in-page insertion (for example «Kopiert» in Story 2.7 or the conflict notice in Story 4.2) with NVDA and VoiceOver.

- source_spec: `.docs/implementation-artifacts/spec-1-4b-paper-rikke-s-images-and-the-private-invitation-page.md`
  summary: A wrong link with more than one path segment (for example `/hei/x/`) shows Django's own 404 page (with the URL list when DEBUG is on) instead of G1; Story 1.8 should set `handler404` to a G1-style page.
  evidence: low. Verified with the test client during the 1.4b review; the story only covers an unknown code or the bare address.
  status: done in Story 1.8 (`guests.views.page_not_found` gives G1 with 404; `tests/test_error_pages.py`).

- source_spec: `.docs/implementation-artifacts/spec-1-4b-paper-rikke-s-images-and-the-private-invitation-page.md`
  summary: No manual check covers Safari, iOS or old iPads, where `filter: url(#edge-b3)` on `::before` and `background-blend-mode` with an SVG data-URI are weakest; the flat fallback is only claimed.
  evidence: medium. Claude can only drive Edge. Settled by Rikke opening `/` on an iPhone or iPad and checking the sheet shows the paper or the flat 5px cream fallback.

- source_spec: `.docs/implementation-artifacts/spec-1-4b-paper-rikke-s-images-and-the-private-invitation-page.md`
  summary: `admin/` (Story 3.1) and `robots.txt` (Story 1.4c) must be routed above the catch-all `<str:code>/`, and their tests must prove `/admin/` and `/robots.txt` do not render G1.
  evidence: medium. `<str:code>/` matches any single segment and APPEND_SLASH redirects `/admin` and `/robots.txt` to it; the rule lives only in the `config/urls.py` docstring.
  status: robots.txt done in Story 1.4c (routed above the guest include; `tests/test_guest_privacy.py` proves it is plain text, not G1). `admin/` stays with Story 3.1.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): the web server's or platform's own access log (gunicorn, nginx, the host's request log) writes the full path, link code included; it must mask the first segment the same way as `config/logging_filters.py` or be turned off (AD-15: production access logs must mask the code too).
  evidence: medium. Only Django's own loggers are masked; no production server is chosen yet, so its log cannot be configured or tested.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): behind a TLS proxy, set `SECURE_PROXY_SSL_HEADER` (and trust only the proxy's header), or `request.scheme` stays `http` and `og:image` says `http://`, which chat apps may refuse or fetch insecurely.
  evidence: medium. `tests/test_guest_privacy.py` proves the tag follows the request scheme (`secure=True` gives `https://`); the proxy setting depends on the host.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): if `SECURE_SSL_REDIRECT` is turned on, SecurityMiddleware answers the HTTP-to-HTTPS redirect itself, before `noindex_middleware` (which sits after it), so that redirect has no `X-Robots-Tag`. Either redirect at the proxy, or move the noindex middleware above SecurityMiddleware and test the redirect's headers.
  evidence: low. The redirect itself carries no page content, but AD-15 says every response; nothing redirects to HTTPS today.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): MT-10 in `docs/manual-test-plan.md` (a test link pasted into Messenger and an SMS shows the watercolour, «Invitasjon» and the description, no names) can only run once the site has a public address.
  evidence: medium. The tags are tested; what each app actually shows is not.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Story 1.8: a 400 page for `DisallowedHost` (a request with a host not in `ALLOWED_HOSTS`) that extends `base.html` must not call `request.get_host` in the link preview, or it raises `DisallowedHost` again while rendering the error page. Render it without `request` (the preview then leaves out `og:image`) or give it its own template.
  evidence: medium. `link-preview.html` builds `og:image` from `request.get_host` whenever `request` is set; Django's default 400 page does not use our templates, so it cannot happen until 1.8 adds one.
  status: done in Story 1.8 (`guests.views.bad_request` renders without `request`; `tests/test_error_pages.py` posts a bad `Host`).

- source_spec: `.docs/implementation-artifacts/spec-1-5-the-invitation-front-page.md`
  summary: An unknown second segment under a valid code (for example `/<code>/svar/`) shows Django's own 404 instead of G1; Story 1.8's handler404 should cover every unmatched path.
  evidence: low. Same case as the multi-segment paths deferred by 1.4b.
  status: done in Story 1.8 (G1 without a valid code, «Vi finner ikke denne siden» with the phones under one; `/<code>/svar/` itself is routed in Story 2.1).

- source_spec: `.docs/implementation-artifacts/spec-1-6-practical-information-and-our-story-pages.md`
  summary: Story 7.4: add «Åpne veibeskrivelse i kart» to «Hvordan komme seg dit» on Praktisk informasjon once the real address exists. Choose the map service first, give the link `rel="noreferrer"` (AD-15), and say on the privacy page (Story 7.1) that the link leaves the site for that service.
  evidence: medium. The approved mockup has the button, but there is no address yet and no map service decided, so Story 1.6 leaves it out (DESIGN.md › Info pages and EXPERIENCE.md › Info sheet carry the dated note).

- source_spec: `.docs/implementation-artifacts/spec-1-7-the-programme-page.md`
  summary: Story 7.4: the programme's placeholder times are plain («10:00», as approved in the mockup), not bracketed, so the «[…]» placeholder test does not catch them. Replace them, and the rest of the programme text, from the content draft `ux/innhold/programmet-og-praktisk.md`, and decide du/dere for the lines that say «dere» (the voluntary line and «Meld dere på»), since a one-person household reads the same text today. The ceremony time stands both on Praktisk informasjon («Lørdag 27. mai kl. [14:00]», `guests/templates/guests/practical.html`) and in the programme («14:00 Vielsen»), with nothing tying them, so update both pages together.
  evidence: medium. Story 1.7 keeps the mockup's times and text on purpose (AD-17, the real text belongs to 7.4); `tests/test_programme_page.py` compares the page with the mockup, so it will fail when 7.4 changes the text and must be updated with it.

- source_spec: `.docs/implementation-artifacts/spec-1-7-the-programme-page.md`
  summary: Story 2.3: when the RSVP form picks a kroner display (thousands with a space, for example «1 450 kr»), use the same display for the programme's meal prices in «Godt å vite», which today print the plain int («340 kr.»).
  evidence: low. Every meal price is under 1000 kr, so the plain int reads correctly now; the first amount ≥ 1000 (the cabin weekend or a total) appears in Story 2.3.

- source_spec: `.docs/implementation-artifacts/spec-1-7-the-programme-page.md`
  summary: Story 4.5 (the settings admin page): a meal price of 0 (a fresh `migrate` without the seed, or a meal the couple pays for) renders «Middagen betales selv: 0 kr.» in the programme's «Godt å vite». Decide how a price of 0 is handled before the couple can save one: refuse it, or let the programme show the meal as free.
  evidence: low. `update_settings` accepts 0 (`wedding/services/settings.py:90`); invitations are not sent before the real prices are entered, so no guest sees it today.

- source_spec: `.docs/implementation-artifacts/spec-1-8-error-pages-that-still-show-how-to-reach-the-couple.md`
  summary: Story 3.1: the error handlers are site-wide, so `/admin/` paths get the impersonal guest error pages («ta kontakt med brudeparet direkte»), and a 404 under `/admin/` gives G1. Decide the couple's own 404, 500 and CSRF pages there (for example by checking the path in `guests.views._reachable` or the handlers, or a dashboard frame). Add `admin` to `NOT_LINK_CODES` in `config/logging_filters.py`, as already planned.
  evidence: medium. Nothing is routed under `/admin/` yet, so a guest page is the right answer today; once the dashboard exists, a logged-in couple who meets an error would see a guest page that tells them to contact themselves.

- source_spec: `.docs/implementation-artifacts/spec-1-8-error-pages-that-still-show-how-to-reach-the-couple.md`
  summary: Story 3.1: there is no `handler403`, so a `PermissionDenied` (the admin raises it for staff without a permission) still gets Django's own bare 403 page. Decide the couple's own 403 together with their 404, 500 and CSRF pages.
  evidence: low. `config/urls.py` sets only `handler400`, `handler404` and `handler500`; no guest code raises `PermissionDenied`, so only the admin can reach it (1.8 review, blind and edge-case layers).

- source_spec: `.docs/implementation-artifacts/spec-1-8-error-pages-that-still-show-how-to-reach-the-couple.md`
  summary: Epic 2 (the RSVP form): `handler400` treats every 400 as an untrusted host, so a form POST under a valid link that trips `RequestDataTooBig`, `TooManyFieldsSent` or a bad multipart body gets the impersonal 400 page with no back button and no phones. Decide there whether a 400 that is not `DisallowedHost` should use `_reachable`.
  evidence: medium. `guests.views.bad_request` never looks up the code; unreachable today because no guest view reads a request body (1.8 review, blind layer).
  status: decided in Story 2.1: the 400 stays impersonal. The step forms are urlencoded with fewer than 20 fields, far below `DATA_UPLOAD_MAX_NUMBER_FIELDS` (1000) and `DATA_UPLOAD_MAX_MEMORY_SIZE` (2.5 MB), so only a forged request can trip `RequestDataTooBig` or `TooManyFieldsSent`, and that request is not owed a personal page.

- source_spec: `.docs/implementation-artifacts/spec-1-8-error-pages-that-still-show-how-to-reach-the-couple.md`
  summary: Before go-live: `MaskLinkCodes` only masks a path that starts with `/`, so a link code in a slash-less path inside a log record (such as Django's `Resolver404` text `{'path': '<code>/finnes-ikke/'}` in a chained traceback) is logged unmasked. Widen `_PATH` in `config/logging_filters.py`, or mask `Resolver404`'s `path`.
  evidence: low. Found while patching 1.8: the new `_reachable` warning chained the `Resolver404` on a 404 and leaked the code; fixed there with `__suppress_context__`. No other known log line carries a slash-less path.

## From the Epic 1 retrospective (2026-11-21)

Routed from [epic-1-retro-2026-11-21.md](epic-1-retro-2026-11-21.md); the finding id in brackets points to the source there.

- source_spec: `.docs/implementation-artifacts/epic-1-retro-2026-11-21.md` (B1)
  summary: Story 3.1 (before the login adds `?next=`) and before go-live: widen `_PATH` in `config/logging_filters.py` (or add a pass for bare 22-character link-code tokens) so a code is masked also when percent-encoded (`?next=%2F<code>%2F`), in brackets (`[/<code>/]`), after a colon (`path:/<code>/`) or without a slash (`code=<code>`). Add each shape to `tests/test_log_masking.py`. Extends the 1.8 «before go-live» entry above.
  evidence: medium. Each shape was checked against `mask_link_codes` in the retrospective and passed through unmasked.

- source_spec: `.docs/implementation-artifacts/epic-1-retro-2026-11-21.md` (B6, B7)
  summary: Story 2.1: decorate the guest read views (`front_page`, `info_page`) with `@require_safe`, so a POST to `/<code>/` gets 405 instead of «Skjemaet ble ikke sendt», and set `Cache-Control: private, no-store` on guest responses (with a test next to the `X-Robots-Tag` test) before the first page shows answer state.
  evidence: low today (no answer state yet), medium once Epic 2 stores answers.
  status: done in Story 2.1 (`front_page` and `info_page` have `@require_safe` and `@never_cache`; the RSVP views, `csrf_failure`, `page_not_found` and `server_error` have `@never_cache`; `tests/test_guest_privacy.py` checks `Cache-Control` private/no-store and the 405).

- source_spec: `.docs/implementation-artifacts/epic-1-retro-2026-11-21.md` (R6, B9)
  summary: Story 2.6d (extends the seed): `seed_testdata` overwrites the single real `Settings` row every run (`seed_testdata.py:80`), although its docstring promises to replace only its own test data. Write settings only while the row still holds the migration placeholders, or say plainly in the help and output that settings are replaced. Also test the «Fant ikke eller kunne ikke lese» path (missing and invalid `seed.toml`) and assert the role labels «(brudeparet)» / «(hjelper)» in the printout.
  evidence: medium. Found by the edge-case and verification-gap lenses; the overwrite was confirmed in the code.

- source_spec: `.docs/implementation-artifacts/epic-1-retro-2026-11-21.md` (B5)
  summary: Story 4.5 (settings page): `update_settings` accepts a phone with no digit («ring meg»), and `tel_number` then returns "", so the contact silently vanishes from every guest page. Refuse a non-empty phone without a digit. Decide this together with the price-0 entry above.
  evidence: low. Only reachable once the couple can edit settings.

- source_spec: `.docs/implementation-artifacts/epic-1-retro-2026-11-21.md` (B8)
  summary: The next story that touches `config/settings.py`: add a test that `whitenoise.runserver_nostatic` is in `INSTALLED_APPS` before `django.contrib.staticfiles`, as `test_noindex_middleware_comes_before_whitenoise` does for the middleware. Removing the line leaves all 666 tests green, and it is the exact bug MT-8 found in 1.4c.
  evidence: medium. Mutation-tested in the retrospective.
  status: done in Story 2.1 (`test_runserver_nostatic_comes_before_staticfiles` in `tests/test_guest_privacy.py`).

- source_spec: `.docs/implementation-artifacts/epic-1-retro-2026-11-21.md` (B2, B3, B4)
  summary: Hosting (no story yet): read `CSRF_TRUSTED_ORIGINS` and the proxy header from env (and list them in `.env.example`), run `manage.py check --deploy` in the production checks, and refuse to start in production while test data (`is_test_data`) exists or while the settings row still holds the migration placeholders (blank phones, price 0, deadline 2028-01-04). Without `CSRF_TRUSTED_ORIGINS` behind a TLS proxy, every RSVP POST lands on the friendly CSRF page.
  evidence: medium. Joins the hosting entries above and the 2026-11-16 issues.md item on a stricter production guard.

- source_spec: `.docs/implementation-artifacts/epic-1-retro-2026-11-21.md` (D1, D2, S2, S3, A2, A3)
  summary: Code tidy-ups for the next story that touches each place: move the copied test helpers (`_row_counts`, `make_admin`, `_get`, `tel:` parsing) into `tests/helpers.py` or a fixture; split `tests/test_design_system.py` when Epic 2 adds form components; rename `_not_found` / `NOT_FOUND` in `guests/views.py`. In Story 3.1, add a test that every reserved first segment is in `NOT_LINK_CODES`, and a test that `guests` and `dashboard` never import each other.
  evidence: low. Maintainability only.
  status: partly done in Story 2.1: `_not_found` / `NOT_FOUND` are renamed `_unknown_link` / `PAGE_NOT_FOUND`, `_row_counts` is `row_counts()` in `tests/helpers.py`, and the form components have their own `tests/test_form_components.py`. Still open: `make_admin`, `_get` and the `tel:` parsing helpers, and the two Story 3.1 tests.

## From Story 2.1 (2026-11-21)

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: Convert the three px breakpoints left in `static/css/site.css` (`max-width: 339.98px`, `299.98px` and `259.98px`, the Narrow widths section) to em, re-measured at the default text size and at 20px default text, in the Impeccable pass (Epic 1 retrospective action 8) or the next story that touches them. `tests/test_form_components.py` allows exactly these three; remove each from `PX_ALLOWED` as it is converted.
  evidence: medium. DESIGN.md › Narrow widths (rule of 2026-11-21) says every layout breakpoint is in em; Stories 1.5 to 1.7 each found a px breakpoint that broke at 20px default text.

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: Story 4.3 (locked states after the deadline): add a README step and an MT row that reach the closed page «Svarfristen har gått ut» by hand (for example by setting the deadline to yesterday in the shell), since today only pytest shows it.
  evidence: low. Blind review.

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: Stories 2.2–2.5: give the step registry (`wedding/rsvp/steps.py`) a `question` field so each step's heading lives in one place, and keep the yes/no values and summary texts next to the form they belong to.
  evidence: low. Blind review; step 1's question is hard-coded in `_render_step` today.

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: Story 4.4 (the couple's mount): test the non-guest branches of `_owner` and `_merged` in `wedding/rsvp/views.py` (first member as respondent, revision 0) when the form is mounted for the couple.
  evidence: low. Blind review; untested until a second mount exists.

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: Household editing: two members with the same name read the same in legends, error lines and the error summary. Warn or require distinct names when the couple adds a guest.
  evidence: low. Blind review; no seed household has duplicates.

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: The Impeccable pass (Epic 1 retrospective action 8): map the RSVP form's raw px values in `static/css/site.css` to the spacing tokens where DESIGN.md allows.
  evidence: low. Blind review.

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: The settings-editing story: validate `rsvp_deadline`; `date.max` makes `is_past_deadline` overflow on `deadline + 1 day` and every /svar/ address would give 500.
  evidence: low. Edge-case review; not reachable until the couple can edit the deadline.

- source_spec: `.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md`
  summary: The CSRF 403 re-render of a step is still a POST response, so the browser's Back to it asks for a resubmission (the invalid-«Fortsett» case was fixed with PRG in 2.1). Revisit if the usability test meets it.
  evidence: low. Found by the orchestrator in Edge; only after an expired token or blocked cookies.
