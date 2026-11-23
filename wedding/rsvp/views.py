"""The RSVP form's step handling, shared by every mount (Stories 2.1, 2.2).

AD-7: one server-rendered form, each step a plain POST validated by the
server, then POST-redirect-GET to the next applicable step. AD-8: between
steps the answers live only in the draft cookie (wedding/rsvp/draft.py); no
session, no messages, no hidden fields and no database row (AD-1). The mount's
own view (guests/views.py for guests) resolves the actor, reads the settings,
checks the deadline and loads the members, then calls `handle_step`.

Step 1 «Hvem kommer?» (FR-12, FR-13, FR-14, FR-22, Story 2.1) and step 2
«Er alle som kommer, med hele helgen?» (FR-14, FR-70, Story 2.2) are built
here. Step 2 is one address: after «Nei» it shows a day group per coming
person at `#velg-dager`. Overnight stay, meals, allergies, the hike and the
check page are frames that Stories 2.3 to 2.5 fill: they show where the guest
is, the respondent line and «Tilbake», so «Fortsett» always lands on a real
address. A later step opens only when every applicable step before it is done
(`first_unfinished`). Every draft write runs `normalise_answer` (FR-75), so a
person who stops coming loses their days, and step 2 stays done only while
its answer is complete.
"""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from wedding.actors import Actor, GuestActor
from wedding.rsvp.draft import Draft, delete_draft, read_draft, write_draft
from wedding.rsvp.forms import (
    ATTENDANCE_CHOICES,
    NO,
    WHOLE_CHOICES,
    WHOLE_FIELD,
    YES,
    DaysForm,
    WhoIsComingForm,
    attendance_field,
    days_field,
    posted_respondent,
)
from wedding.rsvp.steps import CHECK, DAYS, STEPS, FormMount
from wedding.rules.answer import normalise_answer
from wedding.rules.days import day_error
from wedding.rules.form_steps import (
    first_unfinished,
    form_steps,
    next_step,
    previous_step,
    step_position,
)

STEP_TEMPLATE = "rsvp/step.html"
CHECK_TEMPLATE = "rsvp/check_frame.html"
SWITCH = "switch"
# FR-22: the query that asks a step to show its errors after an invalid «Fortsett».
ERRORS_QUERY = "feil"
# AD-7, Story 2.2: where step 2's day groups start, after «Nei».
DAY_GROUPS_ANCHOR = "velg-dager"
Members = list[tuple[int, str]]


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


def _days_complete(draft: Draft, members: Members) -> bool:
    """FR-14, FR-70: step 2 is answered: «Ja», or «Nei» with an allowed set for everyone coming."""
    if draft.whole is None:
        return False
    return draft.whole or all(
        day_error(draft.days.get(guest_id, ())) is None for guest_id, _ in _coming(draft, members)
    )


def _settled(draft: Draft, members: Members) -> Draft:
    """FR-75, AD-8: the draft as it is written: normalised, and step 2 done only when complete.

    Runs on every draft write, so days never outlive their person's «Kommer»
    and a new comer or a removed day sends the guest back to step 2.
    """
    draft.whole, draft.days = normalise_answer(_attendance(draft, members), draft.whole, draft.days)
    if "days" in draft.done and not _days_complete(draft, members):
        draft.done.remove("days")
    return draft


def _merged(draft: Draft | None, actor: Actor, members: Members) -> Draft:
    """AD-8: the existing draft, or a new one started now at the household's revision."""
    if draft is not None:
        return draft
    revision = actor.household.revision if isinstance(actor, GuestActor) else 0
    return Draft.new(revision=revision, respondent=_owner(actor, members), now=timezone.now())


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
    csrf_failed: bool = False,
    status: int = 200,
) -> HttpResponse:
    """FR-12, FR-14, FR-22, UX-DR16, UX-DR18, UX-DR19: one step's page.

    The question from the registry as the `h1`, the progress line, the
    respondent line and «Tilbake». `fields` is the step's own context
    (`_who_fields`, `_days_fields`); with fields, the page also has
    «Fortsett». A frame (steps 3 to 6 until Stories 2.3 to 2.5) has none.
    `errors` are the error summary's links.
    """
    number, total = step_position(steps, key)
    step = STEPS[key]
    previous = previous_step(steps, key)
    context = (
        page_context
        | (fields or {})
        | {
            "key": key,
            "has_fields": fields is not None,
            "heading": step.question,
            "progress": f"Steg {number} av {total}: {step.name}",
            "respondent_id": respondent,
            "respondent_name": dict(members)[respondent],
            "members": [{"id": guest_id, "name": name} for guest_id, name in members],
            "back_url": mount.exit_url if previous is None else mount.url(previous),
            "errors": errors or [],
            "csrf_failed": csrf_failed,
        }
    )
    return render(request, STEP_TEMPLATE, context, status=status)


def _render_check(
    request: HttpRequest, *, steps: tuple[str, ...], mount: FormMount, page_context: dict
) -> HttpResponse:
    """AD-7: the check page's frame, filled in Story 2.5: its heading and «Tilbake»."""
    context = page_context | {"back_url": mount.url(steps[-1])}
    return render(request, CHECK_TEMPLATE, context)


def _switch_respondent(request: HttpRequest, draft: Draft, members: Members) -> Draft:
    """FR-12, UX-DR18: the posted respondent replaces the current one when they are a member."""
    respondent = posted_respondent(request.POST, _member_ids(members))
    if respondent is not None:
        draft.resp = respondent
    return draft


