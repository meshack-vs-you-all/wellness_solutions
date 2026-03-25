"""
Admin configuration for services app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    CorporateProgram,
    Service,
    ServiceCategory,
    ServicePackage,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin configuration for Service model."""

    list_display = ("name", "category", "duration", "get_price_display", "supports_home_visits", "is_corporate_eligible")
    list_filter = ("category", "supports_home_visits", "is_corporate_eligible")
    search_fields = ("name", "description")
    readonly_fields = ("created", "modified")
    fieldsets = (
        (None, {
            "fields": ("name", "category", "description"),
        }),
        (_("Service Details"), {
            "fields": ("duration", "max_participants", "price"),
        }),
        (_("Home Visit Options"), {
            "fields": ("supports_home_visits", "home_visit_surcharge"),
            "classes": ("collapse",),
            "description": _("Configure home visit availability and additional charges"),
        }),
        (_("Corporate Options"), {
            "fields": ("is_corporate_eligible",),
            "classes": ("collapse",),
            "description": _("Enable this service for corporate programs"),
        }),
        (_("Timestamps"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )

    def get_price_display(self, obj):
        """Display formatted price with home visit surcharge if applicable."""
        base_price = f"${obj.price}"
        if obj.supports_home_visits:
            return f"{base_price} (+ ${obj.home_visit_surcharge} for home visits)"
        return base_price
    get_price_display.short_description = _("Price")

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceCategory model."""

    list_display = ("name", "type", "is_active")
    list_filter = ("type", "is_active")
    search_fields = ("name", "description")
    readonly_fields = ("created", "modified")
    fieldsets = (
        (None, {
            "fields": ("name", "description"),
        }),
        (_("Category Details"), {
            "fields": ("type", "is_active"),
        }),
        (_("Timestamps"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )

@admin.register(CorporateProgram)
class CorporateProgramAdmin(admin.ModelAdmin):
    """Admin configuration for CorporateProgram model."""

    list_display = ("name", "min_participants", "max_participants", "get_services_count")
    search_fields = ("name", "description")
    filter_horizontal = ("services",)
    readonly_fields = ("created", "modified")
    fieldsets = (
        (None, {
            "fields": ("name", "description", "services"),
        }),
        (_("Participant Limits"), {
            "fields": ("min_participants", "max_participants"),
            "description": _("Set minimum and maximum number of participants"),
        }),
        (_("Timestamps"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )

    def get_services_count(self, obj):
        """Get the number of services in this program."""
        return obj.services.count()
    get_services_count.short_description = _("Number of Services")

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    """Admin configuration for ServicePackage model."""

    list_display = ("name", "service", "sessions", "price_per_session", "get_total_price", "validity_days")
    list_filter = ("service",)
    search_fields = ("name",)
    readonly_fields = ("created", "modified", "get_total_price")
    fieldsets = (
        (None, {
            "fields": ("name", "service"),
        }),
        (_("Package Details"), {
            "fields": ("sessions", "price_per_session", "validity_days"),
            "description": _("Configure package pricing and validity"),
        }),
        (_("Price Summary"), {
            "fields": ("get_total_price",),
            "description": _("Total package price based on number of sessions"),
        }),
        (_("Timestamps"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )

    def get_total_price(self, obj):
        """Calculate and display total package price."""
        if obj.sessions and obj.price_per_session:
            total = obj.sessions * obj.price_per_session
            return f"${total}"
        return "N/A"
    get_total_price.short_description = _("Total Package Price")
