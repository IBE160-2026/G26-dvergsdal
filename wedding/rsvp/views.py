"""The RSVP form's step handling, shared by every mount (Stories 2.1 to 2.5).

AD-7: one server-rendered form, each step a plain POST validated by the
server, then POST-redirect-GET to the next applicable step. AD-8: between
steps the answers live only in the draft cookie (wedding/rsvp/draft.py); no
session, no messages, no hidden fields and no database row (AD-1). The mount's
own view (guests/views.py for guests) resolves the actor, reads the settings,
checks the deadline and loads the members, then calls `handle_step`.

Step 1 «Hvem kommer?» (FR-12, FR-13, FR-14, FR-22, Story 2.1) and step 2
«Er alle som kommer, med hele helgen?» (FR-14, FR-70, Story 2.2) are built
here. Step 2 is one address: after «Nei» it shows a day group per coming
person at `#velg-dager`. Step 3 «Hvem skal overnatte på Hardingasete?» and
step 4 «Hvilke måltider skal vi bestille?» (FR-15, FR-16, FR-32, FR-33,
FR-70, FR-73, Story 2.3) show their prices first and the household total
from `household_total` (AD-12, NFR-2); `render_total` answers the running
total's `POST <base>/sum/?steg=<slug>` with the same fragment and writes
nothing. Step 5 «Allergier og matbehov» (FR-25 to FR-28, AD-18, UX-DR21,
Story 2.4) asks each coming person for allergies and a «Ja»/«Nei» to
storing them; it is done when nobody has a conflict, a missing confirmation
or a note that is too long, and it warns, without blocking, whose
information will not be saved. Nothing is stored before send. Step 6
«Hvem blir med på fjellturen fredag?» (FR-17, Story 2.5) asks «Ja», «Nei»
or «Kanskje» of each coming person present on Friday. The check page (FR-21,
FR-28, UX-DR23, Story 2.5) shows the answer from `check_parts`
(wedding/rsvp/summary.py) with an «Endre» link per part; a step opened with
`?fra=se-over` returns to the check page on «Fortsett» (`_continue_url`).
«Send svaret» (FR-74, AD-3, AD-9, Story 2.6a) posts `action=send` to the
check page, which calls `wedding.services.answers.send_answer`, deletes the
draft and redirects (303) to the sent page `<base>/sendt/`; that is the only
database write the form makes. Story 2.6b: the same send stores each
person's allergies only with their «Ja» and records each consent answer
(FR-26, FR-29, AD-18). Story 2.6c (AD-7, AD-9, AD-18, AD-20, NFR-1,
UX-DR52): the check page's form carries a one-time submission id
(`innsending`) and the total it showed (`sum`) as hidden fields; neither is an
answer. A repeated id lands on the sent page and writes nothing, also when
the draft is already gone. A send refused because the answer changed
meanwhile, the total changed or the consent text changed, or a send the
database fails, redirects (303) back to the check page with `?sending=<reason>`
and a focused notice; the draft is kept (after a changed answer or consent
text it loses its consent answers). Step 5 records the consent-text version
it showed (`cv`).
A later step opens only when every applicable step before it is done (`first_unfinished`).
Every draft write runs `normalise_answer` (FR-75), so a person who stops
coming loses their days, stay, meals and allergy answers, steps 2, 3 and 5
stay done only while their answers are complete, and a change in who is there on which days
reopens the steps after step 2.

Story 2.9 (FR-78, AD-8, UX-DR26): a guest who comes back in a new browser
session (no `rsvp_visit` cookie) with a usable draft gets the Draft offer
«Vil du fortsette der du slapp?» on any form address instead of the step.
«Ja, fortsett» (`action=resume`) goes to the first unfinished step, or the
check page; «Nei, begynn på nytt» (`action=restart`) deletes the draft and
goes to step 1. Both, and every POST to a step, set `rsvp_visit`, which
holds no answer. A draft whose household changed is cleaned by `read_draft`
and opens at step 1.
"""

import logging
import uuid
from dataclasses import replace
from datetime import datetime

from django.db import DatabaseError, IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import dateformat, timezone

from wedding.actors import Actor, GuestActor
from wedding.rsvp.draft import (
    Draft,
    delete_draft,
    has_visit,
    mark_visit,
    read_draft,
    write_draft,
)
from wedding.rsvp.forms import (
    ATTENDANCE_CHOICES,
    NO,
    PAY_NOTE,
    WHOLE_CHOICES,
    WHOLE_FIELD,
    YES,
    AllergiesForm,
    DaysForm,
    HikeForm,
    MealsForm,
    OvernightForm,
    WhoIsComingForm,
    allergy_field,
    allergy_none_field,
    attendance_field,
    confirm_field,
    consent_field,
    days_field,
    hike_field,
    meals_field,
    note_field,
    overnight_field,
    posted_respondent,
)
from wedding.rsvp.steps import CHECK, CHECK_SLUG, DAYS, KEY_BY_SLUG, STEPS, FormMount
from wedding.rsvp.summary import FROM_QUERY, check_parts
from wedding.rules.allergies import (
    CONFIRM,
    CONFLICT,
    EMPTY,
    NOTE_MAX,
    allergy_problems,
    not_saved,
)
from wedding.rules.answer import Answer, normalise_answer, present_days
from wedding.rules.days import (
    HIKE_ANSWERS,
    can_stay_overnight,
    day_error,
    joins_hike,
    offered_meals,
)
from wedding.rules.form_steps import (
    first_unfinished,
    form_steps,
    next_step,
    previous_step,
    step_position,
)
from wedding.rules.money import CABIN, household_total
from wedding.selectors import household_answer, submitted
from wedding.services.answers import send_answer
from wedding.services.consent import CONSENT_TEXT_VERSION
from wedding.services.exceptions import (
    ConsentTextChanged,
    NotAllowed,
    RevisionConflict,
    TotalChanged,
)

STEP_TEMPLATE = "rsvp/step.html"
OFFER_TEMPLATE = "rsvp/draft_offer.html"
# FR-78, UX-DR26 (Story 2.9): the Draft offer's two answers.
RESUME = "resume"
RESTART = "restart"
CHECK_TEMPLATE = "rsvp/check.html"
TOTAL_TEMPLATE = "rsvp/includes/total.html"
SWITCH = "switch"
# FR-22: the query that asks a step to show its errors after an invalid «Fortsett».
ERRORS_QUERY = "feil"
# AD-7, Story 2.2: where step 2's day groups start, after «Nei».
DAY_GROUPS_ANCHOR = "velg-dager"
# FR-75, AD-7 (Story 2.3): the steps whose questions follow from who is there
# on which days, so a change in that sends the guest through them again.
REOPENED_ON_CHANGE = ("overnight", "meals", "allergies", "hike")
# FR-33, AD-7: the steps with prices, which show the running total.
PAID_STEPS = ("overnight", "meals")
Members = list[tuple[int, str]]
Prices = dict[str, int]
# AD-20, AD-7 (Story 2.6c): the check page form's hidden one-time submission
# id and the total it showed.
SUBMISSION_FIELD = "innsending"
TOTAL_FIELD = "sum"
# UX-DR52 (Story 2.6c): the query that brings a refused or failed send back
# to the check page, and its reasons.
SENDING_QUERY = "sending"
SEND_FAILED = "feilet"
SEND_CHANGED = "endret"
SEND_TOTAL = "sum"
SEND_CONSENT = "samtykke"
NOT_SENT = "Svaret ble ikke sendt, fordi "
TRY_AGAIN = " Ingenting er tapt: alt du fylte ut, står her fortsatt. Prøv igjen med «Send svaret»."

