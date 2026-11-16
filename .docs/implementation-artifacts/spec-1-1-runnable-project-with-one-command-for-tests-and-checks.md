---
title: 'Story 1.1: Runnable project with one command for tests and checks'
type: 'feature'
created: '2026-11-16'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
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
- [ ] `.python-version`, `pyproject.toml`, `uv.lock` -- pin 3.14; Django 6.1.x + WhiteNoise as deps; pytest, pytest-django, Ruff, djLint in `[dependency-groups] dev`; `[tool.pytest.ini_options]` (`DJANGO_SETTINGS_MODULE=config.settings`, `testpaths=["tests"]`), `[tool.ruff]` (py314, sensible rule set incl. isort), `[tool.djlint]` (`profile="django"`, `allow_empty_input=true` until Story 1.4a adds the first template, exclude `.docs,_bmad,.claude,.logs,docs,staticfiles`) -- one locked toolchain.
- [ ] `manage.py`, `config/{__init__,settings,urls,wsgi,asgi}.py` -- startproject output, cleaned; `urls.py` has empty `urlpatterns` -- base.
- [ ] `config/env.py` -- pure helpers: read bool/list env values, `validate_app_env`, `production_problems(debug, secret_key, allowed_hosts) -> list[str]` -- testable guard (AD-14).
- [ ] `config/settings.py` -- settings from env via `config/env.py`; raise `ImproperlyConfigured` with all problems; `USE_TZ`, `Europe/Oslo`, `nb`; SQLite `OPTIONS` = `timeout`, `init_command` WAL, `transaction_mode: IMMEDIATE`; WhiteNoise middleware, `STATIC_ROOT=staticfiles`, `STATICFILES_DIRS=[static]`; apps `wedding`, `guests`, `dashboard` -- AD-5, AD-11, AD-14.
- [ ] `wedding/{__init__,apps,models,selectors,links}.py`, `wedding/{rules,services,rsvp}/__init__.py`, `wedding/management/commands/__init__.py`, `wedding/fixtures/.gitkeep`, `wedding/migrations/0001_initial.py` -- `User(AbstractUser)` with `role` TextChoices `couple`/`helper`, default `helper` (least privilege); `AUTH_USER_MODEL="wedding.User"` -- AD-10, Structural Seed.
- [ ] `guests/`, `dashboard/` (`__init__.py`, `apps.py`), `static/{css,js,fonts,img}/.gitkeep` -- Structural Seed.
- [ ] `tests/test_settings_guard.py` -- unit tests for every matrix row against `config/env.py`, plus one subprocess test that `manage.py check` exits non-zero with `APP_ENV=production` and defaults -- proves the refusal really stops startup.
- [ ] `tests/test_rules_purity.py` -- AST scan of `wedding/rules/**/*.py` forbidding imports of `django`, `config`, `guests`, `dashboard` and `wedding.*` outside `wedding.rules`; the scanner itself tested on a `tmp_path` module with a bad import so the test is not vacuous on an empty package -- AD-2.
- [ ] `tests/test_project_setup.py` -- `AUTH_USER_MODEL`, role choices, `role` in migration 0001, TZ/language/SQLite options, no `ATOMIC_REQUESTS`.
- [ ] `.github/workflows/checks.yml` -- on push and pull_request: `uv sync --locked`, `uv run pytest`, `uv run ruff check`, `uv run ruff format --check`, `uv run djlint --check .`.
- [ ] `.env.example`, `.gitignore` -- every setting with safe example values; drop the Next.js block; add `db.sqlite3*`, `staticfiles/`.
- [ ] `docs/manual-test-plan.md` -- table format (id, step, expected, date, result); first entry: fresh clone → README commands → server starts.
- [ ] `README.md` -- description, prerequisites with versions, exact install/start/test/check commands, settings table, folder tree, planning links; say the front page arrives in Story 1.4b/1.5.
- [ ] `.docs/planning-artifacts/epics.md` -- Story 1.1 djLint command → `uv run djlint --check .`, with a change-log row giving the reason.
- [ ] `.docs/implementation-artifacts/sprint-status.yaml` -- story 1.1 and epic-1 status as the workflow moves.

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

## Spec Change Log

## Review Triage Log
