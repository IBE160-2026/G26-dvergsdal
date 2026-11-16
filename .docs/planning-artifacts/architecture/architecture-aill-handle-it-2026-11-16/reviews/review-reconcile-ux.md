---
title: "Reconcile: ARCHITECTURE-SPINE.md against the UX spines"
reviewed: ../ARCHITECTURE-SPINE.md (status draft, 2026-11-16), rationale in ../.memlog.md
against:
  - ../../../ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md (final, updated 2026-11-16)
  - ../../../ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md (final, updated 2026-11-15)
date: 2026-11-16
scope: UX behaviours and constraints the architecture must support, where the spine is silent or contradicts the UX, and where two independently built stories could diverge. Per-screen detail is out of scope.
---

# Reconcile: architecture spine vs UX

## Verdict

The spine's structure (server-rendered monolith, pure rules, services as sole writers, deadline function, self-hosted assets) fits the UX well, and the closure of open question 5 is consistent. But four UX behaviours have no architectural home and will split between stories: the admin's **confirm-with-consequence dialogs and undo-in-place**, **A7 (the couple answering through "the same form guests use")**, the **running total that updates on every change**, and the **draft cookie's real role as the form's working state**. The closure of **open question 6 rests on a privacy premise that the chosen design does not meet** (allergy data does reach the server before consent, it just is not stored), so Rikke's "A" should be re-confirmed on accurate wording.

## Closures of UX open questions 4–6

| OQ | What EXPERIENCE.md asks | What the spine says | Consistent? |
|---|---|---|---|
| 4 No-JS guest pages in v1 | Should all guest pages and form steps work without scripts, scripts only enhancing? | AD-7: yes, every guest page and step works without JS. | **Mostly.** The answer is yes, but EXPERIENCE › Responsive & Platform still says "draft, running-total updates and copy need scripts", and Component Patterns › Running total says "recalculated on every change, announced politely". The spine makes the draft work without JS (good) but is silent on the running total, which it cannot do live without either a JS price copy (forbidden by AD-7's *Prevents*) or a server fragment endpoint (forbidden by AD-1's "no JSON API"). See F3. EXPERIENCE needs the No-JS row and G2 "Static fallback [2027]" updated to match. |
| 5 Admin session expiry | ≥ 20 h idle, or a two-minute warning; in both cases, is unsaved input restored? | AD-13: 20 h sliding, no warning, no restore, "Logg ut" everywhere. | **Yes.** Two small follow-ups: State Patterns › Save failed says "Input kept, also when the cause is an expired form token" for *any submit*; AD-13 says no restore for admin, so EXPERIENCE should scope that line to guest pages. A1's "expired" state («Du ble logget ut fordi du var borte en stund.») needs a way to tell "expired" from "never logged in" (F11). |
| 6 Device draft content | May the draft hold allergy categories and notes before consent, on a phone others may use? UX default: deleted on send, on "Begynn på nytt" and at the deadline. | AD-8: yes, a signed compressed cookie holds everything; deleted on send / "Begynn på nytt", expires at deadline; "Prevents … allergy data reaching the server before consent". Memlog: "It never leaves the device before 'Send answer'". | **No, on the premise.** See F4. The decision itself (A) may stand, but the stated guarantee is not true of a cookie plus server-rendered steps, and the deletion "at the deadline" collides with the locked-state UX (F5). |

## Findings

Severity: **high** = stories will diverge or the spine contradicts an approved UX behaviour; **medium** = likely divergence, cheap to pin now; **low** = note or small gap.

### F1 (high) — Confirm-with-consequence dialogs and undo-in-place have no mechanism

- **UX:** EXPERIENCE › Admin protection tiers (tier 2 dialog states the consequence: "Da er 900 kr av 900 kr mottatt, og Synne står som betalt", "how many households are locked out" on a deadline change, "number of households whose total changes" on a price change, FR-64/65); Component Patterns › Dialog (`role="alertdialog"`, focus to safe button, on confirm focus moves to a `role="status"` result message); Undo (in place) and Attention item ("row replaced in place by «Merket som håndtert. Angre»; stays until the page is left"); A9 «Registrert: mottatt 300 kr.» + «Angre»; guest consent withdrawal dialog (G11/G12) and the guest leave warning.
- **Gap:** The consequence text must be computed by `rules/` from a *hypothetical* write (new status after this payment, households locked by this deadline) before anything is saved. The spine says nothing about how. One story will do it with a JS `fetch` to a preview endpoint (a JSON API, against AD-1), another with a server-rendered confirm page, a third will duplicate the rule in JS. Likewise "undo in place until the page is left" needs a transient "just marked" state across POST-redirect-GET, which one story will put in the query string, another in `django.contrib.messages`, another in JS. AD-7's no-JS rule binds only the guest RSVP form, so it is also unstated whether admin pages and the guest consent-withdrawal dialog must work without JS.
- **Fix (one rule, e.g. AD-18 "Confirm and undo"):** Tier-2/3 actions are a two-POST pattern: the first POST validates and calls a *preview* function in `rules/`/`selectors` (no write) and re-renders the page with the dialog open as server HTML (`<dialog open>` or a dialog section); the second POST confirms and calls the service. JS only adds focus trap/Esc/scrim. Result and undo state travels by one chosen mechanism (e.g. `messages` framework with a structured payload naming the undoable entry id). State whether admin pages must work without JS (recommend yes, same as guests, since it costs nothing with this pattern). The guest withdrawal dialog uses the same pattern.

