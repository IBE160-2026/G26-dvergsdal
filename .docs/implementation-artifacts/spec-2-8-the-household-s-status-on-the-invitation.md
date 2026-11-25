---
title: "Story 2.8: The household's status on the invitation"
type: 'feature'
created: '2026-11-26'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/answered-1.html'
warnings: ['oversized']
deferred: []
---

<intent-contract>

## Intent

**Problem:** After a household has sent its answer, the invitation still shows «Svar innen …» and the RSVP sheet with «Svar på invitasjonen», so tante Marie cannot see that Arild already answered, and `/<code>/svar/` invites a second answer (FR-24, UX-DR10). «Betal senere» promised that the link always shows what is left to pay (FR-34), which the front page does not yet keep.

**Approach:** When `household_answer(household)` exists, the front page swaps the hero's deadline line for «Svar sendt <date> · Se svaret» and the RSVP sheet for a status block `#status` in the same place; the nav «Svar» (front page and info pages) points to `#status`; GET/HEAD on any `/<code>/svar/` step address redirects to `/<code>/#status`.

## Boundaries & Constraints

**Always:**
- "Answered" means `household_answer(actor.household) is not None` (the 2.6a selector); no new status rule or stored flag (AD-4). Story 5.3's `payment_status` («Ikke svart», FR-60, issues.md) should reuse the same selector; nothing named `payment_status` exists yet, so nothing to align.
- Hero (answered): `<p class="hero__deadline">Svar sendt {{ sent_at|date:"j. F" }} · <a href="#status">Se svaret</a></p>` in Oslo time (e.g. «Svar sendt 12. oktober · Se svaret»); the middle dot `aria-hidden` as elsewhere; plain spaces, no `&nbsp;`. Unanswered hero unchanged.
- Status block (answered), in the RSVP sheet's place and centred like it (DESIGN › Status block, mockup `answered-1.html`): `<section class="paper-sheet rsvp status-block" aria-labelledby="status">` holding, in order: `<h2 id="status" tabindex="-1">Svaret er sendt</h2>`, the small gypsophila (same `img` as the RSVP sheet, `alt=""`, lazy), «Barnefritt bryllup», «Sendt av <sent_by_name> <weekday j. month Y> kl. <H:i>.» (same text as the receipt: move the receipt's sent line into a shared include `rsvp/includes/sent-line.html` and use it in both), «Totalt for husstanden: …» (`rsvp/includes/total.html`), and when `guest_balance(total, None) > 0` a link `button button--secondary` «Slik betaler du» to `guests:rsvp_pay` (FR-34; G7 already shows the same details as the receipt). Nothing owed: no payment link. The `id="status"` heading is the jump target, so following `#status` focuses the heading (EXPERIENCE › Status block); its focus ring is transparent like `#svar:focus`, and `scroll-margin-top` equal to the sheet's top padding keeps the sheet edge visible under the sticky nav.
- Total and balance come from the same code as the receipt: extract from `guests/views.py` `_receipt` a helper (e.g. `_sent_money(actor, settings) -> dict` with `total`, `balance`) used by `_receipt` and `front_page`; never re-compute in templates (AD-12). Guest views never read payment rows.
- Nav «Svar» keeps its label; `href` = `#status` when answered, `#svar` otherwise; from an info page, the front page URL + that fragment. `_guest_context` gains `answered: bool` (one extra SELECT on info pages); `rsvp_closed.html`/error pages that use the context are unaffected.
- `/<code>/svar/` and every step address (`_rsvp`), GET and HEAD, answered household → 302 to `reverse("guests:front_page") + "#status"`, checked **before** the deadline check (an answered household after the deadline gets the status block, not «Svarfristen har gått ut»; decided by Claude: the status block is the closest thing to G9 until Story 4.3). POST is untouched, so 2.6c's double-tap and conflict handling keep working. `sendt/`, `betal/`, `sum/` unchanged.
- After the deadline, answered: hero and status block are the same as before the deadline (EXPERIENCE › Locked after deadline keeps «Svar sendt … · Se svaret»).
- Front page stays read-only: only SELECTs, no cookie, no session (FR-3). Every new/changed view, helper and test names its FR/AD/UX-DR in its docstring. UI Norwegian, code English. Breakpoints only in em.

**Never:**
- No «Meldt betalt» (5.1), no «Dere kan endre svaret fram til …» or «Se eller endre svar» (4.1), no «Se hele svaret»/G9 or never-answered-after-deadline state (4.3), no draft notice (2.9).
- No new model, migration, cookie, script or write; no hard-coded prices or amounts.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Not answered | seeded Mona `/<code>/` | hero «Svar innen …», RSVP sheet `#svar` with «Svar på invitasjonen», nav «Svar» → `#svar`; no `id="status"` | — |
| Answered, owes | seeded Marie (`test-marie000000000000`), Arild sent | hero «Svar sendt <d. month> · Se svaret»; status block: «Svaret er sendt», gypsophila, «Barnefritt bryllup», «Sendt av Arild …», «Totalt for husstanden: 6 480 kr», «Slik betaler du» → `/test-marie000000000000/svar/betal/`; nav «Svar» → `#status`; no «Svar på invitasjonen» | — |
| Answered, nothing owed | seeded Synne | status block with «0 kr», no «Slik betaler du» | — |
| Info page nav | Marie `/program/` | nav «Svar» href `/test-marie000000000000/#status`; Mona's → `/…/#svar` | — |
| Answered opens form | Marie GET `/svar/`, `/svar/se-over/`, HEAD `/svar/` | 302 to `/test-marie000000000000/#status` | — |
| Answered after deadline | deadline yesterday, Marie GET `/` and `/svar/` | same status block; `/svar/` 302 to `#status` | — |
| Unanswered after deadline | Mona `/svar/` | closed page as before (2.1) | — |
| POST by answered household | Marie POST `/svar/se-over/` | unchanged 2.6c behaviour (no redirect) | — |
| Unknown code | `/x/` | G1 404 as before | — |

</intent-contract>

## Code Map

- `guests/views.py:125-139` `_guest_context` — add `answered` (needs `household_answer`, already imported `:55-63`). `:142-163` `front_page` — add `answer`, `total`, `balance` when answered; update docstring (SELECT count). `:214-245` `_rsvp` — redirect after `resolve_code`/`step is None`, before `is_past_deadline`, only for `request.method in ("GET", "HEAD")`. `:261-289` `_receipt` — extract the total/balance helper. Module docstring `:1-23` mention Story 2.8.
- `guests/templates/guests/front_page.html:56-58` hero line, `:151-165` RSVP sheet → `{% if answer %}` status block `{% else %}` existing sheet; update the template comment `:15-19`.
- `guests/templates/guests/components/nav-bar.html:25-26` — fragment by `answered`; update comment.
- `wedding/rsvp/templates/rsvp/sent.html:25-27` — sent line into new `wedding/rsvp/templates/rsvp/includes/sent-line.html` (takes `answer`), included in both templates.
- `wedding/rsvp/templates/rsvp/includes/total.html` — reuse as is.
- `static/css/site.css:865-901` `.rsvp`, `#svar:focus` — add `#status:focus` (transparent ring), `scroll-margin-top` on `#status`, `.status-block` spacing for the sent line/total/link (`.rsvp .button` margin already applies); see the scroll-padding note `:615-623`; narrow-width rule `:1710-1719` already covers `.rsvp`.
- `wedding/selectors.py:135` `household_answer`, `:147` `sent_answer`; `wedding/rules/money.py` `guest_balance`, `household_total` — reuse.
- Tests: `tests/test_front_page.py` uses `seeded` (unanswered, keeps all its tests valid); `:155` query counts become 4 (front page) and 3 (info pages) unanswered — update the parametrisation and docstring. `tests/conftest.py:41` `seeded_with_answers` for answered households. Codes: Sigmund `test-sigmund0000000000` (4 720), Arild/Marie `test-arild000000000000`/`test-marie000000000000` (6 480, sent by Arild), Synne `test-synne000000000000` (0), Mona `test-mona0000000000000` (unanswered); `wedding/fixtures/expected.toml:87-123`. Existing tests that GET `/svar/` for an answered household (check `tests/test_rsvp_*.py`, `test_send_answer.py`) must use `seeded` or be adjusted.
- Docs: `README.md:9` status line, `:81` Svarskjemaet (answered households see the status block; `/svar/` leads there), `docs/manual-test-plan.md` after MT-54 (`:78`); EXPERIENCE.md `:150` and `:209` (mark the built parts decided «avgjort av Claude 2026-11-26, Story 2.8», note the `id` on the heading and the «Slik betaler du» link), `:246` dated note that an answered household's `/svar/` goes to the status block, also after the deadline; `.logs/rikke/issues.md:58` add that 2.8 decides "answered" by `household_answer`; `.docs/implementation-artifacts/sprint-status.yaml:62`.

