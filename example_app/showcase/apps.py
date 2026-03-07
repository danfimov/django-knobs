from django.apps import AppConfig

from knobs.signals import knob_post_change


class ShowcaseConfig(AppConfig):
    name = "showcase"

    def ready(self):
        knob_post_change.connect(_log_change)


def _log_change(sender, name, old_value, new_value, **kwargs):
    import logging

    logger = logging.getLogger("showcase")
    logger.info("[config changed] %s: %r → %r", name, old_value, new_value)
