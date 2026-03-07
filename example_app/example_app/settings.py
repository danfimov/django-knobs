import os
from pathlib import Path

from knobs import Knob

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "example-app-not-for-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "simple_history",
    "knobs",
    "knobs.contrib.history.KnobsHistoryConfig",
    "showcase",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "example_app.urls"

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "knobs_example"),
        "USER": os.environ.get("POSTGRES_USER", "knobs"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "knobs"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
WHITENOISE_USE_FINDERS = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── django-knobs configuration ───────────────────────────────────────────────

KNOBS_CONFIG = {
    # bool: toggle a feature flag
    "SHOW_BANNER": Knob(default=True, help_text="Show the welcome banner", category="ui"),
    "MAINTENANCE_MODE": Knob(default=False, help_text="Put the site in maintenance mode", category="ops"),
    # int/float
    "ITEMS_PER_PAGE": Knob(default=10, help_text="Pagination size", category="ui"),
    "RATE_LIMIT_RPS": Knob(default=100.0, help_text="Max requests per second", category="api"),
    # str
    "BANNER_TEXT": Knob(default="Welcome to django-knobs!", help_text="Banner copy", category="ui"),
    # list / dict (stored as JSON)
    "ALLOWED_THEMES": Knob(default=["light", "dark"], help_text="Available themes", category="ui"),
    "FEATURE_FLAGS": Knob(
        default={"new_checkout": False, "beta_search": False}, help_text="Granular feature flags", category="features"
    ),
}

KNOBS = {
    "SYNC_INTERVAL": 10,  # poll every 10 s so changes are visible quickly
    "STARTUP_SYNC": True,
}
