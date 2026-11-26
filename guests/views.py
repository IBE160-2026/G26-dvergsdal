"""Guest views.

The invitation's front page under `/<code>/` and its three info pages (Story
1.5, FR-2, FR-7, FR-8, FR-11; their content in Story 1.6 and, for Programmet
with the meal prices from the settings, Story 1.7, FR-9), the
private-invitation page G1 for the bare address and for every code that
resolves to nobody (Story 1.4b, FR-5), the local style sample (Story 1.4a),
and the site-wide error pages for 404, 500, 400 and a failed CSRF check
(Story 1.8, FR-5, FR-6, AD-15), and the RSVP form under `/<code>/svar/`
(Story 2.1, FR-12 to FR-14, FR-22, FR-41, AD-7, AD-8, AD-11) with its running
total under `/<code>/svar/sum/` (Story 2.3, FR-33) and its sent page under
`/<code>/svar/sendt/` (Story 2.6a, FR-74), which Story 2.7 makes the receipt
(FR-23, FR-34), with the payment page under `/<code>/svar/betal/` (FR-71).
Once a household has answered, the front page shows its status block instead
of the RSVP sheet and every form address leads there (Story 2.8, FR-24,
FR-34, UX-DR10).

Every guest view only reads (FR-3): one resolver lookup, then selectors. None
of them touches the session, the messages framework or `request.user`, and
the read views (front page, info pages) use no CSRF token, so opening a link
sets no cookie and writes no row. The RSVP form keeps the answer in the draft
cookie only (AD-8); its one write is «Send svaret», through the service
`send_answer` (Story 2.6a, AD-3). The error pages only read too.
Guest responses say `Cache-Control: private, no-store` (`never_cache`), so no
shared or back-forward cache keeps a household's page (AD-15), and the read
views answer only GET and HEAD.
"""

import logging

from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import Resolver404, resolve, reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods, require_POST, require_safe

from wedding.actors import GuestActor
from wedding.links import resolve_code
from wedding.models import HouseholdAnswer, Settings
from wedding.rsvp.draft import COOKIE_NAME, delete_draft, read_draft
from wedding.rsvp.steps import CHECK, KEY_BY_SLUG, FormMount
from wedding.rsvp.summary import receipt_parts
from wedding.rsvp.views import (
    SENDING_QUERY,
    handle_step,
    render_after_csrf_failure,
    render_total,
)
from wedding.rules.answer import Answer, normalise_answer, present_days
from wedding.rules.deadline import is_past_deadline
from wedding.rules.form_steps import form_steps
from wedding.rules.households import household_names, payment_message, speaks_to_one
from wedding.rules.money import digits_only, guest_balance, household_total
from wedding.selectors import (
    footer_contacts,
    form_prices,
    household_answer,
    household_guest_names,
    household_members,
    programme_prices,
    sent_answer,
    site_settings,
)
from wedding.services.exceptions import DeadlinePassed

logger = logging.getLogger(__name__)

# DESIGN.md colour tokens, in the frontmatter's order, for the swatches.
COLOUR_TOKENS = (
    "page-green",
    "green-dark",
    "green-dark-hover",
    "seal",
    "panel-cream",
    "ink",
    "ink-muted",
    "cream-on-green",
    "field-surface",
    "field-border",
    "divider",
    "focus-on-panel",
    "focus-on-green",
    "error",
    "success",
    "warning",
    "scrim",
)


def style_sample(request: HttpRequest) -> HttpResponse:
    """UX-DR1, UX-DR2, UX-DR3, UX-DR15, UX-DR17, UX-DR53, UX-DR54: the design sample.

    A local-only page (Rikke's decision, 2026-11-18) where the couple and the
    examiner can see the design system and run the forced-colours, reduced-motion
    and font checks in docs/manual-test-plan.md (MT-2 to MT-4). It holds no
    personal data and reads nothing from the database. `guests/urls.py` only
    adds its URL when `APP_ENV` is `local`.
    """
    return render(request, "guests/style_sample.html", {"colour_tokens": COLOUR_TOKENS})


