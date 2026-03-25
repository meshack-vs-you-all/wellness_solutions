from typing import ClassVar

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model for Wellness Solutions.
    
    This model extends the default Django user model to include additional
    fields necessary for the stretch hub platform. It uses email as the
    primary identifier instead of username.
    """

    # Basic Information
    first_name = models.CharField(
        _("First Name"),
        max_length=150,
        default="",
        blank=False,
        help_text=_("Enter your first name"),
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=150,
        default="",
        blank=False,
        help_text=_("Enter your last name"),
    )
    email = models.EmailField(
        _("Email Address"),
        unique=True,
        help_text=_("Your email address will be used for login and communications"),
    )
    username = None  # We use email instead of username

    # Contact Information
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
    )
    phone_number = models.CharField(
        _("Phone Number"),
        validators=[phone_regex],
        max_length=17,
        blank=True,
        help_text=_("Enter your phone number in international format"),
    )

    # Profile Information
    date_of_birth = models.DateField(
        _("Date of Birth"),
        null=True,
        blank=True,
        help_text=_("Required for age-appropriate session recommendations"),
    )
    emergency_contact_name = models.CharField(
        _("Emergency Contact Name"),
        max_length=255,
        blank=True,
        help_text=_("Name of person to contact in case of emergency"),
    )
    emergency_contact_phone = models.CharField(
        _("Emergency Contact Phone"),
        validators=[phone_regex],
        max_length=16,
        blank=True,
        help_text=_("Phone number of emergency contact"),
    )

    # Organization Information
    organization = models.ForeignKey(
        "services.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
        verbose_name=_("Organization"),
        help_text=_("Associated organization or company"),
    )

    # Preferences and Settings
    receive_notifications = models.BooleanField(
        _("Receive Notifications"),
        default=True,
        help_text=_("Receive email notifications about sessions and updates"),
    )
    preferred_language = models.CharField(
        _("Preferred Language"),
        max_length=10,
        choices=[("en", _("English")), ("es", _("Spanish"))],
        default="en",
        help_text=_("Preferred language for communications"),
    )

    # Fields configuration
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"pk": self.pk})

    def get_organization(self):
        """Get the user's organization."""
        Organization = apps.get_model("services", "Organization")
        return Organization.objects.filter(contact_email=self.email).first()

    def get_initials(self):
        """Get user's initials for display purposes."""
        initials = ""
        if self.first_name:
            initials += self.first_name[0].upper()
        if self.last_name:
            initials += self.last_name[0].upper()
        return initials if initials else self.email[0].upper()
