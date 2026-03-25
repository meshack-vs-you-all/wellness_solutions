"""
Models for the bookings app.
"""


from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import Location, LocationInstructor, LocationService
from packages.models import Package
from services.models import Organization


class BookingType(models.TextChoices):
    """Types of bookings available."""
    INDIVIDUAL = "individual", _("Individual Booking")
    CORPORATE = "corporate", _("Corporate Booking")
    GROUP = "group", _("Group Session")


class BookingStatus(models.TextChoices):
    """Status options for bookings."""
    PENDING = "pending", _("Pending")
    CONFIRMED = "confirmed", _("Confirmed")
    CANCELLED = "cancelled", _("Cancelled")
    COMPLETED = "completed", _("Completed")
    NO_SHOW = "no_show", _("No Show")


class PaymentStatus(models.TextChoices):
    """Status options for payments."""
    PENDING = "pending", _("Pending")
    PAID = "paid", _("Paid")
    PARTIALLY_PAID = "partially_paid", _("Partially Paid")
    REFUNDED = "refunded", _("Refunded")
    COMPANY_PAID = "company_paid", _("Company Paid")
    FREE = "free", _("Free")


class PaymentMethod(models.TextChoices):
    """Available payment methods."""
    CREDIT_CARD = "credit_card", _("Credit Card")
    MPESA = "mpesa", _("M-Pesa")
    CORPORATE_ACCOUNT = "corporate_account", _("Corporate Account")
    INSURANCE = "insurance", _("Insurance")
    PACKAGE = "package", _("Package Credits")
    CASH = "cash", _("Cash")
    FREE = "free", _("Free Session")


class Booking(models.Model):
    """Main booking model to track wellness sessions."""

    # Basic Information
    booking_number = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Unique identifier for the booking"),
    )
    booking_type = models.CharField(
        max_length=20,
        choices=BookingType.choices,
        default=BookingType.INDIVIDUAL,
        help_text=_("Type of booking (individual, corporate, or group)"),
    )

    # Relationships
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="bookings",
        help_text=_("User who booked the session"),
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text=_("Corporate organization if this is a corporate booking"),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="bookings",
        help_text=_("Location where the session will take place"),
    )
    service = models.ForeignKey(
        LocationService,
        on_delete=models.PROTECT,
        related_name="bookings",
        help_text=_("Service being booked"),
    )
    instructor = models.ForeignKey(
        LocationInstructor,
        on_delete=models.PROTECT,
        related_name="bookings",
        help_text=_("Instructor assigned to this session"),
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
        help_text=_("Package this booking is using, if any"),
    )

    # Scheduling
    start_time = models.DateTimeField(
        help_text=_("Start time of the session"),
    )
    end_time = models.DateTimeField(
        help_text=_("End time of the session"),
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        help_text=_("Current status of the booking"),
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text=_("Current payment status"),
    )

    # Pricing
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Original price of the service"),
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Discount applied to this booking"),
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Final price after discounts"),
    )

    # Additional Info
    notes = models.TextField(
        blank=True,
        help_text=_("Additional notes about the booking"),
    )
    medical_notes = models.TextField(
        blank=True,
        help_text=_("Any medical conditions or concerns"),
    )
    preferences = models.JSONField(
        default=dict,
        help_text=_("Client preferences for this session"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_bookings",
        help_text=_("User who created the booking"),
    )

    class Meta:
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=["booking_number"]),
            models.Index(fields=["start_time", "end_time"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),
        ]
        permissions = [
            ("can_view_all_bookings", "Can view all bookings"),
            ("can_manage_bookings", "Can manage bookings"),
        ]

    def __str__(self):
        return f"Booking {self.booking_number} - {self.client.get_full_name()}"

    def clean(self):
        """Validate booking data."""
        super().clean()

        # Validate instructor availability
        instructor_conflicts = Booking.objects.filter(
            instructor=self.instructor,
            status=BookingStatus.CONFIRMED,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)

        if instructor_conflicts.exists():
            raise ValidationError({
                "instructor": _("Instructor is already booked during this time"),
            })

        # Validate package if used
        if self.package:
            if not self.package.is_valid():
                raise ValidationError({
                    "package": _("This package is no longer valid"),
                })

            if self.package.sessions_remaining() <= 0:
                raise ValidationError({
                    "package": _("This package has no remaining sessions"),
                })

            if self.service != self.package.service:
                raise ValidationError({
                    "package": _("This package cannot be used for this service"),
                })

            if self.package.organization and self.organization != self.package.organization:
                raise ValidationError({
                    "package": _("This package belongs to a different organization"),
                })

    def save(self, *args, **kwargs):
        """Override save to handle package session counting."""
        is_new = self.pk is None
        was_confirmed = False if is_new else Booking.objects.get(pk=self.pk).status == BookingStatus.CONFIRMED

        super().save(*args, **kwargs)

        # Update package used sessions if status changed to confirmed
        if self.package and self.status == BookingStatus.CONFIRMED and (is_new or not was_confirmed):
            self.package.used_sessions = models.F("used_sessions") + 1
            self.package.save()

        # Decrease used sessions if status changed from confirmed
        elif self.package and was_confirmed and self.status != BookingStatus.CONFIRMED:
            self.package.used_sessions = models.F("used_sessions") - 1
            self.package.save()

    def get_absolute_url(self):
        """Get the absolute URL for this booking."""
        from django.urls import reverse
        return reverse("bookings:booking_detail", kwargs={"pk": self.pk})

    def can_be_cancelled(self):
        """Check if booking can be cancelled."""
        if self.status in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
            return False
        # Add more business logic here (e.g., cancellation window)
        return True

    def can_be_modified(self):
        """Check if booking can be modified."""
        return self.status == BookingStatus.PENDING


class BookingPayment(models.Model):
    """Track payments for bookings."""

    booking = models.ForeignKey(
        Booking,
        on_delete=models.PROTECT,
        related_name="payments",
        help_text=_("The booking this payment is for"),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Payment amount"),
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        help_text=_("Method of payment"),
    )
    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("External payment system transaction ID"),
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text=_("Current status of the payment"),
    )
    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="payments_made",
        help_text=_("User who made the payment"),
    )
    payer_organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Organization making the payment if corporate"),
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Date and time of payment"),
    )
    notes = models.TextField(
        blank=True,
        help_text=_("Additional notes about the payment"),
    )

    class Meta:
        ordering = ["-payment_date"]
        indexes = [
            models.Index(fields=["transaction_id"]),
            models.Index(fields=["payment_date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Payment {self.transaction_id} for Booking {self.booking.booking_number}"


class BookingCancellation(models.Model):
    """Track booking cancellations and refunds."""

    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        related_name="cancellation",
        help_text=_("The booking that was cancelled"),
    )
    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("User who cancelled the booking"),
    )
    cancellation_date = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Date and time of cancellation"),
    )
    reason = models.TextField(
        help_text=_("Reason for cancellation"),
    )
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Amount to be refunded"),
    )
    refund_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text=_("Status of the refund"),
    )

    class Meta:
        ordering = ["-cancellation_date"]
        indexes = [
            models.Index(fields=["cancellation_date"]),
            models.Index(fields=["refund_status"]),
        ]

    def __str__(self):
        return f"Cancellation for Booking {self.booking.booking_number}"