PRIVATE_INVITATION = "guests/private_invitation.html"


def private_invitation(request: HttpRequest) -> HttpResponse:
    """FR-5, UX-DR5: the bare address `/` shows only the private-invitation page G1.

    No names, phone numbers, date, place, seal, nav bar or footer. It reads
    nothing from the database, so it renders on an empty, migrated one.
    """
    return render(request, PRIVATE_INVITATION)


def _unknown_link(request: HttpRequest) -> HttpResponse:
    """FR-5: G1 with status 404 for a code that resolves to nobody.

    The visitor sees the same page as on `/`; the 404 tells crawlers and link
    scanners that the code is not a page. It is a normal response, so `DEBUG`
    never shows Django's technical 404 with the URL list.
    """
    return render(request, PRIVATE_INVITATION, status=404)


def _guest_context(
    actor: GuestActor,
    settings: Settings,
    current: str = "",
    answered: bool | None = None,
) -> dict[str, object]:
    """FR-6, FR-8, FR-41: what every guest page under a valid link needs.

    The code for the nav links, the open info page (`current`, empty on the
    front page), whether the household has answered (`answered`, Story 2.8,
    FR-24, AD-4: `household_answer`, one SELECT; the nav «Svar» then goes to
    `#status`; a caller that has read it already passes `answered`) and, from
    the settings row the view has read once, the footer contacts and the
    deadline.
    """
    return {
        "code": actor.guest.code,
        "current": current,
        "answered": household_answer(actor.household) is not None if answered is None else answered,
        "contacts": footer_contacts(settings),
        "deadline": settings.rsvp_deadline,
    }


@never_cache
@require_safe
def front_page(request: HttpRequest, code: str) -> HttpResponse:
    """FR-2, FR-3, FR-5, FR-6, FR-7, FR-8, FR-41, UX-DR51: the invitation's front page (G2).

    The code goes through the one resolver (AD-6); nobody gets G1 with 404.
    Unanswered, four SELECTs: the resolver, the household's guest names, the
    settings row and the answer check. The household line and «deg»/«dere»
    come from the rules; the wedding's date and place are template text
    (AD-17). The RSVP sheet links to the form (Story 2.1). Once the household
    has answered (Story 2.8, FR-24, FR-34, UX-DR10), the hero says when and
    the status block takes the sheet's place, with who sent it, the total and,
    when something is owed, «Slik betaler du» (`_sent_money`, AD-12). Only
    GET and HEAD, never cached (AD-15).

    Story 2.9 (FR-78, AD-8, AD-11, UX-DR26): an unanswered household with a
    draft cookie before the deadline gets the warning notice «Du har et svar
    som ikke er sendt ennå.» on the RSVP sheet, for a usable draft; that
    costs one more SELECT (`household_members`), only when the cookie is
    there. A broken draft, or any draft after the deadline, is deleted
    instead. An answered household's cookie is left alone (Story 4.1).
    """
    actor = resolve_code(code)
    if actor is None:
        return _unknown_link(request)
    names = household_guest_names(actor.household)
    settings = site_settings()
    answer = household_answer(actor.household)
    context = _guest_context(actor, settings, answered=answer is not None) | {
        "household_names": household_names(names),
        "speaks_to_one": speaks_to_one(len(names)),
    }
    if answer is not None:
        context |= {"answer": answer, **_sent_money(sent_answer(actor.household), settings)}
        return render(request, "guests/front_page.html", context)
    if COOKIE_NAME not in request.COOKIES:
        return render(request, "guests/front_page.html", context)
    mount = _guest_mount(actor.guest.code)
    if is_past_deadline(settings.rsvp_deadline, timezone.now()):
        response = render(request, "guests/front_page.html", context)
        delete_draft(response, mount)
        return response
    members = household_members(actor.household)
    found = read_draft(request, {guest_id for guest_id, _ in members}, actor.guest.id)
    context["draft_waiting"] = found.draft is not None
    response = render(request, "guests/front_page.html", context)
    if found.broken:
        delete_draft(response, mount)
    return response


