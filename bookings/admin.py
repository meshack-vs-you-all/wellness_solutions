"""
Admin configuration for the bookings app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Booking, BookingCancellation, BookingPayment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface for bookings."""

    list_display = [
        "booking_number", "client", "booking_type", "location",
        "service", "instructor", "start_time", "status",
        "payment_status", "total_price",
    ]
    list_filter = [
        "booking_type", "status", "payment_status",
        "location", "service", "instructor",
    ]
    search_fields = [
        "booking_number", "client__email", "client__first_name",
        "client__last_name", "notes",
    ]
    readonly_fields = ["booking_number", "created_at", "updated_at"]
    date_hierarchy = "start_time"

    fieldsets = (
        (_("Basic Information"), {
            "fields": (
                "booking_number", "booking_type", "client",
                "organization",
            ),
        }),
        (_("Session Details"), {
            "fields": (
                "location", "service", "instructor",
                "start_time", "end_time",
            ),
        }),
        (_("Status and Payment"), {
            "fields": (
                "status", "payment_status", "base_price",
                "discount_amount", "total_price",
            ),
        }),
        (_("Additional Information"), {
            "fields": (
                "notes", "medical_notes", "preferences",
            ),
        }),
        (_("System Information"), {
            "fields": (
                "created_at", "updated_at", "created_by",
            ),
            "classes": ("collapse",),
        }),
    )


@admin.register(BookingPayment)
class BookingPaymentAdmin(admin.ModelAdmin):
    """Admin interface for booking payments."""

    list_display = [
        "booking", "amount", "payment_method", "status",
        "payment_date", "transaction_id",
    ]
    list_filter = ["payment_method", "status", "payment_date"]
    search_fields = [
        "booking__booking_number", "transaction_id",
        "payer__email", "notes",
    ]
    date_hierarchy = "payment_date"

    fieldsets = (
        (_("Payment Information"), {
            "fields": (
                "booking", "amount", "payment_method",
                "status", "transaction_id",
            ),
        }),
        (_("Payer Information"), {
            "fields": (
                "payer", "payer_organization",
            ),
        }),
        (_("Additional Information"), {
            "fields": (
                "payment_date", "notes",
            ),
        }),
    )


@admin.register(BookingCancellation)
class BookingCancellationAdmin(admin.ModelAdmin):
    """Admin interface for booking cancellations."""

    list_display = [
        "booking", "cancelled_by", "cancellation_date",
        "refund_amount", "refund_status",
    ]
    list_filter = ["cancellation_date", "refund_status"]
    search_fields = [
        "booking__booking_number", "cancelled_by__email",
        "reason",
    ]
    date_hierarchy = "cancellation_date"

    fieldsets = (
        (_("Cancellation Information"), {
            "fields": (
                "booking", "cancelled_by", "cancellation_date",
                "reason",
            ),
        }),
        (_("Refund Information"), {
            "fields": (
                "refund_amount", "refund_status",
            ),
        }),
    )
