---
title: 'Story 4.2: No answer is overwritten without anyone seeing it'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_revision: '5afb6fb2e1262df7b8f4c66c149ca02432a5496e'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-4-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md'
warnings: ['oversized']
deferred:
- summary: >-
    A step form rendered from a cookie draft carries no `revisjon`; if the cookie is lost before the next POST the form is seeded at the newest revision and another member's newer answer can be overwritten without a notice.
  reason: >-
    Narrower than the 4.1 hole (needs the cookie to vanish mid-form); render `revisjon` = `draft.rev` on every step if it shows up in the usability test.
---

<intent-contract>

## Intent

**Problem:** When Arild sends while Marie has a form or draft open, Marie's send is refused (Story 2.6c) but her notice only says who sent and when, not what differs (FR-38, AD-9). A form Marie opened before Arild's send and continued with no cookie draft is seeded at the newer revision, so her first step overwrites Arild's change with no notice at all (Story 4.1 deferred item).

**Approach:** The opened form carries the revision it was opened at in a hidden field `revisjon`, so a cookie-less first POST starts its draft at that revision and the 2.6c check fires at send. The refusal notice becomes a warning with who, when and a list of what differs between Marie's draft and the stored answer, built by a pure rule `answer_differences` and a text module `conflict.py`; consent «Ja» is never carried across (AD-18).

## Boundaries & Constraints

**Always:**
- Hidden field (FR-38, AD-9, deviation from AD-8's «no hidden fields», dated): every form step rendered from a seeded draft (answered household, no cookie draft) carries `<input type="hidden" name="revisjon" value="{{ opened_revision }}">`, the seed's revision. `handle_step` sets `opened_revision` in `page_context` only for a seeded draft. On a POST with no cookie draft for an answered household (and not a send on the check page), `seeded_draft` is followed by `opened_at(draft, posted, current)` in `change.py`: when `posted` is an integer with `0 <= posted < current`, the draft's `rev` becomes `posted` and `cons`, `conf` and `cv` are cleared (AD-18); a missing, non-integer, negative or higher value changes nothing. A cookie draft always wins; the field is then ignored. The cookie is still written only by «Fortsett» or «Velg» (AD-8).
- Conflict check unchanged (Story 2.6c, AD-9, AD-20): the repeat check runs first, then `RevisionConflict`; a refused send writes nothing and records no `Submission`; the draft moves to the current revision with `cons`, `conf`, `cv` cleared; redirect 303 to `se-over/?sending=endret`. A second send from that check page is a new send and is saved.
- The notice for `?sending=endret` is a `warning` variant (not `error`), focused on load (`focus=True`: `tabindex="-1" autofocus`), server-rendered, not a live region and not inserted by script (deferred 1.4a note: nothing is inserted in the page, so no `role="alert"` is added; a test pins `autofocus` and no `live`). Text: «Svaret ble ikke sendt, fordi {name} sendte et svar for husstanden {l j. F Y} kl. {H:i} etter at du begynte.», then the differences, then «Se over svaret og send det på nytt. Samtykke til å lagre allergier må gis på nytt.» Oslo time. `{name}` is `HouseholdAnswer.sent_by_name`. A non-guest actor or no stored answer keeps today's generic sentence (`«svaret for husstanden er endret etter at du begynte.»`) and no list (the couple's mount, Story 4.4, gives it its own text).
- «What differs» (new pure rule `wedding/rules/differences.py`, `answer_differences(mine, sent)`, FR-38, AD-9, AD-2): both answers normalised with `normalise_answer`; per guest id (guests in either), in guest order, one `Difference(guest_id, topic, mine, sent)` for each topic that differs: `attendance` (coming or not), `days` (`present_days`, only when both come), `cabin` (`night` is True; only a guest present in both), `meals` (as sets, only a guest present in both), `hike` (only a guest present in both), `allergies` (`_allergy_key`-style compare of `AllergyEntry`, only a guest present in both; the text names the topic only, never the note). `mine` is the draft, `sent` the stored answer from `sent_answer`; confirmations and consent never count (consent is cleared in the draft by design and the notice says so). Identical answers give an empty list.
- Text of the list (`wedding/rsvp/conflict.py`, `conflict_notice(...)`, UI Norwegian): one line per difference, `{name}: du svarte {mine}, {sent_by_name} sendte {sent}`, with the values in the check page's own words (`kommer`/`kommer ikke`, `hele helgen` or the day names, `hytte hele helgen`/`overnatter ikke`, meal names or `ingen måltider`, `ja`/`nei`/`kanskje`/`ikke oppgitt` for the hike, topic `allergier og matbehov` without values); reuse the formatting helpers of `wedding/rsvp/summary.py` and `join_words`, do not copy them. No differences: «Det du har fylt ut, er likt det som er sendt.» (the notice still says who sent and that nothing was saved).
- Consent (AD-18): a draft whose revision is stale never carries a consent «Ja»: the cleared `cons` on the cookie draft (as today) and on the stale seeded draft (new). A test proves a consent «Ja» given at the old revision is gone after the refusal and after a stale seeded step.
- `wedding/rsvp/views.py` does not grow: `_changed_text` is deleted and replaced by a call into `conflict.py`; the other new code (`opened_at`, `answer_differences`, text) lives in `change.py`, `conflict.py`, `rules/differences.py`. At most +8 net lines in `views.py`. Do not split it (Story 4.4). Every new function, template and test names its FR/AD/UX-DR. UI Norwegian, code English; breakpoints only in em; no new script.

