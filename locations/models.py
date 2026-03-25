"""
Models for managing physical and virtual locations.
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


def validate_operating_hours(value):
    """Validate operating hours format."""
    required_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if not isinstance(value, dict):
        raise ValidationError(_("Operating hours must be a dictionary"))

    if not all(day in value for day in required_days):
        raise ValidationError(_("All days of the week must be specified"))

    for day, hours in value.items():
        if not isinstance(hours, dict) or "open" not in hours or "close" not in hours:
            raise ValidationError(_(f"Invalid format for {day}. Must include open and close times"))

        # Validate time format (HH:MM)
        for time_key in ["open", "close"]:
            time_str = hours[time_key]
            try:
                hour, minute = time_str.split(":")
                if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                    raise ValueError
            except (ValueError, AttributeError):
                raise ValidationError(_(f"Invalid time format for {day} {time_key}"))

def validate_contact_info(value):
    """Validate contact information format."""
    if not isinstance(value, dict):
        raise ValidationError(_("Contact info must be a dictionary"))

    required_fields = ["phone", "email"]
    if not all(field in value for field in required_fields):
        raise ValidationError(_("Contact info must include phone and email"))

    # Validate email format
    from django.core.validators import validate_email
    try:
        validate_email(value["email"])
    except ValidationError:
        raise ValidationError(_("Invalid email format"))

    # Validate phone format (simple check for now)
    if not isinstance(value["phone"], str) or len(value["phone"]) < 10:
        raise ValidationError(_("Invalid phone number format"))

class Location(TimeStampedModel):
    """
    Model for managing physical and virtual locations where services are provided.
    """
    LOCATION_TYPES = [
        ("studio", _("Studio")),
        ("virtual", _("Virtual")),
        ("onsite", _("On-site")),
    ]

    STATUS_CHOICES = [
        ("active", _("Active")),
        ("inactive", _("Inactive")),
        ("maintenance", _("Under Maintenance")),
    ]

    name = models.CharField(
        _("Name"),
        max_length=100,
        help_text=_("Location name"),
    )
    type = models.CharField(
        _("Type"),
        max_length=20,
        choices=LOCATION_TYPES,
        help_text=_("Type of location"),
    )
    address = models.TextField(
        _("Address"),
        blank=True,
        help_text=_("Physical address (if applicable)"),
    )
    contact_info = models.JSONField(
        _("Contact Information"),
        default=dict,
        help_text=_("Contact details in JSON format"),
        validators=[validate_contact_info],
    )
    operating_hours = models.JSONField(
        _("Operating Hours"),
        default=dict,
        help_text=_("Operating hours in JSON format"),
        validators=[validate_operating_hours],
    )
    capacity = models.PositiveIntegerField(
        _("Capacity"),
        validators=[MinValueValidator(1)],
        help_text=_("Maximum capacity of the location"),
    )
    amenities = models.JSONField(
        _("Amenities"),
        default=dict,
        blank=True,
        help_text=_("Available amenities in JSON format"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        help_text=_("Current status of the location"),
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Detailed description of the location"),
    )

    class Meta:
        app_label = "locations"
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def get_absolute_url(self):
        """Get the absolute URL for this location."""
        return reverse("locations:location_detail", kwargs={"pk": self.pk})

    def clean(self):
        """Validate the location data."""
        super().clean()

        # Initialize empty dictionaries if needed
        if not self.operating_hours:
            self.operating_hours = {}
        if not self.contact_info:
            self.contact_info = {}
        if not self.amenities:
            self.amenities = {}

        # Validate operating hours if provided
        if self.operating_hours:
            validate_operating_hours(self.operating_hours)

        # Validate contact info if provided
        if self.contact_info:
            validate_contact_info(self.contact_info)

        # Validate capacity
        if self.capacity is not None and self.capacity < 1:
            raise ValidationError({
                "capacity": _("Capacity must be a positive integer"),
            })

        # Validate uniqueness of name
        if self.pk is None:  # Only check on creation
            if Location.objects.filter(name=self.name).exists():
                raise ValidationError({
                    "name": _("A location with this name already exists"),
                })

        # Validate status transitions
        if self.pk:
            old_instance = Location.objects.get(pk=self.pk)
            if old_instance.status == "inactive" and self.status == "active":
                # Additional validation for reactivating locations
                pass

        # Validate amenities
        if not isinstance(self.amenities, dict):
            raise ValidationError({"amenities": _("Amenities must be a dictionary")})

class ServiceCategory(TimeStampedModel):
    """Model for categorizing services."""
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Parent Category"),
    )
    order = models.PositiveIntegerField(
        _("Order"),
        default=0,
        help_text=_("Order in which to display this category"),
    )

    class Meta:
        app_label = "locations"
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("locations:category-detail", kwargs={"pk": self.pk})

class LocationService(TimeStampedModel):
    """
    Model for managing services offered at specific locations.
    """

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("Location"),
    )
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name=_("Service"),
    )
    price_adjustment = models.DecimalField(
        _("Price Adjustment"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("Price adjustment (positive or negative) for this service at this location"),
    )
    availability_rules = models.JSONField(
        _("Availability Rules"),
        default=dict,
        help_text=_("Rules for service availability"),
    )
    is_available = models.BooleanField(
        _("Available"),
        default=True,
        help_text=_("Whether this service is currently available at this location"),
    )
    notes = models.TextField(
        _("Notes"),
        blank=True,
        help_text=_("Additional notes about this service at this location"),
    )

    class Meta:
        app_label = "locations"
        verbose_name = _("Location Service")
        verbose_name_plural = _("Location Services")
        unique_together = ["location", "service"]
        ordering = ["location", "service"]

    def __str__(self):
        return f"{self.service.name} at {self.location.name}"

    def clean(self):
        """Validate the location service data."""
        super().clean()

        if self.price_adjustment:
            # Calculate final price after adjustment
            final_price = self.get_final_price()

            # Ensure final price isn't negative
            if final_price < 0:
                raise ValidationError({
                    "price_adjustment": _("Price adjustment cannot result in a negative final price"),
                })

            # Ensure adjustment isn't more than 50% of base price
            max_adjustment = abs(self.service.price * Decimal("0.5"))
            if abs(self.price_adjustment) > max_adjustment:
                raise ValidationError({
                    "price_adjustment": _("Price adjustment cannot exceed 50% of the base price"),
                })

    def get_final_price(self, include_home_visit=False):
        """
        Calculate final price including location adjustment and optional home visit surcharge.
        
        Args:
            include_home_visit (bool): Whether to include home visit surcharge
            
        Returns:
            Decimal: Final calculated price
        """
        base_price = self.service.price
        final_price = base_price + self.price_adjustment

        if include_home_visit and self.service.supports_home_visits:
            final_price += self.service.home_visit_surcharge

        return max(final_price, Decimal("0.00"))

    def get_price_adjustment_percentage(self):
        """
        Calculate price adjustment as a percentage of base price.
        
        Returns:
            Decimal: Adjustment percentage
        """
        if not self.service.price:
            return Decimal("0.00")

        return (self.price_adjustment / self.service.price) * Decimal("100.00")

class LocationInstructor(TimeStampedModel):
    """
    Model for managing instructor assignments to locations.
    """

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="location_instructors",
        verbose_name=_("Location"),
    )
    instructor = models.ForeignKey(
        "wellness_instructors.WellnessInstructor",
        on_delete=models.CASCADE,
        related_name="instructor_locations",
        verbose_name=_("Instructor"),
    )
    availability_rules = models.JSONField(
        _("Availability Rules"),
        default=dict,
        help_text=_("Instructor availability rules in JSON format"),
    )
    is_primary = models.BooleanField(
        _("Is Primary Location"),
        default=False,
        help_text=_("Whether this is the primary location for this instructor"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=[
            ("active", _("Active")),
            ("inactive", _("Inactive")),
            ("temporary", _("Temporary")),
        ],
        default="active",
    )
    notes = models.TextField(
        _("Notes"),
        blank=True,
        help_text=_("Additional notes about this instructor at this location"),
    )

    class Meta:
        app_label = "locations"
        verbose_name = _("Location Instructor")
        verbose_name_plural = _("Location Instructors")
        unique_together = ["location", "instructor"]
        ordering = ["location", "instructor"]
        indexes = [
            models.Index(fields=["instructor"]),
            models.Index(fields=["location", "instructor"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.instructor.user.get_full_name()} at {self.location.name}"

    def clean(self):
        """Validate the location instructor data."""
        super().clean()

        # Initialize empty dictionary if needed
        if not self.availability_rules:
            self.availability_rules = {}

        # Validate availability rules format
        if not isinstance(self.availability_rules, dict):
            raise ValidationError({
                "availability_rules": _("Availability rules must be a dictionary"),
            })

        # Validate primary location
        if self.is_primary:
            # Check if another location is already primary for this instructor
            existing_primary = LocationInstructor.objects.filter(
                instructor=self.instructor,
                is_primary=True,
            ).exclude(pk=self.pk)

            if existing_primary.exists():
                raise ValidationError({
                    "is_primary": _("This instructor already has a primary location"),
                })

    def is_available(self, start_time, end_time):
        """
        Check if instructor is available for a given time slot.
        
        Args:
            start_time (datetime): Start time of the booking
            end_time (datetime): End time of the booking
            
        Returns:
            bool: True if instructor is available, False otherwise
        """
        from bookings.models import Booking, BookingStatus

        # Check if instructor is active
        if self.status != "active":
            return False

        # Check if time slot conflicts with existing bookings
        conflicting_bookings = Booking.objects.filter(
            instructor=self,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED],
        ).exists()

        if conflicting_bookings:
            return False

        # Check if time slot is within instructor's availability rules
        # This is a placeholder - implement according to your availability rules schema
        availability_rules = self.availability_rules or {}
        if not availability_rules:
            return True  # If no rules set, assume always available

        # Get day of week (0 = Monday, 6 = Sunday)
        day_of_week = start_time.weekday()
        day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_name = day_names[day_of_week]

        # Check if instructor works on this day
        if day_name not in availability_rules:
            return False

        day_schedule = availability_rules[day_name]
        if not day_schedule.get("available", True):
            return False

        # Check if time is within working hours
        work_start = day_schedule.get("start_time", "00:00")
        work_end = day_schedule.get("end_time", "23:59")

        booking_time = start_time.strftime("%H:%M")
        if booking_time < work_start or booking_time > work_end:
            return False

        return True
