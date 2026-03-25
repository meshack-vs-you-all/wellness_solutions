"""
Forms for the locations app.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Location, LocationInstructor, LocationService


class LocationForm(forms.ModelForm):
    """Form for creating and updating locations."""

    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
        }),
    )
    operating_hours = forms.JSONField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Location
        fields = ["name", "type", "address", "capacity", "status", "description", "operating_hours", "amenities"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
            }),
            "type": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
            }),
            "address": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
            }),
            "capacity": forms.NumberInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
            }),
            "status": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm",
            }),
            "amenities": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})

        # Pre-fill phone and email from contact_info if instance exists
        if instance and hasattr(instance, "contact_info") and instance.contact_info:
            initial.update({
                "phone": instance.contact_info.get("phone", ""),
                "email": instance.contact_info.get("email", ""),
            })

        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # Ensure operating_hours is a dict
        if "operating_hours" not in cleaned_data:
            cleaned_data["operating_hours"] = {}

        # Ensure amenities is a dict
        if "amenities" not in cleaned_data:
            cleaned_data["amenities"] = {}

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set contact_info
        instance.contact_info = {
            "phone": self.cleaned_data.get("phone", ""),
            "email": self.cleaned_data.get("email", ""),
        }

        if commit:
            instance.save()
        return instance


class LocationServiceForm(forms.ModelForm):
    """Form for managing services at locations."""

    class Meta:
        model = LocationService
        fields = [
            "location", "service", "price_adjustment",
            "availability_rules", "is_available", "notes",
        ]

    def clean_availability_rules(self):
        """Validate availability_rules JSON structure."""
        rules = self.cleaned_data.get("availability_rules")
        required_fields = ["schedule_type", "restrictions"]

        for field in required_fields:
            if field not in rules:
                raise forms.ValidationError(
                    _("Availability rules must include %(field)s"),
                    params={"field": field},
                )
        return rules


class LocationInstructorForm(forms.ModelForm):
    """Form for managing instructor assignments to locations."""

    class Meta:
        model = LocationInstructor
        fields = [
            "location", "instructor", "availability_rules",
            "is_primary", "status", "notes",
        ]

    def clean(self):
        """Validate the entire form."""
        cleaned_data = super().clean()
        is_primary = cleaned_data.get("is_primary")
        location = cleaned_data.get("location")
        instructor = cleaned_data.get("instructor")

        if is_primary and location and instructor:
            # Check if another LocationInstructor exists for this instructor
            # that is already marked as primary
            existing_primary = LocationInstructor.objects.filter(
                instructor=instructor,
                is_primary=True,
            ).exclude(pk=self.instance.pk if self.instance else None)

            if existing_primary.exists():
                raise forms.ValidationError(
                    _("This instructor already has a primary location: %(location)s"),
                    params={"location": existing_primary.first().location.name},
                )

        return cleaned_data

    def clean_availability_rules(self):
        """Validate availability_rules JSON structure."""
        rules = self.cleaned_data.get("availability_rules")
        required_fields = ["schedule_type", "hours"]

        for field in required_fields:
            if field not in rules:
                raise forms.ValidationError(
                    _("Availability rules must include %(field)s"),
                    params={"field": field},
                )
        return rules
