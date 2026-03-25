from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ClientProfile, ClientSession


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "phone_number", "preferred_location", "created_at"]
    list_filter = ["preferred_location", "created_at"]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__phone_number",
        "notes",
        "medical_notes",
    ]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {
            "fields": ("user", "preferred_location"),
        }),
        (_("Emergency Contact"), {
            "fields": ("emergency_contact_name", "emergency_contact_phone"),
        }),
        (_("Notes"), {
            "fields": ("notes", "medical_notes"),
        }),
        (_("Metadata"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(ClientSession)
class ClientSessionAdmin(admin.ModelAdmin):
    list_display = ["client", "booking_date", "service", "instructor", "rating"]
    list_filter = ["booking__service", "booking__instructor", "rating"]
    search_fields = [
        "client__user__first_name",
        "client__user__last_name",
        "notes",
        "feedback",
    ]
    readonly_fields = ["booking"]

    def booking_date(self, obj):
        return obj.booking.start_time.date()
    booking_date.short_description = _("Date")

    def service(self, obj):
        return obj.booking.service
    service.short_description = _("Service")

    def instructor(self, obj):
        return obj.booking.instructor
    instructor.short_description = _("Instructor")