logger = logging.getLogger(__name__)


def _member_ids(members: Members) -> set[int]:
    """AD-8: the household's guest ids, the only ids a draft or a POST may name."""
    return {guest_id for guest_id, _ in members}


def _owner(actor: Actor, members: Members) -> int:
    """FR-12: the default respondent, the link's owner (the first member without one)."""
    if isinstance(actor, GuestActor):
        return actor.guest.id
    return members[0][0]


def _attendance(draft: Draft, members: Members) -> dict[int, bool]:
    """FR-13: each member's «Kommer»; a member the draft does not know (added after
    step 1) counts as coming, as everyone does before step 1."""
    return {guest_id: draft.att.get(guest_id, True) for guest_id, _ in members}


def _coming(draft: Draft, members: Members) -> Members:
    """FR-14: the coming members as (id, name), in household order."""
    attendance = _attendance(draft, members)
    return [(guest_id, name) for guest_id, name in members if attendance[guest_id]]


def _steps(draft: Draft | None, members: Members) -> tuple[str, ...]:
    """UX-DR19, FR-17: the applicable steps; all of them until step 1 is completed.

    After «Nei» on step 2 each member counts with their chosen days; an
    unchosen or refused set, or no «Nei», counts as the whole weekend.
    """
    if draft is None or "who" not in draft.done:
        return form_steps(None)
    attendance = _attendance(draft, members)
    days = [draft.days.get(guest_id) for guest_id, _ in members] if draft.whole is False else None
    return form_steps([attendance[guest_id] for guest_id, _ in members], days)


def _answer(draft: Draft, members: Members) -> Answer:
    """AD-2: the draft's answer as the rules take it, with every member's attendance."""
    return Answer(
        _attendance(draft, members),
        draft.whole,
        draft.days,
        draft.night,
        draft.meals,
        draft.alg,
        draft.cons,
        frozenset(draft.conf),
        draft.hike,
    )


def _present(draft: Draft | None, members: Members) -> dict | None:
    """FR-75, UX-DR19: who is there on which days, or None before step 1 is completed."""
    if draft is None or "who" not in draft.done:
        return None
    return present_days(_answer(draft, members))


def _total(draft: Draft, members: Members, prices: Prices) -> int:
    """FR-33, AD-12, NFR-2: the household total of the draft, from `household_total`."""
    return household_total(_answer(draft, members), prices)


def _days_complete(draft: Draft, members: Members) -> bool:
    """FR-14, FR-70: step 2 is answered: «Ja», or «Nei» with an allowed set for everyone coming."""
    if draft.whole is None:
        return False
    return draft.whole or all(
        day_error(draft.days.get(guest_id, ())) is None for guest_id, _ in _coming(draft, members)
    )


def _allergy_problems(draft: Draft, guest_id: int) -> tuple[str, ...]:
    """FR-25, FR-27: `allergy_problems` for one member of the draft."""
    return allergy_problems(
        draft.alg.get(guest_id, EMPTY),
        draft.cons.get(guest_id),
        guest_id in draft.conf,
        guest_id == draft.resp,
    )


def _hiking(draft: Draft, members: Members) -> Members:
    """FR-17: the coming members present on Friday as (id, name), in household order."""
    present = present_days(_answer(draft, members))
    return [
        (guest_id, name)
        for guest_id, name in members
        if guest_id in present and joins_hike(present[guest_id])
    ]


def _settled(draft: Draft, members: Members) -> Draft:
    """FR-75, AD-8: the draft as written: normalised, steps 2, 3 and 5 done only when complete.

    Runs on every draft write, so days, stays and meals never outlive their
    person's «Kommer» or the days that allowed them, a new comer or a removed
    day sends the guest back to step 2, and step 3 stays done only while
    every coming member has answered «Ja» or «Nei». Step 5 stays done only
    while no coming member has an allergy problem or a note that was too long
    (Story 2.4), so a «Bytt» that leaves a confirmation missing reopens it.
    Step 6 stays done only while every member present on Friday has a hike
    answer (Story 2.5, FR-17).
    """
    answer = normalise_answer(_answer(draft, members))
    draft.whole, draft.days = answer.whole, dict(answer.days)
    draft.night, draft.meals = dict(answer.night), dict(answer.meals)
    draft.alg, draft.cons = dict(answer.allergies), dict(answer.consent)
    draft.conf = [guest_id for guest_id in draft.conf if guest_id in answer.confirmed]
    draft.hike = dict(answer.hike)
    if "days" in draft.done and not _days_complete(draft, members):
        draft.done.remove("days")
    coming = _coming(draft, members)
    if "overnight" in draft.done and any(guest_id not in draft.night for guest_id, _ in coming):
        draft.done.remove("overnight")
    coming_ids = {guest_id for guest_id, _ in coming}
    draft.long = [guest_id for guest_id in draft.long if guest_id in coming_ids]
    if "allergies" in draft.done and (
        draft.long or any(_allergy_problems(draft, guest_id) for guest_id in coming_ids)
    ):
        draft.done.remove("allergies")
    hiking = _hiking(draft, members)
    if "hike" in draft.done and any(guest_id not in draft.hike for guest_id, _ in hiking):
        draft.done.remove("hike")
    return draft


def _merged(draft: Draft | None, actor: Actor, members: Members) -> Draft:
    """AD-8: the existing draft, or a new one started now at the household's revision."""
    if draft is not None:
        return draft
    revision = actor.household.revision if isinstance(actor, GuestActor) else 0
    return Draft.new(revision=revision, respondent=_owner(actor, members), now=timezone.now())


def _from_check(request: HttpRequest) -> bool:
    """UX-DR23, AD-7: whether the step was opened from the check page's «Endre» link."""
    return request.GET.get(FROM_QUERY) == CHECK_SLUG


def _keep_from(request: HttpRequest, url: str, query: str = "") -> str:
    """UX-DR23: `url` with `query` and, when the step came from the check page, `fra`.

    A `#fragment` in `url` stays last.
    """
    path, hash_mark, fragment = url.partition("#")
    back = f"{FROM_QUERY}={CHECK_SLUG}" if _from_check(request) else ""
    if parts := [part for part in (query, back) if part]:
        path = f"{path}?{'&'.join(parts)}"
    return f"{path}{hash_mark}{fragment}"


def _gate_url(request: HttpRequest, mount: FormMount, key: str | None) -> str:
    """AD-7, UX-DR23: a gate redirect to step `key`, keeping `fra`; the check page never gets it."""
    url = mount.url(key)
    return url if key is None else _keep_from(request, url)


def _error_url(request: HttpRequest, url: str) -> str:
    """FR-22, UX-DR23: a step's error address `?feil=1`, keeping `fra`."""
    return _keep_from(request, url, f"{ERRORS_QUERY}=1")


def _continue_url(
    request: HttpRequest, mount: FormMount, members: Members, draft: Draft, step: str
) -> str:
    """AD-7, UX-DR23: where a valid «Fortsett» on `step` goes.

    The next applicable step; from the check page (`?fra=se-over`), the first
    unfinished step, or the check page when every step is done. A change that
    reopens later steps (`REOPENED_ON_CHANGE`, cleared after this) is caught
    by the check page's own gate.
    """
    steps = _steps(draft, members)
    if _from_check(request):
        return mount.url(first_unfinished(steps, draft.done, None))
    return mount.url(next_step(steps, step))


