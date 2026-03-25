"""
Models for the wellness_instructors app.

This module contains the core models for managing wellness instructors and their sessions
in the Wellness Solutions platform. The models are designed to be extensible and support
future enhancements while maintaining clean relationships and data integrity.
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class WellnessInstructor(TimeStampedModel):
    """
    Model representing a stretch instructor.
    
    This model extends the base User model through a one-to-one relationship and adds
    instructor-specific fields. It uses TimeStampedModel for automatic created/modified
    timestamp tracking.
    """

    SPECIALIZATION_CHOICES = [
        ("flexibility", _("Flexibility Training")),
        ("recovery", _("Recovery & Rehabilitation")),
        ("sports", _("Sports Performance")),
        ("general", _("General Wellness")),
        ("therapeutic", _("Therapeutic Stretching")),
    ]

    CERTIFICATION_LEVELS = [
        ("certified", _("Certified Professional")),
        ("advanced", _("Advanced Certification")),
        ("specialist", _("Specialist Certification")),
        ("master", _("Master Instructor")),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wellness_instructor",
        verbose_name=_("User Account"),
    )
    bio = models.TextField(
        _("Biography"),
        help_text=_("A brief introduction about the instructor"),
        max_length=1000,
        blank=True,
    )
    specializations = models.CharField(
        _("Specializations"),
        max_length=20,
        choices=SPECIALIZATION_CHOICES,
        default="general",
        help_text=_("Primary area of expertise"),
    )
    certification_level = models.CharField(
        _("Certification Level"),
        max_length=20,
        choices=CERTIFICATION_LEVELS,
        default="certified",
        help_text=_("Current certification level"),
    )
    years_of_experience = models.PositiveSmallIntegerField(
        _("Years of Experience"),
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text=_("Years of professional experience"),
        default=0,
    )
    is_available = models.BooleanField(
        _("Is Available"),
        default=True,
        help_text=_("Indicates if the instructor is currently accepting new clients"),
    )
    hourly_rate = models.DecimalField(
        _("Hourly Rate"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Standard hourly rate for sessions"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Stretch Instructor")
        verbose_name_plural = _("Wellness Instructors")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def get_absolute_url(self):
        return reverse("wellness_instructors:instructor-detail", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email


class Session(TimeStampedModel):
    """
    Model representing a wellness session.
    
    This model defines the structure and metadata for both individual and group
    sessions. It includes scheduling, capacity, and type information.
    """

    SESSION_TYPES = [
        ("one_on_one", _("One-on-One")),
        ("group", _("Group Session")),
        ("workshop", _("Workshop")),
    ]

    DIFFICULTY_LEVELS = [
        ("beginner", _("Beginner")),
        ("intermediate", _("Intermediate")),
        ("advanced", _("Advanced")),
        ("all_levels", _("All Levels")),
    ]

    instructor = models.ForeignKey(
        WellnessInstructor,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("Instructor"),
    )
    time_slot = models.OneToOneField(
        "schedules.TimeSlot",
        on_delete=models.CASCADE,
        related_name="session",
        verbose_name=_("Time Slot"),
        null=True,
        blank=True,
    )
    title = models.CharField(
        _("Title"),
        max_length=200,
        help_text=_("Name or title of the session"),
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Detailed description of the session"),
        blank=True,
    )
    session_type = models.CharField(
        _("Session Type"),
        max_length=20,
        choices=SESSION_TYPES,
        default="one_on_one",
    )
    difficulty_level = models.CharField(
        _("Difficulty Level"),
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default="all_levels",
    )
    duration = models.PositiveSmallIntegerField(
        _("Duration (minutes)"),
        validators=[MinValueValidator(15), MaxValueValidator(180)],
        help_text=_("Session duration in minutes"),
        default=60,
    )
    max_participants = models.PositiveSmallIntegerField(
        _("Maximum Participants"),
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text=_("Maximum number of participants allowed"),
        default=1,
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Price per session"),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Indicates if this session is currently being offered"),
    )

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["instructor", "session_type"]),
            models.Index(fields=["is_active", "difficulty_level"]),
        ]

    def __str__(self):
        return f"{self.title} by {self.instructor}"

    def get_absolute_url(self):
        return reverse("wellness_instructors:session-detail", kwargs={"pk": self.pk})

    @property
    def is_group_session(self):
        return self.session_type in ["group", "workshop"]

    @property
    def is_individual_session(self):
        return self.session_type == "one_on_one"

    @property
    def start_time(self):
        """Get session start time from associated time slot."""
        return self.time_slot.start_datetime if self.time_slot else None

    @property
    def end_time(self):
        """Get session end time from associated time slot."""
        return self.time_slot.end_datetime if self.time_slot else None
