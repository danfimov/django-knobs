# django-knobs

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-knobs?style=for-the-badge&logo=python)](https://pypi.org/project/django-knobs/)
[![PyPI](https://img.shields.io/pypi/v/django-knobs?style=for-the-badge&logo=pypi)](https://pypi.org/project/django-knobs/)
[![Checks](https://img.shields.io/github/actions/workflow/status/danfimov/django-knobs/code-check.yml?branch=main&style=for-the-badge)](https://github.com/danfimov/django-knobs)

Library for dynamic settings / feature flags that can be changed at runtime without restarting the application from Django admin panel.

```bash
pip install django-knobs
```

![](docs/assets/banner.png)

## Setup

**1. Add to `INSTALLED_APPS`:**

  ```python
  INSTALLED_APPS = [
      ...
      "knobs",
  ]
  ```

**2. Run migrations:**

  ```bash
  python manage.py migrate
  ```

**3. Define your config values in `settings.py`:**

  ```python
  from knobs import Knob

  KNOBS_CONFIG = {
      "MAX_LOGIN_ATTEMPTS": Knob(default=5, help_text="Max failed logins before lockout", category="auth"),
      "FEATURE_NEW_UI":     Knob(default=False, help_text="Enable redesigned UI", category="features"),
      "API_TIMEOUT":        Knob(default=30.0, help_text="Outbound request timeout (seconds)", category="api"),
      "WELCOME_MSG":        Knob(default="Hello!", help_text="Welcome banner text", category="general"),
  }
  ```
