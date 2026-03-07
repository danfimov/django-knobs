from typing import Any

from knobs.cache import _cache
from knobs.registry import _registry


class KnobsProxy:
    def __getattr__(self, name: str) -> Any:
        if name not in _registry:
            raise AttributeError(f"No config key '{name}' defined in KNOBS_CONFIG")
        return _cache.get(name, _registry[name].default)

    def __dir__(self) -> list[str]:
        return list(_registry.keys())


config = KnobsProxy()