def _see_other(url: str) -> HttpResponse:
    """FR-22, AD-7: 303 See Other to a step's error page, so its GET never resubmits."""
    response = HttpResponseRedirect(url)
    response.status_code = 303
    return response


def _who_fields(
    members: Members, checked: dict[int, bool], show_errors: bool
) -> tuple[dict[str, object], list[dict[str, str]]]:
    """FR-13, FR-22: step 1's groups, and its error-summary links.

    One group per member with `checked` pre-selected; with `show_errors`, an
    error line for each member with no answer in `checked`.
    """
    rows, errors = [], []
    for guest_id, name in members:
        field = attendance_field(guest_id)
        coming = checked.get(guest_id)
        error = WhoIsComingForm.error_text(name) if show_errors and coming is None else ""
        rows.append(
            {
                "name": name,
                "field": field,
                "value": "" if coming is None else (YES if coming else NO),
                "error": error,
            }
        )
        if error:
            errors.append({"target": f"{field}_{YES}", "text": WhoIsComingForm.summary_text(name)})
    return {"rows": rows, "choices": ATTENDANCE_CHOICES}, errors


def _days_fields(
    coming: Members,
    *,
    whole: bool | None,
    days: dict[int, list[str]],
    show_groups: bool,
    show_errors: bool,
) -> tuple[dict[str, object], list[dict[str, str]]]:
    """FR-14, FR-22, FR-70: step 2's day list, «Ja»/«Nei» and day groups, and its errors.

    `show_groups` shows one group of day checkboxes per coming member, ticked
    from `days`. With `show_errors`, an unanswered «Ja»/«Nei» and every coming
    member whose set `day_error` refuses get an error line.
    """
    whole_error = DaysForm.WHOLE_ERROR if show_errors and whole is None else ""
    errors = (
        [{"target": f"{WHOLE_FIELD}_{YES}", "text": DaysForm.WHOLE_SUMMARY}] if whole_error else []
    )
    groups = []
    for guest_id, name in coming if show_groups else ():
        field = days_field(guest_id)
        chosen = days.get(guest_id, [])
        problem = day_error(chosen) if show_errors and whole is False else None
        error = DaysForm.day_error_text(name, problem) if problem else ""
        boxes = [
            {
                "id": f"{field}_{day.key}",
                "value": day.key,
                "label": day.label,
                "checked": day.key in chosen,
            }
            for day in DAYS.values()
        ]
        groups.append({"name": name, "field": field, "error": error, "boxes": boxes})
        if error:
            errors.append({"target": boxes[0]["id"], "text": DaysForm.day_summary_text(name)})
    fields = {
        "day_list": list(DAYS.values()),
        "whole_field": WHOLE_FIELD,
        "whole_value": "" if whole is None else (YES if whole else NO),
        "whole_choices": WHOLE_CHOICES,
        "whole_error": whole_error,
        "groups_anchor": DAY_GROUPS_ANCHOR,
        "show_groups": show_groups,
        "groups": groups,
    }
    return fields, errors


def _overnight_fields(
    coming: Members,
    *,
    present: dict,
    night: dict[int, bool],
    prices: Prices,
    show_errors: bool,
) -> tuple[dict[str, object], list[dict[str, str]]]:
    """FR-16, FR-22, FR-32, FR-70: step 3's lead, price, groups and errors.

    One group per coming member with «Ja»/«Nei» checked from `night`. With
    `show_errors`, each member with no answer gets an error line: «Velg «Ja»
    eller «Nei» …» when their days in `present` allow a stay, and the reason
    why not otherwise (a refused «Ja» is never saved, so it shows here).
    """
    groups, errors = [], []
    for guest_id, name in coming:
        field = overnight_field(guest_id)
        stays = night.get(guest_id)
        error = ""
        if show_errors and stays is None:
            days = present[guest_id]
            if can_stay_overnight(days):
                error = OvernightForm.error_text(name)
            else:
                error = OvernightForm.blocked_text(name, sorted(days))
        groups.append(
            {
                "name": name,
                "field": field,
                "value": "" if stays is None else (YES if stays else NO),
                "error": error,
            }
        )
        if error:
            errors.append({"target": f"{field}_{YES}", "text": OvernightForm.summary_text(name)})
    fields = {
        "lead": OvernightForm.lead(),
        "price_label": OvernightForm.PRICE_LABEL,
        "price_unit": OvernightForm.PRICE_UNIT,
        "cabin_price": prices[CABIN],
        "pay_note": PAY_NOTE,
        "choices": OvernightForm.choices(prices[CABIN]),
        "groups": groups,
    }
    return fields, errors


def _meal_groups(coming: Members, present: dict) -> list[tuple[int, str, tuple[str, ...]]]:
    """FR-15, FR-73: (id, name, offered meal keys) for each coming member offered a meal."""
    shown = []
    for guest_id, name in coming:
        if offered := offered_meals(present[guest_id]):
            shown.append((guest_id, name, offered))
    return shown


def _meals_fields(
    coming: Members, *, present: dict, meals: dict[int, list[str]], prices: Prices
) -> dict[str, object]:
    """FR-15, FR-32, FR-73: step 4's note, hint and one group per member offered a meal.

    Each group has a checkbox per offered meal with its price, ticked from
    `meals`. Saturday's lunch and dinner are never asked about.
    """
    groups = []
    for guest_id, name, offered in _meal_groups(coming, present):
        field = meals_field(guest_id)
        chosen = meals.get(guest_id, [])
        boxes = [
            {
                "id": f"{field}_{meal}",
                "value": meal,
                "label": MealsForm.meal_label(meal, prices[meal]),
                "checked": meal in chosen,
            }
            for meal in offered
        ]
        groups.append({"name": name, "field": field, "boxes": boxes})
    return {"pay_note": PAY_NOTE, "hint": MealsForm.HINT, "groups": groups}


