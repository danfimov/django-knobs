import threading
from typing import Any


class LocalCache:
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._lock = threading.RLock()

    def get(self, name: str, default: Any = None) -> Any:
        with self._lock:
            return self._data.get(name, default)

    def update_all(self, values: dict[str, Any]) -> None:
        with self._lock:
            self._data = dict(values)

    def set(self, name: str, value: Any) -> None:
        with self._lock:
            self._data[name] = value

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._data.keys())


_cache = LocalCache()