**Never:**
- No change to `send_answer`, the revision bump, `answer_changed` or `changed_at` (Story 4.1). No couple mount or couple override conflict (Story 4.4). No stored copy of the stale draft or of the answer as it was at the old revision (AD-4): the list compares the draft with the current stored answer only.
- No `role="alert"`/live region and no new script for the notice. No note text from allergy entries in the notice.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Two members in sequence | Marie's cookie draft at revision n; Arild sends (n+1); Marie «Send svaret» | 303 `se-over/?sending=endret`, nothing written, revision stays n+1; draft `rev` n+1, `cons` `{}`; page shows the warning with «Arild», date, time and the differing lines | — |
| Review and send again | Marie's next «Send svaret» from the refused page's hidden fields | 303 `sendt/`, revision n+2, `sent_by_name` Marie | — |
| Form opened before the send | Marie GET `/svar/` (revision n, no cookie, field `revisjon=n`); Arild sends; Marie POSTs step 1 with `revisjon=n` | cookie draft has `rev` n, `cons` `{}`; her later send is refused with the warning | — |
| Differences listed | Marie's draft has Filippa's cabin «Ja», Arild sent «Nei» | line «Filippa: du svarte hytte hele helgen, Arild sendte overnatter ikke» | — |
| Identical content | Arild sent what Marie's draft holds | warning with «Det du har fylt ut, er likt det som er sendt.»; second send saved | — |
| Forged or missing field | `revisjon` absent, `abc`, `-1` or higher than current | seeded at the current revision as in Story 4.1 | no error |
| Cookie draft present | cookie draft at n, post carries `revisjon=n+1` | cookie draft used, field ignored | — |
| Double tap on a send | same `innsending` posted twice | second POST: 303 `sendt/`, no warning (Story 4.1 test unchanged) | — |
| Non-guest actor | `conflict_notice` without a guest household | generic sentence, no list | — |

</intent-contract>

## Code Map

