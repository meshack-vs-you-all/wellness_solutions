"""
Models for managing services, packages, and corporate programs.

This module provides models for handling:
- Service categories and types
- Individual and group services
- Corporate wellness programs
- Service packages
- Organization management
- Proposal system
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class ServiceCategory(TimeStampedModel):
    """
    Model representing different categories of services offered.
    """

    CATEGORY_TYPES = [
        ("individual", _("Individual Services")),
        ("group", _("Group Services")),
        ("corporate", _("Corporate Services")),
        ("therapeutic", _("Therapeutic Services")),
    ]

    name = models.CharField(
        _("Name"),
        max_length=100,
        help_text=_('Category name (e.g., "25min Stretch", "Corporate Wellness")'),
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Detailed description of this service category"),
    )
    type = models.CharField(
        _("Type"),
        max_length=20,
        choices=CATEGORY_TYPES,
        default="individual",
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Whether this category is currently active"),
    )

    class Meta:
        app_label = "services"
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Service(TimeStampedModel):
    """
    Model representing specific services that can be offered.
    """

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("Category"),
    )
    name = models.CharField(
        _("Name"),
        max_length=200,
        help_text=_("Name of the service"),
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Detailed description of the service"),
    )
    duration = models.PositiveIntegerField(
        _("Duration (minutes)"),
        help_text=_("Duration of the service in minutes"),
        validators=[MinValueValidator(15), MaxValueValidator(480)],
    )
    max_participants = models.PositiveIntegerField(
        _("Maximum Participants"),
        help_text=_("Maximum number of participants allowed"),
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        default=1,
    )
    price = models.DecimalField(
        _("Base Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Base price for this service"),
    )
    supports_home_visits = models.BooleanField(
        _("Supports Home Visits"),
        default=False,
        help_text=_("Whether this service can be provided at client's home"),
    )
    home_visit_surcharge = models.DecimalField(
        _("Home Visit Surcharge"),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Additional charge for home visits"),
    )
    is_corporate_eligible = models.BooleanField(
        _("Is Corporate Eligible"),
        default=False,
        help_text=_("Whether this service is eligible for corporate programs"),
    )

    class Meta:
        app_label = "services"
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CorporateProgram(TimeStampedModel):
    """
    Model representing corporate wellness programs.
    """

    name = models.CharField(
        _("Program Name"),
        max_length=100,
        help_text=_("Name of the corporate program"),
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Detailed description of the program"),
    )
    services = models.ManyToManyField(
        Service,
        related_name="corporate_programs",
        verbose_name=_("Included Services"),
        limit_choices_to={"is_corporate_eligible": True},
    )
    min_participants = models.PositiveIntegerField(
        _("Minimum Participants"),
        default=5,
    )
    max_participants = models.PositiveIntegerField(
        _("Maximum Participants"),
        default=20,
    )

    class Meta:
        verbose_name = _("Corporate Program")
        verbose_name_plural = _("Corporate Programs")
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServicePackage(TimeStampedModel):
    """
    Model representing service packages (both individual and corporate).
    """

    name = models.CharField(
        _("Package Name"),
        max_length=100,
        help_text=_("Name of the package"),
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="packages",
        verbose_name=_("Service"),
    )
    sessions = models.PositiveIntegerField(
        _("Number of Sessions"),
        help_text=_("Number of sessions included in this package"),
        validators=[MinValueValidator(1)],
    )
    price_per_session = models.DecimalField(
        _("Price per Session"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text=_("Price per session (must be greater than 0)"),
    )
    validity_days = models.PositiveIntegerField(
        _("Validity Period"),
        help_text=_("Number of days the package is valid for"),
        validators=[MinValueValidator(1)],
        default=30,
    )
    discount_percentage = models.DecimalField(
        _("Discount Percentage"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
        help_text=_("Discount percentage off regular service price"),
    )

    class Meta:
        app_label = "services"
        verbose_name = _("Service Package")
        verbose_name_plural = _("Service Packages")
        ordering = ["service", "name"]

    def __str__(self):
        return f"{self.name} ({self.sessions} sessions)"

    def clean(self):
        """Validate package data."""
        super().clean()

        if hasattr(self, "service") and self.service:
            # Calculate minimum allowed price per session (50% of regular price)
            min_price = self.service.price * Decimal("0.5")

            if self.price_per_session < min_price:
                raise ValidationError({
                    "price_per_session": _(
                        "Price per session cannot be less than 50% of the regular service price "
                        f"(minimum: ${min_price})",
                    ),
                })

            # If discount percentage is set, validate price_per_session matches
            if self.discount_percentage:
                expected_price = self.service.price * (1 - self.discount_percentage / 100)
                if abs(self.price_per_session - expected_price) > Decimal("0.01"):
                    raise ValidationError({
                        "price_per_session": _(
                            "Price per session must match the discount percentage",
                        ),
                    })

    def save(self, *args, **kwargs):
        """Override save to auto-calculate price_per_session from discount."""
        if self.discount_percentage and hasattr(self, "service") and self.service:
            # Calculate price_per_session based on discount
            self.price_per_session = self.service.price * (1 - self.discount_percentage / 100)

        super().save(*args, **kwargs)

    def get_total_price(self):
        """Calculate total package price."""
        return self.price_per_session * self.sessions

    def get_savings_amount(self):
        """Calculate total savings compared to regular price."""
        if not hasattr(self, "service") or not self.service:
            return Decimal("0.00")

        regular_total = self.service.price * self.sessions
        package_total = self.get_total_price()
        return regular_total - package_total

    def get_savings_percentage(self):
        """Calculate savings as percentage of regular price."""
        if not hasattr(self, "service") or not self.service:
            return Decimal("0.00")

        regular_total = self.service.price * self.sessions
        if regular_total == 0:
            return Decimal("0.00")

        savings = self.get_savings_amount()
        return (savings / regular_total) * 100


class Organization(TimeStampedModel):
    """
    Model representing corporate/institutional clients.
    """

    name = models.CharField(
        _("Organization Name"),
        max_length=200,
        help_text=_("Name of the organization"),
    )
    industry = models.CharField(
        _("Industry"),
        max_length=100,
        help_text=_("Industry sector of the organization"),
    )
    contact_email = models.EmailField(
        _("Contact Email"),
        help_text=_("Primary contact email"),
    )
    contact_phone = models.CharField(
        _("Contact Phone"),
        max_length=20,
        help_text=_("Primary contact phone number"),
        validators=[
            RegexValidator(
                regex=r"^\+\d{10,}$",
                message=_("Phone number must start with + followed by at least 10 digits."),
                code="invalid_phone",
            ),
        ],
    )
    address = models.TextField(
        _("Address"),
        help_text=_("Physical address of the organization"),
    )
    employee_count = models.PositiveIntegerField(
        _("Number of Employees"),
        help_text=_("Total number of employees"),
        validators=[MinValueValidator(1)],
    )
    active_programs = models.ManyToManyField(
        CorporateProgram,
        related_name="organizations",
        verbose_name=_("Active Programs"),
        blank=True,
    )
    contract_start_date = models.DateField(
        _("Contract Start Date"),
        null=True,
        blank=True,
    )
    contract_end_date = models.DateField(
        _("Contract End Date"),
        null=True,
        blank=True,
    )
    special_requirements = models.TextField(
        _("Special Requirements"),
        blank=True,
        help_text=_("Any special requirements or notes"),
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Proposal(TimeStampedModel):
    """
    Model representing proposals sent to organizations.
    
    This model tracks proposals for corporate programs and services
    that are sent to organizations. It includes details about the
    proposed services, pricing, and tracks the status of the proposal.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="proposals",
        verbose_name=_("Organization"),
        null=True,  # Temporarily allow null
        blank=True,  # Temporarily allow blank
    )
    title = models.CharField(
        _("Title"),
        max_length=200,
        help_text=_("Title of the proposal"),
    )
    date_submitted = models.DateTimeField(
        _("Date Submitted"),
        null=True,  # Temporarily allow null
        blank=True,  # Temporarily allow blank
        help_text=_("Date when the proposal was submitted"),
    )
    programs = models.ManyToManyField(
        CorporateProgram,
        verbose_name=_("Programs"),
        help_text=_("Corporate programs included in this proposal"),
    )
    custom_services = models.TextField(
        _("Custom Services"),
        blank=True,
        help_text=_("Description of any custom services offered"),
    )
    pricing_details = models.TextField(
        _("Pricing Details"),
        help_text=_("Detailed pricing information"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=[
            ("draft", _("Draft")),
            ("sent", _("Sent")),
            ("accepted", _("Accepted")),
            ("rejected", _("Rejected")),
        ],
        default="draft",
        help_text=_("Current status of the proposal"),
    )
    valid_until = models.DateField(
        _("Valid Until"),
        help_text=_("Date until which this proposal is valid"),
    )
    terms_conditions = models.TextField(
        _("Terms and Conditions"),
        help_text=_("Terms and conditions of the proposal"),
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_proposals",
        verbose_name=_("Created By"),
    )

    class Meta:
        verbose_name = _("Proposal")
        verbose_name_plural = _("Proposals")
        ordering = ["-date_submitted"]

    def __str__(self):
        return f"{self.title} - {self.organization.name}"

    def get_absolute_url(self):
        return reverse("services:proposal-detail", kwargs={"pk": self.pk})