### F2 (high) — A7 "the same form guests use" contradicts the module boundaries and lock rule

- **UX:** A7 "Household answer via the guest form — admin as author, also after deadline (FR-63)"; UJ-3 step 5 "the same form guests use … recorded with Rikke as author"; A7 states: edit · after deadline · conflict; A6 Svar panel "who sent and when"; status block «Sendt av <name> …»; Last updated «Sist endret av Arild, 3. november kl. 18:40» (FR-38).
- **Gap/contradiction:** The guest form lives in `guests/` under `/<code>/`, a request counts as a guest request *only* through a link (AD-10), guest views run the lock check (AD-11), and `guests` and `dashboard` may never import each other. So "the same form" cannot be reused by `dashboard` without breaking a rule, and an admin cannot use the guest URLs without being treated as a guest (and locked out after the deadline). The likely outcome is a second copy of the step forms and step templates in `dashboard/` that drifts. Separately, the ER sketch and AD-4's stored-facts list have no "sent by (guest *or* admin user) and when" per revision, which the status block, the last-updated notice, the conflict notice (FR-38 "who, when") and A6 all display; nor is it said where A7's unsent draft lives (the AD-8 cookie is scoped to `/<code>/`).
- **Fix:** Move the step definitions (form classes, step order/sequencing calls into `rules/`, step template partials) to a shared place in `wedding/` (e.g. `wedding/rsvp/`), used by both `guests/` and `dashboard/`. `send_answer` takes an author that is either a `Guest` or an admin `User` and an explicit `override_lock` flag that the service allows only for the `couple` role (AD-10/AD-11). Add "who sent and when" to AD-4's stored facts and the ER sketch. State where A7's working state lives (session for admins is natural, since admins have one).

### F3 (high) — Running total "recalculated on every change" has no allowed implementation

- **UX:** Component Patterns › Running total ("Recalculated on every change, announced politely; removed choices drop out (FR-75); identical on check page and receipt (FR-33)"); Accessibility Floor › Announcements (live region for the running total); UJ-1 step 4 "Running total updates".
- **Contradiction:** AD-7 computes the total on the server per step POST and explicitly prevents "a JavaScript copy of … what it costs". AD-1 forbids a JSON API for the site's own pages. So within a step the total cannot change until "Fortsett". One story will keep it per-step (silently deviating from UX), another will add a price table in JS (violating AD-7).
- **Fix:** Decide one: (a) the total updates on step submit only and EXPERIENCE is changed (the polite live region then applies only if a later enhancement exists), or (b) an explicit, narrow exception: a no-write POST endpoint that returns a server-rendered HTML fragment of the total from `rules/`, used only as enhancement. Record which in the spine; (a) is the simpler fit for the course version.

### F4 (high) — OQ6 closure states a privacy guarantee the design does not give

- **UX:** State Patterns › Draft on device "nothing reaches the server before «Send svaret»"; Interaction Primitives › Unsent answer kept "kept on the guest's own device"; Consent & Privacy UX "The unsent draft stays on the guest's device only"; OQ6 framed as a device question. Memlog: "It never leaves the device before 'Send answer'"; AD-8 *Prevents*: "allergy data reaching the server before consent".
- **Contradiction:** With server-rendered steps (AD-7), the allergy step is POSTed to the server, and the signed cookie is then sent back to the server with every request under `/<code>/`. The server *receives and processes* allergy categories and notes before consent on every step; it only does not *store* them. `django.core.signing` signs, it does not encrypt, so the cookie content is readable on the device (acceptable under OQ6) and in transit/request dumps. Rikke chose "A" on the "never leaves the device" framing, so the decision was made on an inaccurate premise (sensorveiledning criterion 1 values exactly this kind of traceable correction).
- **Fix:** (1) Reword AD-8's *Prevents* and the memlog to "no allergy data is **stored** on the server before 'Send answer' with consent"; (2) add a rule that the draft cookie and allergy POST fields are excluded from logs and error reports (a custom `SafeExceptionReporterFilter` / `sensitive_post_parameters`, and AD-15's log rule extended to request bodies and cookies); cookie `HttpOnly`, `Secure` in production, `SameSite=Lax`; (3) re-confirm OQ6 with Rikke on the accurate wording and update EXPERIENCE's three sentences and the privacy page text («Hva vi lagrer») to match.

