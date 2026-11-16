# Architecture Spine Review (good-spine rubric) — AI'll handle it

*Reviewed: `ARCHITECTURE-SPINE.md` (draft, 2026-11-16) against the good-spine checklist, with `.memlog.md` as rationale. Driving spec: `prds/prd-aill-handle-it-2026-11-07/prd.md` (final, 2026-11-16). Also read for cross-checks: `ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md` (Open Questions, draft and form sections). Greenfield, altitude: feature (the level below is epics and stories). Builder: a beginner solo developer working through AI agents, so every rule must be one an agent can follow and a reviewer can check without deep Django knowledge. The spine itself was not edited.*

## Verdict

A clear, well-reasoned spine that is close to build-ready but needs one revision pass: a handful of high-impact divergence points are still open (the shared RSVP form that FR-63 needs, where in-progress answers live between steps, the service caller/actor contract with household scoping, and how the admin role is stored), and the deferred production envelope lacks the SQLite-specific constraints that would stop a 2027 hosting choice from breaking the design.

## What the spine does well

- **One paradigm, stated once and drawn.** Functional core / imperative shell with a dependency diagram and a one-line import rule (`rules` imports nothing from the project; `guests` and `dashboard` never import each other). This is exactly the kind of rule an AI agent can follow.
- **The riskiest logic is isolated.** AD-2 + AD-4 + AD-16 together (pure rules, nothing derived stored, a hand-written oracle) target NFR-2 / SM-2 directly, and the "Prevents" lines name the real failure (the guest page and the admin summary counting differently).
- **Open decisions from upstream are closed with traceable reasons.** D12 (AD-17), D14 (AD-6), D15 (AD-1, AD-5, Stack) and UX open questions 4–6 (AD-7, AD-8, AD-13), each with Rikke's verbatim direction in the memlog.
- **Concrete, checkable values.** 128-bit codes via `secrets.token_urlsafe(16)`, 20-hour sliding sessions, 23:59:59 Europe/Oslo, whole-kroner `int`, WAL + `transaction_mode: IMMEDIATE`, a 4 KB draft test.
- **The 2027 upgrade is not left to memory.** Django 6.1 → 6.2 LTS is in Stack, Deferred and GitHub issue #13 (verified open: "2027: Oppgradere Django 6.1 til 6.2 LTS før nettsida går live").
- **Zero-config + production guard (AD-14)** fits NFR-8 and FR-72 and is easy to test.

## Checklist results

| # | Checklist item | Result | Notes |
|---|---|---|---|
| 1 | Fixes the real divergence points for the level below, misses none | **Partial** | Most are fixed. Missed: R-01 shared RSVP form (FR-63), R-02 between-step state carrier, R-03 service actor + household scoping, R-04 admin role storage / custom user model, R-06 seed codes vs AD-6, R-07 rule input types and FR-55 drill-down, R-08 "Needs attention" item identity. |
| 2 | Every AD's Rule is enforceable and actually prevents its stated divergence | **Partial** | Most rules are concrete. AD-8's "Prevents" claim is not what the rule achieves (R-09); AD-15's log rule is defeated by default access logs (R-09); AD-3 conflicts with the default seed approach and with Django framework writes (R-06, R-10); no mechanism enforces the layering rules or "before every commit" (R-10). |
| 3 | Nothing under Deferred could let two units diverge | **Partial** | Hosting/backup deferrals lack constraints that bind the v1 design (R-05). FR-77 [2027] collides with AD-8 as worded (R-11). "Throttling details" is really a decision sitting in Deferred (R-12). English version deferral leaves i18n markup undecided (R-12). |
| 4 | Named tech is verified-current; memlog lists what was checked | **Pass, with two gaps** | Versions are plausible for 2026-11-16 and the memlog records official/PyPI checks for Django, Ruff, pytest, pytest-django, WhiteNoise, djLint. uv 0.12 and Python 3.14 are not recorded as checked against an official source; Python 3.15 is now out, so the Python version should be pinned (R-12). |
| 5 | If a spec drove it, it covers the spec's capabilities | **Pass, with gaps** | Every live FR group appears in the Capability map. Gaps are in how, not whether: FR-63 (R-01), FR-55 (R-07), FR-29 consent-text version only in memlog (R-12), FR-77 (R-11). NFR-5 and NFR-7 are not mapped (acceptable: UX-owned and trivially met at 70 guests). |
| 6 | Every dimension the altitude owns is decided, deferred or an open question | **Partial** | Silent dimensions: production error visibility/observability, CI and the pre-commit mechanism, migration/deploy procedure, single-instance and disk-type constraints for SQLite (R-05, R-10). The spine has no Open Questions section at all, so nothing is explicitly parked. |
| 7 | Mermaid diagrams valid | **Pass** | All three parse by inspection (see Mermaid section). |
| 8 | No template comments or placeholders | **Pass** | No `<!-- -->`, TODO, TBD, `{{ }}` or `[ASSUMPTION]` markers. The `[ADOPTED: …]` tags are used on AD-8, AD-13, AD-17 but not on AD-6, AD-7 or AD-1/AD-5, which also close upstream questions (cosmetic, R-12). |