- `wedding/rsvp/views.py:665-682` `_changed_text` -- delete; `:685-698` `_sending_notice` `SEND_CHANGED` branch calls `conflict_notice`, so it needs the draft and members (add parameters; its one caller is `_render_check` `:787-823`, which has `draft`, `members`, `actor`). Return value becomes a small dataclass or `(text, items)`; pass `sending_items` into the check context. `:723-775` `_send` (RevisionConflict branch `:763-765`) unchanged. `:1302-1365` `handle_step` -- after `seeded_draft` (`:1339-1343`) apply `opened_at` for a POST and add `opened_revision` to `page_context`. Do not touch `_later_step`.
- `wedding/rsvp/change.py` -- add `opened_at(draft, posted, current)` (pure on the draft) and a tiny `posted_revision(post)` if clearer; `seeded_draft` stays.
- `wedding/rules/differences.py` (new, pure) -- `Difference`, `answer_differences(mine, sent)`; reuses `normalise_answer`, `present_days` (`wedding/rules/answer.py`), `AllergyEntry`/`EMPTY` (`wedding/rules/allergies.py`); `wedding/rules/changes.py` `_allergy_key` is the model (import it if made public, else share through a rename, no copy).
- `wedding/rsvp/conflict.py` (new) -- `conflict_notice(actor, mine, members)`: `household_answer`, `sent_answer` (`wedding/selectors.py:135-204`), `last` sender/time text moved from `_changed_text`; value words from `wedding/rsvp/summary.py` (`_day_names` `:57`, `MEALS`, `HIKE` in `wedding/rsvp/steps.py`); `join_words` (`wedding/rsvp/text.py`).
- Templates: `wedding/rsvp/templates/rsvp/check.html:40-44` the `data-send-notice` block (variant `warning`, add `items`); `wedding/rsvp/templates/rsvp/step.html:50-52` hidden `revisjon` field under `{% csrf_token %}` when `opened_revision` is set, and its comment «No hidden fields (AD-1, AD-8)» updated; `wedding/templates/wedding/components/notice.html` optional `items` list rendered as a `<ul class="notice__list">` after the text (add to its comment); the CSRF re-render of a step must keep the field (it posts the same form; check it carries `opened_revision`). `static/css/site.css:456-490` `.notice`, `:1063` `.form-sheet .notice` -- `.notice__list` spacing, em only.
- Reuse: `delete_draft`, `_see_other`, `_hidden_in`/`_walk_to_check`/`_send` helpers in `tests/test_rsvp_send_views.py:55-75,546-558` (move shared ones to `tests/helpers.py` if reused by the new test file, no copies), fixtures `seeded_with_answers`; codes: Arild `test-arild000000000000`, Marie `test-marie000000000000`; Arild's total 6 480 kr, 4 980 kr with Filippa's cabin «Nei» (`wedding/fixtures/expected.toml:94-96`).
- Tests to update: `tests/test_rsvp_send_views.py:~351-390` `test_a_send_from_an_older_revision` (`notice--error` becomes `notice--warning`, new text); `tests/test_rsvp_draft.py`/`test_rsvp_who_is_coming.py` only if they assert the absence of hidden fields.
- Docs: `ARCHITECTURE-SPINE.md` (`.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/`, AD-8 `:133`, AD-9 `:148-157`, AD-18 `:240`: hidden `revisjon`, what-differs, dated 2026-11-27); `EXPERIENCE.md` `:240` (changed-meanwhile text becomes a warning with the list; wording decided by Claude 2026-11-27, Story 4.2) and `:247`; `DESIGN.md` Notice (optional list); `README.md` status line and Svarskjemaet paragraph; `deferred-work.md`; `sprint-status.yaml`; `.logs/rikke/issues.md`; `docs/manual-test-plan.md` after MT-96.

## Tasks & Acceptance

**Execution (chunk 1: rule and text, with tests, about 350 lines):**
- [x] `wedding/rules/differences.py`, `tests/test_answer_differences.py` (new) -- `answer_differences`; unit-test every topic (attendance, days, cabin, meals as sets, hike, allergies), a guest present on one side only (attendance only), identical gives `[]`, normalisation first (a day kept for a non-coming guest does not count) -- FR-38, AD-9.
- [x] `wedding/rsvp/conflict.py`, `tests/test_rsvp_conflict.py` (new) -- `conflict_notice`: sender, date, time in Oslo time, one line per difference with the exact words of the matrix, empty list sentence, no note text, generic sentence for no stored answer or a non-guest actor; `change.py` `opened_at` with the table «Forged or missing field» and «Cookie draft present» parametrised -- FR-38, AD-9, AD-18.

