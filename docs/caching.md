# How Caching Works

## Overview

django-knobs uses a three-tier architecture to make reads zero-latency:

```
knobs.MY_SETTING
      │
      ▼
 LocalCache (in-process dict)     ← only read source, zero latency
      ▲
      │ full reload when MAX(updated_at) changes
 SyncThread (daemon)  ──────────────────────────► KnobValue (DB)
                                                       ▲
                                              immediate write on admin save
                                              + post_save signal → LocalCache
```

## Tier 1 — Local In-Process Cache

`LocalCache` is a plain Python dict protected by a `threading.RLock`. Reading a knob value is a single dict lookup — no network, no serialization overhead, no blocking.

Each process has its own `LocalCache`. They are independent; writes to one do not automatically propagate to others.

## Tier 2 — Background Sync Thread

A daemon thread (`knobs-sync`) wakes up every `SYNC_INTERVAL` seconds and runs:

```sql
SELECT MAX(updated_at) FROM knobs_knobvalue
```

If the result changed since the last check, it issues a second query to fetch all rows and rebuilds the local cache atomically. This means:

- **No change:** one cheap query, nothing else.
- **Any change:** one more query to fetch all rows.

The reload replaces the entire cache at once (not entry by entry), so readers always see a consistent snapshot.

## Startup Sync

When `STARTUP_SYNC = True` (default), `AppConfig.ready()` calls `_sync()` synchronously before the first request. This ensures the cache is populated with DB values before any traffic hits the server.

## Admin Save — Same-Process Instant Update

When a `KnobValue` is saved (e.g., via the Django admin), the `post_save` signal fires `knob_post_change` and immediately calls `_cache.set(name, coerced_value)` in the same process. No waiting for the next sync cycle.

Other processes pick up the change at their next sync tick, within `SYNC_INTERVAL` seconds.

## Comparison with django-constance

| | django-knobs | django-constance |
|---|---|---|
| Per-request database call | Never | Always |
| Cross-process propagation | Within `SYNC_INTERVAL` seconds | Immediate (shared cache) |
| Dependency on external cache | None | Required (Redis/Memcached) |
| Latency for reading a value | ~50 ns (dict lookup) | ~1–5 ms (cache hit) |

django-knobs trades instant cross-process propagation for zero per-request overhead. This is the right trade-off for most settings that change infrequently.

## Signals

`knob_post_change` is fired after a value is saved, in the same process:

```python
from knobs.signals import knob_post_change

def on_change(sender, name, old_value, new_value, user, **kwargs):
    print(f"{name} changed from {old_value!r} to {new_value!r} by {user}")

knob_post_change.connect(on_change)
```

`knob_pre_change` is available for pre-save validation hooks (not yet wired to admin save — use Django's model validation for that).
