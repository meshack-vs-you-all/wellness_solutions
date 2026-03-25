"""Admin configuration for the wellness_instructors app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Session, WellnessInstructor


@admin.register(WellnessInstructor)
class WellnessInstructorAdmin(admin.ModelAdmin):
    """Admin interface for WellnessInstructor model."""

    list_display = [
        "user",
        "full_name",
        "email",
        "specializations",
        "certification_level",
        "years_of_experience",
        "is_available",
    ]
    list_filter = [
        "is_available",
        "specializations",
        "certification_level",
        "created",
        "modified",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "bio",
    ]
    raw_id_fields = ["user"]
    readonly_fields = ["created", "modified"]

    fieldsets = [
        (None, {
            "fields": ("user", "bio"),
        }),
        (_("Professional Details"), {
            "fields": (
                "specializations",
                "certification_level",
                "years_of_experience",
                "hourly_rate",
            ),
        }),
        (_("Status"), {
            "fields": ("is_available",),
        }),
        (_("Metadata"), {
            "classes": ("collapse",),
            "fields": ("created", "modified"),
        }),
    ]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin interface for Session model."""

    list_display = [
        "title",
        "instructor",
        "session_type",
        "difficulty_level",
        "duration",
        "max_participants",
        "price",
        "is_active",
    ]
    list_filter = [
        "is_active",
        "session_type",
        "difficulty_level",
        "created",
        "modified",
    ]
    search_fields = [
        "title",
        "description",
        "instructor__user__username",
        "instructor__user__email",
    ]
    raw_id_fields = ["instructor"]
    readonly_fields = ["created", "modified"]

    fieldsets = [
        (None, {
            "fields": ("instructor", "title", "description"),
        }),
        (_("Session Details"), {
            "fields": (
                "session_type",
                "difficulty_level",
                "duration",
                "max_participants",
                "price",
            ),
        }),
        (_("Status"), {
            "fields": ("is_active",),
        }),
        (_("Metadata"), {
            "classes": ("collapse",),
            "fields": ("created", "modified"),
        }),
    ]
