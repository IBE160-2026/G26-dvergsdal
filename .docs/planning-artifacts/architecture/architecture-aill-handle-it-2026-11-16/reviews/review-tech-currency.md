---
title: Technology currency review of ARCHITECTURE-SPINE.md
reviewed: ARCHITECTURE-SPINE.md and .memlog.md (both dated 2026-11-16)
date: 2026-11-16
lens: technology currency (versions, existence, fit, maintenance, compatibility)
method: PyPI (pip index versions + PyPI JSON API), official docs (djangoproject.com, python.org, sqlite.org, docs.python.org, MDN), GitHub repos via gh, and a local smoke test of the exact stack in a throwaway venv
---

# Technology currency review: ARCHITECTURE-SPINE.md

## Verdict

The stack is current and installs and runs together. One committed rule is wrong in practice: `Referrer-Policy: no-referrer` (AD-15) makes Django reject every guest form POST with a CSRF 403. Two smaller items are out of date: the uv version, and the SQLite minimum Django needs. The rest holds up, with a few fit caveats to write down.

## How this was checked

- **Versions:** `py -m pip index versions <pkg>` and `https://pypi.org/pypi/<pkg>/<ver>/json`, giving upload dates, `requires_python` and classifiers.
- **Release and support dates:** djangoproject.com/download, the Django 6.2 roadmap, the 6.1 and 6.2 release notes, and python.org/downloads.
- **Compatibility:** the GitHub repos (tox.ini, pyproject.toml, changelogs, commits since the last tag) for WhiteNoise, pytest-django and djLint.
- **Reality check:** a scratch venv with Python 3.14.0, Django 6.1.3, WhiteNoise 6.12.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.5 and djLint 1.50.4. All resolved together without conflicts. The smoke test covered these:
  - **SQLite options:** `OPTIONS` with `init_command` (WAL, busy_timeout, synchronous) and `transaction_mode: IMMEDIATE`. The PRAGMAs read back as `wal`, `5000` and `1`, and `connection.transaction_mode` is `IMMEDIATE`.
  - **DatabaseCache:** `createcachetable`, `cache.add`/`incr`.
  - **Signing:** `signing.dumps(..., compress=True)` / `loads(max_age=...)`.
  - **Link codes:** `secrets.token_urlsafe(16)` gives 22 characters.
  - **Sessions:** `SESSION_COOKIE_AGE` + `SESSION_SAVE_EVERY_REQUEST`.
  - **Headers and CSRF:** SecurityMiddleware with `SECURE_REFERRER_POLICY = "no-referrer"`, and CSRF with `Origin: http://testserver` vs `Origin: null`.
  - **WhiteNoise:** `collectstatic` with `CompressedManifestStaticFilesStorage`, then serving a hashed file.
  - **pytest-django:** a test under pytest 9.2 with `-W error::DeprecationWarning`. It passed.

## Version table

