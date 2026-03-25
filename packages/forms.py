"""Forms for the packages app."""

from django import forms
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import ClientPackage, Package


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
