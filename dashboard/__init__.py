"""The couple's and helpers' pages under `/admin/` (AD-10).

Story 3.1 adds the login, the logout, the admin frame and the Oversikt page. The
rules this package keeps (tests/test_architecture_imports.py): it never imports
`guests` or `wedding.rsvp`, and `guests` never imports it. The site-wide error
handlers that choose between the two sides live in `config/error_handlers.py`,
which is neither.
"""
