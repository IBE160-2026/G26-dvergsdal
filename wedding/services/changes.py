"""The couple's «Changed» marker (Story 4.1; FR-39, AD-19, AD-3).

`mark_changed` is the only code that writes `Household.changed_at`. The
services that change a sent answer call it inside their own transaction
(`send_answer` now; the couple's override and consent withdrawal later), so the
marker and the answer never disagree. It takes no actor of its own: its
caller has already checked who may write.
"""

from datetime import datetime

from wedding.models import Household


def mark_changed(household: Household, now: datetime) -> None:
    """FR-39, AD-19: record that `household`'s sent answer changed at `now`."""
    Household.objects.filter(pk=household.pk).update(changed_at=now)
