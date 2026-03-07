from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.html import mark_safe

from knobs.models import KnobValue
from knobs.registry import Knob, _registry


def _render_widget(name: str, knob: Knob, raw_value: str) -> str:
    field_name = f"value_{name}"
    attrs = {"id": f"id_{field_name}"}
    t = knob.type

    if t is bool:
        widget = forms.CheckboxInput(attrs=attrs)
        value = knob.coerce(raw_value)
    elif t is int:
        widget = forms.NumberInput(attrs={**attrs, "class": "vIntegerField"})
        value = raw_value
    elif t is float:
        widget = forms.NumberInput(attrs={**attrs, "class": "vFloatField", "step": "any"})
        value = raw_value
    elif t in (list, dict):
        widget = forms.Textarea(attrs={**attrs, "rows": 4, "cols": 60})
        value = raw_value
    else:
        widget = forms.TextInput(attrs={**attrs, "class": "vTextField"})
        value = raw_value

    return widget.render(field_name, value)


@admin.register(KnobValue)
class KnobValueAdmin(admin.ModelAdmin):
    def get_urls(self):
        from django.urls import path

        custom = [
            path(
                "",
                self.admin_site.admin_view(self.knobs_view),
                name="knobs_knobvalue_changelist",
            ),
        ]
        return custom + super().get_urls()

    def knobs_view(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST":
            return self._handle_save(request)
        return self._render_form(request)

    def _build_context(self, request: HttpRequest, submitted: dict[str, str] | None = None) -> dict:
        db_rows = {kv.name: kv for kv in KnobValue.objects.all()}
        categories: dict[str, list] = {}

        for name, knob in _registry.items():
            kv = db_rows.get(name)
            if submitted is not None and name in submitted:
                raw = submitted[name]
            else:
                raw = kv.raw_value if kv else knob.serialize(knob.default)

            categories.setdefault(knob.category, []).append(
                {
                    "name": name,
                    "knob": knob,
                    "updated_at": kv.updated_at.isoformat() if kv else "",
                    "widget_html": mark_safe(_render_widget(name, knob, raw)),
                }
            )

        return {
            **self.admin_site.each_context(request),
            "title": "Config",
            "categories": dict(sorted(categories.items())),
            "opts": self.model._meta,
        }

    def _render_form(self, request: HttpRequest, submitted: dict[str, str] | None = None) -> HttpResponse:
        return render(
            request,
            "admin/knobs/knobvalue/knobs_form.html",
            self._build_context(request, submitted=submitted),
        )

    def _handle_save(self, request: HttpRequest) -> HttpResponse:
        with transaction.atomic():
            db_rows = {kv.name: kv for kv in KnobValue.objects.select_for_update()}

            conflicts = [
                name
                for name in _registry
                if (submitted_ts := request.POST.get(f"ts_{name}", ""))
                and (kv := db_rows.get(name))
                and submitted_ts != kv.updated_at.isoformat()
            ]

            if conflicts:
                messages.error(
                    request,
                    "Config was changed before you. Please reload the page and resubmit your changes.",
                )
                return redirect(".")

            raw_values: dict[str, str] = {}
            for name, knob in _registry.items():
                if knob.type is bool:
                    raw_values[name] = knob.serialize(f"value_{name}" in request.POST)
                else:
                    raw_values[name] = request.POST.get(f"value_{name}", "")

            validation_errors = []
            for name, raw in raw_values.items():
                try:
                    _registry[name].coerce(raw)
                except Exception as e:
                    validation_errors.append(f"{name}: {e}")

            if validation_errors:
                for msg in validation_errors:
                    messages.error(request, f"Invalid value — {msg}")
                return self._render_form(request, submitted=raw_values)

            for name, raw in raw_values.items():
                kv = db_rows.get(name)
                if kv:
                    if kv.raw_value != raw:
                        kv.raw_value = raw
                        kv.save()
                else:
                    KnobValue.objects.create(name=name, raw_value=raw)

        messages.success(request, "Config saved.")
        return redirect(".")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
