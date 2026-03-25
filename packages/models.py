"""
Models for managing purchased service packages and their assignments.
"""


from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from services.models import Organization


class Package(models.Model):
    """Represents a purchased package instance."""
    name = models.CharField(
        max_length=100,
        help_text=_("Name of the package"),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="package_instances",
        help_text=_("User who owns this package"),
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text=_("Organization if this is a corporate package"),
    )
    service_package = models.ForeignKey(
        "services.ServicePackage",
        on_delete=models.PROTECT,
        related_name="purchased_packages",
        help_text=_("Service package template this package is based on"),
    )
    total_sessions = models.PositiveIntegerField(
        help_text=_("Total number of sessions in the package"),
    )
    used_sessions = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of sessions already used"),
    )
    expiry_date = models.DateField(
        help_text=_("Date when the package expires"),
    )
    purchase_date = models.DateTimeField(
        default=timezone.now,
        help_text=_("Date when the package was purchased"),
    )
    active = models.BooleanField(
        default=True,
        help_text=_("Whether this package is currently active"),
    )

    class Meta:
        ordering = ["-expiry_date"]
        indexes = [
            models.Index(fields=["expiry_date"]),
            models.Index(fields=["active"]),
            models.Index(fields=["purchase_date"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.sessions_remaining()} sessions remaining)"

    def clean(self):
        """Validate package data."""
        if self.total_sessions < self.used_sessions:
            raise ValidationError(_("Used sessions cannot exceed total sessions"))
        if self.expiry_date and self.expiry_date < timezone.now().date():
            raise ValidationError(_("Expiry date cannot be in the past"))

    def save(self, *args, **kwargs):
        """Override save to handle initialization from service package."""
        if not self.pk and self.service_package:
            # Initialize from service package template
            if not self.name:
                self.name = self.service_package.name
            if not self.total_sessions:
                self.total_sessions = self.service_package.sessions
            if not self.expiry_date:
                self.expiry_date = timezone.now().date() + timezone.timedelta(days=self.service_package.validity_days)
        super().save(*args, **kwargs)

    def sessions_remaining(self):
        """Calculate remaining sessions in the package."""
        return max(0, self.total_sessions - self.used_sessions)

    def is_valid(self):
        """Check if the package is still valid."""
        return (
            self.active and
            self.sessions_remaining() > 0 and
            self.expiry_date >= timezone.now().date()
        )


class ClientPackage(models.Model):
    """Track package assignments to clients."""
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="client_packages",
        help_text=_("Client assigned to this package"),
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name="client_assignments",
        help_text=_("Package assigned to the client"),
    )
    assigned_date = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Date when package was assigned"),
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="package_assignments",
        help_text=_("User who assigned the package"),
    )
    notes = models.TextField(
        blank=True,
        help_text=_("Additional notes about the assignment"),
    )

    class Meta:
        ordering = ["-assigned_date"]
        indexes = [
            models.Index(fields=["assigned_date"]),
        ]
        unique_together = ["client", "package"]

    def __str__(self):
        return f"{self.client.get_full_name()} - {self.package.name}"
