"""The admin nav: Oversikt, Gjester, Betalinger, Innstillinger (UX-DR34, FR-46).

An item without a `url_name` is shown as plain text until the story that builds
its page adds one, so the frame shows the final nav without a dead link: Gjester
comes in Story 3.4, Betalinger in Story 5.3 and Innstillinger in Story 4.5.
«Logg ut» is a POST button in the template, not an item here.
"""

from dataclasses import dataclass

from django.urls import reverse


@dataclass(frozen=True)
class NavItem:
    """One word of the admin nav. `url_name` is None until its page exists."""

    key: str
    label: str
    url_name: str | None = None


NAV_ITEMS = (
    NavItem("home", "Oversikt", "dashboard:home"),
    NavItem("guests", "Gjester"),
    NavItem("payments", "Betalinger"),
    NavItem("settings", "Innstillinger"),
)


def nav_items(current: str | None) -> list[dict[str, object]]:
    """UX-DR34: the nav for a template, with the page that is open (`current`) marked.

    Each entry has `label`, `url` (None for an unbuilt page) and `current`.
    """
    return [
        {
            "label": item.label,
            "url": reverse(item.url_name) if item.url_name else None,
            "current": item.key == current,
        }
        for item in NAV_ITEMS
    ]