**Execution (chunk 2: wiring and views, about 450 lines):**
- [x] `wedding/rsvp/views.py` (≤ +8 net), `wedding/rsvp/templates/rsvp/check.html`, `step.html`, `wedding/templates/wedding/components/notice.html`, `static/css/site.css` -- hidden `revisjon`, `opened_at` in `handle_step`, `_sending_notice` through `conflict_notice`, `_changed_text` deleted, warning notice with list, CSS -- FR-38, AD-9, UX-DR28, NFR-5.
- [x] `tests/test_rsvp_conflict_views.py` (new), `tests/test_rsvp_send_views.py`, `tests/test_form_components.py` if it pins `notice.html` -- real client flows: Marie and Arild in two clients: (1) cookie draft at n, Arild sends, Marie refused (303, nothing written, revision n+1, warning with «Arild», time and the cabin line, `autofocus`, no `role="alert"`), second send saved at n+2 with `sent_by_name` Marie; (2) opened form with `revisjon=n`, Arild sends, Marie's steps and send refused; (3) consent «Ja» at n gone from the cookie after the refusal and from a stale seeded draft; (4) forged `revisjon` ignored; (5) the notice component renders `items` and still no role when not `live`; update the 2.6c test for the warning -- FR-38, AD-9, AD-18, AD-20.

**Execution (chunk 3: process, about 250 lines):**
- [x] `docs/manual-test-plan.md` -- add MT-97 to MT-102 (Norwegian, result cells empty), see Verification -- FR-38, AD-9, UX-DR28.
- [ ] planning docs per Code Map -- dated 2026-11-27; reasons: hidden `revisjon` is the one hidden field because a GET may not write the cookie (AD-8); the list compares with the current stored answer (no history, AD-4), so on a cookie-less stale form it shows only what the guest's own steps changed; the warning is `warning` as the epics say, not the `error` of 2.6c.
- [x] `.docs/implementation-artifacts/deferred-work.md` -- mark done: 2.6c «what differs», 4.1 stale seed; update the 1.4a live-region entry (4.2 notice is server-rendered with focus, no in-page insertion; the NVDA/VoiceOver check remains for «Kopiert»); leave open «conflict notice must not name a send as cause» (first non-send bump, Story 4.4 or Epic 7) and the 4.4 generic text; `dashboard.access.admin_actor` stays open (no admin write in this story).
- [x] `README.md`, `sprint-status.yaml` (4-2 done), `.logs/rikke/issues.md` -- sync -- criterion 6.

**Acceptance Criteria:**
- Given Marie's draft started at revision n, when Arild sends and Marie presses «Send svaret», then nothing is written and Marie sees a warning with who sent, when and the lines that differ between her draft and the stored answer, replacing the 2.6c notice.
- Given that warning, when Marie reviews and sends again, then the second send is saved (revision n+2).
- Given a form opened before Arild's send and continued with no cookie draft, when Marie sends, then the refusal fires as above, because the opened revision travelled in the form.
- Given a draft or seeded form at a stale revision, then no consent «Ja» is carried and the notice says consent must be given again.
- Given the conflict check, when tests run, then they cover two members sending in sequence.
- Given a forged or missing `revisjon`, then the form behaves as in Story 4.1.

## Spec Change Log

| Date | Change | Reason |
|---|---|---|
| 2026-11-27 | List line format `{name}: du har {mine}, {sender} har sendt {sent}` became `{name}: du svarte {mine}, {sender} sendte {sent}` (golden line updated). | Review finding: «du har kommer ikke» and «du har overnatter ikke» are ungrammatical. |

## Review Triage Log

