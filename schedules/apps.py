"""
Application configuration for the schedules app.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SchedulesConfig(AppConfig):
    """Configuration for the schedules app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "schedules"
    verbose_name = _("Schedules")

    def ready(self):
        try:
            import schedules.signals  # noqa: F401
        except ImportError:
            pass
