# Deferred work

Findings from build reviews that belong to a later story. Each entry names the spec that found it.

- source_spec: `.docs/implementation-artifacts/spec-1-4a-the-invitation-s-colours-type-buttons-and-notices.md`
  summary: A notice inserted after page load with `live=True` arrives with its text already inside the new `role="status"`/`role="alert"` element, which some screen readers do not announce; the story that first inserts notices with JavaScript should keep an empty live region in the page at load and put only the text into it.
  evidence: maybe-false, would be medium. Nothing inserts notices with JavaScript yet (all of 1.4a is server-rendered and JS-free), so it cannot be observed now. It is settled by testing the first in-page insertion (for example «Kopiert» in Story 2.7 or the conflict notice in Story 4.2) with NVDA and VoiceOver.

- source_spec: `.docs/implementation-artifacts/spec-1-4b-paper-rikke-s-images-and-the-private-invitation-page.md`
  summary: A wrong link with more than one path segment (for example `/hei/x/`) shows Django's own 404 page (with the URL list when DEBUG is on) instead of G1; Story 1.8 should set `handler404` to a G1-style page.
  evidence: low. Verified with the test client during the 1.4b review; the story only covers an unknown code or the bare address.

- source_spec: `.docs/implementation-artifacts/spec-1-4b-paper-rikke-s-images-and-the-private-invitation-page.md`
  summary: No manual check covers Safari, iOS or old iPads, where `filter: url(#edge-b3)` on `::before` and `background-blend-mode` with an SVG data-URI are weakest; the flat fallback is only claimed.
  evidence: medium. Claude can only drive Edge. Settled by Rikke opening `/` on an iPhone or iPad and checking the sheet shows the paper or the flat 5px cream fallback.

- source_spec: `.docs/implementation-artifacts/spec-1-4b-paper-rikke-s-images-and-the-private-invitation-page.md`
  summary: `admin/` (Story 3.1) and `robots.txt` (Story 1.4c) must be routed above the catch-all `<str:code>/`, and their tests must prove `/admin/` and `/robots.txt` do not render G1.
  evidence: medium. `<str:code>/` matches any single segment and APPEND_SLASH redirects `/admin` and `/robots.txt` to it; the rule lives only in the `config/urls.py` docstring.
  status: robots.txt done in Story 1.4c (routed above the guest include; `tests/test_guest_privacy.py` proves it is plain text, not G1). `admin/` stays with Story 3.1.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): the web server's or platform's own access log (gunicorn, nginx, the host's request log) writes the full path, link code included; it must mask the first segment the same way as `config/logging_filters.py` or be turned off (AD-15: production access logs must mask the code too).
  evidence: medium. Only Django's own loggers are masked; no production server is chosen yet, so its log cannot be configured or tested.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): behind a TLS proxy, set `SECURE_PROXY_SSL_HEADER` (and trust only the proxy's header), or `request.scheme` stays `http` and `og:image` says `http://`, which chat apps may refuse or fetch insecurely.
  evidence: medium. `tests/test_guest_privacy.py` proves the tag follows the request scheme (`secure=True` gives `https://`); the proxy setting depends on the host.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): if `SECURE_SSL_REDIRECT` is turned on, SecurityMiddleware answers the HTTP-to-HTTPS redirect itself, before `noindex_middleware` (which sits after it), so that redirect has no `X-Robots-Tag`. Either redirect at the proxy, or move the noindex middleware above SecurityMiddleware and test the redirect's headers.
  evidence: low. The redirect itself carries no page content, but AD-15 says every response; nothing redirects to HTTPS today.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Hosting (no story yet): MT-10 in `docs/manual-test-plan.md` (a test link pasted into Messenger and an SMS shows the watercolour, «Invitasjon» and the description, no names) can only run once the site has a public address.
  evidence: medium. The tags are tested; what each app actually shows is not.

- source_spec: `.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md`
  summary: Story 1.8: a 400 page for `DisallowedHost` (a request with a host not in `ALLOWED_HOSTS`) that extends `base.html` must not call `request.get_host` in the link preview, or it raises `DisallowedHost` again while rendering the error page. Render it without `request` (the preview then leaves out `og:image`) or give it its own template.
  evidence: medium. `link-preview.html` builds `og:image` from `request.get_host` whenever `request` is set; Django's default 400 page does not use our templates, so it cannot happen until 1.8 adds one.
