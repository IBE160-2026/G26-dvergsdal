"""`guests`, `dashboard` and `wedding.rsvp` never import each other the wrong way (Story 3.1).

The architecture keeps the guest side and the couple's side apart: `dashboard`
imports neither `guests` nor `wedding.rsvp` (yet), `guests` does not import
`dashboard`, and `wedding.rsvp` imports neither `guests` nor `dashboard`; `guests`
may import `wedding.rsvp`, since it mounts the form (AD-1, AD-7, AD-10; epic 1
retrospective D1, epic 2 A1). `config/error_handlers.py` imports both and is
neither, so it is not scanned. `wedding.rules` keeps its own purity test
(tests/test_rules_purity.py). The scanner reads the imports with `ast`, as that
test does, and is itself tested on a deliberately bad module.
"""

from pathlib import Path

import pytest

from tests.test_rules_purity import BASE_DIR, _imported_modules

# package folder, imports it must not have (a name or a dotted prefix)
RULES = [
    (BASE_DIR / "dashboard", ("guests", "wedding.rsvp")),
    (BASE_DIR / "guests", ("dashboard",)),
    (BASE_DIR / "wedding" / "rsvp", ("guests", "dashboard")),
]


def _matches(name: str, forbidden: tuple[str, ...]) -> bool:
    return any(name == prefix or name.startswith(prefix + ".") for prefix in forbidden)


def forbidden_imports(package: Path, forbidden: tuple[str, ...], root: Path) -> list[str]:
    """`file: module` for every import under `package` that starts with a forbidden name."""
    return [
        f"{path.relative_to(root).as_posix()}: {name}"
        for path in sorted(package.rglob("*.py"))
        for name in _imported_modules(path, root)
        if _matches(name, forbidden)
    ]


@pytest.mark.parametrize(("package", "forbidden"), RULES, ids=lambda value: str(value))
def test_no_forbidden_import(package, forbidden):
    """AD-1, AD-7, AD-10: the three packages keep to the one-way rules above."""
    assert any(package.rglob("*.py")), f"{package} has no modules to check"
    assert forbidden_imports(package, forbidden, BASE_DIR) == []


def test_the_scanner_finds_every_form_of_a_forbidden_import(tmp_path):
    """The check is not vacuous: plain, from, aliased and relative imports are all found."""
    package = tmp_path / "dashboard"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "bad.py").write_text(
        "import guests.views\n"
        "from guests import urls\n"
        "from wedding.rsvp.steps import KEYS\n"
        "from wedding import rsvp\n"
        "import wedding.models\n",
        encoding="utf-8",
    )

    found = forbidden_imports(package, ("guests", "wedding.rsvp"), tmp_path)

    assert found == [
        "dashboard/bad.py: guests.views",
        "dashboard/bad.py: guests.urls",
        "dashboard/bad.py: wedding.rsvp.steps.KEYS",
        "dashboard/bad.py: wedding.rsvp",
    ]
