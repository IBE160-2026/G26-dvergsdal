"""Django settings for the wedding website.

Every value that differs between a developer's machine and production comes from
an environment variable with a safe local default, so the app runs with no `.env`
file (AD-14, NFR-8). All variables are listed in `.env.example`. With
`APP_ENV=production` the app refuses to start on unsafe values.
"""

import os
from pathlib import Path

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


# Environment and the production guard (AD-14)

APP_ENV = validate_app_env(os.environ.get("APP_ENV"))
IS_PRODUCTION = APP_ENV == "production"

DEBUG = read_bool(os.environ, "DEBUG", default=not IS_PRODUCTION)
SECRET_KEY = read_str(os.environ, "SECRET_KEY", default=LOCAL_SECRET_KEY)
ALLOWED_HOSTS = read_list(
    os.environ, "ALLOWED_HOSTS", default=[] if IS_PRODUCTION else LOCAL_ALLOWED_HOSTS
)

if IS_PRODUCTION and (problems := production_problems(DEBUG, SECRET_KEY, ALLOWED_HOSTS)):
    raise ImproperlyConfigured(refusal_message(problems))


# Applications. `/admin/` belongs to the `dashboard` app, so Django's own admin
# is not installed (AD-10).

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wedding",
    "guests",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database: SQLite everywhere, through the ORM only (AD-5). Short IMMEDIATE
# transactions and WAL let readers and one writer work side by side; requests
# are deliberately not wrapped in transactions (no ATOMIC_REQUESTS).

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 20,
            "init_command": "PRAGMA journal_mode=WAL;",
            "transaction_mode": "IMMEDIATE",
        },
    }
}


# Users: the couple and helpers log in; guests never do (AD-10).

AUTH_USER_MODEL = "wedding.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Language and time: Norwegian bokmål, stored in UTC and shown in Oslo time
# (NFR-6, AD-11).

LANGUAGE_CODE = "nb"
TIME_ZONE = "Europe/Oslo"
USE_I18N = True
USE_TZ = True


# Static files: self-hosted and served by WhiteNoise (AD-15).

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


# Email is never sent; the console backend keeps anything Django tries to send
# on the machine.

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