# FR-8, FR-11: each info page's key (its URL name and current nav word) and
# template. The text lives in the templates (AD-17): Praktisk informasjon
# (FR-10) and Vår historie (UX-DR14) are filled in Story 1.6, Programmet
# (FR-9, UX-DR13) in Story 1.7.
INFO_PAGES = {
    "programme": "guests/programme.html",
    "practical": "guests/practical.html",
    "our_story": "guests/our_story.html",
}


@never_cache
@require_safe
def info_page(request: HttpRequest, code: str, page: str) -> HttpResponse:
    """FR-3, FR-5, FR-6, FR-8, FR-9, FR-11: one of the three info pages (G3) under `/<code>/`.

    `page` is a key of `INFO_PAGES`, set by the route. Three SELECTs: the
    resolver, the settings row and the answer check for the nav (Story 2.8);
    nobody gets G1 with 404. The page's content is template text (AD-17):
    Praktisk informasjon (FR-10) and Vår historie (UX-DR14) since Story 1.6,
    Programmet (UX-DR13) since Story 1.7. The
    programme also gets the three meal prices from the same settings row
    (FR-32, AD-12), so «Godt å vite» never holds a price of its own. Only GET
    and HEAD, never cached (AD-15).
    """
    actor = resolve_code(code)
    if actor is None:
        return _unknown_link(request)
    settings = site_settings()
    context = _guest_context(actor, settings, current=page)
    if page == "programme":
        context["prices"] = programme_prices(settings)
    return render(request, INFO_PAGES[page], context)


# The RSVP form (Story 2.1, AD-7, AD-8, AD-11)
#
# The guest mount of the one form in wedding/rsvp/. The views resolve the code,
# read the settings, check the deadline and load the members, then hand the
# step to wedding.rsvp.views: three SELECTs per request while the form is open.
# After the deadline every step address shows the closed page instead.

RSVP_CLOSED = "guests/rsvp_closed.html"


def _guest_mount(code: str) -> FormMount:
    """AD-7, AD-8: the form under `/<code>/svar/`, its draft cookie scoped to `/<code>/`."""
    front = reverse("guests:front_page", args=[code])
    return FormMount(
        base_path=reverse("guests:rsvp", args=[code]), cookie_path=front, exit_url=f"{front}#svar"
    )


def _closed(request: HttpRequest, context: dict, mount: FormMount) -> HttpResponse:
    """FR-41, AD-11, FR-78 (Story 2.9): the closed page, which also deletes the draft."""
    response = render(request, RSVP_CLOSED, context)
    if COOKIE_NAME in request.COOKIES:
        delete_draft(response, mount)
    return response


def _rsvp(request: HttpRequest, code: str, step: str | None) -> HttpResponse:
    """FR-5, FR-41, AD-6, AD-11: the checks every RSVP address shares, then the step.

    An unknown code gives G1 with 404 after the one resolver query; an unknown
    step slug (`step` None) gives «Vi finner ikke denne siden». After the
    deadline, GET and POST alike show the closed page and write nothing; so
    does a send `send_answer` refuses with `DeadlinePassed` (FR-41, Story 2.6a).
    A GET or HEAD by a household that has answered goes (302) to the front
    page's status block, before the deadline check, so it holds after the
    deadline too (Story 2.8, FR-24, UX-DR10). POSTs are untouched, and so,
    before the deadline only, is the check page a refused send comes back to
    (`se-over/?sending=…`), so the double-tap and conflict handling of Story
    2.6c keep working; every other step with `?sending=` still redirects.
    The closed page deletes the draft cookie (AD-11, Story 2.9).
    """
    actor = resolve_code(code)
    if actor is None:
        return _unknown_link(request)
    if step is None:
        raise Http404
    settings = site_settings()
    context = _guest_context(actor, settings)
    if (
        request.method in ("GET", "HEAD")
        and context["answered"]
        and not (
            step == CHECK
            and SENDING_QUERY in request.GET
            and not is_past_deadline(settings.rsvp_deadline, timezone.now())
        )
    ):
        return HttpResponseRedirect(reverse("guests:front_page", args=[code]) + "#status")
    mount = _guest_mount(actor.guest.code)
    if is_past_deadline(settings.rsvp_deadline, timezone.now()):
        return _closed(request, context, mount)
    try:
        return handle_step(
            request,
            actor=actor,
            mount=mount,
            members=household_members(actor.household),
            step=step,
            prices=form_prices(settings),
            page_context=context,
        )
    except DeadlinePassed:
        return _closed(request, context, mount)