### F5 (medium) — The draft cookie is the form's working state, not just a draft

- **UX:** Interaction Primitives › Unsent answer kept ("Every change in the form is kept", the Draft offer is shown "by any route (either Svar, the RSVP button, or a reload of a step)", it records "when it was started"; "Where device storage is unavailable (private mode, no scripts) there is no draft and the leave warning is the only guard"); State Patterns › Locked after deadline ("A waiting draft is not offered; the notice says the answer was not sent and to call the couple"); Leave warning text «Det du har fylt ut, er tatt vare på på denne telefonen.»; Responsive › In-app browsers (Messenger must work).
- **Gaps:**
  1. Since nothing is written to the database before send (AD-8), the cookie is the only place the answers to earlier steps live. If cookies are blocked (some in-app or privacy browsers), the multi-step form does not just lose its draft, it cannot be completed at all. The spine has no fallback (e.g. hidden fields carrying the signed state in the form itself, or a clear message) and no rule for detecting it.
  2. Granularity: the cookie is updated per step POST, so input typed within a step is lost on reload, which the leave-warning text and "every change is kept" promise. Either the UX wording is narrowed to "every finished step" or an enhancement writes in-step changes (which cannot sign the cookie client-side). Pin it.
  3. When the Draft offer appears: a reload of a step after PRG is indistinguishable from arriving by redirect, so "offer on a reload of a step" needs a server rule (e.g. offer only on the form's entry URL and when the draft's "last step" differs from the requested step; a fresh browser session marker). Two stories (form entry, draft offer) will otherwise pick different triggers.
  4. Expiry at the deadline contradicts the locked-state UX: once the browser drops the cookie at the deadline, the server cannot say "your answer was not sent". Also the couple can move the deadline (A12, FR-64), so a max-age set at the old deadline is wrong in both directions.
- **Fix:** In AD-8: the cookie max-age is a backstop only (e.g. deadline + some days, or the wedding date); the server decides with AD-11's `is_locked` whether a draft is offered or shown as "not sent, call us", and deletes it then. Add `started_at` and `last_step` to the draft payload and a single rule for when the offer is shown. Decide the no-cookie fallback (recommend: signed state in a hidden field, which also makes the steps cookie-independent) and update EXPERIENCE's "no draft without scripts" line, which the cookie design already makes untrue.

### F6 (medium) — Double submits: own answer shown as a conflict; payments registered twice

- **UX:** Primary button "On submit it shows «Sender …» and ignores repeat taps until the server answers **[ASSUMPTION]**" (JS-only); State Patterns › Saving; WCAG 2.2.1 line "a send rejected for any reason keeps every answer, and pressing again works"; A9 "Registrer" (tier 2, undoable).
- **Gap:** Without JS, or on a slow 4G double tap, two "Send svaret" POSTs arrive with the same draft revision. Under AD-9 the second one finds the revision changed and shows the guest a conflict with *their own* answer. In admin, a double "Registrer" creates two `Payment` rows. "Pressing again works" after a failure also needs to be safe if the first attempt actually committed.
- **Fix:** Add an idempotency rule to AD-3/AD-9: each rendered write form carries a one-time token (for the RSVP, a draft id in the cookie); a service seeing a token it already committed returns the earlier result (redirect to the receipt / the "Registrert" message) instead of a conflict or a second row.

### F7 (medium) — Error pages and expired CSRF tokens

- **UX:** FR-6 via EXPERIENCE Navigation ("The footer band with phone numbers and «Personvern» is on every valid-link page, including error pages"); State Patterns › Save failed ("what happened, that nothing is lost, «Prøv igjen», and (guest side) the couple's phone numbers. Input kept, also when the cause is an expired form token"); UJ-3 Failure "any error page still shows the couple's phone numbers".
- **Gap:** Django's default CSRF failure is a bare 403 that loses the POST, and default 404/500 handlers know nothing about the link or the contacts. Contacts live in the `Settings` row (AD-4), which a 500 page cannot safely query. The spine's Errors convention covers service exceptions only.
- **Fix:** One rule: custom `CSRF_FAILURE_VIEW` that, for guest step URLs, re-renders the step with the submitted values and a "Prøv igjen" notice; custom `handler404`/`handler500` templates that show the footer; for the 500 page, the contact numbers come from a static source that needs no database (e.g. environment/settings value, or a cached copy), stated explicitly. 404 under a valid code shows the footer, under an invalid code shows G1.

### F8 (medium) — Which writes the deadline lock gates is not stated

