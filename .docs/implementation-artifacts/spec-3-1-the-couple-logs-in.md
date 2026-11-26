---
title: 'Story 3.1: The couple logs in'
type: 'feature'
created: '2026-11-26'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-3-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md'
warnings: [oversized, multiple-goals]
deferred: []
---

<intent-contract>

## Intent

**Problem:** Nothing exists under `/admin/`: the couple cannot log in, `create_admin` does not exist, `admin/` and the couple's error pages are unrouted, the log mask leaks percent-encoded, bracketed, colon-prefixed and slash-less link codes (and the login adds `?next=`), and the rules «`guests`, `dashboard` and `wedding.rsvp` never import each other» and «every reserved first segment is in `NOT_LINK_CODES`» are only docstrings (FR-46, FR-47, NFR-4, AD-10, AD-13, UX-DR34, UX-DR36).

**Approach:** (1) widen the log mask first; (2) an `OperatorActor` and `create_admin_account` service, with the `create_admin` command, kept apart from the seed's `create_admin_user`; (3) `dashboard/` with login, logout, the admin frame, a minimal Oversikt page, `admin_required`, 20-hour sessions scoped to `/admin/`; (4) `/admin/` routed above `<str:code>/`, and one error-handler dispatcher that gives `/admin/` paths the couple's own 403/404/500/CSRF pages; (5) the architecture tests and tidy-ups routed here.

## Boundaries & Constraints

**Always:**
- Every rule, view, service, template comment and test names its FR/NFR/UX-DR/AD ids. UI text Norwegian, code and the spec English; URLs Norwegian. Breakpoints in `em`; tokens from DESIGN.md (`--space-admin-*`, `admin-title`, `admin-body`), 44px targets, flat `page-green` (no grain) on admin pages, straight-edged cream admin panels.
- Passwords: Django default hashing, never in the repo, logs or `.env.example`. The command prompts with `getpass` twice and runs `validate_password`; it never takes the password as an argument or env var.
- Access = `request.user` is authenticated, active and `role in User.Role.values`; anything else redirects to `/admin/logg-inn/?next=<path>` (`next` only honoured when it starts with `/admin/`). Admin responses use `never_cache`. `AdminActor(request.user)` is the only way a view makes an actor.
- `create_admin_user` (system actor, `is_test_data=True`) stays seed-only and unchanged; `create_admin_account` (new `OperatorActor`, `is_test_data=False`) is the only path for real accounts. Both share one validator. `User.role` gets a DB check constraint (`couple`/`helper`), keeps default `helper`; `--role` has no default.
- Session: `SESSION_COOKIE_AGE = 20 * 60 * 60`, `SESSION_SAVE_EVERY_REQUEST = True`, `SESSION_COOKIE_PATH = "/admin/"` (AD-13, AD-10). Guest requests still create no session row (`row_counts()` tests stay green).
- `dashboard` imports neither `guests` nor `wedding.rsvp` (yet); `guests` does not import `dashboard`; `wedding.rsvp` imports neither. `config/error_handlers.py` may import both (it is neither).
- `admin` joins `NOT_LINK_CODES`. The log mask passes (path pass and bare-token pass) run in `mask_link_codes`; over-masking is acceptable, under-masking is not.

**Never:**
- No Django admin site, `createsuperuser` advice in the README, self-registration, password reset or «glemt passord».
- No login throttling (Story 6.6; the «slowed» state is not built), no helper read-only line or role-specific pages (Story 6.1), no Oversikt panels (3.2), no Gjester/Betalinger/Innstillinger pages (those nav items are not links until their story; no dead links).
- No JavaScript. No expiry warning or restore of input (AD-13). No guest page may render `request.user`.
- `wedding/rsvp/views.py` (1528 lines) is not touched; do not grow `guests/views.py` beyond the one small `forbidden` view.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Create account | `create_admin rikke --role couple`, same password twice | User with role couple, `is_test_data=False`, hashed password; prints «Opprettet rikke (brudeparet).» | — |
| Refused | Existing username; role `admin`/missing; passwords differ; weak password | `CommandError` with the Norwegian message, nothing written; username and role are checked before the password prompt | Service raises `InvalidUser`/`NotAllowed` |
| Seed afterwards | A real account exists, `seed_testdata` runs | Real account untouched; a seed username equal to a real one stops the seed with the existing conflict message | — |
| Login ok | Right username/password | 302 to `next` (under `/admin/`) else `/admin/`; session cookie path `/admin/`, HttpOnly; marker cookie `admin_seen` set | — |
| Login wrong | Wrong password, unknown user, inactive user or invalid role | 200 on the login page with notice «Brukernavnet eller passordet stemmer ikke. Prøv igjen.» (same text for every case), username kept, password empty, focus on the notice | No session |
| Logged out | GET `/admin/` or any `/admin/…` page without login | 302 to `/admin/logg-inn/?next=/admin/…` | — |
| Expired | Not authenticated, `admin_seen` present, GET login page | Info notice «Du ble logget ut fordi du var borte en stund.», cookie `admin_seen` deleted so it shows once | Not shown after a wrong login or after «Logg ut» |
| Logout | POST `/admin/logg-ut/` | Session flushed, `admin_seen` deleted, 302 to login with no expired notice; GET gives 405 | — |
| Unknown admin path | `/admin/hei/`, `/admin/program/` | The couple's 404, never G1 and never a guest page | — |
| No slash | `/admin` | 301 to `/admin/` (not G1) | — |
| Error pages | 403 (`PermissionDenied`), 404, 500, CSRF failure under `/admin/` | Couple's own page in the admin frame with a way back, status kept, no «brudeparet direkte» text; nav only when the visitor is a logged-in admin (never on 500) | A failing lookup falls back to the plain frame |
| Same errors on guest paths | Same errors on `/<code>/…` or `/` | Unchanged guest pages; a `PermissionDenied` there gives a new impersonal 403 page | — |
| Link codes in logs | `?next=%2F<code>%2F`, `[/<code>/]`, `path:/<code>/`, `code=<code>`, `{'path': '<code>/x/'}` | All show `[code]`; `/admin/…` stays readable; `HTTP/1.1`, `http://127.0.0.1:8000/` unchanged | — |

</intent-contract>

## Code Map

