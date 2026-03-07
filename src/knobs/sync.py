import logging
import threading
import time
from datetime import datetime

from django.db.models import Max

from knobs.cache import LocalCache
from knobs.models import KnobValue
from knobs.registry import Knob

logger = logging.getLogger("django_knobs.sync")

_UNSET = object()


class SyncThread(threading.Thread):
    def __init__(
        self, interval: int, cache: LocalCache, registry: dict[str, Knob],
    ) -> None:
        super().__init__(daemon=True, name="knobs-sync")
        self._interval = interval
        self._cache = cache
        self._registry = registry
        self._last_max_updated_at: datetime | object = _UNSET

    def run(self) -> None:
        while True:
            try:
                self._sync()
            except Exception:
                logger.exception("knobs: background sync error")
            time.sleep(self._interval)

    def _sync(self) -> None:
        latest = KnobValue.objects.aggregate(t=Max("updated_at"))["t"]
        if latest != self._last_max_updated_at:
            self._reload_all()
            self._last_max_updated_at = latest

    def _reload_all(self) -> None:
        db_values = {kv.name: kv.raw_value for kv in KnobValue.objects.all()}
        result: dict = {}
        missing = []
        for name, knob in self._registry.items():
            if name in db_values:
                result[name] = knob.coerce(db_values[name])
            else:
                result[name] = knob.default
                missing.append(
                    KnobValue(name=name, raw_value=knob.serialize(knob.default)),
                )
        if missing:
            KnobValue.objects.bulk_create(missing, ignore_conflicts=True)
        self._cache.update_all(result)
