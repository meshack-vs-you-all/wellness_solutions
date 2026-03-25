from django.apps import AppConfig


class PackagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "packages"
    verbose_name = "Service Packages"

    def ready(self):
        try:
            import packages.signals  # noqa F401
        except ImportError:
            pass
