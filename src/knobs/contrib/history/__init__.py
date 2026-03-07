"""
Optional django-simple-history integration for django-knobs.

Add to INSTALLED_APPS *after* "knobs":

    INSTALLED_APPS = [
        ...
        "simple_history",
        "knobs",
        "knobs.contrib.history.KnobsHistoryConfig",
    ]

Also add the middleware so history records capture the acting user:

    MIDDLEWARE = [
        ...
        "simple_history.middleware.HistoryRequestMiddleware",
    ]

Then run to apply the migrations: python manage.py makemigrations && python manage.py migrate
"""

from knobs.contrib.history.config import KnobsHistoryConfig

__all__ = ["KnobsHistoryConfig"]
