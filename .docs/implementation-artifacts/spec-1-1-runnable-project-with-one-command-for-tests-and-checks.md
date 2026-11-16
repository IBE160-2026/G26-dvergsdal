---
title: 'Story 1.1: Runnable project with one command for tests and checks'
type: 'feature'
created: '2026-11-16'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '0d0f1063d684062ddf688399bb8207185f70efe7'
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repo has planning documents but no code. Ingrid the examiner must be able to install, start and test the app with a few copyable commands and no keys (NFR-8, NFR-9), and every later story needs the structure, settings and custom User to exist first (Story 1.1 in epics.md).

**Approach:** Start from `django-admin startproject config .`, shape it into the Structural Seed, add the custom `wedding.User` in the first migration, read all settings from environment variables with safe local defaults plus a production guard, and wire pytest, Ruff, djLint, CI, `.env.example` and the README.

## Boundaries & Constraints

**Always:** Python 3.14 / `requires-python >=3.14,<3.15`, Django 6.1.x, everything locked in `uv.lock`. Code and comments in English; anything a person reads at runtime (startup refusal messages) in Norwegian bokmål; README in Norwegian like today. ORM only. Docstrings name the FR/NFR/AD they implement. Small commits, one concern each.

**Never:** no models other than `User`; no views, templates, CSS or URLs beyond an empty root urlconf; no `django.contrib.admin` (`/admin/` belongs to `dashboard`, AD-10); no raw SQL; no `ATOMIC_REQUESTS`; no real secrets anywhere; no Node tooling.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Zero config | no env vars, no `.env` | `APP_ENV=local`, `DEBUG=True`, local `SECRET_KEY`, hosts `localhost,127.0.0.1,[::1]`; `migrate` + `runserver` work | N/A |
| Prod, DEBUG on | `APP_ENV=production`, `DEBUG=true`, real key, hosts set | refuses to start | `ImproperlyConfigured` naming `DEBUG` |
| Prod, default key | `APP_ENV=production`, no `SECRET_KEY` | refuses to start | message naming `SECRET_KEY` |
| Prod, no hosts | `APP_ENV=production`, `ALLOWED_HOSTS` unset/empty | refuses to start | message naming `ALLOWED_HOSTS` |
| Prod, all set | real key, hosts, `DEBUG` unset | starts, `DEBUG=False` | N/A |
| Unknown env | `APP_ENV=prod` or `Production` | refuses to start (allow list, AD-14) | message naming `APP_ENV` and allowed values |
| Several problems | prod with all three wrong | one message listing all three | N/A |

</frozen-after-approval>

## Code Map

- Repo has no app code. Tracked root files: `.gitignore` (Next.js block irrelevant), `README.md` (Norwegian, docs links, folder tree), `AGENTS.md`, `CLAUDE.md`, `docs/sensorveiledning/`.
- Tooling present: uv 0.13.8, CPython 3.14.10.
- Versions (ARCHITECTURE-SPINE.md "Stack"): WhiteNoise 6.12, pytest 9.2, pytest-django 4.14, Ruff 0.17, djLint 1.50 (1.50.4 verified). CI actions: `actions/checkout@v7`, `astral-sh/setup-uv@v10`.
- djLint 1.50 requires a path (`djlint --check` alone exits 2) and exits 2 on "No files to check" unless `allow_empty_input = true` in `[tool.djlint]` (verified: then exit 0). `.docs/` contains HTML mockups that must not be linted.
- `.docs/planning-artifacts/epics.md:136` — Story 1.1 AC with the command `uv run djlint --check`; must be updated to the path form, with the reason in the epics change log.

## Tasks & Acceptance

**Execution:**
- [x] `.python-version`, `pyproject.toml`, `uv.lock` -- pin 3.14; Django 6.1.x + WhiteNoise as deps; pytest, pytest-django, Ruff, djLint in `[dependency-groups] dev`; `[tool.pytest.ini_options]` (`DJANGO_SETTINGS_MODULE=config.settings`, `testpaths=["tests"]`), `[tool.ruff]` (py314, sensible rule set incl. isort), `[tool.djlint]` (`profile="django"`, `allow_empty_input=true` until Story 1.4a adds the first template, exclude `.docs,_bmad,.claude,.logs,docs,staticfiles`) -- one locked toolchain.
- [x] `manage.py`, `config/{__init__,settings,urls,wsgi,asgi}.py` -- startproject output, cleaned; `urls.py` has empty `urlpatterns` -- base.
- [x] `config/env.py` -- pure helpers: read bool/list env values, `validate_app_env`, `production_problems(debug, secret_key, allowed_hosts) -> list[str]` -- testable guard (AD-14).
- [x] `config/settings.py` -- settings from env via `config/env.py`; raise `ImproperlyConfigured` with all problems; `USE_TZ`, `Europe/Oslo`, `nb`; SQLite `OPTIONS` = `timeout`, `init_command` WAL, `transaction_mode: IMMEDIATE`; WhiteNoise middleware, `STATIC_ROOT=staticfiles`, `STATICFILES_DIRS=[static]`; apps `wedding`, `guests`, `dashboard` -- AD-5, AD-11, AD-14.
- [x] `wedding/{__init__,apps,models,selectors,links}.py`, `wedding/{rules,services,rsvp}/__init__.py`, `wedding/management/commands/__init__.py`, `wedding/fixtures/.gitkeep`, `wedding/migrations/0001_initial.py` -- `User(AbstractUser)` with `role` TextChoices `couple`/`helper`, default `helper` (least privilege); `AUTH_USER_MODEL="wedding.User"` -- AD-10, Structural Seed.
- [x] `guests/`, `dashboard/` (`__init__.py`, `apps.py`), `static/{css,js,fonts,img}/.gitkeep` -- Structural Seed.
- [x] `tests/test_settings_guard.py` -- unit tests for every matrix row against `config/env.py`, plus one subprocess test that `manage.py check` exits non-zero with `APP_ENV=production` and defaults -- proves the refusal really stops startup.
- [x] `tests/test_rules_purity.py` -- AST scan of `wedding/rules/**/*.py` forbidding imports of `django`, `config`, `guests`, `dashboard` and `wedding.*` outside `wedding.rules`; the scanner itself tested on a `tmp_path` module with a bad import so the test is not vacuous on an empty package -- AD-2.
- [x] `tests/test_project_setup.py` -- `AUTH_USER_MODEL`, role choices, `role` in migration 0001, TZ/language/SQLite options, no `ATOMIC_REQUESTS`.
- [x] `.github/workflows/checks.yml` -- on push and pull_request: `uv sync --locked`, `uv run pytest`, `uv run ruff check`, `uv run ruff format --check`, `uv run djlint --check .`.
- [x] `.env.example`, `.gitignore` -- every setting with safe example values; drop the Next.js block; add `db.sqlite3*`, `staticfiles/`.
- [x] `docs/manual-test-plan.md` -- table format (id, step, expected, date, result); first entry: fresh clone → README commands → server starts.
- [x] `README.md` -- description, prerequisites with versions, exact install/start/test/check commands, settings table, folder tree, planning links; say the front page arrives in Story 1.4b/1.5.
- [x] `.docs/planning-artifacts/epics.md` -- Story 1.1 djLint command → `uv run djlint --check .`, with a change-log row giving the reason.
- [x] `.docs/implementation-artifacts/sprint-status.yaml` -- story 1.1 and epic-1 status as the workflow moves.

**Acceptance Criteria:**
- Given a fresh clone with uv and no `.env`, when `uv sync`, `uv run manage.py migrate` and `uv run manage.py runserver` run, then the server starts on localhost with SQLite.
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass locally and in CI.
- Given the repo root, when listed, then only the Structural Seed folders, config files, `README.md`, `AGENTS.md`, `CLAUDE.md` and `manage.py` are there, and `git status` after running the app shows no `db.sqlite3` or `staticfiles/`.