## Tasks & Acceptance

**Execution:**
- [ ] `wedding/rsvp/templates/rsvp/includes/sent-line.html` (new), `wedding/rsvp/templates/rsvp/sent.html` -- share the sent line -- FR-24, FR-74.
- [ ] `guests/views.py` -- money helper, `_guest_context.answered`, `front_page` context, `_rsvp` redirect, docstrings -- FR-24, FR-34, AD-4, AD-12, UX-DR10.
- [ ] `guests/templates/guests/front_page.html`, `guests/templates/guests/components/nav-bar.html`, `static/css/site.css` -- hero line, status block, nav fragment -- FR-24, FR-34, UX-DR10.
- [ ] `tests/test_front_page_status.py` (new) -- every matrix row with `seeded_with_answers` (and `seeded` for unanswered); DOM order in the status block; `<h2 id="status" tabindex="-1">`; `#status` count 3 (nav, hero, heading) when answered; no `&nbsp;`; SELECT-only/no-cookie for the answered front page with a pinned query count; `tests/test_front_page.py` -- query counts; fix any older test broken by the redirect.
- [ ] `docs/manual-test-plan.md` -- add MT-55 to MT-58 (Norwegian, result cells empty), see Verification.
- [ ] README.md, EXPERIENCE.md, issues.md, sprint-status.yaml -- sync as in Code Map, dated 2026-11-26.

**Acceptance Criteria:**
- Given Arild's household has answered, when Marie opens `/test-marie000000000000/`, then the hero reads «Svar sendt <d. month> · Se svaret» and the status block shows «Svaret er sendt», «Barnefritt bryllup», «Sendt av Arild <weekday date> kl. <time>.», «Totalt for husstanden: 6 480 kr» and «Slik betaler du» linking to `/test-marie000000000000/svar/betal/`.
- Given Synne's answered household owes nothing, when she opens her link, then the status block shows «0 kr» and no «Slik betaler du».
- Given the answered front page, when the guest activates nav «Svar» or «Se svaret», then the page scrolls to the status block and `document.activeElement` is the `h2#status`.
- Given an answered household, when a member GETs `/<code>/svar/`, then the response is 302 to `/<code>/#status`, before and after the deadline.
- Given Mona's unanswered household, when she opens her link, then the front page is unchanged from Story 2.1.

## Design Notes

- **Heading carries the id:** the AC wants focus on the heading after a fragment jump without JavaScript; only the fragment's target is focused, so the `h2` is `#status` and the section is labelled by it. The mockup puts the id on the sheet; the scroll margin keeps the same visual position.
- **«Slik betaler du» as a secondary link button:** the block's one primary button is «Se eller endre svar» (Story 4.1); a secondary now leaves room for it above.
- **Redirect only on GET/HEAD and before the deadline check:** POSTs carry 2.6c's double-tap and conflict handling, which must keep landing on the receipt or the conflict notice.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes.

**Manual checks (Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`) after `uv run manage.py migrate`, `uv run manage.py seed_testdata`, `uv run manage.py runserver`; rows written by the implementer with empty result cells):**
- MT-55 Forsiden før og etter svar: `test-mona0000000000000/` (hero «Svar innen …», «Svar på invitasjonen», nav → `#svar`); `test-marie000000000000/` (first AC); `test-synne000000000000/` (second AC); `test-marie000000000000/svar/` lands on `/#status`.
- MT-56 Etter fristen: `uv run manage.py shell -c "from wedding.models import Settings; import datetime; Settings.objects.filter(pk=1).update(rsvp_deadline=datetime.date.today()-datetime.timedelta(days=1))"`; Marie's front page shows the same status block and `/svar/` lands on `/#status`; Mona's `/svar/` shows «Svarfristen har gått ut». Run `seed_testdata` again afterwards.
- MT-57 Bare tastatur: on Marie's front page, Tab to nav «Svar» and Enter → focus on `h2#status`; Tab to «Se svaret», Enter → same; Tab reaches «Slik betaler du», Enter opens `betal/`; focused links have `outline-style` `solid`.
- MT-58 Oppsett: Marie's and Synne's front page at 360 × 640 and 180 × 320, with and without 20px default text size (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`): `scrollWidth` ≤ `innerWidth`, the hero line and sent line wrap inside their sheets, «Slik betaler du» ≥ 44px high, after jumping to `#status` the heading is not under the nav bar.
