"""Configuration for the wellness_instructors app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WellnessInstructorsConfig(AppConfig):
    """Configuration class for the wellness_instructors app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "wellness_instructors"
    verbose_name = _("Wellness Instructors")

    def ready(self):
        """Connect signal handlers when the app is ready."""
        try:
            import wellness_instructors.signals  # noqa: F401
        except ImportError:
            pass
