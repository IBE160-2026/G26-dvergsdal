"""The consent text's version (Story 2.4; FR-26, FR-29, AD-18).

AD-18: each recorded consent names the version of the text the guest read.
The text is `wedding/rsvp/templates/rsvp/includes/consent_text.html`; change
this constant in the same commit as the text (a test pairs the version with
a hash of the template). Story 2.6b records it with each `Consent`
(`wedding.services.answers.send_answer`).
"""

CONSENT_TEXT_VERSION = "2026-11-23"
