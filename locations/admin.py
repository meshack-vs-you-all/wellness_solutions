"""
Admin interface for the locations app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Location, LocationInstructor, LocationService


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin interface for Location model."""
    list_display = ["name", "type", "status", "capacity", "created", "modified"]
    list_filter = ["type", "status"]
    search_fields = ["name", "address"]
    readonly_fields = ["created", "modified"]
    fieldsets = (
        (None, {
            "fields": ("name", "type", "status", "description"),
        }),
        (_("Details"), {
            "fields": ("address", "contact_info", "operating_hours", "capacity"),
        }),
        (_("Additional Information"), {
            "fields": ("amenities",),
        }),
        (_("Metadata"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )


@admin.register(LocationService)
class LocationServiceAdmin(admin.ModelAdmin):
    """Admin interface for LocationService model."""
    list_display = ["location", "service", "is_available", "price_adjustment"]
    list_filter = ["location", "service", "is_available"]
    search_fields = ["location__name", "service__name"]
    readonly_fields = ["created", "modified"]
    fieldsets = (
        (None, {
            "fields": ("location", "service", "is_available"),
        }),
        (_("Pricing"), {
            "fields": ("price_adjustment",),
        }),
        (_("Availability"), {
            "fields": ("availability_rules",),
        }),
        (_("Additional Information"), {
            "fields": ("notes",),
        }),
        (_("Metadata"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )


@admin.register(LocationInstructor)
class LocationInstructorAdmin(admin.ModelAdmin):
    """Admin interface for LocationInstructor model."""
    list_display = ["location", "instructor", "status", "is_primary"]
    list_filter = ["location", "instructor", "status", "is_primary"]
    search_fields = ["location__name", "instructor__user__first_name",
                    "instructor__user__last_name"]
    readonly_fields = ["created", "modified"]
    fieldsets = (
        (None, {
            "fields": ("location", "instructor", "status", "is_primary"),
        }),
        (_("Availability"), {
            "fields": ("availability_rules",),
        }),
        (_("Additional Information"), {
            "fields": ("notes",),
        }),
        (_("Metadata"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )
