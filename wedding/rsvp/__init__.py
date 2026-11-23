"""The one RSVP form: steps, forms, templates and the draft cookie (AD-7, AD-8).

Mounted for guests at `/<code>/svar/` (guests/views.py, Story 2.1) and later
for the couple's override (Story 4.4), with the actor passed in. `steps.py` is
the step registry and `FormMount`, `draft.py` the signed draft cookie,
`forms.py` the step forms, `views.py` the step handling every mount calls, and
`templates/rsvp/` the step templates. Which steps apply and the deadline are
pure rules in `wedding.rules` (AD-2).
"""
