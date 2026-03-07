# Configuration Reference

All settings live under the `KNOBS` dict in your Django `settings.py`:

```python
KNOBS = {
    "SYNC_INTERVAL": 30,
    "STARTUP_SYNC": True,
    "ALLOW_MISSING_DB": False,
    "SERIALIZER": "knobs.serializers.JsonSerializer",
}
```

---

## `SYNC_INTERVAL`

**Type:** `int`
**Default:** `30`

Seconds between background DB polls. Lower values mean faster cross-process propagation but more DB load. A value of `10` is fine for most applications; go lower only if you need near-realtime propagation.

---

## `STARTUP_SYNC`

**Type:** `bool`
**Default:** `True`

When `True`, the cache is populated from the DB inside `AppConfig.ready()` before the first request is served. This ensures knobs reflect DB values immediately on startup rather than showing defaults until the first sync cycle.

Set to `False` in test environments where the DB may not exist at `django.setup()` time.

---

## `ALLOW_MISSING_DB`

**Type:** `bool`
**Default:** `False`

When `True`, a DB error during startup sync is caught and logged as a warning rather than raising. Knobs fall back to their `default` values. Useful for environments where the database might not be available immediately (e.g., read-only deployments, preview environments).

---

## `SERIALIZER`

**Type:** `str` (dotted import path)
**Default:** `"knobs.serializers.JsonSerializer"`

Controls how `list` and `dict` knob values are serialized to/from the `raw_value` text column. The class must implement the `KnobSerializer` protocol:

```python
class KnobSerializer(Protocol):
    def dumps(self, value: Any) -> str: ...
    def loads(self, raw: str) -> Any: ...
```

To use `orjson` for faster serialization:

```python
# myproject/serializers.py
import orjson

class OrjsonSerializer:
    def dumps(self, value):
        return orjson.dumps(value).decode()

    def loads(self, raw):
        return orjson.loads(raw)
```

```python
# settings.py
KNOBS = {"SERIALIZER": "myproject.serializers.OrjsonSerializer"}
```

Scalar types (`bool`, `int`, `float`, `str`) bypass the serializer entirely and are handled with simple string conversion.

---

## `KNOBS_CONFIG`

Not part of the `KNOBS` dict — defined at the top level of `settings.py`:

```python
KNOBS_CONFIG = {
    "MY_KNOB": Knob(default=42, help_text="...", category="..."),
}
```

See the [quickstart](quickstart.md) for full details.
