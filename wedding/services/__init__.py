"""The only code that writes to the database (AD-3).

Each service is one `transaction.atomic()` block and takes an explicit actor from
`wedding.actors`: a guest, an admin user or the system (seed command only). A
refused write raises an error from `exceptions.py` and writes nothing. Admin
writes check the role with `permissions.require_couple` (AD-10).
`tests/test_only_services_write.py` fails if code outside this package calls one
of the ORM write methods it lists (`save`, `delete`, `create`, `update` and their
bulk and get-or-create forms).
"""
