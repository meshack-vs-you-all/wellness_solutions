"""
Forms for the services app.
"""


from django import forms
from django.utils.translation import gettext_lazy as _

from .models import (
    CorporateProgram,
    Organization,
    Proposal,
    Service,
    ServiceCategory,
    ServicePackage,
)


# Common Tailwind classes for form inputs
INPUT_CLASSES = "form-input"
SELECT_CLASSES = "form-select"
TEXTAREA_CLASSES = "form-input"
CHECKBOX_CLASSES = "form-checkbox"
NUMBER_INPUT_CLASSES = "form-input"


class ServiceCategoryForm(forms.ModelForm):
    """Form for creating and updating service categories."""

    class Meta:
        model = ServiceCategory
        fields = ["name", "description", "type", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter category name"),
            }),
            "description": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 3,
                "placeholder": _("Enter category description"),
            }),
            "type": forms.Select(attrs={
                "class": SELECT_CLASSES,
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": CHECKBOX_CLASSES,
            }),
        }

    def clean_name(self):
        """Ensure category name is unique."""
        name = self.cleaned_data["name"]
        if ServiceCategory.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("A service category with this name already exists."))
        return name


class ServiceForm(forms.ModelForm):
    """Form for creating and updating services."""

    class Meta:
        model = Service
        fields = [
            "category", "name", "description", "duration",
            "max_participants", "price", "supports_home_visits",
            "home_visit_surcharge", "is_corporate_eligible",
        ]
        widgets = {
            "category": forms.Select(attrs={
                "class": SELECT_CLASSES,
                "required": True,
            }),
            "name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter service name"),
                "required": True,
            }),
            "description": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 3,
                "placeholder": _("Enter service description"),
                "required": True,
            }),
            "duration": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "15",
                "max": "480",
                "required": True,
            }),
            "max_participants": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "1",
                "max": "50",
                "required": True,
            }),
            "price": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "0",
                "step": "0.01",
                "required": True,
            }),
            "supports_home_visits": forms.CheckboxInput(attrs={
                "class": CHECKBOX_CLASSES,
            }),
            "home_visit_surcharge": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "0",
                "step": "0.01",
            }),
            "is_corporate_eligible": forms.CheckboxInput(attrs={
                "class": CHECKBOX_CLASSES,
            }),
        }

    def clean(self):
        """Validate service data."""
        cleaned_data = super().clean()
        duration = cleaned_data.get("duration")
        max_participants = cleaned_data.get("max_participants")
        price = cleaned_data.get("price")

        if duration and duration < 15:
            raise forms.ValidationError(_("Duration must be at least 15 minutes."))

        if max_participants and max_participants < 1:
            raise forms.ValidationError(_("Maximum participants must be at least 1."))

        if price and price < 0:
            raise forms.ValidationError(_("Price cannot be negative."))

        return cleaned_data


class ServicePackageForm(forms.ModelForm):
    """Form for creating and updating service packages."""

    class Meta:
        model = ServicePackage
        fields = [
            "name", "service", "sessions",
            "price_per_session", "validity_days",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter package name"),
            }),
            "service": forms.Select(attrs={
                "class": SELECT_CLASSES,
            }),
            "sessions": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "1",
            }),
            "price_per_session": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "0",
                "step": "0.01",
            }),
            "validity_days": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "1",
            }),
        }

    def clean(self):
        """Validate package data."""
        cleaned_data = super().clean()
        # Add validation logic here
        return cleaned_data


class CorporateProgramForm(forms.ModelForm):
    """Form for creating and updating corporate programs."""

    class Meta:
        model = CorporateProgram
        fields = ["name", "description", "services", "min_participants", "max_participants"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter program name"),
            }),
            "description": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 3,
                "placeholder": _("Enter program description"),
            }),
            "services": forms.SelectMultiple(attrs={
                "class": SELECT_CLASSES,
            }),
            "min_participants": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "1",
            }),
            "max_participants": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "1",
            }),
        }

    def clean_assessment_frequency(self):
        """Validate assessment frequency."""
        frequency = self.cleaned_data.get("assessment_frequency")
        if frequency and frequency < 1:
            raise forms.ValidationError(_("Assessment frequency must be at least 1 day."))
        return frequency

    def clean(self):
        """Validate corporate program data."""
        cleaned_data = super().clean()
        # Add validation logic here
        return cleaned_data


class OrganizationForm(forms.ModelForm):
    """Form for creating and updating organizations."""

    class Meta:
        model = Organization
        fields = [
            "name",
            "industry",
            "contact_email",
            "contact_phone",
            "address",
            "employee_count",
            "active_programs",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter organization name"),
            }),
            "industry": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter industry"),
            }),
            "contact_email": forms.EmailInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter contact email"),
            }),
            "contact_phone": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter contact phone"),
            }),
            "address": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 3,
                "placeholder": _("Enter address"),
            }),
            "employee_count": forms.NumberInput(attrs={
                "class": NUMBER_INPUT_CLASSES,
                "min": "1",
            }),
            "active_programs": forms.SelectMultiple(attrs={
                "class": SELECT_CLASSES,
            }),
        }

    def clean_contact_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get("contact_phone")
        if not phone.startswith("+"):
            raise forms.ValidationError(_("Phone number must start with +."))
        return phone

    def clean(self):
        """Validate organization data."""
        cleaned_data = super().clean()
        # Add validation logic here
        return cleaned_data


class ProposalForm(forms.ModelForm):
    """Form for creating and updating proposals."""

    class Meta:
        model = Proposal
        fields = [
            "organization", "title", "date_submitted", "programs",
            "custom_services", "pricing_details", "status",
            "valid_until", "terms_conditions",
        ]
        widgets = {
            "organization": forms.Select(attrs={
                "class": SELECT_CLASSES,
            }),
            "title": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": _("Enter proposal title"),
            }),
            "date_submitted": forms.DateInput(attrs={
                "class": INPUT_CLASSES,
                "type": "date",
            }),
            "programs": forms.SelectMultiple(attrs={
                "class": SELECT_CLASSES,
            }),
            "custom_services": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 3,
                "placeholder": _("Enter custom services"),
            }),
            "pricing_details": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 3,
                "placeholder": _("Enter pricing details"),
            }),
            "status": forms.Select(attrs={
                "class": SELECT_CLASSES,
            }),
            "valid_until": forms.DateInput(attrs={
                "class": INPUT_CLASSES,
                "type": "date",
            }),
            "terms_conditions": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 3,
                "placeholder": _("Enter terms and conditions"),
            }),
        }
        error_messages = {
            "organization": {"required": _("Organization is required.")},
            "title": {"required": _("Title is required.")},
            "date_submitted": {"required": _("Submission date is required.")},
            "programs": {"required": _("At least one program must be selected.")},
            "pricing_details": {"required": _("Pricing details are required.")},
            "valid_until": {"required": _("Valid until date is required.")},
            "terms_conditions": {"required": _("Terms and conditions are required.")},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["organization"].required = True
        self.fields["date_submitted"].required = True

    def clean(self):
        """Validate proposal data."""
        cleaned_data = super().clean()
        # Add validation logic here
        return cleaned_data