### 2026-11-27 — Review pass
- verdicts: 16 findings — high 0, medium 3, low 12, false 1, maybe-false 0
- findings:
  - `[medium]` `[patch]` `posted_revision` does `int()` on any ASCII digit string; over 4300 digits raises ValueError, so a forged `revisjon` gives a 500 (blind hunter, edge case hunter) — verified at `wedding/rsvp/change.py`; capped at 9 digits.
  - `[medium]` `[patch]` The difference lines read «du har kommer ikke, Arild har sendt kommer» and «du har overnatter ikke»: ungrammatical, and the same name appears twice when the sender is the row's guest (blind hunter) — verified in the MT-97 notice; reworded «du svarte …, Arild sendte …».
  - `[low]` `[patch]` A difference for a guest not in `members` gives a line starting with «: » (blind hunter, edge case hunter) — fallback name «en gjest».
  - `[medium]` `[patch]` No test that a first step posted with invalid data from a stale form keeps `revisjon` in the error page, which is the hole this story closes (verification gap).
  - `[low]` `[defer]` A form rendered from a cookie draft carries no `revisjon`; if the cookie is lost before the next POST the form is seeded at the newest revision (edge case hunter) — narrower than the 4.1 hole, needs the cookie to vanish mid-form; to deferred-work.
  - `[low]` `[reject]` `render_after_csrf_failure` echoes a posted `revisjon` for an unanswered household (verification gap, edge case hunter, blind hunter) — harmless: `opened_at` runs only for answered households and the next POST revalidates.
  - `[low]` `[reject]` A forged low `revisjon` gives a spurious conflict notice (edge case hunter) — it only affects the forger's own send; nothing is written.
  - `[low]` `[reject]` A cookie draft opened at an older revision keeps consent answers until a send is refused (edge case hunter) — the refused send clears them (AD-18), which is the AC; MT-100 shows «Ikke oppgitt» after the refusal.
  - `[false]` `[reject]` MT-97 to MT-102 unrun while the story is marked done (blind hunter, intent alignment) — run and recorded in step 10; sprint-status is set in the finalize commit.
  - `[low]` `[reject]` No screen-reader check of the focused notice (blind hunter) — it is not a live region by design (EXPERIENCE note); NVDA/VoiceOver stays an open item for Rikke on issues.md.
  - `[low]` `[reject]` AD-8 text still says «no hidden fields»; PRD and epics not updated (blind hunter) — the spine carries a dated «Changed» note with the reason; the epics AC is met as written.
  - `[low]` `[reject]` Notice("") as «no notice», NOT_SENT in conflict.py, two selector calls (blind hunter) — style only, consistent with the code around it.
  - `[low]` `[reject]` README paragraph keeps growing (blind hunter) — kept short; README restructuring belongs with the polish story.
  - `[low]` `[reject]` Notice wrapper markup has no regression test beyond the new component test (blind hunter) — the existing notice tests render through it and pass; MT-102 measured the layout.
  - `[low]` `[reject]` Cookie-less stale form lists only the guest's own edits (blind hunter) — known, documented in the spine (no revision history, AD-4).
  - `[low]` `[reject]` Intent alignment: tests exercise the Django client, not the browser (intent alignment) — MT-97 to MT-102 run in Edge with two sessions.

## Design Notes

- **Why a hidden field and not the cookie:** AD-8 forbids writing the cookie on a GET, and the revision must come from what the page showed (as `sum` does, Story 2.6c). The field exists only on a seeded form; a cookie draft already carries `rev`.
- **Why compare with the current answer only:** there is no history of earlier revisions (AD-4). When Marie's draft was seeded at n+1 (cookie-less first POST), the steps she did not touch already hold Arild's newer values, so the list shows what her own edits differ in; the sentence says who sent what and when either way.
- **Golden line:** `Filippa: du svarte hytte hele helgen, Arild sendte overnatter ikke`.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes.