def _allergy_fields(
    coming: Members,
    *,
    respondent: int,
    draft: Draft,
    show_errors: bool,
) -> tuple[dict[str, object], list[dict[str, str]]]:
    """FR-22, FR-25 to FR-28, UX-DR21: step 5's lead, groups, warning and errors.

    One group per coming member, filled from `draft` (after a CSRF failure,
    a copy with the posted values merged in). The confirmation shows for
    everyone but the `respondent`. With `show_errors`, each member's
    problems from `allergy_problems` and a note that was too long get their
    error lines, and the summary links them in page order. The FR-28
    warning names whoever has information but no «Ja».
    """
    groups, errors = [], []
    for guest_id, name in coming:
        entry = draft.alg.get(guest_id, EMPTY)
        consent = draft.cons.get(guest_id)
        problems = _allergy_problems(draft, guest_id) if show_errors else ()
        none_id = allergy_none_field(guest_id)
        note_id = note_field(guest_id)
        confirm_id = confirm_field(guest_id)
        conflict = AllergiesForm.conflict_text(name) if CONFLICT in problems else ""
        long = AllergiesForm.long_text(name) if show_errors and guest_id in draft.long else ""
        confirm = AllergiesForm.confirm_text(name) if CONFIRM in problems else ""
        if conflict:
            errors.append({"target": none_id, "text": AllergiesForm.conflict_summary(name)})
        if long:
            errors.append({"target": note_id, "text": AllergiesForm.long_summary(name)})
        if confirm:
            errors.append({"target": confirm_id, "text": AllergiesForm.confirm_summary(name)})
        field = allergy_field(guest_id)
        groups.append(
            {
                "name": name,
                "none_field": none_id,
                "none": entry.none,
                "field": field,
                "boxes": [
                    {
                        "id": f"{field}_{key}",
                        "value": key,
                        "label": label,
                        "checked": key in entry.cats,
                    }
                    for key, label in AllergiesForm.categories()
                ],
                "note_field": note_id,
                "note": entry.note,
                "note_label": AllergiesForm.note_label(name),
                "consent_field": consent_field(guest_id),
                "consent_legend": AllergiesForm.consent_legend(name),
                "consent_value": "" if consent is None else (YES if consent else NO),
                "confirm_field": confirm_id if guest_id != respondent else "",
                "confirm_label": AllergiesForm.confirm_label(name),
                "confirmed": guest_id in draft.conf,
                "conflict": conflict,
                "long": long,
                "confirm_error": confirm,
            }
        )
    unsaved = set(not_saved([guest_id for guest_id, _ in coming], draft.alg, draft.cons))
    warning_names = [name for guest_id, name in coming if guest_id in unsaved]
    fields = {
        "lead": AllergiesForm.LEAD,
        "warning": AllergiesForm.warning_text(warning_names) if warning_names else "",
        "none_label": AllergiesForm.NONE_LABEL,
        "or_line": AllergiesForm.OR_LINE,
        "note_hint": AllergiesForm.NOTE_HINT,
        "note_max": NOTE_MAX,
        "consent_choices": AllergiesForm.CONSENT_CHOICES,
        "groups": groups,
    }
    return fields, errors


def _back_url(request: HttpRequest, mount: FormMount, previous: str | None) -> str:
    """UX-DR18, UX-DR23: «Tilbake»: the check page when opened from it, else the step before."""
    if _from_check(request):
        return mount.url(CHECK)
    return mount.exit_url if previous is None else mount.url(previous)


def _render_step(
    request: HttpRequest,
    *,
    key: str,
    steps: tuple[str, ...],
    mount: FormMount,
    members: Members,
    respondent: int,
    page_context: dict[str, object],
    fields: dict[str, object] | None = None,
    errors: list[dict[str, str]] | None = None,
    total: int | None = None,
    csrf_failed: bool = False,
    status: int = 200,
) -> HttpResponse:
    """FR-12, FR-14, FR-22, FR-33, UX-DR16, UX-DR18, UX-DR19: one step's page.

    The question from the registry as the `h1`, the progress line, the
    respondent line and «Tilbake». `fields` is the step's own context
    (`_who_fields`, `_days_fields`, `_overnight_fields`, `_meals_fields`,
    `_allergy_fields`, `_hike_fields`), shown through the registry's
    `fields_template`; with fields, the page also has «Fortsett». `errors`
    are the error summary's links. `total`, on the paid steps, is the
    household total from `household_total`, shown with the running total's
    address.
    """
    number, count = step_position(steps, key)
    step = STEPS[key]
    previous = previous_step(steps, key)
    context = (
        page_context
        | (fields or {})
        | {
            "key": key,
            "has_fields": fields is not None,
            "fields_template": step.fields_template if fields is not None else "",
            "total": total,
            "total_url": mount.total_url(key) if total is not None else "",
            "heading": step.question,
            "progress": f"Steg {number} av {count}: {step.name}",
            "respondent_id": respondent,
            "respondent_name": dict(members)[respondent],
            "members": [{"id": guest_id, "name": name} for guest_id, name in members],
            "back_url": _back_url(request, mount, previous),
            "errors": errors or [],
            "csrf_failed": csrf_failed,
        }
    )
    return render(request, STEP_TEMPLATE, context, status=status)


def _phones(contacts: list[dict[str, str]]) -> str:
    """UX-DR52, FR-6 (Story 2.6c): « Går det fortsatt ikke, ring …» with the
    couple's phones, or nothing without contacts."""
    calls = [f"{contact['name']} på {contact['phone']}" for contact in contacts]
    if not calls:
        return ""
    return f" Går det fortsatt ikke, ring {' eller '.join(calls)}."


def _changed_text(actor: Actor) -> str:
    """AD-9 (Story 2.6c): why a send was refused after the household's answer
    changed: who sent it and when (Oslo time, as on the sent page)."""
    sent = household_answer(actor.household) if isinstance(actor, GuestActor) else None
    if sent is None:
        reason = "svaret for husstanden er endret etter at du begynte."
    else:
        local = timezone.localtime(sent.sent_at)
        reason = (
            f"{sent.sent_by_name} sendte et svar for husstanden "
            f"{dateformat.format(local, 'l j. F Y')} kl. {dateformat.format(local, 'H:i')} "
            "etter at du begynte."
        )
    return (
        NOT_SENT
        + reason
        + " Se over svaret og send det på nytt. Samtykke til å lagre allergier må gis på nytt."
    )


def _sending_notice(request: HttpRequest, actor: Actor, contacts: list) -> str:
    """UX-DR52, AD-7, AD-9, AD-18 (Story 2.6c): the notice for `?sending=<reason>`,
    or "" for no or an unknown reason."""
    reason = request.GET.get(SENDING_QUERY)
    if reason == SEND_FAILED:
        return NOT_SENT + "noe gikk galt da det skulle lagres." + TRY_AGAIN + _phones(contacts)
    if reason == SEND_CHANGED:
        return _changed_text(actor)
    if reason == SEND_TOTAL:
        return NOT_SENT + "summen har endret seg. Se over den nye summen og send svaret på nytt."
    if reason == SEND_CONSENT:
        return (
            NOT_SENT + "teksten om lagring av allergier er endret etter at du svarte. Les den nye "
            "teksten under «Allergier og matbehov» og svar på nytt før du sender."
        )
    return ""


def _submission(request: HttpRequest) -> uuid.UUID | None:
    """AD-20 (Story 2.6c): the posted one-time submission id, or None when it is not a UUID."""
    try:
        return uuid.UUID(request.POST.get(SUBMISSION_FIELD, ""))
    except ValueError:
        return None


def _shown_total(request: HttpRequest) -> int | None:
    """AD-7 (Story 2.6c): the posted total the check page showed, or None unless whole kroner."""
    value = request.POST.get(TOTAL_FIELD, "")
    return int(value) if value.isascii() and value.isdigit() else None


def _log_failed(actor: Actor, error: Exception) -> None:
    """NFR-3, UX-DR52 (Story 2.6c): a failed send, with the household id and the class only."""
    household = actor.household.pk if isinstance(actor, GuestActor) else None
    logger.error("Sending the answer failed (%s) for household %s", type(error).__name__, household)