| Item | Spine says | Verified current (2026-11-16) | Status | Source |
| --- | --- | --- | --- | --- |
| Python | 3.14 | 3.14.10 is the latest 3.14 patch (2026-10-25). 3.15.2 is the newest Python. 3.14 is in bugfix until Oct 2027 and has security support until Oct 2030 | OK as a series. Local install is 3.14.0, ten patches behind | https://www.python.org/downloads/ |
| uv | 0.12 | **0.13.8** (2026-11-12). 0.13.0 came out 2026-10-09 and **defaults to Python 3.15** when nothing is pinned. Local install is 0.12.18 | **Out of date** (F2) | https://pypi.org/project/uv/ , https://github.com/astral-sh/uv/releases/tag/0.13.0 |
| Django | 6.1.x | 6.1.3 (2026-11-03). 6.1 was released 2026-08-05. Mainstream support ends Apr 2027, extended support Dec 2027. Supports Python 3.12–3.15 | OK | https://www.djangoproject.com/download/ , https://docs.djangoproject.com/en/6.1/releases/6.1/ |
| Django 6.2 LTS | 6 Apr 2027, support to Apr 2030 | Final release 6 Apr 2027 (alpha 19 Jan, beta 23 Feb, RC 23 Mar). LTS confirmed. Extended support to Apr 2030. Python 3.12–3.15 | OK, matches issue #13 | https://www.djangoproject.com/download/6.2/roadmap/ , https://docs.djangoproject.com/en/dev/releases/6.2/ |
| Django 5.2 LTS ends Apr 2028 | yes | yes (5.2.19) | OK | https://www.djangoproject.com/download/ |
| SQLite | "bundled with Python (Django requires 3.31 or newer)" | **Django 6.1 requires SQLite 3.37.0+**. The bundled SQLite in the Python 3.14.0 Windows build is 3.50.4 | **Stale fact** (F3), no practical impact | https://docs.djangoproject.com/en/6.1/releases/6.1/ , https://docs.djangoproject.com/en/6.1/ref/databases/ |
| WhiteNoise | 6.12 | 6.12.0 (2026-02-27) is the latest on PyPI. Its classifiers stop at Django 6.0. Django 6.1 support is on `main` (PR #702, metadata/CI only) but not released yet | Works, not officially declared (F4) | https://whitenoise.readthedocs.io/en/stable/changelog.html , https://github.com/evansd/whitenoise/pull/702 |
| pytest | 9.2 | 9.2.0 (2026-10-27) | OK | https://pypi.org/project/pytest/ |
| pytest-django | 4.14 | 4.14.0 (2026-08-10) is the latest. Its classifiers list Django 5.2 and 6.0. Django 6.1 support was merged after the tag (PR #1288, CI/metadata only). Upstream CI runs pytest>=9 | Works, not officially declared (F4) | https://pytest-django.readthedocs.io/en/latest/changelog.html , https://github.com/pytest-dev/pytest-django/pull/1288 |
| Ruff | 0.17 | 0.17.5 (2026-11-12) | OK | https://pypi.org/project/ruff/ |
| djLint | 1.50 | 1.50.4 (2026-11-15). Actively maintained: 15 releases between 1 and 15 Nov 2026, almost all by one maintainer. Requires Python >= 3.11 | OK, high churn (F8) | https://github.com/djlint/djLint/releases |

## Findings

### F1 · High · `Referrer-Policy: no-referrer` breaks every guest form POST (AD-15 vs AD-7 and the Forms convention)

- **What the spine says:** AD-15 requires every guest response to send `Referrer-Policy: no-referrer`. AD-7 makes every RSVP step a plain HTML form POST, and the Forms convention puts CSRF on every POST.
- **What browsers do:** under `no-referrer`, browsers send `Origin: null` on form submissions, because these are navigate-mode requests and not GET/HEAD (MDN, "Effect on the Origin header").
- **What Django does:** since 4.0, CsrfViewMiddleware checks the Origin header whenever one is present, over HTTP as well as HTTPS. `null` never matches. Django's CSRF docs warn about this directly: "you might use … `Referrer-Policy: no-referrer` … those techniques cause a CSRF failure on requests with 'unsafe' methods. Instead, use alternatives like `<a rel="noreferrer" ...>`."
- **Reality check:** with `SECURE_REFERRER_POLICY = "no-referrer"`, a POST with `Origin: http://testserver` returned 200. A POST with `Origin: null` returned **403**. An HTTPS POST without Origin or Referer also returned **403**.
- **Why tests won't catch it:** Django's test client does not imitate the browser's `Origin: null`, so the planned test-client tests (AD-7, Tests) would pass while the real guest flow fails in every browser.
- **Sources:**
  - https://docs.djangoproject.com/en/6.1/ref/csrf/
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Origin
- **Fix:**
  - Change AD-15 to `Referrer-Policy: same-origin`. This is Django's default `SECURE_REFERRER_POLICY`. The link code is then never sent to another site, which is the goal of FR-4, while same-origin POSTs keep a real Origin.
  - Add `rel="noreferrer"` on any external links (map, payment app, and so on).
  - Record the change and its reason in the memlog.
  - Add one test that asserts the header value. Manual browser testing must cover at least one real form submission.

### F2 · Medium · uv 0.12 is out of date, and uv 0.13 picks Python 3.15 unless the repo pins 3.14

- **The issue:** uv 0.13.0 (2026-10-09) made Python 3.15 the default when no version is requested or pinned. An examiner who installs uv today gets 0.13.x (NFR-8). If the repo has no `.python-version` and no `requires-python`, uv may download Python 3.15. Django 6.1.3 supports 3.15, but the project would then run on a version it was not tested on.
- **What the memlog recorded:** "uv 0.12 (already used in the repo)" and "Python 3.14 (installed on Rikke's PC as 3.14.0)". These come from the local machine, not from a currency check.
- **Local Python is behind:** Rikke's 3.14.0 is ten patches behind 3.14.10. Django officially supports only the latest micro release of each Python series.
- **Sources:**
  - https://github.com/astral-sh/uv/releases/tag/0.13.0
  - https://pypi.org/project/uv/
  - https://docs.djangoproject.com/en/6.1/faq/install/
- **Fix:**
  - Stack table: uv "0.13 (0.12 also works)".
  - Add `.python-version` with `3.14` (`uv python pin 3.14`).
  - Add `requires-python = ">=3.14"` to `pyproject.toml`, or `">=3.14,<3.15"` to pin the series.
  - README: say uv installs the right Python.
  - Locally: `uv self update` and `uv python install 3.14`, which picks 3.14.10.

### F3 · Medium · The SQLite minimum in the Stack table is stale (3.31, should be 3.37)

- **The issue:** Django 6.1 raised the minimum SQLite from 3.31.0 to 3.37.0 (6.1 release notes, ticket #36671).
- **Impact:** none in practice. uv's Python builds and python.org's Windows builds bundle a far newer SQLite (3.50.4 here). But the spine states a requirement that is no longer true, which is exactly what this review is meant to catch.
- **Sources:**
  - https://docs.djangoproject.com/en/6.1/releases/6.1/
  - https://code.djangoproject.com/ticket/36671
- **Fix:** change the Stack row to "Django 6.1 requires 3.37 or newer".

### F4 · Low · WhiteNoise 6.12.0 and pytest-django 4.14.0 do not officially declare Django 6.1 support

- **The issue:** both projects added Django 6.1 only on their `main` branches after their latest release.
  - WhiteNoise: PR #702, merged 2026-06-14. The unreleased changelog says "Add Django 6.1 support".
  - pytest-django: PR #1288, merged 2026-08-10, right after 4.14.0.
- **Why it still works:** both PRs change only CI and metadata files (tox.ini, pyproject classifiers, changelog). The released code is what upstream CI now tests against Django 6.1. The local smoke test confirms both packages work with Django 6.1.3 on Python 3.14, with no deprecation warnings.
- **Sources:**
  - https://github.com/evansd/whitenoise/pull/702
  - https://whitenoise.readthedocs.io/en/stable/changelog.html
  - https://github.com/pytest-dev/pytest-django/pull/1288
- **Fix:** record in the memlog that compatibility was checked this way. Bump to WhiteNoise 6.13 and pytest-django 4.15 when they are released. Re-check both against Django 6.2 under issue #13.

### F5 · Medium (deferred, but it changes a stated rationale) · WAL makes the database more than one file, and it needs a local disk

- **The rationale that breaks:** the memlog says "a single file is the simplest thing to back up". With WAL, the `-wal` file "is part of the persistent state of the database and should be kept with the database if the database is copied or moved". A plain file copy of `db.sqlite3` can lose committed transactions or be corrupt.
- **The hosting limit:** "WAL does not work over a network filesystem". Some PaaS "persistent volumes" are network-backed.
- **Sources:** https://www.sqlite.org/wal.html
- **Fix:**
  - Deferred backup row: back up with SQLite's online backup API (`sqlite3.Connection.backup`) or `VACUUM INTO`, never a raw file copy. Rehearse the restore from that copy.
  - Hosting constraint: the persistent disk must be local block storage, not a network filesystem.
  - WAL in `init_command` is fine. It is persistent once set, and setting it on every connection is harmless.

### F6 · Low · Busy timeout and the database cache: use the documented knobs and note their limits

- **Busy timeout:** the smoke test showed `PRAGMA busy_timeout` in `init_command` works. Django's documented setting is the `"timeout"` key in `OPTIONS`, used together with `transaction_mode: "IMMEDIATE"` ("To make sure your transactions wait until `timeout` before raising 'Database is Locked'…").
  - **Fix:** use `"timeout": 20` (or similar) rather than a PRAGMA, so the timeout is set in one place.
  - Source: https://docs.djangoproject.com/en/6.1/ref/databases/
- **DatabaseCache as the throttle store:**
  - It needs `manage.py createcachetable` after `migrate`. This must go in the README and in test setup (NFR-8).
  - `incr()` is not atomic on this backend (a two-step read/update).
  - The default `MAX_ENTRIES` is 300 with culling. An attacker spraying unknown link codes from many keys can push throttle counters out of the cache.
  - Django 6.2 adds `CULL_PROBABILITY` and deprecates passing table names to `createcachetable`.
  - None of this blocks the design at 70 guests, but the throttling story should set `MAX_ENTRIES` explicitly and accept or handle the non-atomic `incr`.
  - Sources: https://docs.djangoproject.com/en/6.1/topics/cache/ , https://docs.djangoproject.com/en/dev/releases/6.2/

### F7 · Info · Header handling and signing: what is built in and what needs code

- **X-Robots-Tag:** Django has no built-in support. AD-15 needs a small custom middleware, or a response helper, for guest URLs. The meta tag goes in the base template.
  - Source: https://docs.djangoproject.com/en/6.1/ref/middleware/
- **Signing:** `django.core.signing.dumps(obj, salt=..., compress=True)` and `loads(..., max_age=...)` exist and work. Compression cut a repetitive 6-person draft from 2287 to 220 characters. Real free-text notes compress less, so keep the planned 4 KB test.
  - `HttpResponse.set_signed_cookie()` has no `compress` option. Implement AD-8 with `signing.dumps` + `set_cookie(path=f"/{code}/", httponly=True, samesite="Lax", secure=...)`.
  - Use a salt that includes the link code.
  - Django 6.1 changed signed-cookie salt derivation and deprecated `SIGNED_COOKIE_LEGACY_SALT_FALLBACK`. This only affects `set_signed_cookie`, so it is not a problem for a design built on `signing.dumps`.
  - Sources: https://docs.djangoproject.com/en/6.1/topics/signing/ , https://docs.djangoproject.com/en/6.1/ref/settings/
- **Sessions:** `SESSION_SAVE_EVERY_REQUEST` and `SESSION_COOKIE_AGE` exist in 6.1 with no deprecation notice. Two consequences to note:
  - Every admin request writes the session row, which is a short write on SQLite and fine for 5 admins.
  - Expired sessions pile up until `manage.py clearsessions` runs. Add it to the deferred production operations.
- **CSP (optional improvement):** Django 6.0+ has a built-in `ContentSecurityPolicyMiddleware`. A `default-src 'self'` policy would enforce AD-15's "nothing from other companies" in the browser, not just by convention.
- **Link codes:** `secrets.token_urlsafe(16)` gives 22 characters and 128 bits. The Python docs suggest 32 bytes for general tokens. 128 bits combined with throttling is well above what is needed for an unguessable link, but say in the memlog that this is a deliberate choice.
  - Source: https://docs.python.org/3.14/library/secrets.html

### F8 · Low · djLint is healthy but changes very fast

- **Status:** djLint is not unmaintained. It had commits and releases on 2026-11-15/16, Renovate keeps its dependencies current, and it supports Python 3.11–3.16.
- **The risk:**
  - Bus factor of about one: almost all recent releases are by a single maintainer.
  - High churn: 1.49.0 to 1.50.4 in two weeks. 1.50.0 changed exit codes and config-error handling, and the docs site recently removed formatting guidance.
- **Source:** https://github.com/djlint/djLint/releases
- **Fix:** rely on the exact version in `uv.lock`, and pin djLint in pre-commit if it is used there. Record that a formatter change after an upgrade is a separate commit. Ruff is unaffected.

## What was verified and holds

- Django is current (6.1.3), and so are its support dates for 6.1 (Dec 2027), 6.2 LTS (6 Apr 2027 to Apr 2030) and 5.2 LTS (Apr 2028). The upgrade decision (issue #13) rests on correct dates.
- Django 6.2 supports Python 3.14, so the planned upgrade does not force a Python change.
- `OPTIONS["transaction_mode"]` and `OPTIONS["init_command"]` on SQLite exist (added in 5.1) and behave as the spine assumes. Django's docs advise against `ATOMIC_REQUESTS` with IMMEDIATE, which matches AD-5.
- pytest 9.2, Ruff 0.17.5 and djLint 1.50.4 are the current releases.
- The memlog's PyPI check (line "Checked on PyPI 2026-11-16") matches PyPI exactly for Django, Ruff, pytest, pytest-django, WhiteNoise and djLint.

## Process note (criterion 1, traceability)

The memlog records sources for Django, the LTS dates and the PyPI versions. It does not record a check for:

- uv
- Python patch currency
- WhiteNoise and pytest-django compatibility with Django 6.1
- the `no-referrer` header's effect on CSRF
- `X-Robots-Tag` support
- the SQLite minimum

Adding a `(version)` or `(check)` line for each fix above, with the source URL, would make the corrections traceable as KI-styring: an AI-proposed rule (`no-referrer`) caught and corrected by verification.
