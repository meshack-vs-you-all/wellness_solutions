"""Admin configuration for packages app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ClientPackage, Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """Admin configuration for Package model."""

    list_display = [
        "name", "owner", "organization", "service_package",
        "total_sessions", "used_sessions", "expiry_date", "active",
    ]
    list_filter = ["active", "service_package", "organization"]
    search_fields = ["name", "owner__email", "organization__name"]
    date_hierarchy = "purchase_date"
    readonly_fields = ["purchase_date"]

    fieldsets = [
        (None, {
            "fields": [
                "name", "owner", "organization", "service_package",
                "total_sessions", "used_sessions", "expiry_date",
            ],
        }),
        (_("Status"), {
            "fields": ["active", "purchase_date"],
        }),
    ]


@admin.register(ClientPackage)
class ClientPackageAdmin(admin.ModelAdmin):
    """Admin configuration for ClientPackage model."""

    list_display = [
        "client", "package", "assigned_date", "assigned_by",
    ]
    list_filter = ["assigned_date", "package__active"]
    search_fields = [
        "client__email", "package__name",
        "assigned_by__email",
    ]
    date_hierarchy = "assigned_date"
    readonly_fields = ["assigned_date"]