def _send(
    request: HttpRequest, *, actor: Actor, mount: FormMount, members: Members, draft: Draft
) -> tuple[HttpResponse, Draft | None]:
    """FR-74, AD-7, AD-9, AD-18, AD-20, NFR-1, UX-DR52 (Stories 2.6a, 2.6c): «Send svaret».

    Without a valid submission id or total, back to the check page (303),
    nothing written. Sent, or a repeat of a send: 303 to the sent page and
    the draft deleted. `TotalChanged`: back with `?sending=sum`, the draft
    unchanged. `RevisionConflict`: the draft moves to the current revision
    and loses its consent answers and confirmations (AD-18, no «Ja» across a
    revision change), back with `?sending=endret`. `ConsentTextChanged`: the
    consent answers, confirmations and seen version are cleared, back with
    `?sending=samtykke`. A database failure is logged with its class name
    only, back with `?sending=feilet`, the draft untouched; an
    `IntegrityError` after the same id was written by a racing request is a
    repeat. `NotAllowed` (another household's id) goes back to the check page. `DeadlinePassed`
    is left to the mount's view (FR-41).
    """
    check_url = mount.url(CHECK)
    submission = _submission(request)
    shown_total = _shown_total(request)
    if submission is None or shown_total is None:
        return _see_other(check_url), None
    try:
        send_answer(
            actor,
            household=actor.household if isinstance(actor, GuestActor) else None,
            respondent=draft.resp,
            answer=_answer(draft, members),
            now=timezone.now(),
            submission=submission,
            revision=draft.rev,
            shown_total=shown_total,
            consent_version=draft.cv,
        )
    except NotAllowed:
        # AD-3, AD-20: a submission id written for another household.
        return _see_other(check_url), None
    except TotalChanged:
        return _see_other(f"{check_url}?{SENDING_QUERY}={SEND_TOTAL}"), None
    except RevisionConflict as conflict:
        new = replace(draft, rev=conflict.revision, cons={}, conf=[])
        return _see_other(f"{check_url}?{SENDING_QUERY}={SEND_CHANGED}"), new
    except ConsentTextChanged:
        new = replace(draft, cons={}, conf=[], cv=None)
        return _see_other(f"{check_url}?{SENDING_QUERY}={SEND_CONSENT}"), new
    except IntegrityError as error:
        # AD-20, NFR-1: the same id raced and the other request wrote it.
        if isinstance(actor, GuestActor) and submitted(actor.household, submission):
            response = _see_other(mount.sent_url())
            delete_draft(response, mount)
            return response, None
        _log_failed(actor, error)
        return _see_other(f"{check_url}?{SENDING_QUERY}={SEND_FAILED}"), None
    except DatabaseError as error:
        _log_failed(actor, error)
        return _see_other(f"{check_url}?{SENDING_QUERY}={SEND_FAILED}"), None
    response = _see_other(mount.sent_url())
    delete_draft(response, mount)
    return response, None


def _render_check(
    request: HttpRequest,
    *,
    actor: Actor,
    steps: tuple[str, ...],
    mount: FormMount,
    members: Members,
    draft: Draft,
    prices: Prices,
    page_context: dict,
    csrf_failed: bool = False,
    status: int = 200,
) -> HttpResponse:
    """FR-21, FR-28, FR-33, UX-DR23: the check page.

    One block per applicable step from `check_parts`, the household total
    from `household_total` (AD-12), «Send svaret» and «Tilbake» to the last
    applicable step. `csrf_failed` (UX-DR52, Story 2.6a) adds the focused
    error notice, with `status` 403. Story 2.6c (AD-7, AD-20, UX-DR52): a
    fresh submission id per render and the rendered total as hidden fields,
    the focused notice for `?sending=<reason>`, and the hidden notice the
    script shows when the connection breaks.
    """
    contacts = page_context.get("contacts") or []
    context = page_context | {
        "parts": check_parts(
            _answer(draft, members),
            members=members,
            respondent=draft.resp,
            steps=steps,
            mount=mount,
        ),
        "total": _total(draft, members, prices),
        "back_url": mount.url(steps[-1]),
        "csrf_failed": csrf_failed,
        "submission": uuid.uuid4(),
        "sending_notice": _sending_notice(request, actor, contacts),
        "send_failed_text": NOT_SENT + "forbindelsen ble brutt." + TRY_AGAIN + _phones(contacts),
    }
    return render(request, CHECK_TEMPLATE, context, status=status)


def _switch_respondent(request: HttpRequest, draft: Draft, members: Members) -> Draft:
    """FR-12, UX-DR18: the posted respondent replaces the current one when they are a member."""
    respondent = posted_respondent(request.POST, _member_ids(members))
    if respondent is not None:
        draft.resp = respondent
    return draft


def _switched(request: HttpRequest, draft: Draft, members: Members) -> Draft:
    """FR-12, UX-DR18: «Velg» in «Bytt» on step 1.

    The posted respondent replaces the current one when they are a member;
    every valid posted attendance is kept in the draft without validating the
    rest and without marking the step done, so nothing typed is lost.
    """
    draft = _switch_respondent(request, draft, members)
    posted = WhoIsComingForm(members, data=request.POST).posted_attendance()
    draft.att = draft.att | posted
    return draft