## Findings

Severity: **high** = two stories will very likely build incompatible things, or a security/privacy rule has a hole; **medium** = likely rework or a rule that does not do what it says; **low** = clarity, hygiene, upstream sync.

### R-01 [high] FR-63 "same form as the guests" has no home that both apps can import

- **Evidence:** FR-63: the couple can change any household's answer "using the same form as the guests". Structural Seed puts forms in `guests/` ("guest views, forms, templates under /<code>/", line 239). The paradigm rule says `guests` and `dashboard` never import each other (line 49). AD-8 scopes the draft cookie to `/<code>/` (line 109), so the admin side has no defined place for its in-progress answers.
- **Why it matters:** The dashboard override story (tier 2, item 1) will either import from `guests/` (breaking the rule), copy the step forms (exactly the drift AD-2/AD-7 exist to prevent), or invent a second step engine. It will also have to choose where the couple's half-finished override lives (session, hidden fields, a second cookie), with allergy data involved (FR-31).
- **Fix:** Add a module in `wedding/` (for example `wedding/rsvp/`) that owns the step sequence, the step forms and the "next applicable step" logic (calling `rules/`). Both `guests/` and `dashboard/` use it. Decide in AD-8 (or a new AD) that the couple's override uses the same draft mechanism, scoped to the household's admin URL (for example `/admin/husstander/<id>/svar/`), and that its "Send" goes through the same `send_answer` service with an admin actor (see R-03).

### R-02 [high] The carrier of answers between form steps is not fixed

