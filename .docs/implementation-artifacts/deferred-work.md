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
