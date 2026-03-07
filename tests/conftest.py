from django.conf import settings


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "knobs",
        ],
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        KNOBS_CONFIG={},
        KNOBS={"STARTUP_SYNC": False},
    )
