"""The RSVP form's step handling, shared by every mount (Story 2.1).

AD-7: one server-rendered form, each step a plain POST validated by the
server, then POST-redirect-GET to the next applicable step. AD-8: between
steps the answers live only in the draft cookie (wedding/rsvp/draft.py); no
session, no messages, no hidden fields and no database row (AD-1). The mount's
own view (guests/views.py for guests) resolves the actor, reads the settings,
checks the deadline and loads the members, then calls `handle_step`.

Step 1 «Hvem kommer?» (FR-12, FR-13, FR-14, FR-22) is built here. Days,
overnight stay, meals, allergies, the hike and the check page are frames that
Stories 2.2 to 2.5 fill: they show where the guest is, the respondent line and
«Tilbake», so «Fortsett» always lands on a real address.
"""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from wedding.actors import Actor, GuestActor
from wedding.rsvp.draft import Draft, delete_draft, read_draft, write_draft
from wedding.rsvp.forms import (
    COMING,
    NOT_COMING,
    WhoIsComingForm,
    attendance_field,
    posted_respondent,
)
from wedding.rsvp.steps import CHECK, STEPS, FormMount
from wedding.rules.form_steps import form_steps, next_step, previous_step, step_position

STEP_TEMPLATE = "rsvp/step.html"
CHECK_TEMPLATE = "rsvp/check_frame.html"
SWITCH = "switch"
# FR-22: the query that asks step 1 to show its errors after an invalid «Fortsett».
ERRORS_QUERY = "feil"
Members = list[tuple[int, str]]


def _member_ids(members: Members) -> set[int]:
    """AD-8: the household's guest ids, the only ids a draft or a POST may name."""
    return {guest_id for guest_id, _ in members}


def _owner(actor: Actor, members: Members) -> int:
    """FR-12: the default respondent, the link's owner (the first member without one)."""
    if isinstance(actor, GuestActor):
        return actor.guest.id
    return members[0][0]


def _steps(draft: Draft | None, members: Members) -> tuple[str, ...]:
    """UX-DR19: the applicable steps; all of them until step 1 is completed.

    A member the draft does not know (added after step 1) counts as coming,
    as everyone does before step 1.
    """
    if draft is None or "who" not in draft.done:
        return form_steps(None)
    return form_steps([draft.att.get(guest_id, True) for guest_id, _ in members])


def _merged(draft: Draft | None, actor: Actor, members: Members) -> Draft:
    """AD-8: the existing draft, or a new one started now at the household's revision."""
    if draft is not None:
        return draft
    revision = actor.household.revision if isinstance(actor, GuestActor) else 0
    return Draft.new(revision=revision, respondent=_owner(actor, members), now=timezone.now())


def _render_step(
    request: HttpRequest,
    *,
    key: str,
    steps: tuple[str, ...],
    mount: FormMount,
    members: Members,
    respondent: int,
    page_context: dict[str, object],
    checked: dict[int, bool] | None = None,
    show_errors: bool = False,
    csrf_failed: bool = False,
    status: int = 200,
) -> HttpResponse:
    """FR-12, FR-14, FR-22, UX-DR16, UX-DR18, UX-DR19: one step's page.

    Step 1 gets one group per member with `checked` pre-selected and, with
    `show_errors`, the error summary and an error line for each member with no
    answer in `checked`. A frame (any other step) has no groups and no
    «Fortsett».
    """
    number, total = step_position(steps, key)
    step = STEPS[key]
    previous = previous_step(steps, key)
    names = dict(members)
    rows, errors = [], []
    if key == "who":
        checked = checked or {}
        for guest_id, name in members:
            field = attendance_field(guest_id)
            coming = checked.get(guest_id)
            missing = show_errors and coming is None
            error = f"Velg «Kommer» eller «Kommer ikke» for {name}." if missing else ""
            rows.append(
                {
                    "id": guest_id,
                    "name": name,
                    "field": field,
                    "value": "" if coming is None else (COMING if coming else NOT_COMING),
                    "error": error,
                }
            )
            if error:
                errors.append({"target": f"{field}_{COMING}", "text": f"Velg om {name} kommer"})
    context = page_context | {
        "heading": "Hvem kommer?" if key == "who" else step.name,
        "progress": f"Steg {number} av {total}: {step.name}",
        "respondent_id": respondent,
        "respondent_name": names[respondent],
        "members": [{"id": guest_id, "name": name} for guest_id, name in members],
        "back_url": mount.exit_url if previous is None else mount.url(previous),
        "rows": rows,
        "errors": errors,
        "csrf_failed": csrf_failed,
    }
    return render(request, STEP_TEMPLATE, context, status=status)


def _render_check(
    request: HttpRequest, *, steps: tuple[str, ...], mount: FormMount, page_context: dict
) -> HttpResponse:
    """AD-7: the check page's frame, filled in Story 2.5: its heading and «Tilbake»."""
    context = page_context | {"back_url": mount.url(steps[-1])}
    return render(request, CHECK_TEMPLATE, context)


def _switched(request: HttpRequest, draft: Draft, members: Members) -> Draft:
    """FR-12, UX-DR18: «Velg» in «Bytt».

    The posted respondent replaces the current one when they are a member;
    every valid posted attendance is kept in the draft without validating the
    rest and without marking the step done, so nothing typed is lost.
    """
    respondent = posted_respondent(request.POST, _member_ids(members))
    if respondent is not None:
        draft.resp = respondent
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
        response = _render_step(
            request,
            key="who",
            steps=_steps(draft, members),
            mount=mount,
            members=members,
            respondent=respondent,
            page_context=page_context,
            checked=checked,
            show_errors=ERRORS_QUERY in request.GET,
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
        response = HttpResponseRedirect(f"{mount.url('who')}?{ERRORS_QUERY}=1")
        response.status_code = 303  # See Other: the GET never resubmits
        return response, new
    posted = posted_respondent(request.POST, _member_ids(members))
    new = _merged(draft, actor, members)
    new.att = form.attendance()
    if "who" not in new.done:
        new.done.append("who")
    if posted is not None:
        new.resp = posted
    steps = _steps(new, members)
    return HttpResponseRedirect(mount.url(next_step(steps, "who"))), new


def _frame(
    request: HttpRequest,
    *,
    step: str,
    mount: FormMount,
    members: Members,
    draft: Draft | None,
    page_context: dict,
) -> tuple[HttpResponse, Draft | None]:
    """AD-7: a later step's frame or the check page, until Stories 2.2 to 2.5 fill them.

    Before step 1 is completed it sends the guest to step 1, and a step that
    does not apply to the answers sends them on to the next one that does. A
    POST only handles «Velg» in «Bytt»; anything else goes back to the address.
    """
    if draft is None or "who" not in draft.done:
        return HttpResponseRedirect(mount.url("who")), None
    steps = _steps(draft, members)
    if step != CHECK and step not in steps:
        return HttpResponseRedirect(mount.url(next_step(steps, step))), None
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
    """AD-7, AD-8: GET or POST one step (a key of `STEPS`, or `CHECK`) of the form.

    Reads the draft cookie, answers the step, and writes the draft only on a
    «Fortsett» (valid or not) or a «Velg». A broken draft is deleted and the
    form starts empty. Nothing is written to the database.
    """
    draft, broken = read_draft(request, _member_ids(members))
    arguments = {"mount": mount, "members": members, "draft": draft, "page_context": page_context}
    if step == "who":
        response, new = _who_is_coming(request, actor=actor, **arguments)
    else:
        response, new = _frame(request, step=step, **arguments)
    if new is not None:
        write_draft(response, new, mount)
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
    a fresh token. No draft is written, and a broken one is deleted. None when
    the step is not one the guest could have posted from (the caller then shows
    the generic page).
    """
    draft, broken = read_draft(request, _member_ids(members))
    posted = posted_respondent(request.POST, _member_ids(members))
    steps = _steps(draft, members)
    if step == "who":
        saved = draft.att if draft is not None else {}
        checked = saved | WhoIsComingForm(members, data=request.POST).posted_attendance()
    elif step != CHECK and draft is not None and "who" in draft.done and step in steps:
        checked = None
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
        checked=checked,
        csrf_failed=True,
        status=403,
    )
    if broken:
        delete_draft(response, mount)
    return response