- **UX:** State Patterns › Locked after deadline ("Payment, «Jeg har betalt», info and consent withdrawal still work (FR-42)"); Consent & Privacy UX ("it works after the deadline"); G9.
- **Gap:** AD-11 says every lock check calls one function, but not *which* services check it. A story building consent withdrawal or the "Jeg har betalt" report could reasonably add a lock check and break FR-42.
- **Fix:** In AD-11 list the lock-gated services (send/change answer: attendance, days, meals, overnight, hike, allergies) and state that payment reports, consent withdrawal and all couple writes are never lock-gated, with a test per exempt service.

### F9 (medium) — Helper restrictions on *reading* are not covered

- **UX:** A6 "Only the couple can copy links. Helpers can neither see nor copy them"; Surface coverage A6 "read-only (no links, no buttons)"; State Patterns › Helper read-only (buttons hidden, forms show values as text, the «Du kan se alt, men ikke endre noe.» line); A12 "helpers read".
- **Gap:** AD-10 enforces roles in write services only. Hiding link codes from helpers is a *read* restriction that no service touches, so it depends on each template remembering it (and a helper could still reach a code through any other page that renders it, e.g. a test-link list or A7). Templates may also test the role in different ways.
- **Fix:** Add to AD-10: link codes are returned only by a selector that requires the `couple` role (helpers get `None`), and one template context flag (e.g. `can_edit` from a context processor) drives the read-only rendering and the helper line on every admin page. Add a test that no helper response contains a link code.

### F10 (low–medium) — Identity of a "handled" attention item

- **UX:** Attention item / Undo (in place) / «Vis håndterte» (unmark later); A2 states; PRD addendum "Needs attention behaviour" (leave rules per item).
- **Gap:** The spine stores "Needs attention handled marks" but not what a mark is attached to. If it is attached to the household only, a *new* mismatch or a *new* change after a mark stays hidden; if attached to the specific fact (report id, answer revision), it reappears correctly. The attention panel story and the payment/answer stories will choose differently. Also, attention membership is a derived value but is not listed among AD-2's rule outputs.
- **Fix:** State that attention membership is computed in `rules/` (AD-2) and that a handled mark records the item kind plus the fact it refers to (e.g. revision number or payment-report id) and who/when (PRD review PM-21). Note the PRD addendum says "Refund owed" leaves only when the refund is registered, while EXPERIENCE gives every item a "Merk som håndtert" action; that UX/PRD mismatch should be settled in EXPERIENCE.

### F11 (low) — Smaller gaps

- **Map link** (EXPERIENCE › Info sheet, explicitly delegated: "[ASSUMPTION — which map service and whether it leaves the site: architecture, privacy page]"). The spine does not answer it. Suggest a line under AD-15: outbound map link with the venue address only, opened as a normal link (no embed or iframe), covered by `Referrer-Policy: no-referrer`; name the service; the privacy page says it leaves the site.
- **Session expired message** (A1 "expired"): Django cannot tell an expired session from no session by default. One line in AD-13 (e.g. a non-secret "was logged in" cookie, or check for a stale session cookie) keeps the login story from inventing it.
- **Envelope reveal [If time]** needs "first visit only" per device, but FR-3 forbids writes on GET; say it is a client-side `localStorage` flag (UX already skips it without storage) so it is not confused with AD-8's "no localStorage" intent.
- **Fonts** (DESIGN › Typography): self-hosting is covered by AD-15. DESIGN adds "WOFF2 Latin subsets including æ, ø, å, keeping the `lnum` and `tnum` features"; with "no build step", say the subset files are generated once by a committed script and committed, and the subsetting must keep `lnum`/`tnum` (default subsetters drop unused features).
- **"Endret" on consent withdrawal:** EXPERIENCE says a guest's withdrawal tags the household «Endret» in admin. AD-3 lists the Changed marker and withdrawal deletion as side effects, but not that withdrawal itself sets the marker. One clause in AD-3 avoids divergence.
- **Reduced motion and animation:** no gap. The only motion is CSS smooth scroll under `prefers-reduced-motion: no-preference` and the [If time] envelope, both client-side.
- **Admin on phone** (FR-48, "quick tasks fit one screen", tables become stacked rows, A4 search "on submit" with a polite live region): no architectural gap; fits AD-1. The «Vis alle n» expansion needs no JS (a query parameter), which F1's rule would cover if it states admin works without JS.

## Not flagged (checked and consistent)

AD-6 `/<code>/` and G1 for unknown codes and bare `/`; AD-11 Oslo time and deadline wording; AD-12 whole kroner and the "1 450 kr" display; AD-15 noindex, no-referrer, name-free titles (matches Accessibility Floor › Page titles); AD-9's conflict notice (who, when, what differs) matches State Patterns › Conflict; AD-13 matches OQ5; the light-only and contrast rules need nothing from the architecture beyond AD-1's single CSS file with tokens.