- **Evidence:** AD-7 says each step is POSTed, validated and redirected (POST-redirect-GET) but not where the accumulated answers are kept until "Send answer". AD-8 describes the cookie as the FR-78 *draft* (kept if the guest leaves). Only by combining them does it follow that the cookie must also be the step-to-step state. EXPERIENCE.md still says "Where device storage is unavailable (private mode, no scripts) there is no draft", which no longer matches a server-set cookie.
- **Why it matters:** Tier 1 contains both the step form and FR-78. An agent building the step form first will naturally reach for `request.session` (a database write before send, violating AD-8 and FR-26) or hidden fields; the FR-78 story then adds a cookie on top. Two state stores for one form is the divergence AD-8 claims to prevent.
- **Fix:** Add to AD-7/AD-8: "The signed draft cookie is the *only* carrier of in-progress answers between steps. No `request.session`, no hidden fields carrying earlier steps, no database rows. Each step POST reads the cookie, merges the step, and writes the cookie back." Add one line on what happens if cookies are blocked (for example: the form detects the missing cookie on step 2 and shows a plain message with the couple's phone numbers). Update EXPERIENCE.md's FR-78 section to match.

### R-03 [high] Services have no caller contract: who is acting, and on which household

- **Evidence:** AD-3 makes services the only writers; AD-10 says admin-facing services check the `couple` role. Nothing says how a service learns who is acting, and nothing scopes guest-originated writes to the household resolved from the link. Yet FR-12 (who answered), FR-29/FR-31 (who gave or registered consent), FR-39 (guest or couple change sets "Changed"), FR-63 (records the admin as author) and FR-35 (who reported paying) all need the actor.
- **Why it matters:** (a) Stories will diverge on signatures: some services take `request`, some `user`, some `guest_id`. (b) Security: a forged POST from a valid link could name a guest ID in another household (for example in consent withdrawal or "I have paid"), and nothing in the spine requires the service to refuse it. That breaks FR-2 and the NFR-4 line "only logged-in admins see guest answers" for writes.
- **Fix:** Add an AD or convention: every service takes a keyword `actor` (one small type in `wedding/`, either a resolved guest + household from AD-6 or an admin user) and never a `request`. Guest actors may only read or write their own household; the service checks that every guest/household ID in the input belongs to `actor.household` and raises otherwise. Admin actors pass the `couple` check from AD-10. Add a test per write service for the cross-household case.

### R-04 [medium-high] How the admin role is stored is undecided, and it must be decided before the first migration

- **Evidence:** AD-10: "each admin user is a Django user with exactly one role, `couple` or `helper`". The ER diagram shows `AdminUser`. Nothing says whether this is a custom user model with a `role` field, Django Groups, or a profile model.
- **Why it matters:** Django's documentation recommends setting `AUTH_USER_MODEL` to a custom user model at project start; switching after the first migration is painful, especially for a beginner. The login story, the `create admin` command (FR-47), the role check in services (AD-10) and the helper read-only rendering will each pick their own approach if this is open. "Exactly one role" is also only enforceable with a single field, not with Groups.
- **Fix:** Decide in AD-10: `wedding.User(AbstractUser)` with `role = CharField(choices=[couple, helper])`, set as `AUTH_USER_MODEL` in the very first migration; one helper (for example `wedding.services.auth.require_couple(actor)`) used by every admin write service; templates read `user.role` for read-only rendering. Rename the ER entity to `User` to match.

### R-05 [medium-high] The deferred production envelope lacks constraints that bind the v1 design; several operational dimensions are silent

- **Evidence:** AD-5 fixes SQLite + WAL for production. The Deferred hosting row lists "EU/EEA, a persistent disk, a data processing agreement"; the backup row lists "daily encrypted copy … 30 days". Not stated anywhere: how many app instances, what kind of disk, how a consistent backup is taken, how errors are seen in production, how deploys and migrations run, and whether there is CI.
- **Why it matters:**
  - SQLite with WAL needs a local block disk; it is unsafe on network file systems (NFS/SMB, which some "persistent volume" products are), and it cannot be shared by more than one machine. A 2027 host picked on price could violate both and silently corrupt data.
  - Copying a live WAL-mode database file is not a consistent backup; it must use SQLite's backup API (`sqlite3 .backup` or `VACUUM INTO`).
  - With email removed (D16) and third parties excluded (AD-15), Django's default "email the ADMINS on 500" path is gone and nothing replaces it. A broken guest flow in production could go unnoticed; PRD 3.2 monitoring only covers "site is down".
  - PRD 3.2 "Updates" requires tests to pass, a backup first and a check after; there is no CI or deploy procedure in the spine, and "both run before every commit" (Style) names no mechanism (see R-10).
- **Fix:** Add to the Deferred hosting row (or a short "Production envelope" AD): exactly one app instance; SQLite on a local block disk, not a network file system; backups via the SQLite backup API, then encrypted; migrations run after the pre-update backup. Add a Deferred or Open Question row for production error visibility (for example: server-side error log on the host plus the uptime check hitting a health URL that exercises the database), with the constraint that no error service may receive guest data unless covered by a DPA. Decide now whether v1 has CI (a GitHub Actions job running `uv run pytest`, Ruff and djLint is cheap and helps sensorveiledning criteria 3 and 5).

### R-06 [medium] Seed data contradicts AD-6 and is likely to bypass AD-3; the oracle file has no format

- **Evidence:** UJ-6/FR-68: the README lists "a test link per guest". AD-6: "each guest has one active code from `secrets.token_urlsafe(16)`". If the seed command generates random codes, the README links break on every reseed. AD-3: management commands call services and never `.save()`, but the default Django way to load seed data is `loaddata` fixtures, which writes rows directly. AD-16 says the oracle is "a committed data file next to the seed data" without naming the format or shape.
- **Why it matters:** The seed story, the README story and the oracle-test story are all tier-1 foundation work and will likely be built by different agent sessions; each will make its own assumption.
- **Fix:** Amend AD-6: production codes come from `secrets.token_urlsafe(16)`; seed codes are fixed 22-character URL-safe strings stored in the seed file (so README links are stable), allowed only because AD-14 blocks seeding in production. Amend AD-3 or AD-16: the seed command builds data by calling services (no `loaddata`), so the seed exercises the same write paths as real use. Fix the formats: for example `wedding/fixtures/seed.toml` and `wedding/fixtures/expected_results.toml` (TOML is in the standard library via `tomllib`), with a stated top-level shape (counts by name, totals per household, payment status per household, lock state at stated moments).

### R-07 [medium] Rule inputs are unspecified, and FR-55's drill-down can drift from the count

- **Evidence:** AD-2: rule functions "take plain values and return plain values". It does not say which value types, or who converts models into them. FR-55: "every count opens a list of the people behind it." The spine says counts come from `rules/`, but not that the lists do.
- **Why it matters:** Each story will invent its own dicts or tuples for the same household, which duplicates the conversion code across selectors and views. Worse, the natural way to build a drill-down list is an ORM filter in a selector; that filter is a second implementation of the rule and can disagree with the count (for example on FR-75 removed choices). This is the exact drift AD-2 exists to prevent, at the place it is most likely to happen.
- **Fix:** Add to AD-2: the input types are frozen dataclasses in `wedding/rules/types.py` (for example `Person`, `HouseholdAnswer`, `Prices`, `PaymentLedger`), and `selectors.py` is the only code that converts models into them. Count rules return the *set of people* (IDs), and the count shown is the size of that set; drill-down pages render that same set.

### R-08 [medium] "Needs attention" items have no identity, and the "Changed" marker has two possible owners

- **Evidence:** AD-4 stores "Needs attention handled marks" and the "Changed" marker as facts; the ER diagram links `AttentionMark` to `Household` only. FR-56 items are derived (not answered, allergy question unanswered per *guest*, report mismatch, refund owed, Changed). Nothing defines what a mark points at, or whether handling a "Changed" item clears the marker or adds a mark.
- **Why it matters:** If a mark is just (household, kind), handling a mismatch hides every later mismatch for that household. The "Changed" story and the "Needs attention" story can implement "handled" in two incompatible ways. Allergy items are per guest, but marks are per household.
- **Fix:** Define the item key in a rule function (for example `attention_items(...)` returns items with `kind`, `household_id`, optional `guest_id`, and a `fingerprint` of the state that raised it, such as the report ID or the answer revision). A mark stores that key; an item reappears when its fingerprint changes. State that "Changed" is cleared only by marking the item handled (one owner).

### R-09 [medium] AD-8 and AD-15 do not do exactly what they claim

- **Evidence:** AD-8 "Prevents … allergy data reaching the server before consent", but a cookie scoped to `/<code>/` is sent to the server with every request under that path, and the server must read it to render the steps and the check page. `django.core.signing` signs and compresses but does not encrypt; the value is readable after base64/zlib decoding. AD-15 "no names, link codes or allergy content are written to logs", but the link code is the first URL path segment, and both `runserver` and typical production app servers write the request path to the access log by default.
- **Why it matters:** The privacy page (FR-66) and the GDPR reasoning will be written from these claims. A reviewer or sensor reading the code will find the gap. In production, a host's access logs could hold every guest's link code for weeks.
- **Fix:** Reword AD-8's Prevents to "allergy data being *stored* on the server before consent" and add "the server reads the draft only to render the current request and never logs or persists it". In AD-15, name the mechanism: the production app server's access log is either off or formatted without the path, and Django logging uses a filter that replaces the first path segment with `<code>`; request headers (cookies) are never logged. Local `runserver` logs are acceptable because only fictional data exists there.

### R-10 [medium] No mechanism enforces the layering rules or the commit-time checks

- **Evidence:** The import rules (line 49), AD-2 ("no Django or database imports"), AD-3 ("views … never call `.save()`") and Style ("both run before every commit") rely on people noticing. No tool is named. Django's own `ModelForm.save()` and `LoginView` (writes `last_login` and session rows) are the defaults AI agents reach for, and they conflict with AD-3 as worded.
- **Why it matters:** The builder is a beginner using agents; rules that are not machine-checked will erode quietly, and the spine is the place to say how they are checked.
- **Fix:** Add a convention: an architecture test in `tests/` (or `import-linter` contracts in `pyproject.toml`) that fails if `wedding/rules/` imports Django or the project, if `guests` and `dashboard` import each other, or if `.save(`/`.delete(`/`.create(` appears outside `wedding/services/` and migrations. Name the commit hook (for example the `pre-commit` framework running Ruff and djLint) and add it to Stack. Scope AD-3 to the project's own models, so Django's auth/session writes are explicitly allowed.

### R-11 [medium] FR-77 [2027] conflicts with AD-8 as worded

- **Evidence:** FR-77 [2027]: "The site records when a household has started: pressed Start or saved an answer, never just loaded the page." AD-8: "nothing about an unsent answer is written to the database. 'Send answer' is the first write."
- **Why it matters:** The 2027 story must either break an invariant or drop a requirement; an agent will not know which.
- **Fix:** Carve it out now in AD-8: "Exception [2027]: the FR-77 'started' timestamp on the household, written by a service on the first step POST, holds no answer content." Or list it under Deferred with that constraint.

### R-12 [low] Hygiene, memlog-only rules and upstream sync

- **Rules that live only in the memlog** but bind stories: consent records store a consent-text version constant (FR-29); the guest subpaths (`/<code>/svar/…`, `/program/`, `/praktisk/`, `/historie/`, `/personvern/`); the admin area at `/admin/` with **Django's own admin site not installed or mounted** (an agent running `startproject` gets `path("admin/", admin.site.urls)` by default, which collides with the dashboard); `uv run pytest` as the one test command (NFR-9). Promote these to the Consistency Conventions table.
- **Throttling** in Deferred is actually decided (one limiter on Django's database cache). That cache needs `createcachetable`, which adds a README setup step (NFR-8). Move the decision to a convention and leave only "thresholds" deferred.
- **AD-6 "a GET request never writes"**: the unknown-code throttle (database cache) and AD-13's `SESSION_SAVE_EVERY_REQUEST` both write on GET. Scope the rule to guest and household data.
- **Python pin**: Python 3.15 has been released; pin `requires-python = ">=3.14,<3.15"` and add `.python-version` so `uv` does not pick a version Django 6.1 may not support yet. Record uv 0.12 and Python 3.14 as checked against official sources in the memlog, like the other versions.
- **i18n**: with an English version "if ever", say whether v1 templates use `{% translate %}` or plain Norwegian strings; otherwise some templates will and some will not.
- **`Settings` model name** collides with `django.conf.settings` in conversation and in agent prompts; consider `SiteSettings`.
- **APP_ENV default**: the production guard only runs when `APP_ENV=production` is set; a host that forgets it runs with local defaults (including `DEBUG`). Add it to the deferred go-live checklist, or make the guard also trigger when `ALLOWED_HOSTS` contains a non-local host.
- **`[ADOPTED: …]` tags** appear on AD-8, AD-13 and AD-17 but not on AD-6 (D14), AD-7 (UX OQ 4) or AD-1/AD-5 (D15). Use them consistently or not at all.
- **Upstream documents not yet synced** (AGENTS.md: keep planning documents living): PRD §8 still lists D12, D14 and D15 as open; EXPERIENCE.md still lists UX Open Questions 4–6 as open and says the running total and draft need scripts; PRD 3.2 still puts the static no-script fallback in [2027], while AD-7 makes it v1; the memlog says the 6.2 upgrade is "to be added to PRD section 3.2 Setup", which has not happened.
- **Spec binds** list "FR-1 to FR-78", which includes the removed FR-18 and FR-43–FR-45. Harmless, but "live FRs in FR-1 to FR-78" is more exact.

## AD-by-AD check

| AD | Rule enforceable? | Prevents its stated divergence? | Note |
|---|---|---|---|
| AD-1 Monolith | Yes | Yes | Clear and checkable (no `package.json`, no JSON views). |
| AD-2 Rules only in `rules/` | Partly | Partly | Needs input types and set-returning counts (R-07); needs an import check (R-10). |
| AD-3 Services only writers | Partly | Partly | Needs actor/scoping contract (R-03), seed path (R-06), scoping to project models and an automated check (R-10). |
| AD-4 Facts stored | Yes | Yes | Good list. Attention-mark identity missing (R-08). |
| AD-5 SQLite + ORM | Yes | Yes for dev/prod parity | Production disk/instance/backup constraints missing (R-05). |
| AD-6 Personal links | Yes | Yes | Seed codes conflict (R-06); GET-write scope (R-12). |
| AD-7 Server-rendered steps | Yes | Partly | State carrier not named (R-02); step forms must be shareable (R-01). |
| AD-8 Draft on device | Yes | Partly | "Reaching the server" claim inaccurate (R-09); admin override not covered (R-01); FR-77 conflict (R-11). |
| AD-9 Revision check | Yes | Yes | Concrete and testable. |
| AD-10 Roles in services | Partly | Partly | Role storage open (R-04); guest-side scoping missing (R-03). |
| AD-11 Deadline function | Yes | Yes | Takes the moment as input, so tests can pass a fixed `now`. |
| AD-12 Integer kroner | Yes | Yes | |
| AD-13 Admin sessions | Yes | Yes | Exact settings named. |
| AD-14 Zero config | Yes | Yes | Guard is opt-in (R-12). |
| AD-15 No third parties | Partly | Partly | Asset/header parts are enforceable; log part needs a mechanism (R-09). |
| AD-16 Oracle | Partly | Yes in intent | File format and shape unspecified (R-06). |
| AD-17 Editable info text | Yes | Yes | Escaped + paragraph breaks is the right constraint. |

## Deferred table check

| Deferred item | Can two units diverge while it waits? | Note |
|---|---|---|
| Hosting, app server, domain, HTTPS | **Yes, indirectly** | Missing single-instance and local-disk constraints that AD-5 depends on (R-05). |
| Backup tooling, monitoring | **Yes, indirectly** | Missing "SQLite backup API" constraint; error visibility not covered (R-05). |
| Django 6.2 LTS upgrade | No | Tracked in issue #13. |
| FR-40 history, FR-67 delete all | No | Both bound to services (AD-3). |
| Editable info pages | No | AD-17 already fixes the shape. |
| Throttling details | No, but it is a decision, not a deferral | Move to conventions; note `createcachetable` (R-12). |
| Browser tests | No | Reasonable given AD-7. |
| PC layout, English | **Possibly** | i18n markup undecided (R-12). |

## Version check (as of 2026-11-16)

| Item | Spine | Plausible and current? | Recorded as checked in memlog? |
|---|---|---|---|
| Django | 6.1.x, 6.2 LTS before go-live | Yes. 6.1 released August 2026, security support to December 2027; 6.2 LTS due April 2027 with support to April 2030; 5.2 LTS ends April 2028, correctly rejected. | Yes (djangoproject.com, PyPI 6.1.3) |
| Python | 3.14 | Yes, supported by Django 6.1/6.2. 3.15 is out, so pin it (R-12). | Only "installed on Rikke's PC" |
| uv | 0.12 | Plausible | No official check recorded |
| SQLite | bundled, ≥ 3.31 | Yes; `transaction_mode` and `init_command` exist since Django 5.1 | Yes (Django docs) |
| WhiteNoise | 6.12 | Plausible | Yes (PyPI 6.12.0) |
| pytest / pytest-django | 9.2 / 4.14 | Plausible | Yes (PyPI) |
| Ruff | 0.17 | Plausible | Yes (PyPI 0.17.5) |
| djLint | 1.50 | Plausible | Yes (PyPI 1.50.4) |

## Spec coverage (PRD → spine)

| PRD area | Covered | Gap |
|---|---|---|
| FR-1–FR-6 links | AD-6, AD-15 | Seed codes (R-06) |
| FR-7–FR-11 pages | AD-1, AD-15, AD-17 | — |
| FR-12–FR-24, FR-70, FR-78 RSVP | AD-2, AD-7, AD-8, AD-9 | State carrier (R-02) |
| FR-25–FR-31 allergies/consent | AD-3, AD-8 | Consent-text version only in memlog; FR-31 actor (R-03, R-12) |
| FR-32–FR-36, FR-71 money | AD-2, AD-4, AD-12 | — |
| FR-37–FR-42 change/lock | AD-9, AD-11 | — |
| FR-46–FR-48 admin access | AD-10, AD-13 | Role storage (R-04) |
| FR-49–FR-53, FR-76 guest list | AD-3, AD-6 | — |
| FR-54–FR-58, FR-77 overview | AD-2, AD-4 | Drill-down (R-07), attention identity (R-08), FR-77 (R-11) |
| FR-59–FR-62 payments | AD-2, AD-4, AD-12 | — |
| FR-63–FR-65 overrides/settings | AD-10, AD-11 | Shared form (R-01) |
| FR-66–FR-67 privacy | AD-15 | Log mechanism (R-09) |
| FR-68, FR-69, FR-72 test data | AD-14, AD-16 | Formats and seed path (R-06) |
| FR-73–FR-75 counting rules | AD-2 | — |
| NFR-1 reliability (production) | Deferred | Envelope constraints (R-05) |
| NFR-3/NFR-4 privacy, security | AD-6, AD-10, AD-13–AD-15 | R-03, R-09 |
| NFR-5, NFR-6, NFR-7 | Language convention; otherwise UX-owned | Acceptable |
| NFR-8, NFR-9 | AD-14, conventions | Commit hook / CI mechanism (R-10) |

## Dimension coverage at feature altitude

| Dimension | Status |
|---|---|
| Paradigm, module boundaries | Decided |
| Data model and ownership | Decided (role storage open, R-04) |
| Interfaces (URLs, no API) | Mostly decided; subpaths and `/admin/` only in memlog (R-12) |
| State and concurrency | Decided (AD-8, AD-9), carrier implicit (R-02) |
| AuthN/AuthZ | Partly (R-03, R-04) |
| Errors | Decided (convention) |
| Configuration and secrets | Decided (AD-14) |
| Testing strategy | Decided (AD-16, memlog); formats open (R-06) |
| Code quality tooling | Tools named; enforcement mechanism silent (R-10) |
| Deployment and environments | Local decided; production deferred with partial constraints (R-05) |
| Infra/provider strategy | Deferred with constraints, missing disk/instance (R-05) |
| Operations: backups, monitoring | Deferred with constraints, missing backup method (R-05) |
| Operations: error visibility, logging destination | **Silent** (R-05, R-09) |
| CI / delivery pipeline | **Silent** (R-05, R-10) |
| Migrations | **Silent** (R-05) |
| i18n | Convention for v1 language; markup for later English silent (R-12) |
| Performance/scale | Implicit (NFR-7 trivially met); acceptable |
| Open questions | No section; consider adding one for R-05's error-visibility item |

## Mermaid check

- **Dependency flowchart (lines 33–47):** valid `flowchart LR`; quoted labels, one `subgraph wedding … end`, a cylinder node `db[("SQLite")]`. Nodes first referenced outside the subgraph (`services`, `selectors`) are moved into it by their later declaration inside, which is the intended picture.
- **ER diagram (lines 247–257):** valid `erDiagram`; all cardinalities (`||--|{`, `||--o|`, `||--o{`) are legal and labels are quoted where they contain spaces. Content notes: `Settings` is mentioned in prose but not drawn; `AdminUser` should match the chosen user model name (R-04); `AttentionMark` linked only to `Household` (R-08).
- **Environments flowchart (lines 261–273):** valid `flowchart TB`; subgraph IDs with quoted titles (an apostrophe inside double quotes is fine), edge labels `|HTTPS|` and `|daily, encrypted|` are legal.

Checked by reading against Mermaid syntax; no renderer was run.

## Suggested order of fixes

1. R-01, R-02, R-03, R-04 before the first tier-1 story is written (they shape `wedding/` and the first migration).
2. R-06 and R-07 before the seed and oracle stories (tier-1 foundation).
3. R-08, R-09, R-10, R-11 in the same revision pass; they are small text changes.
4. R-05 can be written now as constraints in the Deferred table; the actual choices stay in 2027.
5. R-12 as a tidy-up, including the upstream PRD and EXPERIENCE.md sync.
