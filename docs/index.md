# Quickstart

## Installation

```
pip install django-knobs
```

## Setup

**1. Add to `INSTALLED_APPS`:**

```python
INSTALLED_APPS = [
    ...
    "knobs",
]
```

**2. Run migrations:**

```
python manage.py migrate
```

**3. Define knobs in `settings.py`:**

```python
from knobs import Knob

KNOBS_CONFIG = {
    "MAX_LOGIN_ATTEMPTS": Knob(default=5, help_text="Max failed logins before lockout", category="auth"),
    "FEATURE_NEW_UI":     Knob(default=False, help_text="Enable redesigned UI", category="features"),
    "API_TIMEOUT":        Knob(default=30.0, help_text="Outbound request timeout (seconds)", category="api"),
    "WELCOME_MSG":        Knob(default="Hello!", help_text="Welcome banner text", category="general"),
}
```

**4. Use knobs in your code:**

```python
from knobs import config

def my_view(request):
    if config.FEATURE_NEW_UI:
        return render(request, "new_ui.html")
    return render(request, "old_ui.html")
```

**5. Edit values at runtime:**

Go to `/admin/knobs/knobvalue/` and change any value. The change is effective immediately in the same process and within `SYNC_INTERVAL` seconds in other processes.

## Supported types

Type is inferred from `default`:

| Python type | Example default | Notes |
|---|---|---|
| `bool` | `False` | Stored as `"true"` / `"false"` |
| `int` | `5` | Stored as decimal string |
| `float` | `3.14` | Stored as decimal string |
| `str` | `"hello"` | Stored verbatim |
| `list` | `[]` | Stored as JSON |
| `dict` | `{}` | Stored as JSON |
