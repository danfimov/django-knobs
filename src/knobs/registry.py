from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Type

from django.conf import settings

from knobs.conf import knobs_settings


@dataclass
class Knob:
    default: Any
    help_text: str = ""
    category: str = "general"
    type: Type | None = None
    validators: list[Callable] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.type is None:
            self.type = builtins_type(self.default)

    def coerce(self, raw: str) -> Any:
        t = self.type
        if t is bool:
            return raw.lower() in ("1", "true", "yes")
        if t is int:
            return int(raw)
        if t is float:
            return float(raw)
        if t is str:
            return raw
        # list, dict, or other — delegate to serializer
        return knobs_settings.SERIALIZER.loads(raw)

    def serialize(self, value: Any) -> str:
        t = self.type
        if t is bool:
            return "true" if value else "false"
        if t in (int, float):
            return str(value)
        if t is str:
            return value
        return knobs_settings.SERIALIZER.dumps(value)


def builtins_type(value: Any) -> type:
    """Return the built-in type of value, defaulting to str for unknowns."""
    t = type(value)
    if t in (bool, int, float, str, list, dict):
        return t
    return str


_registry: dict[str, Knob] = {}


def build_registry() -> None:
    config: dict[str, Knob] = getattr(settings, "KNOBS_CONFIG", {})
    _registry.clear()
    _registry.update(config)