- `config/logging_filters.py` -- `NOT_LINK_CODES` (L22), `_PATH` (L29-33; lookbehind only `\s " ' ( =`, slashes only `/`), `mask_link_codes` (L44). Widen the lookbehind (`[ : , { < ; |`), accept `%2F`/`%2f` as a slash and as a segment end, then a second `re.sub` for a bare 22-character `[A-Za-z0-9_-]` token that is not adjacent to `[\w-]` and holds an uppercase letter or digit. `CODE_LENGTH` is 22 in `wedding/links.py`; the filter keeps its own constant and a test keeps them equal (as `Guest.code` does). Docstring examples change.
- `tests/test_log_masking.py` -- 8 tests, `CODE`, `UNKNOWN_CODE`, `mask_link_codes` parametrised cases (L35-); add the five shapes, a mistyped short code in the path shapes, `/admin/logg-inn/?next=/admin/` unchanged, and the real `django.request` warning after a login redirect.
- `config/urls.py` -- `urlpatterns` (robots.txt, guests include), docstring says Story 3.1 adds `admin/` and no `handler403`. Add `path("admin/", include("dashboard.urls"))` after robots.txt and before `include("guests.urls")`; handlers become `config.error_handlers.*` incl. `handler403`; update the docstring.
- `config/error_handlers.py` -- New. `bad_request` re-exports `guests.views.bad_request` (always impersonal); `page_not_found`, `permission_denied`, `server_error`, `csrf_failure` choose `dashboard.errors.*` when `request.path_info` is `/admin` or starts with `/admin/`, else `guests.views.*` (403 outside admin: new `guests.views.forbidden`). `CSRF_FAILURE_VIEW` in `config/settings.py` L72 points here.
- `config/settings.py` -- L72 `CSRF_FAILURE_VIEW`; users block (L117-) add the session settings, `LOGIN_URL = "dashboard:login"`, `LOGIN_REDIRECT_URL = "dashboard:home"`; `INSTALLED_APPS` already has `dashboard`, no Django admin.
- `guests/views.py` -- `page_not_found` L507, `csrf_failure` L557, `server_error` L580, `bad_request` L592; add `forbidden` (impersonal, 403, `@never_cache`) and templates `guests/errors/forbidden.html` (copy the shape of `bad_request.html`). `guests/templates/guests/error_page.html` is the frame the admin pages do not reuse.
- `wedding/templates/wedding/base.html` -- add `{% block body_class %}{% endblock body_class %}` on `<body>` so `admin-page` can switch off the grain.
- `dashboard/` -- `__init__.py` docstring says «Never imports `guests`»; `apps.py`. New: `urls.py` (`app_name="dashboard"`: `home ""`, `login "logg-inn/"`, `logout "logg-ut/"`, last `<path:rest>` raising `Http404` so `/admin/program/` never falls through to `guests`), `access.py` (`admin_required`, `admin_actor`), `forms.py` (`AdminLoginForm(AuthenticationForm)`: Norwegian messages, `confirm_login_allowed` refuses an invalid role), `views.py` (`AdminLoginView`, `logout_view`, `home`), `errors.py` (the couple's 403/404/500/CSRF), `navigation.py` (`NAV_ITEMS`: Oversikt `dashboard:home`, Gjester/Betalinger/Innstillinger with no url until 3.4/5.3/4.5), templates `dashboard/admin_base.html` (extends `wedding/base.html`, `body_class` `admin-page`, `<nav aria-label="Administrasjon">`, «Logg ut» as a POST button), `dashboard/login.html`, `dashboard/home.html`, `dashboard/errors/*.html`.
- `static/css/site.css` -- tokens at L109-110, L168-174 already exist; add one labelled section «Admin frame» (`.admin-page`, `.admin-nav`, `.admin-title`, `.admin-panel`, login fields reusing `.text-field`, `.button`, `.notice`). `tests/test_form_components.py` bans new px breakpoints; `tests/test_design_system.py` checks tokens against DESIGN.md.
- `wedding/actors.py` -- `AdminActor`, `SystemActor`, `Actor` union (L46); add `OperatorActor` (the person at the server console, AD-3) and `OPERATOR`.
- `wedding/services/users.py` -- `create_admin_user` (system only, `is_test_data=True`), `_validate_user`, `USERNAME_MAX_LENGTH`; add `check_new_admin(username, role)` (used by `_validate_user` and the command) and `create_admin_account(actor, username, password, role)` (operator only, `is_test_data=False`). Docstring says Story 3.1 adds the command.
- `wedding/services/permissions.py` -- `require_couple` refuses every non-`AdminActor`, including `OperatorActor`; read-only evidence.
- `wedding/models.py` -- `User` (L33-47): add `CheckConstraint(role in Role.values)` in `Meta`; new migration `0008_user_role_check.py`.
- `wedding/management/commands/create_admin.py` -- New, modelled on `seed_testdata.py`; `ServiceError` → `CommandError`.
- `wedding/services/testdata.py` -- `reset_test_data` deletes only `is_test_data=True` users: read-only evidence for the «seed leaves real accounts alone» test; `wedding/selectors.py` `seed_conflicts` makes a clashing username stop the seed.
- `tests/error_urls.py` / `tests/error_settings.py` -- test-only URLconf; add `admin/feil/` (RuntimeError), `admin/forbudt/` and `<str:code>/forbudt/` (PermissionDenied) before the site routes, export `handler403`.
- `tests/helpers.py` -- add `make_admin(role, username="rikke")` (copied today in `tests/test_households.py:22` and `tests/test_settings_service.py:41`; move both to the import). `_get` (3 files) and `tel:` parsing stay open in deferred-work.
- `tests/test_guest_privacy.py` -- `test_every_fixed_route_stays_readable_in_the_log` (L373) already iterates fixed routes and will cover `admin/` once routed; keep it.
- `tests/test_seed_testdata.py`, `tests/test_users_service.py`, `tests/test_error_pages.py` -- patterns to follow; `tests/conftest.py` fixtures `local_env`, `seeded`.

## Tasks & Acceptance

**Execution:**
- `config/logging_filters.py`, `tests/test_log_masking.py` -- first commit: widen the mask and add `admin` to `NOT_LINK_CODES`; tests per shape (FR-4, NFR-4, AD-15) -- closes sprint action `epic-1-retro-item-4` and the 1.8 slash-less entry.
- `wedding/actors.py`, `wedding/services/users.py`, `tests/test_users_service.py` -- `OperatorActor`, `check_new_admin`, `create_admin_account`: real account not test data, hashed, role set deliberately; system/admin/guest actors refused by `create_admin_account`, operator refused by `create_admin_user`; duplicates and invalid roles refused with nothing written (FR-47, AD-3, AD-10, AD-16).
- `wedding/models.py`, `wedding/migrations/0008_user_role_check.py`, `tests/test_settings_model.py` or `tests/test_users_service.py` -- role check constraint; a blank role raises `IntegrityError`; migration applies on a database with seed users (AD-10).
- `wedding/management/commands/create_admin.py`, `tests/test_create_admin.py` -- command, `getpass` monkeypatched; every matrix row incl. «seed leaves it alone» and a clashing seed username (FR-47, AD-10, AD-16).
- `wedding/rsvp/` untouched; `tests/test_architecture_imports.py` -- AST scan of `guests`, `dashboard`, `wedding/rsvp`: `dashboard` and `guests` never import each other, and `wedding.rsvp` imports neither (`guests` may import `wedding.rsvp`, as it mounts the form); `wedding.rules` keeps its existing purity test (architecture spine, Epic 1 A3, Epic 2 A1).
- `config/settings.py`, `config/urls.py`, `config/error_handlers.py`, `dashboard/*`, `wedding/templates/wedding/base.html` -- login, logout, `admin_required`, frame, Oversikt, `/admin/` above the catch-all, session settings, dispatcher (FR-46, NFR-4, AD-10, AD-13, UX-DR34, UX-DR36).
- `dashboard/templates/dashboard/*`, `static/css/site.css` -- login page (A1): `h1` «Logg inn», labels «Brukernavn» and «Passord» tied with `for`/`id`, `autocomplete="username"` / `"current-password"`, no paste blocking, `type="password"`, button «Logg inn», errors as notices; Oversikt: `h1` «Oversikt», one admin panel «Innlogget som <username>.» and the line «Her kommer oversikten over svarene.» [forslag]; nav words Oversikt · Gjester · Betalinger · Innstillinger · Logg ut, current page `aria-current="page"`, unbuilt items plain text.
- `dashboard/errors.py`, `dashboard/templates/dashboard/errors/*`, `guests/views.py`, `guests/templates/guests/errors/forbidden.html` -- couple's 403 «Du har ikke tilgang til denne siden», 404 «Vi finner ikke denne siden», 500 «Noe gikk galt», CSRF «Skjemaet ble ikke sendt» [forslag, DESIGN › Error page]; each with «Til oversikten» (logged in) or «Til innlogging» (otherwise); the 500 is rendered without the request (AD-15) (FR-5 spirit, deferred-work 1.4b/1.8 entries).
- `tests/test_admin_login.py`, `tests/test_admin_errors.py`, `tests/test_admin_routing.py` -- login right/wrong/inactive/invalid role, `next` safety (`https://evil.example/`, `/<code>/` go to `/admin/`), redirect when logged out for `/admin/` and an unknown admin path, expired notice once, logout POST/GET, hashed password (`pbkdf2_sha256$` prefix with the real hasher via `settings.PASSWORD_HASHERS`), cookie attributes (`path=/admin/`, HttpOnly) and settings values, session expiry (set `Session.expire_date` in the past → redirect to login), admin responses `no-store`, error pages per matrix, `/admin/`, `/admin`, `/admin/program/` and `/robots.txt` never render G1, every reserved first segment from the root URLconf is in `NOT_LINK_CODES`, the guest pages still create no session and render no nav, the frame on every admin page (nav words, «Logg ut», `aria-current`).
- `docs/manual-test-plan.md` -- rows MT-65 onwards (Norwegian, result cells empty), «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)» after `migrate`, `seed_testdata`, `runserver`: login with `testpar` / `bryllup-test-2028` reaches `/admin/` with nav and «Logg ut»; wrong password shows the notice with the username kept and focus on it; `/admin/` and `/admin/hei/` logged out go to login, the couple's 404 logged in; keyboard only (Tab order username, password, «Logg inn», Enter submits; visible focus); 360 × 640 and 180 × 320 at 16px and 20px default text (CDP `Page.setFontSizes`): `scrollWidth` ≤ `innerWidth`, targets ≥ 44px; the session cookie path is `/admin/`; paste and password-manager autofill attributes present.
- `README.md` -- status line, «Admin» section (seed logins, `uv run manage.py create_admin <brukernavn> --role couple|helper`, the prompt, `createsuperuser` not used), folder tree (`dashboard/`, `config/error_handlers.py`), the new test files.
- `.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md` -- dated notes (2026-11-26, Story 3.1): AD-10 `OperatorActor` and the role check constraint; AD-13 the `admin_seen` marker cookie (the browser drops the session cookie at expiry, so the server cannot tell «expired» from «never logged in» without it); error-handler dispatcher in the Structural Seed (`config/error_handlers.py`) and the `OperatorActor` in `actors.py`.
- `.docs/planning-artifacts/epics.md` -- Story 3.1 AC: add the actor wording («through its own `OperatorActor` path»), the login/logout paths and the marker cookie, with the reason.
- `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md`, `DESIGN.md` -- A1 microcopy marked [forslag] with the texts above; admin error pages row; unbuilt nav items are plain text until their story (dated).
- `.docs/implementation-artifacts/deferred-work.md` -- mark done: `admin/` routing (1.4b), `admin` in `NOT_LINK_CODES`, the couple's error pages and `handler403` (1.8), the slash-less/percent-encoded mask entries (1.8, Epic 1 B1), the import and reserved-segment tests and `make_admin` tidy-up (Epic 1 D1/A3; `_get` and `tel:` still open), the Epic 2 retro rename items only if `tests/test_send_answer.py` / `test_rsvp_send.py` are renamed here (rename them: `test_answers_service.py`, `test_rsvp_send_views.py`, docstrings updated).
- `.docs/implementation-artifacts/sprint-status.yaml` -- action `epic-1-retro-item-4` done; epic 3 and story 3.1 status.

