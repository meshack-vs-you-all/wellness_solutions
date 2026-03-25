"""
Bookings app configuration.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BookingsConfig(AppConfig):
    """Configuration for the bookings app."""

    name = "bookings"
    verbose_name = _("Bookings")

    def ready(self):
        """
        Initialize app when it's ready.
        Import signal handlers and other initialization code here.
        """
        try:
            import bookings.signals  # noqa
        except ImportError:
            pass