@never_cache
@sensitive_post_parameters()
@require_http_methods(["GET", "HEAD", "POST"])
def rsvp(request: HttpRequest, code: str) -> HttpResponse:
    """FR-12, FR-13, FR-14, FR-22, AD-7, AD-8: step 1 of the RSVP form, «Hvem kommer?»."""
    return _rsvp(request, code, "who")


@never_cache
@sensitive_post_parameters()
@require_http_methods(["GET", "HEAD", "POST"])
def rsvp_step(request: HttpRequest, code: str, slug: str) -> HttpResponse:
    """AD-7: a later step or the check page of the RSVP form, by its slug."""
    return _rsvp(request, code, KEY_BY_SLUG.get(slug))


def _sent_money(answer: Answer, settings: Settings) -> dict[str, int]:
    """FR-33, FR-34, AD-12 (Stories 2.7, 2.8): the sent answer's total and what is owed.

    `total` from `household_total` over the stored answer (from `sent_answer`), so
    it equals the check page's; `balance` from `guest_balance` (no report
    until Story 5.1). Shared by the receipt and the front page's status block;
    never reads payment rows.
    """
    total = household_total(answer, form_prices(settings))
    return {"total": total, "balance": guest_balance(total, None)}


def _receipt(actor: GuestActor, sent: HouseholdAnswer, settings: Settings) -> dict[str, object]:
    """FR-23, FR-34, FR-71, AD-12, UX-DR51 (Story 2.7): what the receipt and the payment page show.

    From the stored answer (`sent_answer`): the steps that apply, the summary
    parts, the total from `household_total` (so it equals the check page's),
    what is owed from `guest_balance` (no report until Story 5.1), whether
    anyone comes, du/dere and the payment message. Never reads payment rows.
    """
    members = household_members(actor.household)
    answer = sent_answer(actor.household)
    present = present_days(normalise_answer(answer))
    steps = form_steps(
        [answer.attendance.get(guest_id, False) for guest_id, _ in members],
        [present.get(guest_id) for guest_id, _ in members],
    )
    names = [name for _, name in members]
    return {
        "parts": receipt_parts(
            answer, members=members, respondent=sent.sent_by_id or 0, steps=steps
        ),
        **_sent_money(answer, settings),
        "anyone_coming": bool(present),
        "speaks_to_one": speaks_to_one(len(members)),
        "payment_message": payment_message(names),
    }


@never_cache
@require_safe
def rsvp_sent(request: HttpRequest, code: str) -> HttpResponse:
    """FR-23, FR-34, FR-74, AD-7, AD-12, UX-DR24, UX-DR51 (Stories 2.6a, 2.7): the receipt (G6).

    Where «Send svaret» lands. An unknown code gives G1 with 404; a household
    that has sent nothing is sent (302) to step 1. Otherwise «Svaret er
    sendt» with who sent it and when (Oslo time), Rikke's message, the
    summary of the stored answer, the total and, when something is owed,
    «Betal nå» and «Betal senere». `?betal=senere` adds the focused notice
    that the link always shows what is left to pay (only when owed; any
    other value is ignored). It only reads, so the deadline does not close
    it. Only GET and HEAD, never cached (AD-15).
    """
    actor = resolve_code(code)
    if actor is None:
        return _unknown_link(request)
    sent = household_answer(actor.household)
    if sent is None:
        return HttpResponseRedirect(reverse("guests:rsvp", args=[code]))
    settings = site_settings()
    receipt = _receipt(actor, sent, settings)
    context = (
        _guest_context(actor, settings)
        | receipt
        | {
            "answer": sent,
            "pay_later": receipt["balance"] > 0 and request.GET.get("betal") == "senere",
        }
    )
    return render(request, "rsvp/sent.html", context)