**Manual checks (Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`) after `uv run manage.py migrate`, `uv run manage.py seed_testdata`, `uv run manage.py runserver`; two browser contexts A (Marie, `/test-marie000000000000/`) and B (Arild, `/test-arild000000000000/`); the implementer writes the rows with empty result cells; run `seed_testdata` again before each row):**
- MT-97 Utkast og nytt svar: A: `/svar/`, «Fortsett» på steg 1 til 4, på steg 3 sett Filippa til «Ja» (hytte), «Fortsett» på steg 4 til 6 (bekreft Arild på steg 5), «Se over svaret» (6 480 kr). B: `/svar/`, steg 3 Filippa «Nei», steg 4 til 6, «Send svaret» (4 980 kr). A: «Send svaret». Forvent redirect til `se-over/?sending=endret`, varselet «Obs: Svaret ble ikke sendt, fordi Arild sendte et svar for husstanden … etter at du begynte.» med linjen «Filippa: du svarte hytte hele helgen, Arild sendte overnatter ikke», fokus på varselet, `Household.revision` uendret av A (kommando: `uv run manage.py shell -c "from wedding.models import Household; print(Household.objects.get(guests__code='test-arild000000000000').revision)"`).
- MT-98 Se over og send på nytt: fortsett fra MT-97; A: «Send svaret» på siden. Forvent `/svar/sendt/`, revisjon én høyere, «Sendt av Marie».
- MT-99 Skjema åpnet før sendingen: A åpner `/svar/` og lar siden stå; B sender som i MT-97; A: «Fortsett» på steg 1, så steg 2 til 6 og «Send svaret». Forvent samme varsel og at ingenting er lagret før A sender på nytt.
- MT-100 Samtykke tas ikke med: som MT-97, men A svarer «Ja» til samtykke for Arild på steg 5 (med bekreftelse). Etter avvisningen viser «Se over svaret» samtykket som «Ikke oppgitt», og varselet sier at samtykke må gis på nytt.
- MT-101 Bare tastatur: A etter avvisningen: fokus står på varselet, Tab går til første lenke i skjemaet og videre til «Send svaret», Enter sender; fokuserte kontroller har `outline-style` `solid`.
- MT-102 Oppsett: varselet med liste ved 360 × 640 og 180 × 320, med og uten 20 px standardtekst (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`): `scrollWidth` ≤ `innerWidth`, listelinjene brytes innenfor arket, og «Send svaret» er minst 44 px høy.

## Auto Run Result

Status: done

**Summary:** A refused send after another member's send (Story 2.6c) now shows a warning notice with who sent, when, and one line per difference between the guest's draft and the stored answer («Filippa: du svarte hytte hele helgen, Arild sendte overnatter ikke»). A seeded form carries the revision it was opened at in a hidden `revisjon`, so a cookie-less first POST starts its draft there and the 2.6c check fires at send (the 4.1 deferred hole). Consent «Ja» and confirmations are cleared on a stale draft (AD-18). `wedding/rsvp/views.py` shrank by 8 lines.

**Files changed:**
- `wedding/rules/differences.py`, `wedding/rsvp/conflict.py`, `wedding/rsvp/change.py` — the difference rule, the notice text and the opened-revision handling.
- `wedding/rsvp/views.py`, `templates/rsvp/step.html`, `check.html`, `components/notice.html`, `static/css/site.css` — warning notice with list, hidden field.
- `tests/test_answer_differences.py`, `test_rsvp_conflict.py`, `test_rsvp_conflict_views.py` — rule, text and two-member view tests.
- `ARCHITECTURE-SPINE.md`, `DESIGN.md`, `EXPERIENCE.md`, `README.md`, `docs/manual-test-plan.md` (MT-97 to MT-102), `deferred-work.md`, `sprint-status.yaml` — dated notes and status.

**Review:** 4 rows patched (digit cap on `revisjon`, grammar of the difference lines, fallback name, error-path test), 1 deferred, 11 rejected with reasons in the triage log.

**Follow-up review recommendation:** false. No high found; the medium findings were patched and covered by tests, and the flow was re-run in Edge after the patches.

**Verification:** `uv run pytest` 1704 passed; ruff, ruff format and djlint clean; MT-97 to MT-102 run by Claude with Playwright 1.56.1 in Edge with two sessions (refusal, second send saved at revision 3, form opened before the send, consent not carried, keyboard, 360/180px at 16 and 20px).

**Residual risks:** the list on the cookie-less stale path shows only the guest's own edits because there is no revision history (AD-4); the second send is accepted with consent left unanswered (2.6c behaviour); the NVDA/VoiceOver check of the focused, non-live notice remains an open item for Rikke.