## Design Notes

The guard is a pure function so each case is a plain unit test; `settings.py` only collects values and raises. Unknown `APP_ENV` refuses to start because local defaults (DEBUG on) on a misspelled production server would be unsafe; this extends the AD-14 allow list from the seed command to startup.

## Verification

**Commands:**
- `uv sync --locked && uv run manage.py migrate && uv run manage.py check` -- expected: no errors
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0

**Manual checks:**
- `uv run manage.py runserver`, open http://127.0.0.1:8000/ -- Django's default start page (no URLs yet); stop the server.

## Implementation Notes

Commits 5e787cb..475a2b6 on `feat/1-1-kjorbart-prosjekt` (toolchain, settings + guard, Structural Seed + User, rules-purity test, CI, README + manual test plan, epics). Locked versions: Django 6.1.3, WhiteNoise 6.12.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.5, djLint 1.50.4.

- **Guard shape:** `config/env.py` has `validate_app_env`, `read_bool`/`read_str`/`read_list` (take the environ mapping, so they are pure) and `production_problems` + `refusal_message`. Unset, empty and blank values all mean "use the default", so `SECRET_KEY=` in a copied `.env.example` still gives the local key, and `ALLOWED_HOSTS=` in production is the "no hosts" case. `APP_ENV` is matched exactly (`"local "` with a trailing space is refused). An unreadable `DEBUG` (e.g. `maybe`) also refuses to start, naming `DEBUG`.
- **Settings tests:** besides the helper unit tests, `tests/test_settings_guard.py` executes `config/settings.py` fresh with `runpy.run_path` for each matrix row, and the subprocess test runs `manage.py check`.
- **`.env` loading:** no python-dotenv; `.env.example` and the README use `uv run --env-file .env ...` (verified to read the file).
- **Ruff:** rule set E, W, F, I, B, UP, DJ, SIM, C4, PT, RUF, line length 100; generated migrations are formatted but ignore E501 and RUF012. Migration 0001 is the `makemigrations` output, formatted by Ruff; a test runs `makemigrations --check`.
- **djLint:** `extend_exclude` (keeps djLint's defaults such as `.venv`) rather than `exclude`.
- **Extras within scope:** `wedding/management/__init__.py` and `wedding/migrations/__init__.py` (needed for commands and migrations); `build/` and `dist/` kept in `.gitignore` from the dropped Next.js block, as they are also Python build output; Django 6.1's generated `MAILERS` console backend kept so nothing is ever sent.
- **MT-1** in `docs/manual-test-plan.md` was run by the agent in a fresh local clone (sync, migrate, runserver on port 8765, `curl` → 200 with Django's start page, `git status` clean, `db.sqlite3`, `db.sqlite3-wal` and `staticfiles/` ignored). Rikke should repeat it in a browser from a GitHub clone.
- **Not verified:** the GitHub Actions run itself (the branch is not pushed).
- **Task verification (orchestrator):** diff read against the spec; 42 tests passed, none skipped; every matrix row has a passing test. One fix (6517882): the README linked `architecture/technology.md` as "teknologivalg", but that file is the teacher's reference for another project (Pytagoras: FastAPI, Next.js, Supabase); it now links `oversikt.md`, `ARCHITECTURE-SPINE.md` and `.memlog.md`.
- **Review pass 1 patches** (d5c5ba9..d2cc723): WhiteNoise/static settings test, `.env.example` load test, `.env.example` SECRET_KEY wording, purity scanner names absolute `from X import a` as `X.a`, forbids `tests` and reads `utf-8-sig`, README production-default column, fixing commands and `management/commands/` as empty. After patches: 44 tests pass, Ruff and djLint exit 0.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-16): Blind Hunter (B), Edge Case Hunter (E), Verification Gap (V).

| # | Layer | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|---|
| 1 | V | WhiteNoise middleware, `STATIC_ROOT`, `STATICFILES_DIRS` have no test | medium | Pre-verified: grep of `tests/` finds no assertion; deleting the lines leaves 42 tests green | patch |
| 2 | V | `.env.example` never loaded or compared to the variables settings reads | medium | Pre-verified: no test reads the file; `APP_ENV=Local` in it would pass every test | patch |
| 3 | V | GitHub Actions workflow has never run | medium | Pre-verified: branch not pushed; the "passes in CI" criterion is unproven | push + record run before done (needs Rikke's go) |
| 4 | V, B, E | Spec says `in-review`, sprint-status says `in-progress` | low | `sprint-status.yaml` line 39; header says dev moves story to `review` | patch (orchestrator) |
| 5 | B | Implementation Notes commit range `5e787cb..475a2b6` incomplete | low | True, but the fix edits this build's spec | reject |
| 6 | B, E | `.env.example` promises "its own long, random key"; guard only rejects empty or the local key; `ALLOWED_HOSTS=*` and `SECRET_KEY=x` pass | medium | `config/env.py` `production_problems`; AD-14 names exactly the three checks, and hosting is deferred to 2027 | patch: make `.env.example` say exactly what is checked; stronger key/host rules noted for 2027 hosting |
| 7 | B | Unreadable `DEBUG`/`APP_ENV` raise before the production list, so not all problems show at once | low | Real but rare (a typo is fixed and the next start shows the rest); fix adds branching | reject |
| 8 | B | Purity scanner flags allowed `from wedding import rules` and reports `from wedding import models` as `wedding`; `tests` not forbidden | low | `_imported_modules` uses only `node.module` for absolute ImportFrom, unlike the relative branch; direct correction | patch |
| 9 | B, E | Dynamic imports (`importlib.import_module`, `__import__`) not caught | low | Unlikely in pure rule functions; fix adds AST call matching | reject |
| 10 | E | Purity test fails on a UTF-8 file with BOM | low | `read_text(encoding="utf-8")` keeps U+FEFF and `ast.parse` raises (E verified); PowerShell 5.1 on this machine writes BOM; direct correction to `utf-8-sig` | patch |
| 11 | B | CI does not pin the uv version; push + pull_request runs twice | low | Lock format change is unlikely before 2027; double run costs nothing | reject |
| 12 | B | README "uv 0.12 virker også" untested | low | Taken from the architecture Stack table, which records it | reject |
| 13 | B | No session log for this work | false | Written at the end of the session by the `sesjonslogg` skill, as CLAUDE.md requires | reject |
| 14 | B | Spec Change Log and Triage Log empty | low | Fix edits this build's spec (triage log is now filled) | reject |
| 15 | B, E | No secure cookies, proxy/HSTS, `CSRF_TRUSTED_ORIGINS`, AD-13 session age, WhiteNoise `STORAGES`, collectstatic in production | false | Out of intent: AD-13 is Epic 3 (epics.md line 71); hosting, HTTPS and production setup are deferred to 2027 (epics.md line 30) | reject |
| 16 | B | `createsuperuser` gives a superuser with role `helper` | low | Real, but no admin pages exist and accounts come from the FR-47 command (Story 3.1) | reject |
| 17 | B | README settings table mixes local and production defaults; `cp` fails in Windows cmd | low | Production defaults for `ALLOWED_HOSTS`/`SECRET_KEY` not shown; direct README correction. `cp` works in PowerShell and Git Bash | patch (table only) |
| 18 | B | Structural Seed test skips migrations/models/package `__init__`; README omits `management/commands/` from empty folders | low | Test gap unlikely to matter (`makemigrations --check` and the purity test cover them); README sentence is a direct correction | patch (README only) |
| 19 | B | README lists check commands but not the fixing ones | low | Direct README addition; contributors meet it when CI fails | patch |
| 20 | E | `node_modules/` no longer ignored | low | Architecture forbids Node tooling (AD-1); unlikely | reject |