def _who_is_coming(
    request: HttpRequest,
    *,
    actor: Actor,
    mount: FormMount,
    members: Members,
    draft: Draft | None,
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """FR-12, FR-13, FR-14, FR-22: step 1. The response and the draft to write, if any."""
    respondent = draft.resp if draft is not None else _owner(actor, members)
    if request.method != "POST":
        checked = draft.att if draft is not None else {}
        fields, errors = _who_fields(members, checked, ERRORS_QUERY in request.GET)
        response = _render_step(
            request,
            key="who",
            steps=_steps(draft, members),
            mount=mount,
            members=members,
            respondent=respondent,
            page_context=page_context,
            fields=fields,
            errors=errors,
        )
        return response, None
    if request.POST.get("action") == SWITCH:
        new = _switched(request, _merged(draft, actor, members), members)
        return HttpResponseRedirect(_keep_from(request, mount.url("who"))), new
    form = WhoIsComingForm(members, data=request.POST)
    if not form.is_valid():
        # FR-22, AD-7: POST-redirect-GET for errors too, so Back to the error
        # page never asks to resubmit. The valid choices and respondent are kept
        # in the draft, step 1 stays not done, and the GET shows the errors.
        new = _switched(request, _merged(draft, actor, members), members)
        return _see_other(_error_url(request, mount.url("who"))), new
    new = _switch_respondent(request, _merged(draft, actor, members), members)
    new.att = form.attendance()
    if "who" not in new.done:
        new.done.append("who")
    new = _settled(new, members)
    return HttpResponseRedirect(_continue_url(request, mount, members, new, "who")), new


def _days_switched(request: HttpRequest, draft: Draft, members: Members) -> Draft:
    """FR-12, FR-14, UX-DR18: «Velg» in «Bytt» on step 2.

    Keeps the posted respondent, the posted «Ja»/«Nei» and, when the day
    groups were on the page, the valid posted days, without validating them.
    """
    draft = _switch_respondent(request, draft, members)
    form = DaysForm(_coming(draft, members), data=request.POST)
    groups_shown = draft.whole is False or form.has_posted_days()
    posted_whole = form.posted_whole()
    if posted_whole is not None:
        draft.whole = posted_whole
    if groups_shown:
        draft.days = form.posted_days()
    return draft


def _which_days(
    request: HttpRequest,
    *,
    mount: FormMount,
    members: Members,
    draft: Draft,
    steps: tuple[str, ...],
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """FR-14, FR-22, FR-70, UX-DR16, UX-DR19: step 2. The response and the draft to write.

    GET shows the question, the three days and «Ja»/«Nei», and the day groups
    once «Nei» is saved. «Ja» completes the step. «Nei» without day groups on
    the page saves «Nei» and reveals them at `#velg-dager` (not an error).
    «Nei» with days completes the step when every coming person's set is
    allowed; otherwise the posted days are saved and `?feil=1` shows the
    errors, computed from the draft (PRG, as on step 1).
    """
    url = mount.url("days")
    coming = _coming(draft, members)
    if request.method != "POST":
        fields, errors = _days_fields(
            coming,
            whole=draft.whole,
            days=draft.days,
            show_groups=draft.whole is False,
            show_errors=ERRORS_QUERY in request.GET,
        )
        response = _render_step(
            request,
            key="days",
            steps=steps,
            mount=mount,
            members=members,
            respondent=draft.resp,
            page_context=page_context,
            fields=fields,
            errors=errors,
        )
        return response, None
    if request.POST.get("action") == SWITCH:
        return HttpResponseRedirect(_keep_from(request, url)), _days_switched(
            request, draft, members
        )
    form = DaysForm(coming, data=request.POST)
    whole = form.posted_whole()
    new = _switch_respondent(request, draft, members)
    if whole is None:
        return _see_other(_error_url(request, url)), new
    if whole is False and new.whole is not False and not form.has_posted_days():
        new.whole, new.days = False, {}
        return HttpResponseRedirect(_keep_from(request, f"{url}#{DAY_GROUPS_ANCHOR}")), new
    new.whole = whole
    new.days = {} if whole else form.posted_days()
    if "days" not in new.done:
        new.done.append("days")
    new = _settled(new, members)
    if "days" not in new.done:
        return _see_other(_error_url(request, url)), new
    return HttpResponseRedirect(_continue_url(request, mount, members, new, "days")), new


def _with_posted(
    request: HttpRequest,
    draft: Draft,
    members: Members,
    step: str,
    *,
    keep_long: bool = False,
) -> Draft:
    """FR-15 to FR-17, FR-25: a copy of `draft` with step 3's to 6's posted choices merged in.

    Nothing is validated: on step 3 each coming member's posted «Ja» or «Nei»
    replaces theirs (a «Ja» their days do not allow is removed when the draft
    is normalised, FR-70); on step 4 each member shown a meal group gets
    exactly the offered meals that were ticked; on step 5 each coming
    member's entry, consent and confirmation are replaced by the posted ones,
    and `long` names those whose note was too long (that note is not kept
    unless `keep_long`, which only the CSRF re-render uses, since it writes
    nothing); on step 6 each member present on Friday gets their posted hike
    answer. The draft itself is not changed, so the running total and the
    CSRF re-render can use the copy.
    """
    coming = _coming(draft, members)
    if step == "hike":
        posted = HikeForm(_hiking(draft, members), data=request.POST).posted_hike()
        return replace(draft, done=list(draft.done), hike=draft.hike | posted)
    if step == "allergies":
        form = AllergiesForm(coming, data=request.POST)
        posted = posted_respondent(request.POST, _member_ids(members))
        respondent = draft.resp if posted is None else posted
        ids = {guest_id for guest_id, _ in coming}
        alg = {guest_id: entry for guest_id, entry in draft.alg.items() if guest_id not in ids}
        cons = {guest_id: given for guest_id, given in draft.cons.items() if guest_id not in ids}
        conf = [guest_id for guest_id in draft.conf if guest_id not in ids]
        return replace(
            draft,
            done=list(draft.done),
            alg=alg | form.posted_entries(None if keep_long else draft.alg),
            cons=cons | form.posted_consent(),
            conf=conf + form.posted_confirmed(respondent),
            long=form.long_notes(),
        )
    if step == "overnight":
        posted = OvernightForm(coming, data=request.POST).posted_night()
        return replace(draft, done=list(draft.done), night=draft.night | posted)
    shown = _meal_groups(coming, present_days(_answer(draft, members)))
    posted = MealsForm(shown, data=request.POST).posted_meals()
    kept = {guest_id: meals for guest_id, meals in draft.meals.items() if guest_id not in posted}
    chosen = {guest_id: meals for guest_id, meals in posted.items() if meals}
    return replace(draft, done=list(draft.done), meals=kept | chosen)


def _paid_step(
    request: HttpRequest,
    *,
    step: str,
    mount: FormMount,
    members: Members,
    draft: Draft,
    steps: tuple[str, ...],
    prices: Prices,
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """FR-15, FR-16, FR-22, FR-32, FR-33, FR-70, FR-73: step 3 or 4. The response and the draft.

    GET shows the prices before any choice, a group per coming member (on
    step 4 only those offered a meal) and the household total. «Fortsett»
    saves the valid posted choices; step 3 is done when every coming member
    has «Ja» or «Nei» and no «Ja» was refused, otherwise `?feil=1` shows the
    errors, computed from the draft (PRG). Step 4 has no error: no meal is a
    fine answer. «Velg» keeps the posted choices without marking the step done.
    """
    url = mount.url(step)
    if request.method != "POST":
        coming = _coming(draft, members)
        present = present_days(_answer(draft, members))
        if step == "overnight":
            fields, errors = _overnight_fields(
                coming,
                present=present,
                night=draft.night,
                prices=prices,
                show_errors=ERRORS_QUERY in request.GET,
            )
        else:
            fields = _meals_fields(coming, present=present, meals=draft.meals, prices=prices)
            errors = []
        response = _render_step(
            request,
            key=step,
            steps=steps,
            mount=mount,
            members=members,
            respondent=draft.resp,
            page_context=page_context,
            fields=fields,
            errors=errors,
            total=_total(draft, members, prices),
        )
        return response, None
    new = _switch_respondent(request, _with_posted(request, draft, members, step), members)
    if request.POST.get("action") == SWITCH:
        return HttpResponseRedirect(_keep_from(request, url)), new
    if step not in new.done:
        new.done.append(step)
    new = _settled(new, members)
    if step not in new.done:
        return _see_other(_error_url(request, url)), new
    return HttpResponseRedirect(_continue_url(request, mount, members, new, step)), new


def _allergies_step(
    request: HttpRequest,
    *,
    mount: FormMount,
    members: Members,
    draft: Draft,
    steps: tuple[str, ...],
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """FR-22, FR-25 to FR-28, AD-8, UX-DR21: step 5. The response and the draft.

    GET shows the consent text, a group per coming person and, when someone
    has information but no «Ja», the FR-28 warning; with `?feil=1` the
    errors, computed from the draft. «Fortsett» saves everything posted
    (a note that is too long is not kept) and is done when nobody has a
    problem; otherwise PRG to `?feil=1`. Missing consent never blocks.
    «Velg» keeps the posted values without validating them.
    """
    url = mount.url("allergies")
    if request.method != "POST":
        fields, errors = _allergy_fields(
            _coming(draft, members),
            respondent=draft.resp,
            draft=draft,
            show_errors=ERRORS_QUERY in request.GET,
        )
        response = _render_step(
            request,
            key="allergies",
            steps=steps,
            mount=mount,
            members=members,
            respondent=draft.resp,
            page_context=page_context,
            fields=fields,
            errors=errors,
        )
        return response, None
    new = _switch_respondent(request, _with_posted(request, draft, members, "allergies"), members)
    # AD-18 (Story 2.6c): the consent text this step showed, checked at send.
    new.cv = CONSENT_TEXT_VERSION
    if request.POST.get("action") == SWITCH:
        return HttpResponseRedirect(_keep_from(request, url)), new
    if "allergies" not in new.done:
        new.done.append("allergies")
    new = _settled(new, members)
    if "allergies" not in new.done:
        return _see_other(_error_url(request, url)), new
    return HttpResponseRedirect(_continue_url(request, mount, members, new, "allergies")), new


def _hike_fields(
    asked: Members, *, hike: dict[int, str], show_errors: bool
) -> tuple[dict[str, object], list[dict[str, str]]]:
    """FR-17, FR-22: step 6's lead, one group per member present on Friday, and errors.

    Each group has «Ja», «Nei» and «Kanskje», checked from `hike`; with
    `show_errors`, each member with no answer gets an error line.
    """
    groups, errors = [], []
    for guest_id, name in asked:
        field = hike_field(guest_id)
        error = HikeForm.error_text(name) if show_errors and guest_id not in hike else ""
        groups.append(
            {"name": name, "field": field, "value": hike.get(guest_id, ""), "error": error}
        )
        if error:
            errors.append(
                {"target": f"{field}_{HIKE_ANSWERS[0]}", "text": HikeForm.summary_text(name)}
            )
    return {"lead": HikeForm.LEAD, "choices": HikeForm.CHOICES, "groups": groups}, errors


def _hike_step(
    request: HttpRequest,
    *,
    mount: FormMount,
    members: Members,
    draft: Draft,
    steps: tuple[str, ...],
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """FR-17, FR-22: step 6. The response and the draft.

    GET shows a «Ja»/«Nei»/«Kanskje» group per coming member present on
    Friday, nothing checked until chosen; with `?feil=1` the errors, computed
    from the draft. «Fortsett» saves the valid posted answers and is done when
    everyone asked has one; otherwise PRG to `?feil=1`. «Velg» keeps the
    posted answers without validating them.
    """
    url = mount.url("hike")
    if request.method != "POST":
        fields, errors = _hike_fields(
            _hiking(draft, members), hike=draft.hike, show_errors=ERRORS_QUERY in request.GET
        )
        response = _render_step(
            request,
            key="hike",
            steps=steps,
            mount=mount,
            members=members,
            respondent=draft.resp,
            page_context=page_context,
            fields=fields,
            errors=errors,
        )
        return response, None
    new = _switch_respondent(request, _with_posted(request, draft, members, "hike"), members)
    if request.POST.get("action") == SWITCH:
        return HttpResponseRedirect(_keep_from(request, url)), new
    if "hike" not in new.done:
        new.done.append("hike")
    new = _settled(new, members)
    if "hike" not in new.done:
        return _see_other(_error_url(request, url)), new
    return HttpResponseRedirect(_continue_url(request, mount, members, new, "hike")), new


def _later_step(
    request: HttpRequest,
    *,
    actor: Actor,
    step: str,
    mount: FormMount,
    members: Members,
    draft: Draft | None,
    prices: Prices,
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """AD-7, UX-DR19: steps 2 to 6 or the check page.

    Before step 1 is completed it sends the guest to step 1, a step that does
    not apply to the answers sends them on to the next one that does, and a
    step with an applicable step before it not done sends them to that one.
    A POST with `action=send` to the check page sends the answer through
    `send_answer` (FR-74, AD-3, Story 2.6a), deletes the draft and redirects
    (303) to the sent page; a member missing from the draft's attendance
    sends the guest to step 1 instead (303), before the gate. `DeadlinePassed` is left to the
    mount's view (FR-41). Any other POST to the check page redirects (303)
    back to it and writes nothing. Story 2.6c (AD-20, NFR-1): a send whose
    submission id was already written for this household lands on the sent
    page before any other gate, so a late second tap after the draft was
    deleted still shows the receipt; `_send` maps the refusals.
    """
    sending = step == CHECK and request.method == "POST" and request.POST.get("action") == "send"
    if sending and isinstance(actor, GuestActor):
        submission = _submission(request)
        if submission is not None and submitted(actor.household, submission):
            response = _see_other(mount.sent_url())
            delete_draft(response, mount)
            return response, None
    if draft is None or "who" not in draft.done:
        return HttpResponseRedirect(mount.url("who")), None
    if sending and any(guest_id not in draft.att for guest_id, _ in members):
        # FR-13, AD-9: a member added after step 1 has no «Kommer»; ask it first.
        return _see_other(mount.url("who")), None
    # FR-75, AD-7: the stored `done` is not trusted on its own; a member added
    # after step 2 has no days, so step 2 is not done for the gate.
    draft = _settled(draft, members)
    steps = _steps(draft, members)
    if step != CHECK and step not in steps:
        return HttpResponseRedirect(_gate_url(request, mount, next_step(steps, step))), None
    unfinished = first_unfinished(steps, draft.done, None if step == CHECK else step)
    if unfinished is not None:
        return HttpResponseRedirect(_gate_url(request, mount, unfinished)), None
    if step == "days":
        return _which_days(
            request,
            mount=mount,
            members=members,
            draft=draft,
            steps=steps,
            page_context=page_context,
        )
    if step in PAID_STEPS:
        return _paid_step(
            request,
            step=step,
            mount=mount,
            members=members,
            draft=draft,
            steps=steps,
            prices=prices,
            page_context=page_context,
        )
    if step == "allergies":
        return _allergies_step(
            request,
            mount=mount,
            members=members,
            draft=draft,
            steps=steps,
            page_context=page_context,
        )
    if step == "hike":
        return _hike_step(
            request,
            mount=mount,
            members=members,
            draft=draft,
            steps=steps,
            page_context=page_context,
        )
    if request.method == "POST":
        if request.POST.get("action") != "send":
            return _see_other(mount.url(CHECK)), None
        return _send(request, actor=actor, mount=mount, members=members, draft=draft)
    response = _render_check(
        request,
        actor=actor,
        steps=steps,
        mount=mount,
        members=members,
        draft=draft,
        prices=prices,
        page_context=page_context,
    )
    return response, None


def handle_step(
    request: HttpRequest,
    *,
    actor: Actor,
    mount: FormMount,
    members: Members,
    step: str,
    prices: Prices,
    page_context: dict[str, object],
) -> HttpResponse:
    """AD-7, AD-8, FR-75: GET or POST one step (a key of `STEPS`, or `CHECK`) of the form.

    Reads the draft cookie, answers the step, and writes the draft only on a
    «Fortsett» (valid or not) or a «Velg», always normalised. When the write
    changes who is there on which days (`present_days`), by step 1, step 2 or
    «Velg», the steps after step 2 are no longer done, so the guest goes
    through the questions that now ask more. `prices` are `form_prices` of the
    settings. A broken draft is deleted and the form starts empty. The
    database is written only by «Send svaret» on the check page, through
    `send_answer` (Story 2.6a).
    """
    draft, broken, _ = read_draft(request, _member_ids(members), _owner(actor, members))
    if request.method == "POST" and request.POST.get("action") in (RESUME, RESTART):
        response = _answer_offer(request, mount=mount, members=members, draft=draft)
        if broken:
            delete_draft(response, mount)
        return response
    if draft is not None and request.method in ("GET", "HEAD") and not has_visit(request):
        return _render_offer(request, draft=draft, page_context=page_context)
    before = _present(draft, members)
    arguments = {"mount": mount, "members": members, "draft": draft, "page_context": page_context}
    if step == "who":
        response, new = _who_is_coming(request, actor=actor, **arguments)
    else:
        response, new = _later_step(request, actor=actor, step=step, prices=prices, **arguments)
    if new is not None:
        new = _settled(new, members)
        if _present(new, members) != before:
            new.done = [key for key in new.done if key not in REOPENED_ON_CHANGE]
        write_draft(response, new, mount)
    elif broken:
        delete_draft(response, mount)
    if request.method == "POST":
        mark_visit(response, mount)
    return response


def _start_line(draft: Draft) -> str:
    """FR-78, UX-DR26 (Story 2.9): when the draft was started, in Oslo time, without the year."""
    local = timezone.localtime(datetime.fromisoformat(draft.started))
    return (
        f"Du begynte på svaret {dateformat.format(local, 'l j. F')} kl. "
        f"{dateformat.format(local, 'H:i')}. "
        "Det du har fylt ut, er tatt vare på på denne telefonen."
    )


def _render_offer(
    request: HttpRequest, *, draft: Draft, page_context: dict[str, object]
) -> HttpResponse:
    """FR-78, AD-8, UX-DR26 (Story 2.9): the Draft offer, in place of the requested step.

    Shown on a GET or HEAD of any form address when a usable draft exists and
    the guest has no `rsvp_visit` cookie (a new browser session). Writes
    nothing: the draft is written only on a POST (AD-8).
    """
    context = page_context | {"start_line": _start_line(draft)}
    return render(request, OFFER_TEMPLATE, context)


def _answer_offer(
    request: HttpRequest, *, mount: FormMount, members: Members, draft: Draft | None
) -> HttpResponse:
    """FR-78, AD-8, UX-DR26 (Story 2.9): «Ja, fortsett» or «Nei, begynn på nytt».

    «Ja» (`action=resume`) writes the (cleaned) draft and goes (303) to the
    first unfinished applicable step, the check page when all are done; a
    changed household has no step done, so that is step 1. «Nei»
    (`action=restart`) deletes the draft and goes to step 1, which starts
    empty. Without a usable draft both go to step 1. Both set `rsvp_visit`,
    so the offer does not come back in this visit. `?fra` is ignored.
    """
    if draft is None:
        response = _see_other(mount.base_path)
    elif request.POST.get("action") == RESUME:
        draft = _settled(draft, members)
        response = _see_other(mount.url(first_unfinished(_steps(draft, members), draft.done, None)))
        write_draft(response, draft, mount)
    else:
        response = _see_other(mount.base_path)
        delete_draft(response, mount)
    mark_visit(response, mount)
    return response


def render_after_csrf_failure(
    request: HttpRequest,
    *,
    actor: Actor,
    mount: FormMount,
    members: Members,
    step: str,
    prices: Prices,
    page_context: dict[str, object],
) -> HttpResponse | None:
    """UX-DR52: a step POSTed without a valid CSRF token, shown again with status 403.

    The posted valid choices stay checked, with no field errors, and a focused
    error notice at the top says what happened and to try again; the page has
    a fresh token. On step 2 the posted «Ja»/«Nei» and days are kept, and the
    day groups show when «Nei» is posted or saved. On steps 3 and 4 the posted
    choices are merged into the saved ones, and the total is that of the
    merged answer (FR-33). On step 5 the posted ticks, notes, consent and
    confirmations are shown, the confirmation following the posted
    respondent. On step 6 the posted hike answers are shown. The check page
    (Story 2.6a), when every applicable step is done, is shown again with
    the same notice. No draft is written, and a broken one is deleted.
    None when the step is not one the guest could have posted from (the
    caller then shows the generic page).
    """
    draft, broken, _ = read_draft(request, _member_ids(members), _owner(actor, members))
    posted = posted_respondent(request.POST, _member_ids(members))
    steps = _steps(draft, members)
    fields = None
    total = None
    if step == "who":
        saved = draft.att if draft is not None else {}
        checked = saved | WhoIsComingForm(members, data=request.POST).posted_attendance()
        fields, _ = _who_fields(members, checked, show_errors=False)
    elif step == CHECK:
        if draft is None or "who" not in draft.done:
            return None
        draft = _settled(draft, members)
        steps = _steps(draft, members)
        if first_unfinished(steps, draft.done, None) is not None:
            return None
        return _render_check(
            request,
            actor=actor,
            steps=steps,
            mount=mount,
            members=members,
            draft=draft,
            prices=prices,
            page_context=page_context,
            csrf_failed=True,
            status=403,
        )
    elif (
        draft is not None
        and "who" in draft.done
        and step in steps
        and first_unfinished(steps, draft.done, step) is None
    ):
        if step == "days":
            form = DaysForm(_coming(draft, members), data=request.POST)
            posted_whole = form.posted_whole()
            fields, _ = _days_fields(
                _coming(draft, members),
                whole=draft.whole if posted_whole is None else posted_whole,
                days=form.posted_days(),
                show_groups=posted_whole is False or draft.whole is False,
                show_errors=False,
            )
        elif step in PAID_STEPS:
            merged = _with_posted(request, draft, members, step)
            coming = _coming(merged, members)
            present = present_days(_answer(merged, members))
            if step == "overnight":
                fields, _ = _overnight_fields(
                    coming, present=present, night=merged.night, prices=prices, show_errors=False
                )
            else:
                fields = _meals_fields(coming, present=present, meals=merged.meals, prices=prices)
            total = _total(merged, members, prices)
        elif step == "allergies":
            merged = _with_posted(request, draft, members, step, keep_long=True)
            fields, _ = _allergy_fields(
                _coming(merged, members),
                respondent=draft.resp if posted is None else posted,
                draft=merged,
                show_errors=False,
            )
        elif step == "hike":
            merged = _with_posted(request, draft, members, step)
            fields, _ = _hike_fields(_hiking(merged, members), hike=merged.hike, show_errors=False)
    else:
        return None
    if posted is not None:
        respondent = posted
    else:
        respondent = draft.resp if draft is not None else _owner(actor, members)
    response = _render_step(
        request,
        key=step,
        steps=steps,
        mount=mount,
        members=members,
        respondent=respondent,
        page_context=page_context,
        fields=fields,
        total=total,
        csrf_failed=True,
        status=403,
    )
    if broken:
        delete_draft(response, mount)
    return response


def render_total(
    request: HttpRequest, *, members: Members, slug: str, prices: Prices
) -> HttpResponse:
    """AD-7, FR-33, NFR-2: the running total for `POST <base>/sum/?steg=<slug>`.

    The posted choices of step 3 (`overnatting`) or step 4 (`maltider`) are
    merged into a copy of the draft, and the response is the total fragment
    (rsvp/includes/total.html, the same the step shows) with that answer's
    `household_total`. 204 with no body for any other `slug`, and without a
    usable draft (none, broken, or step 1 not completed). It never sets or
    deletes a cookie and writes nothing, so the draft changes only on
    «Fortsett» or «Velg». The mount's view checks the code and the deadline.
    """
    step = KEY_BY_SLUG.get(slug)
    draft = read_draft(request, _member_ids(members), members[0][0]).draft
    if step not in PAID_STEPS or draft is None or "who" not in draft.done:
        return HttpResponse(status=204)
    merged = _with_posted(request, draft, members, step)
    return render(request, TOTAL_TEMPLATE, {"total": _total(merged, members, prices)})
