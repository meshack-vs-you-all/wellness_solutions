"""
Forms for the bookings app.
"""

from django import forms
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from locations.models import LocationInstructor
from packages.models import ClientPackage, Package
from services.models import Service

from .models import Booking, BookingCancellation, BookingPayment


class BookingForm(forms.ModelForm):
    """Form for creating and updating bookings."""

    class Meta:
        model = Booking
        fields = [
            "service", "instructor", "start_time", "end_time",
            "notes", "package",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter package choices to only show valid packages for this user
        if self.user:
            self.fields["package"].queryset = Package.objects.filter(
                Q(owner=self.user) | Q(client_assignments__client=self.user),
                active=True,
                expiry_date__gte=timezone.now().date(),
            ).distinct()

        # Filter services based on location if selected
        if self.data.get("location"):
            self.fields["service"].queryset = Service.objects.filter(
                locations__location_id=self.data["location"],
                locations__is_available=True,
            ).distinct()
        else:
            self.fields["service"].queryset = Service.objects.none()

        # Filter instructors based on location and service if both are selected
        if self.data.get("location") and self.data.get("service"):
            self.fields["instructor"].queryset = LocationInstructor.objects.filter(
                location_id=self.data["location"],
                instructor__services__service_id=self.data["service"],
                status="active",
            ).select_related("instructor", "location")
        else:
            self.fields["instructor"].queryset = LocationInstructor.objects.none()

    def clean(self):
        """Validate the booking form data."""
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        service = cleaned_data.get("service")
        instructor = cleaned_data.get("instructor")

        if start_time and end_time:
            # Check if end time is after start time
            if end_time <= start_time:
                raise forms.ValidationError(
                    _("End time must be after start time"),
                )

            # Check if start time is in the future
            if start_time <= timezone.now():
                raise forms.ValidationError(
                    _("Booking must be for a future time"),
                )

            # Check if duration matches service duration
            if service:
                expected_duration = service.duration
                actual_duration = (end_time - start_time).total_seconds() / 60
                if int(actual_duration) != expected_duration:
                    raise forms.ValidationError(
                        _("Session duration must be %(duration)d minutes for this service") %
                        {"duration": expected_duration},
                    )

        # Validate service availability
        if service and not service.locations.filter(
            is_available=True,
        ).exists():
            raise forms.ValidationError(
                _("This service is not available"),
            )

        # Validate instructor availability and service capability
        if instructor and service:
            if not instructor.instructor.services.filter(service=service).exists():
                raise forms.ValidationError(
                    _("Selected instructor does not provide this service"),
                )

            # Check if instructor is available at this time
            if start_time and end_time:
                if not instructor.is_available(start_time, end_time):
                    raise forms.ValidationError(
                        _("Instructor is not available at this time"),
                    )

        return cleaned_data


class BookingPaymentForm(forms.ModelForm):
    """Form for processing booking payments."""

    class Meta:
        model = BookingPayment
        fields = ["amount", "payment_method", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.booking = kwargs.pop("booking", None)
        super().__init__(*args, **kwargs)

        if self.booking:
            # Set initial amount to remaining balance
            self.fields["amount"].initial = self.booking.total_price

            # Customize payment methods based on booking type
            if self.booking.booking_type == "corporate":
                self.fields["payment_method"].choices = [
                    ("corporate_account", _("Corporate Account")),
                    ("credit_card", _("Credit Card")),
                ]


class BookingCancellationForm(forms.ModelForm):
    """Form for cancelling bookings."""

    class Meta:
        model = BookingCancellation
        fields = ["reason"]
        widgets = {
            "reason": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.booking = kwargs.pop("booking", None)
        super().__init__(*args, **kwargs)

        if self.booking and not self.booking.can_be_cancelled():
            raise forms.ValidationError(
                _("This booking cannot be cancelled"),
            )

    def clean(self):
        """Validate cancellation."""
        cleaned_data = super().clean()
        return cleaned_data


class PackageForm(forms.ModelForm):
    """Form for creating and updating packages."""

    class Meta:
        model = Package
        fields = [
            "name", "service_package", "owner",
            "organization", "total_sessions", "expiry_date",
        ]
        widgets = {
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        """Validate package data."""
        cleaned_data = super().clean()
        expiry_date = cleaned_data.get("expiry_date")

        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError(_("Expiry date cannot be in the past"))

        return cleaned_data


class ClientPackageForm(forms.ModelForm):
    """Form for assigning packages to clients."""

    class Meta:
        model = ClientPackage
        fields = ["client", "package", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter package choices to only show active packages
        self.fields["package"].queryset = Package.objects.filter(
            active=True,
            expiry_date__gte=timezone.now().date(),
        )

        # Filter client choices based on user permissions
        if self.user and not self.user.is_staff:
            self.fields["client"].queryset = self.fields["client"].queryset.filter(
                Q(instructor=self.user) | Q(client=self.user),
            )