**Acceptance Criteria:**
- Given `create_admin <username> --role couple|helper` and a valid password typed twice, when it runs, then a real account (`is_test_data=False`) with that role exists with a hashed password, and a later `seed_testdata` leaves it; an existing username or any other role is refused with a message and nothing is written.
- Given the login page at `/admin/logg-inn/`, when the right details are posted, then the user reaches `/admin/` with the admin nav and «Logg ut»; with wrong details the page shows «Brukernavnet eller passordet stemmer ikke. Prøv igjen.»; the session cookie path is `/admin/`.
- Given no login, when any `/admin/` page is opened, then the response redirects to the login page; `/admin/`, `/admin` and `/robots.txt` never render G1.
- Given a session unused for 20 hours, when the next request arrives, then it redirects to login and the login page says «Du ble logget ut fordi du var borte en stund.» once.
- Given an error under `/admin/` (403, 404, 500, CSRF), when it renders, then it is the couple's own page with a way back; the same errors under a guest path still give the guest pages.
- Given the five shapes of a link code in a log message, when masked, then each shows `[code]`.
- Given the three packages, when the import test runs, then no forbidden import exists.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why a new actor.** The epics AC forbids the system actor for real accounts, and AD-3 wants an explicit actor on every service. `OperatorActor` names the real caller (the person at the server console); `require_couple` still refuses it, so it cannot write through admin services.
- **Why a marker cookie.** The session cookie lives exactly as long as the server session (both 20 hours, renewed together), so after expiry the browser has already dropped it. A 30-day, path-scoped `admin_seen=1` cookie set at login and removed at logout is the only server-visible sign of «was logged in». It holds no data.
- **Why a dispatcher in `config/`.** `guests` and `dashboard` must not import each other, so neither can own the site-wide handlers' branching; `config/` imports both.
- **Nav items.** `NAV_ITEMS` entries without a url render as plain text, so the frame shows the final nav without a dead link; Stories 3.4, 5.3 and 4.5 add the url.

```
mask_link_codes("Not Found: /x/?next=%2FAbC…%2F")  ->  "Not Found: /x/?next=%2F[code]%2F"
mask_link_codes("code=AbC…(22)")                    ->  "code=[code]"
mask_link_codes("GET /admin/logg-inn/ HTTP/1.1")    ->  unchanged
```

## Verification

**Commands:**
- `uv run pytest` -- expected: all tests pass (1,338 before this story)
- `uv run ruff check` -- expected: no findings
- `uv run ruff format --check` -- expected: no files would be reformatted
- `uv run djlint --check .` -- expected: no files would be updated
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes after `0008`
- `uv run manage.py migrate` and `uv run manage.py seed_testdata` -- expected: succeed; then `uv run manage.py create_admin rikke --role couple` prompts and `seed_testdata` again leaves `rikke`

**Manual checks (orchestrator, Playwright against Edge, MT-65 onwards):**
- Login right and wrong, logged-out access, keyboard only, 360 and 180px, 20px text: see the task above for exact URLs and expected values.
