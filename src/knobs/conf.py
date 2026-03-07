from importlib import import_module
from typing import Any

from django.conf import settings

DEFAULTS: dict[str, Any] = {
    "SYNC_INTERVAL": 30,
    "STARTUP_SYNC": True,
    "ALLOW_MISSING_DB": False,
    "SERIALIZER": "knobs.serializers.JsonSerializer",
}


class KnobsSettings:
    def __init__(self) -> None:
        self._user_settings: dict[str, Any] = getattr(settings, "KNOBS", {})
        self._serializer_instance = None

    def _get(self, key: str) -> Any:
        return self._user_settings.get(key, DEFAULTS[key])

    @property
    def SYNC_INTERVAL(self) -> int:
        return int(self._get("SYNC_INTERVAL"))

    @property
    def STARTUP_SYNC(self) -> bool:
        return bool(self._get("STARTUP_SYNC"))

    @property
    def ALLOW_MISSING_DB(self) -> bool:
        return bool(self._get("ALLOW_MISSING_DB"))

    @property
    def SERIALIZER(self):
        if self._serializer_instance is None:
            dotted_path: str = self._get("SERIALIZER")
            module_path, class_name = dotted_path.rsplit(".", 1)
            module = import_module(module_path)
            cls = getattr(module, class_name)
            self._serializer_instance = cls()
        return self._serializer_instance


knobs_settings = KnobsSettings()
