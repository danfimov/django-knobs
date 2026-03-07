from django.db import models


class KnobValue(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    raw_value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "knobs"
        verbose_name = "config"
        verbose_name_plural = "config"

    def __str__(self) -> str:
        return str(self.name)
