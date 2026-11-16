"""Only `wedding/services/` writes to the database (AD-3, Story 1.2).

The test reads every module in `config/`, `wedding/`, `guests/` and `dashboard/`
with `ast`, skipping `wedding/services/` and migrations, and fails on any call to
a method that writes through the ORM. It flags the method name on any receiver,
so it has no allow list; a later false positive (say `dict.update`) is narrowed in
the story that meets it. The scanner is itself tested on a deliberately bad module.
"""

import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCANNED_PACKAGES = ("config", "wedding", "guests", "dashboard")
WRITER_PACKAGE = Path("wedding", "services")
WRITE_METHODS = {
    "save",
    "delete",
    "create",
    "get_or_create",
    "update_or_create",
    "bulk_create",
    "bulk_update",
    "update",
}


def _is_scanned(relative: Path) -> bool:
    if "migrations" in relative.parts:
        return False
    return relative.parts[: len(WRITER_PACKAGE.parts)] != WRITER_PACKAGE.parts


def writer_calls(root: Path) -> list[str]:
    """List `file:line: .method()` for every write call outside the services under `root`.

    Sorted by file and line, so a failure reads like a list of places to fix.
    """
    found = []
    for package in SCANNED_PACKAGES:
        for path in sorted((root / package).rglob("*.py")):
            relative = path.relative_to(root)
            if not _is_scanned(relative):
                continue
            # utf-8-sig: Windows PowerShell 5.1 writes a BOM, which ast.parse rejects.
            source = path.read_text(encoding="utf-8-sig")
            for node in ast.walk(ast.parse(source, filename=str(path))):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr in WRITE_METHODS
                ):
                    found.append((relative.as_posix(), node.lineno, node.func.attr))
    return [f"{path}:{line}: .{method}()" for path, line, method in sorted(found)]


def test_no_code_outside_the_services_writes():
    """AD-3: views, commands, selectors, links and settings never write themselves."""
    assert writer_calls(BASE_DIR) == []


def test_scanner_catches_every_write_call(tmp_path):
    """AD-3: the scanner finds each write method, so a clean result means something."""
    for folder in [
        "config",
        "wedding/services",
        "wedding/migrations",
        "wedding/management/commands",
        "guests/migrations",
        "dashboard",
    ]:
        (tmp_path / folder).mkdir(parents=True)
    write_lines = [f"Guest.objects.{method}()" for method in sorted(WRITE_METHODS)]
    (tmp_path / "wedding" / "management" / "commands" / "bad.py").write_text(
        "\n".join(
            [
                "from wedding.models import Guest",
                "",
                *write_lines,
                "guest.save(update_fields=['name'])",
                "Guest.objects.filter(pk=1).update(name='x')",
                "",
                "def handle():",
                "    Guest(name='x').save()",
                "",
                "Guest.objects.all()",
                "Guest.objects.filter(code='x').exists()",
                "saved = guest.save",  # a reference, not a call
            ]
        ),
        encoding="utf-8-sig",  # with a BOM, as Windows PowerShell 5.1 writes files
    )
    (tmp_path / "dashboard" / "views.py").write_text("household.delete()\n", encoding="utf-8")
    (tmp_path / "config" / "settings.py").write_text("DEBUG = False\n", encoding="utf-8")
    for allowed in ["wedding/services/households.py", "wedding/migrations/0003_x.py"]:
        (tmp_path / allowed).write_text("Guest.objects.create()\n", encoding="utf-8")
    (tmp_path / "guests" / "migrations" / "0001_x.py").write_text("x.save()\n", encoding="utf-8")

    found = writer_calls(tmp_path)

    bad = "wedding/management/commands/bad.py"
    assert found == [
        "dashboard/views.py:1: .delete()",
        f"{bad}:3: .bulk_create()",
        f"{bad}:4: .bulk_update()",
        f"{bad}:5: .create()",
        f"{bad}:6: .delete()",
        f"{bad}:7: .get_or_create()",
        f"{bad}:8: .save()",
        f"{bad}:9: .update()",
        f"{bad}:10: .update_or_create()",
        f"{bad}:11: .save()",
        f"{bad}:12: .update()",
        f"{bad}:15: .save()",
    ]
