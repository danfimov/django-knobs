import json
from typing import Any, Protocol


class KnobSerializer(Protocol):
    def dumps(self, value: Any) -> str: ...
    def loads(self, raw: str) -> Any: ...


class JsonSerializer:
    def dumps(self, value: Any) -> str:
        return json.dumps(value)

    def loads(self, raw: str) -> Any:
        return json.loads(raw)