@never_cache
@require_safe
def rsvp_pay(request: HttpRequest, code: str) -> HttpResponse:
    """FR-34, FR-64, FR-71, AD-12, UX-DR25 (Story 2.7): «Slik betaler du» (G7).

    The amount owed, the Vipps number, the account number and the payment
    message, as selectable text with «Kopier» buttons the script shows. A
    setting left blank is left out. An unknown code gives G1 with 404; no
    sent answer gives 302 to step 1; nothing owed gives 302 to the receipt.
    It only reads, so the deadline does not close it. Only GET and HEAD,
    never cached (AD-15).
    """
    actor = resolve_code(code)
    if actor is None:
        return _unknown_link(request)
    sent = household_answer(actor.household)
    if sent is None:
        return HttpResponseRedirect(reverse("guests:rsvp", args=[code]))
    settings = site_settings()
    receipt = _receipt(actor, sent, settings)
    if receipt["balance"] <= 0:
        return HttpResponseRedirect(reverse("guests:rsvp_sent", args=[code]))
    context = _guest_context(actor, settings) | {
        "balance": receipt["balance"],
        "vipps_number": settings.vipps_number,
        "account_number": settings.account_number,
        "account_digits": digits_only(settings.account_number),
        "payment_message": receipt["payment_message"],
    }
    return render(request, "rsvp/pay.html", context)


@never_cache
@sensitive_post_parameters()
@require_POST
def rsvp_total(request: HttpRequest, code: str) -> HttpResponse:
    """FR-33, AD-7, AD-12 (Story 2.3): the running total of step 3 or 4, `?steg=<slug>`.

    The script on the paid steps posts the step's form here on every change
    and swaps in the returned fragment. Three SELECTs: the resolver, the
    settings row and the members. An unknown code gives G1 with 404; after the
    deadline, and whenever `render_total` has no total to give, it is 204 with
    no body. It never sets a cookie and writes nothing.
    """
    actor = resolve_code(code)
    if actor is None:
        return _unknown_link(request)
    settings = site_settings()
    if is_past_deadline(settings.rsvp_deadline, timezone.now()):
        return HttpResponse(status=204)
    return render_total(
        request,
        actor=actor,
        members=household_members(actor.household),
        slug=request.GET.get("steg", ""),
        prices=form_prices(settings),
    )


# Error pages (Story 1.8, FR-5, FR-6, AD-15)
#
# config/urls.py sets handler404, handler500 and handler400 to these views, and
# CSRF_FAILURE_VIEW in config/settings.py points to csrf_failure, so a 400,
# 404, 500 or failed CSRF check never shows one of Django's own pages. There is
# no handler403: no guest view raises PermissionDenied. Under a valid link (the first path
# segment resolves) an error page shows the back button to the invitation and
# the footer band with the couple's phones; otherwise it shows nothing personal.

PAGE_NOT_FOUND = "guests/errors/not_found.html"
SERVER_ERROR = "guests/errors/server_error.html"
BAD_REQUEST = "guests/errors/bad_request.html"
CSRF_FAILURE = "guests/errors/csrf_failure.html"


def _reachable(request: HttpRequest) -> dict[str, object]:
    """FR-5, FR-6, AD-15: the code and the couple's contacts when the path starts with a valid link.

    The first segment of the path goes through the one resolver (AD-6): no query
    when it is not in the code format, one when it is, and one more for the
    settings row when it resolves. `{}` when it resolves to nobody.
    """
    segment = request.path_info.lstrip("/").split("/", 1)[0]
    # The error page must never fail itself (FR-5): any error in the lookup, such
    # as a broken database, gives the impersonal page. It is logged once here,
    # since on a 404 or a CSRF failure nothing else would log it; the LOGGING
    # handlers mask the link code (AD-15).
    try:
        actor = resolve_code(segment)
        if actor is None:
            return {}
        return {"code": actor.guest.code, "contacts": footer_contacts(site_settings())}
    except Exception as error:
        # On a 404 the error is raised while Django handles its Resolver404, whose
        # text holds the path without a leading slash, which the mask cannot
        # find; it says nothing about the lookup, so it is left out of the log.
        error.__suppress_context__ = True
        logger.warning("Error page lookup failed for %s", request.path_info, exc_info=True)
        return {}


