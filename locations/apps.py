"""
Configuration for the locations app.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    """Configuration class for the locations app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "locations"
    verbose_name = _("Locations")
