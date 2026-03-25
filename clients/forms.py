from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ClientProfile, ClientSession


class ClientProfileForm(forms.ModelForm):
    """Form for updating client profile information."""

    class Meta:
        model = ClientProfile
        fields = [
            "emergency_contact_name",
            "emergency_contact_phone",
            "medical_notes",
            "preferred_location",
            "notes",
        ]

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data.get("emergency_contact_phone")
        if phone:
            # Remove any spaces or special characters except +
            phone = "".join(c for c in phone if c.isdigit() or c == "+")
            if not phone.startswith("+"):
                phone = "+" + phone
        return phone


class ClientSessionForm(forms.ModelForm):
    """Form for creating/updating client sessions."""

    class Meta:
        model = ClientSession
        fields = ["notes", "feedback", "rating", "status"]
        widgets = {
            "rating": forms.RadioSelect,
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        rating = cleaned_data.get("rating")
        feedback = cleaned_data.get("feedback")

        if status == "completed":
            if not rating and not self.instance.rating:
                self.add_error("rating", _("Rating is required for completed sessions."))
            if not feedback and not self.instance.feedback:
                self.add_error("feedback", _("Feedback is required for completed sessions."))

        return cleaned_data


class SessionFeedbackForm(forms.ModelForm):
    """Form for clients to provide session feedback."""

    class Meta:
        model = ClientSession
        fields = ["rating", "feedback"]
        widgets = {
            "rating": forms.RadioSelect(attrs={"class": "rating-input"}),
            "feedback": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": _("Please share your experience with this session..."),
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].required = True
        self.fields["feedback"].required = True
