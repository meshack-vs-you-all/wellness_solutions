"""
Admin interface for schedule management.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import BlackoutDate, Schedule, TimeSlot


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "instructor",
        "weekday",
        "start_time",
        "end_time",
        "is_active",
        "created",
    ]
    list_filter = [
        "is_active",
        "weekday",
        "instructor",
    ]
    search_fields = [
        "instructor__user__first_name",
        "instructor__user__last_name",
        "instructor__user__email",
    ]
    ordering = ["weekday", "start_time"]
    readonly_fields = ["created", "modified"]
    fieldsets = (
        (None, {
            "fields": ("instructor", "weekday"),
        }),
        (_("Time Information"), {
            "fields": ("start_time", "end_time"),
        }),
        (_("Status"), {
            "fields": ("is_active",),
        }),
        (_("Metadata"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = [
        "schedule",
        "start_datetime",
        "end_datetime",
        "status",
        "created",
    ]
    list_filter = [
        "status",
        "schedule__instructor",
        "start_datetime",
    ]
    search_fields = [
        "schedule__instructor__user__first_name",
        "schedule__instructor__user__last_name",
        "notes",
    ]
    ordering = ["-start_datetime"]
    readonly_fields = ["created", "modified"]
    fieldsets = (
        (None, {
            "fields": ("schedule", "status"),
        }),
        (_("Time Information"), {
            "fields": ("start_datetime", "end_datetime"),
        }),
        (_("Additional Information"), {
            "fields": ("notes",),
        }),
        (_("Metadata"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )


@admin.register(BlackoutDate)
class BlackoutDateAdmin(admin.ModelAdmin):
    list_display = [
        "instructor",
        "start_date",
        "end_date",
        "reason",
        "is_recurring",
        "created",
    ]
    list_filter = [
        "is_recurring",
        "instructor",
        "start_date",
    ]
    search_fields = [
        "instructor__user__first_name",
        "instructor__user__last_name",
        "reason",
    ]
    ordering = ["-start_date"]
    readonly_fields = ["created", "modified"]
    fieldsets = (
        (None, {
            "fields": ("instructor", "reason"),
        }),
        (_("Time Information"), {
            "fields": ("start_date", "end_date"),
        }),
        (_("Options"), {
            "fields": ("is_recurring",),
        }),
        (_("Metadata"), {
            "fields": ("created", "modified"),
            "classes": ("collapse",),
        }),
    )