@never_cache
def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """FR-5, FR-6, AD-15: handler404, for every address that is not a page.

    Without a valid code it is G1 with 404, the same page as `/`, so an unknown
    address tells nothing. Under a valid link it is «Vi finner ikke denne siden»
    with the back button and the phones. The host is already checked by then, so
    it renders with the request.
    """
    context = _reachable(request)
    if not context:
        return _unknown_link(request)
    return render(request, PAGE_NOT_FOUND, context, status=404)


def _rsvp_after_csrf_failure(request: HttpRequest) -> HttpResponse | None:
    """UX-DR52, AD-7: an RSVP step posted without a valid token, shown again; else None.

    Only for a POST to `guests:rsvp` or `guests:rsvp_step` (a known step) whose
    code resolves. While the form is open, the step is re-rendered with what
    was posted, a focused notice and status 403; no draft is written. After the
    deadline it is the closed page, as on every step address (AD-11).
    """
    if request.method != "POST":
        return None
    try:
        match = resolve(request.path_info)
    except Resolver404:
        return None
    if match.namespace != "guests" or match.url_name not in ("rsvp", "rsvp_step"):
        return None
    step = KEY_BY_SLUG.get(match.kwargs["slug"]) if "slug" in match.kwargs else "who"
    actor = resolve_code(match.kwargs["code"])
    if actor is None or step is None:
        return None
    settings = site_settings()
    if is_past_deadline(settings.rsvp_deadline, timezone.now()):
        # AD-11: after the deadline every step address shows the closed page.
        return render(request, RSVP_CLOSED, _guest_context(actor, settings))
    return render_after_csrf_failure(
        request,
        actor=actor,
        mount=_guest_mount(actor.guest.code),
        members=household_members(actor.household),
        step=step,
        prices=form_prices(settings),
        page_context=_guest_context(actor, settings),
    )


@never_cache
def csrf_failure(request: HttpRequest, reason: str = "") -> HttpResponse:
    """FR-5, FR-6, AD-15, UX-DR52: CSRF_FAILURE_VIEW, a form sent without a valid CSRF token.

    A step of the RSVP form is shown again with what the guest chose and a
    notice to try again (Story 2.1). Anything else gets «Skjemaet ble ikke
    sendt» with status 403; under a valid link with the back button and the
    phones. The host is already checked, so it renders with the request.
    `reason` is Django's technical cause and is never shown.
    """
    # The friendly page must never fail itself (FR-5): any error in the step's
    # re-render falls back to the generic page. It is logged once; the LOGGING
    # handlers mask the link code (AD-15).
    try:
        response = _rsvp_after_csrf_failure(request)
    except Exception:
        logger.warning("RSVP re-render after a CSRF failure failed", exc_info=True)
        response = None
    if response is not None:
        return response
    return render(request, CSRF_FAILURE, _reachable(request), status=403)


@never_cache
def server_error(request: HttpRequest) -> HttpResponse:
    """FR-5, FR-6, AD-15: handler500, «Noe gikk galt hos oss».

    Rendered without the request, because a 500 can come from a middleware before
    the host is checked: the link preview then leaves out og:image and nothing
    calls `request.get_host`. Under a valid link it has the back button and the
    phones; if the lookup fails as well, the impersonal page.
    """
    return HttpResponseServerError(render_to_string(SERVER_ERROR, _reachable(request)))


@never_cache
def bad_request(request: HttpRequest, exception: Exception) -> HttpResponse:
    """FR-5, AD-15: handler400, for a request Django cannot trust, such as a bad `Host`.

    Always impersonal: the request itself is untrusted, so the code is never
    looked up, and the page is rendered without the request, because
    `request.get_host` would raise the same `DisallowedHost` again.
    """
    return HttpResponseBadRequest(render_to_string(BAD_REQUEST))