def _switched(request: HttpRequest, draft: Draft, members: Members) -> Draft:
    """FR-12, UX-DR18: «Velg» in «Bytt» on step 1 or a frame.

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
        return HttpResponseRedirect(mount.url("who")), new
    form = WhoIsComingForm(members, data=request.POST)
    if not form.is_valid():
        # FR-22, AD-7: POST-redirect-GET for errors too, so Back to the error
        # page never asks to resubmit. The valid choices and respondent are kept
        # in the draft, step 1 stays not done, and the GET shows the errors.
        new = _switched(request, _merged(draft, actor, members), members)
        return _see_other(f"{mount.url('who')}?{ERRORS_QUERY}=1"), new
    new = _switch_respondent(request, _merged(draft, actor, members), members)
    new.att = form.attendance()
    if "who" not in new.done:
        new.done.append("who")
    steps = _steps(_settled(new, members), members)
    return HttpResponseRedirect(mount.url(next_step(steps, "who"))), new


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
        return HttpResponseRedirect(url), _days_switched(request, draft, members)
    form = DaysForm(coming, data=request.POST)
    whole = form.posted_whole()
    new = _switch_respondent(request, draft, members)
    if whole is None:
        return _see_other(f"{url}?{ERRORS_QUERY}=1"), new
    if whole is False and new.whole is not False and not form.has_posted_days():
        new.whole, new.days = False, {}
        return HttpResponseRedirect(f"{url}#{DAY_GROUPS_ANCHOR}"), new
    new.whole = whole
    new.days = {} if whole else form.posted_days()
    if "days" not in new.done:
        new.done.append("days")
    new = _settled(new, members)
    if "days" not in new.done:
        return _see_other(f"{url}?{ERRORS_QUERY}=1"), new
    return HttpResponseRedirect(mount.url(next_step(_steps(new, members), "days"))), new


def _later_step(
    request: HttpRequest,
    *,
    step: str,
    mount: FormMount,
    members: Members,
    draft: Draft | None,
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """AD-7, UX-DR19: step 2, a later step's frame or the check page.

    Before step 1 is completed it sends the guest to step 1, a step that does
    not apply to the answers sends them on to the next one that does, and a
    step with an applicable step before it not done sends them to that one.
    A frame's POST only handles «Velg» in «Bytt»; anything else goes back to
    the address.
    """
    if draft is None or "who" not in draft.done:
        return HttpResponseRedirect(mount.url("who")), None
    # FR-75, AD-7: the stored `done` is not trusted on its own; a member added
    # after step 2 has no days, so step 2 is not done for the gate.
    draft = _settled(draft, members)
    steps = _steps(draft, members)
    if step != CHECK and step not in steps:
        return HttpResponseRedirect(mount.url(next_step(steps, step))), None
    unfinished = first_unfinished(steps, draft.done, None if step == CHECK else step)
    if unfinished is not None:
        return HttpResponseRedirect(mount.url(unfinished)), None
    if step == "days":
        return _which_days(
            request,
            mount=mount,
            members=members,
            draft=draft,
            steps=steps,
            page_context=page_context,
        )
    if request.method == "POST":
        new = _switched(request, draft, members) if request.POST.get("action") == SWITCH else None
        return HttpResponseRedirect(mount.url(step)), new
    if step == CHECK:
        return _render_check(request, steps=steps, mount=mount, page_context=page_context), None
    response = _render_step(
        request,
        key=step,
        steps=steps,
        mount=mount,
        members=members,
        respondent=draft.resp,
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
    page_context: dict[str, object],
) -> HttpResponse:
    """AD-7, AD-8, FR-75: GET or POST one step (a key of `STEPS`, or `CHECK`) of the form.

    Reads the draft cookie, answers the step, and writes the draft only on a
    «Fortsett» (valid or not) or a «Velg», always normalised. A broken draft is
    deleted and the form starts empty. Nothing is written to the database.
    """
    draft, broken = read_draft(request, _member_ids(members))
    arguments = {"mount": mount, "members": members, "draft": draft, "page_context": page_context}
    if step == "who":
        response, new = _who_is_coming(request, actor=actor, **arguments)
    else:
        response, new = _later_step(request, step=step, **arguments)
    if new is not None:
        write_draft(response, _settled(new, members), mount)
    elif broken:
        delete_draft(response, mount)
    return response


def render_after_csrf_failure(
    request: HttpRequest,
    *,
    actor: Actor,
    mount: FormMount,
    members: Members,
    step: str,
    page_context: dict[str, object],
) -> HttpResponse | None:
    """UX-DR52: a step POSTed without a valid CSRF token, shown again with status 403.

    The posted valid choices stay checked, with no field errors, and a focused
    error notice at the top says what happened and to try again; the page has
    a fresh token. On step 2 the posted «Ja»/«Nei» and days are kept, and the
    day groups show when «Nei» is posted or saved. No draft is written, and a
    broken one is deleted. None when the step is not one the guest could have
    posted from (the caller then shows the generic page).
    """
    draft, broken = read_draft(request, _member_ids(members))
    posted = posted_respondent(request.POST, _member_ids(members))
    steps = _steps(draft, members)
    fields = None
    if step == "who":
        saved = draft.att if draft is not None else {}
        checked = saved | WhoIsComingForm(members, data=request.POST).posted_attendance()
        fields, _ = _who_fields(members, checked, show_errors=False)
    elif (
        step != CHECK
        and draft is not None
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
        csrf_failed=True,
        status=403,
    )
    if broken:
        delete_draft(response, mount)
    return response
