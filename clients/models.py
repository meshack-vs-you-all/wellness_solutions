from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ClientProfile(models.Model):
    """
    Essential client profile information that extends the User model.
    Keeps core functionality while allowing for future expansion.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_profile",
        verbose_name=_("User"),
    )
    emergency_contact_name = models.CharField(
        _("Emergency Contact Name"),
        max_length=100,
        blank=True,
        help_text=_("Name of emergency contact"),
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
    )
    emergency_contact_phone = models.CharField(
        _("Emergency Contact Phone"),
        max_length=15,
        validators=[phone_regex],
        blank=True,
        help_text=_("Phone number of emergency contact"),
    )
    notes = models.TextField(
        _("Notes"),
        blank=True,
        help_text=_("Additional notes about the client"),
    )
    medical_notes = models.TextField(
        _("Medical Notes"),
        blank=True,
        help_text=_("Important medical information or conditions"),
    )
    preferred_location = models.ForeignKey(
        "locations.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="preferred_clients",
        verbose_name=_("Preferred Location"),
        help_text=_("Preferred location for sessions"),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Designates whether this client is active. Unselect instead of deleting accounts."),
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Client Profile")
        verbose_name_plural = _("Client Profiles")
        permissions = [
            ("view_client_medical", "Can view client medical information"),
            ("manage_client_sessions", "Can manage client sessions"),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

    def get_absolute_url(self):
        return reverse("clients:client-detail", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def phone_number(self):
        return self.user.phone_number

    def save(self, *args, **kwargs):
        # Ensure the user has a client group
        from django.contrib.auth.models import Group
        client_group, _ = Group.objects.get_or_create(name="Clients")
        self.user.groups.add(client_group)
        super().save(*args, **kwargs)


class ClientSession(models.Model):
    """
    Tracks individual client sessions, linking to bookings and storing session-specific data.
    """
    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("Client"),
    )
    booking = models.OneToOneField(
        "bookings.Booking",
        on_delete=models.CASCADE,
        related_name="client_session",
        verbose_name=_("Booking"),
    )
    notes = models.TextField(
        _("Session Notes"),
        blank=True,
        help_text=_("Notes from the session"),
    )
    feedback = models.TextField(
        _("Client Feedback"),
        blank=True,
        help_text=_("Feedback provided by the client"),
    )
    rating = models.PositiveSmallIntegerField(
        _("Session Rating"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text=_("Client rating of the session (1-5)"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=[
            ("scheduled", _("Scheduled")),
            ("completed", _("Completed")),
            ("cancelled", _("Cancelled")),
            ("no_show", _("No Show")),
        ],
        default="scheduled",
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Client Session")
        verbose_name_plural = _("Client Sessions")
        ordering = ["-booking__start_time"]
        permissions = [
            ("can_view_session_notes", "Can view session notes"),
            ("can_manage_session_status", "Can manage session status"),
        ]

    def __str__(self):
        return f"Session for {self.client.full_name} on {self.booking.start_time}"

    def get_absolute_url(self):
        return reverse("clients:session-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:  # New session
            from django.conf import settings
            from django.core.mail import send_mail
            from django.template.loader import render_to_string

            # Send confirmation email
            context = {
                "client": self.client,
                "session": self,
                "site_name": settings.SITE_NAME,
            }
            subject = f"Session Confirmation - {settings.SITE_NAME}"
            html_message = render_to_string("clients/email/session_confirmation.html", context)
            text_message = render_to_string("clients/email/session_confirmation.txt", context)

            try:
                send_mail(
                    subject=subject,
                    message=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.client.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception:
                # Log the error but don't prevent session creation
                import logging
                logger = logging.getLogger(__name__)
                logger.exception("Failed to send session confirmation email")

        super().save(*args, **kwargs)
