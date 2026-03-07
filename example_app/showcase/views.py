from django.http import JsonResponse
from django.shortcuts import render

from knobs import config
from knobs.registry import _registry


def index(request):
    if config.MAINTENANCE_MODE:
        return render(request, "showcase/maintenance.html")

    context = {
        "show_banner": config.SHOW_BANNER,
        "maintenance_mode": config.MAINTENANCE_MODE,
        "banner_text": config.BANNER_TEXT,
        "items_per_page": config.ITEMS_PER_PAGE,
        "rate_limit_rps": config.RATE_LIMIT_RPS,
        "allowed_themes": config.ALLOWED_THEMES,
        "feature_flags": config.FEATURE_FLAGS,
        "items": [f"Item {i}" for i in range(1, config.ITEMS_PER_PAGE + 1)],
    }
    return render(request, "showcase/index.html", context)


def knobs_api(request):
    """JSON endpoint that returns all current config values — useful for watching live changes."""
    data = {name: getattr(config, name) for name in _registry}
    return JsonResponse(data)
