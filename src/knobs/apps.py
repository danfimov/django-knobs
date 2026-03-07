import logging

from django.apps import AppConfig

logger = logging.getLogger("django_knobs")


class KnobsConfig(AppConfig):
    name = "knobs"
    verbose_name = "Knobs"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        import knobs.signals  # noqa: F401 — ensure receivers are connected
        from knobs.conf import knobs_settings
        from knobs.registry import build_registry

        build_registry()

        if knobs_settings.STARTUP_SYNC:
            from django.db.backends.signals import connection_created

            connection_created.connect(_start_sync_on_first_connection, weak=False)


def _start_sync_on_first_connection(sender, connection, **kwargs):
    # Disconnect immediately — we only want to run once.
    from django.db.backends.signals import connection_created

    connection_created.disconnect(_start_sync_on_first_connection)

    from django.db import ProgrammingError

    from knobs.cache import _cache
    from knobs.conf import knobs_settings
    from knobs.registry import _registry
    from knobs.sync import SyncThread

    thread = SyncThread(knobs_settings.SYNC_INTERVAL, _cache, _registry)
    try:
        thread._sync()
    except ProgrammingError:
        logger.warning("django-knobs: table not found, skipping startup sync (run migrate)")
        return  # table doesn't exist yet — don't start the background thread
    except Exception:
        if not knobs_settings.ALLOW_MISSING_DB:
            raise
        logger.warning("django-knobs: could not load from DB at startup, using defaults")
    thread.start()
