"""Settings come from the environment and production refuses unsafe values (AD-14, NFR-8, NFR-4).

The helpers in `config/env.py` are tested directly for every row of the Story 1.1
I/O matrix. `config/settings.py` is then executed fresh for the same rows, and a
subprocess proves that a refusal really stops `manage.py` from starting.
"""

import os
import runpy
import subprocess
import sys
from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured

from config.env import (
    LOCAL_ALLOWED_HOSTS,
    LOCAL_SECRET_KEY,
    production_problems,
    read_bool,
    read_list,
    read_str,
    refusal_message,
    validate_app_env,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_FILE = BASE_DIR / "config" / "settings.py"
ENV_VARS = ("APP_ENV", "DEBUG", "SECRET_KEY", "ALLOWED_HOSTS")
REAL_KEY = "a-long-random-production-key-for-tests-only-0123456789"


# The helpers in config/env.py


def test_app_env_defaults_to_local_when_unset_or_empty():
    """NFR-8: the examiner needs no `.env`; unset and empty both mean local."""
    assert validate_app_env(None) == "local"
    assert validate_app_env("") == "local"
    assert validate_app_env("local") == "local"
    assert validate_app_env("production") == "production"


@pytest.mark.parametrize("value", ["prod", "Production", "PRODUCTION", "dev", "local "])
def test_unknown_app_env_is_refused_with_the_allowed_values(value):
    """AD-14: an allow list, so a misspelled production never falls back to local defaults."""
    with pytest.raises(ImproperlyConfigured) as excinfo:
        validate_app_env(value)
    message = str(excinfo.value)
    assert "APP_ENV" in message
    assert "«local»" in message
    assert "«production»" in message


@pytest.mark.parametrize(
    ("value", "expected"),
    [("true", True), ("True", True), ("1", True), ("on", True), ("false", False), ("0", False)],
)
def test_read_bool_parses_common_spellings(value, expected):
    """AD-14: DEBUG is read from the environment."""
    assert read_bool({"DEBUG": value}, "DEBUG", default=not expected) is expected


def test_read_bool_uses_default_when_unset_or_empty():
    """AD-14: an unset or empty variable gives the safe default."""
    assert read_bool({}, "DEBUG", default=True) is True
    assert read_bool({"DEBUG": ""}, "DEBUG", default=False) is False


def test_read_bool_refuses_an_unreadable_value():
    """AD-14: a value that is neither true nor false names the variable instead of guessing."""
    with pytest.raises(ImproperlyConfigured, match="DEBUG"):
        read_bool({"DEBUG": "maybe"}, "DEBUG", default=False)


def test_read_list_splits_on_commas_and_drops_blanks():
    """AD-14: ALLOWED_HOSTS is a comma-separated list."""
    environ = {"ALLOWED_HOSTS": " example.com, www.example.com ,,"}
    assert read_list(environ, "ALLOWED_HOSTS", default=[]) == ["example.com", "www.example.com"]
    assert read_list({"ALLOWED_HOSTS": " "}, "ALLOWED_HOSTS", default=["x"]) == ["x"]


def test_read_str_uses_default_when_unset_or_empty():
    """AD-14: an empty SECRET_KEY means the local default, never an empty key."""
    assert read_str({}, "SECRET_KEY", default="d") == "d"
    assert read_str({"SECRET_KEY": ""}, "SECRET_KEY", default="d") == "d"
    assert read_str({"SECRET_KEY": "k"}, "SECRET_KEY", default="d") == "k"


def test_production_with_safe_values_has_no_problems():
    """AD-14, matrix row "Prod, all set"."""
    assert production_problems(False, REAL_KEY, ["example.com"]) == []


def test_production_with_debug_on_names_debug():
    """AD-14, matrix row "Prod, DEBUG on"."""
    problems = production_problems(True, REAL_KEY, ["example.com"])
    assert len(problems) == 1
    assert "DEBUG" in problems[0]


@pytest.mark.parametrize("key", [LOCAL_SECRET_KEY, "", "   "])
def test_production_with_default_or_missing_key_names_secret_key(key):
    """AD-14, matrix row "Prod, default key"."""
    problems = production_problems(False, key, ["example.com"])
    assert len(problems) == 1
    assert "SECRET_KEY" in problems[0]


def test_production_without_hosts_names_allowed_hosts():
    """AD-14, matrix row "Prod, no hosts"."""
    problems = production_problems(False, REAL_KEY, [])
    assert len(problems) == 1
    assert "ALLOWED_HOSTS" in problems[0]


def test_several_problems_are_listed_in_one_message():
    """AD-14, matrix row "Several problems": one restart shows everything to fix."""
    message = refusal_message(production_problems(True, LOCAL_SECRET_KEY, []))
    assert "APP_ENV=production" in message
    for name in ("DEBUG", "SECRET_KEY", "ALLOWED_HOSTS"):
        assert name in message


# config/settings.py itself, executed fresh for each matrix row


def load_settings(monkeypatch, **env):
    """Execute `config/settings.py` with exactly the given variables and return its names."""
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    return runpy.run_path(str(SETTINGS_FILE))


def test_zero_config_gives_safe_local_defaults(monkeypatch):
    """NFR-8, matrix row "Zero config": no variables and no `.env` still runs locally."""
    settings = load_settings(monkeypatch)
    assert settings["APP_ENV"] == "local"
    assert settings["DEBUG"] is True
    assert settings["SECRET_KEY"] == LOCAL_SECRET_KEY
    assert settings["ALLOWED_HOSTS"] == LOCAL_ALLOWED_HOSTS == ["localhost", "127.0.0.1", "[::1]"]


def test_env_example_lists_every_setting_and_runs_locally(monkeypatch):
    """AD-14: `.env.example` names exactly the settings read, and its values start the app."""
    example = {}
    for line in (BASE_DIR / ".env.example").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            name, _, value = line.partition("=")
            example[name.strip()] = value.strip()
    assert sorted(example) == sorted(ENV_VARS)

    settings = load_settings(monkeypatch, **example)
    assert settings["APP_ENV"] == "local"
    assert settings["DEBUG"] is True
    assert settings["SECRET_KEY"] == LOCAL_SECRET_KEY
    assert settings["ALLOWED_HOSTS"] == LOCAL_ALLOWED_HOSTS


def test_production_with_safe_values_starts_with_debug_off(monkeypatch):
    """AD-14, matrix row "Prod, all set": DEBUG unset means off in production."""
    settings = load_settings(
        monkeypatch, APP_ENV="production", SECRET_KEY=REAL_KEY, ALLOWED_HOSTS="example.com"
    )
    assert settings["DEBUG"] is False
    assert settings["ALLOWED_HOSTS"] == ["example.com"]


@pytest.mark.parametrize(
    ("env", "named"),
    [
        (
            {"DEBUG": "true", "SECRET_KEY": REAL_KEY, "ALLOWED_HOSTS": "example.com"},
            ["DEBUG"],
        ),
        ({"ALLOWED_HOSTS": "example.com"}, ["SECRET_KEY"]),
        ({"SECRET_KEY": REAL_KEY}, ["ALLOWED_HOSTS"]),
        ({"SECRET_KEY": REAL_KEY, "ALLOWED_HOSTS": ""}, ["ALLOWED_HOSTS"]),
        ({"DEBUG": "true"}, ["DEBUG", "SECRET_KEY", "ALLOWED_HOSTS"]),
    ],
    ids=["debug-on", "default-key", "no-hosts", "empty-hosts", "all-three"],
)
def test_production_refuses_unsafe_settings(monkeypatch, env, named):
    """AD-14: production refuses to start and names every problem."""
    with pytest.raises(ImproperlyConfigured) as excinfo:
        load_settings(monkeypatch, APP_ENV="production", **env)
    message = str(excinfo.value)
    for name in named:
        assert name in message
    for name in {"DEBUG", "SECRET_KEY", "ALLOWED_HOSTS"} - set(named):
        assert name not in message


def test_unknown_app_env_refuses_to_load_settings(monkeypatch):
    """AD-14, matrix row "Unknown env"."""
    with pytest.raises(ImproperlyConfigured, match="APP_ENV"):
        load_settings(monkeypatch, APP_ENV="prod")


def test_manage_py_refuses_to_start_in_production_with_defaults():
    """AD-14: the refusal really stops startup, not just a test import of settings."""
    env = {name: value for name, value in os.environ.items() if name not in ENV_VARS}
    env.update(APP_ENV="production", PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, "manage.py", "check"],
        cwd=BASE_DIR,
        env=env,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode != 0
    assert "Appen starter ikke med APP_ENV=production" in result.stderr
    assert "SECRET_KEY" in result.stderr
    assert "ALLOWED_HOSTS" in result.stderr
