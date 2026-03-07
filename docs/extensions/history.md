# django-simple-history

django-knobs ships an optional integration with
[django-simple-history](https://django-simple-history.readthedocs.io/) that
records every change to a knob value — who changed it, when, and what the
previous value was.

## Installation

**1. Install the extra dependency:**

```
pip install django-knobs[history]
# or
pip install django-simple-history
```

**2. Add apps and middleware to `settings.py`:**

```python
INSTALLED_APPS = [
    ...
    "simple_history",   # must come before knobs.contrib.history
    "knobs",
    "knobs.contrib.history.KnobsHistoryConfig",  # registers history on KnobValue
]

MIDDLEWARE = [
    ...
    "simple_history.middleware.HistoryRequestMiddleware",  # captures request user
]
```

**3. Run migrations:**

```
python manage.py migrate
```

This creates the `knobs_history_historicalknobvalue` table.

## What gets recorded

Every time a `KnobValue` row is saved (via the admin or programmatically),
simple-history creates a snapshot containing:

| Field | Description |
|---|---|
| `name` | Knob name |
| `raw_value` | Serialized value at the time of change |
| `updated_at` | Timestamp of the change |
| `history_user` | The user who triggered the save (via middleware) |
| `history_type` | `+` created, `~` changed, `-` deleted |
| `history_date` | When the history record was written |

## Viewing history in the admin

History records are available at:

```
/admin/knobs_history/historicalknobvalue/
```

You can filter by knob name, date, or user to audit any change.

## Querying history programmatically

```python
from knobs.models import KnobValue

kv = KnobValue.objects.get(name="FEATURE_NEW_UI")

# Full history for one knob (newest first)
for record in kv.history.all():
    print(record.history_date, record.history_user, record.raw_value)

# Most recent change
latest = kv.history.first()

# Diff between two versions
new_record = kv.history.first()
old_record = kv.history.all()[1]
delta = new_record.diff_against(old_record)
for change in delta.changes:
    print(f"{change.field}: {change.old!r} → {change.new!r}")
```

## Without the middleware

If you cannot add `HistoryRequestMiddleware` (e.g. in async contexts), history
records will still be created but `history_user` will be `None`. You can set
the user explicitly:

```python
from knobs.models import KnobValue

kv = KnobValue.objects.get(name="MY_KNOB")
kv.raw_value = "new_value"
kv._history_user = request.user
kv.save()
```
