"""`wedding/rules/` stays pure: no Django and no other project code (AD-2).

The rules are the one place totals, counts and states are decided, so they must
run on plain values. This test reads every module's imports with `ast` instead of
importing it, and the scanner is itself tested on a deliberately bad module so
the check is not vacuous while the package is still empty.
"""

import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_PACKAGE = "wedding.rules"
FORBIDDEN_TOP_LEVEL = {"django", "config", "guests", "dashboard", "tests"}


def _module_name(path: Path, root: Path) -> str:
    """Dotted module name of `path`, relative to the folder that holds the `wedding` package."""
    parts = list(path.relative_to(root).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _imported_modules(path: Path, root: Path) -> list[str]:
    """Every module the file imports, with relative imports resolved to absolute names."""
    module = _module_name(path, root)
    is_package = path.name == "__init__.py"
    package = module.split(".") if is_package else module.split(".")[:-1]
    names = []
    # utf-8-sig: Windows PowerShell 5.1 writes a BOM, which ast.parse rejects.
    source = path.read_text(encoding="utf-8-sig")
    for node in ast.walk(ast.parse(source, filename=str(path))):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = [] if node.level == 0 else package[: len(package) - (node.level - 1)]
            parent = [*base, *([node.module] if node.module else [])]
            # `from wedding import models` imports `wedding.models`, so name each alias.
            names.extend(".".join([*parent, alias.name]) for alias in node.names)
    return names


def _is_forbidden(name: str) -> bool:
    top = name.split(".")[0]
    if top in FORBIDDEN_TOP_LEVEL:
        return True
    if top == "wedding":
        return not (name == RULES_PACKAGE or name.startswith(RULES_PACKAGE + "."))
    return False


def forbidden_imports(rules_dir: Path, root: Path) -> list[str]:
    """List `file: module` for every import under `rules_dir` that breaks AD-2."""
    return [
        f"{path.relative_to(root).as_posix()}: {name}"
        for path in sorted(rules_dir.rglob("*.py"))
        for name in _imported_modules(path, root)
        if _is_forbidden(name)
    ]


def test_rules_import_nothing_from_django_or_the_project():
    """AD-2, NFR-2: rule functions take plain values and import no Django or project code."""
    rules_dir = BASE_DIR / "wedding" / "rules"
    assert (rules_dir / "__init__.py").is_file()
    assert forbidden_imports(rules_dir, BASE_DIR) == []


def test_scanner_catches_bad_imports(tmp_path):
    """AD-2: the scanner finds every kind of forbidden import, so a clean result means something."""
    rules_dir = tmp_path / "wedding" / "rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "__init__.py").write_text("", encoding="utf-8")
    (rules_dir / "totals.py").write_text("", encoding="utf-8")
    (rules_dir / "bad.py").write_text(
        "\n".join(
            [
                "import math",
                "from datetime import date",
                "from wedding.rules import totals",
                "from wedding import rules",
                "from . import totals as same_package",
                "import django",
                "from django.db import models",
                "import config.settings",
                "from guests import views",
                "from dashboard.views import overview",
                "from tests import helpers",
                "from wedding import models as wedding_models",
                "from wedding.services import send_answer",
                "from .. import selectors",
                "",
                "def total():",
                "    from wedding.models import Guest",
                "    return Guest",
            ]
        ),
        encoding="utf-8-sig",  # with a BOM, as Windows PowerShell 5.1 writes files
    )

    found = forbidden_imports(rules_dir, tmp_path)

    assert found == [
        "wedding/rules/bad.py: django",
        "wedding/rules/bad.py: django.db.models",
        "wedding/rules/bad.py: config.settings",
        "wedding/rules/bad.py: guests.views",
        "wedding/rules/bad.py: dashboard.views.overview",
        "wedding/rules/bad.py: tests.helpers",
        "wedding/rules/bad.py: wedding.models",
        "wedding/rules/bad.py: wedding.services.send_answer",
        "wedding/rules/bad.py: wedding.selectors",
        "wedding/rules/bad.py: wedding.models.Guest",
    ]
