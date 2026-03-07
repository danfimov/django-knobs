from django.apps import AppConfig


class KnobsHistoryConfig(AppConfig):
    name = "knobs.contrib.history"
    label = "knobs_history"
    verbose_name = "Knobs History"

    def ready(self) -> None:
        from django.contrib import admin
        from django.contrib.admin import ModelAdmin

        from knobs.models import KnobValue

        HistoricalKnobValue = KnobValue.history.model
        HistoricalKnobValue._meta.verbose_name = "history entry"
        HistoricalKnobValue._meta.verbose_name_plural = "history"

        class HistoricalKnobValueAdmin(ModelAdmin):
            list_display = ["name", "raw_value", "history_date", "history_user", "history_type"]
            list_filter = ["name", "history_type"]
            search_fields = ["name"]
            readonly_fields = ["name", "raw_value", "history_date", "history_user", "history_type"]

            def has_add_permission(self, request):
                return False

            def has_change_permission(self, request, obj=None):
                return False

            def has_delete_permission(self, request, obj=None):
                return False

        if not admin.site.is_registered(HistoricalKnobValue):
            admin.site.register(HistoricalKnobValue, HistoricalKnobValueAdmin)
