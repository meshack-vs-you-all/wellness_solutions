"""
Models for managing instructor schedules and availability.

This module provides models for handling:
- Regular working hours
- Recurring availability patterns
- Time slots
- Blackout dates and exceptions
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from wellness_instructors.models import WellnessInstructor


class Schedule(TimeStampedModel):
    """
    Represents an instructor's regular working schedule.
    This is the base schedule that defines when an instructor typically works.
    """

    class Meta:
        app_label = "schedules"
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")
        ordering = ["weekday", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["instructor", "weekday", "start_time"],
                name="unique_instructor_weekday_start",
            ),
        ]

    WEEKDAY_CHOICES = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    ]

    instructor = models.ForeignKey(
        WellnessInstructor,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name=_("Instructor"),
    )
    weekday = models.IntegerField(
        _("Day of Week"),
        choices=WEEKDAY_CHOICES,
        help_text=_("Day of the week for this schedule"),
    )
    start_time = models.TimeField(
        _("Start Time"),
        help_text=_("Start time for this schedule"),
    )
    end_time = models.TimeField(
        _("End Time"),
        help_text=_("End time for this schedule"),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Whether this schedule is currently active"),
    )

    def __str__(self):
        return f"{self.instructor} - {self.get_weekday_display()} ({self.start_time} - {self.end_time})"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(_("End time must be after start time"))

        # Check for overlapping schedules
        overlapping = Schedule.objects.filter(
            instructor=self.instructor,
            weekday=self.weekday,
            is_active=True,
        ).exclude(pk=self.pk)

        for schedule in overlapping:
            if (self.start_time < schedule.end_time and
                self.end_time > schedule.start_time):
                raise ValidationError(
                    _("This schedule overlaps with another schedule for this instructor"),
                )


class TimeSlot(TimeStampedModel):
    """
    Represents specific time slots within a schedule.
    These are the actual bookable time periods.
    """

    class Meta:
        app_label = "schedules"
        verbose_name = _("Time Slot")
        verbose_name_plural = _("Time Slots")
        ordering = ["start_datetime"]
        indexes = [
            models.Index(fields=["start_datetime", "status"]),
            models.Index(fields=["schedule", "status"]),
        ]

    STATUS_CHOICES = [
        ("available", _("Available")),
        ("booked", _("Booked")),
        ("blocked", _("Blocked")),
    ]

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name="time_slots",
        verbose_name=_("Schedule"),
    )
    start_datetime = models.DateTimeField(
        _("Start Time"),
        help_text=_("Start time for this slot"),
    )
    end_datetime = models.DateTimeField(
        _("End Time"),
        help_text=_("End time for this slot"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
    )
    notes = models.TextField(
        _("Notes"),
        blank=True,
        help_text=_("Any additional notes about this time slot"),
    )

    def __str__(self):
        return f"{self.schedule.instructor} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')} ({self.get_status_display()})"

    def clean(self):
        if self.start_datetime and self.end_datetime:
            if self.start_datetime >= self.end_datetime:
                raise ValidationError(_("End time must be after start time"))

            if self.start_datetime < timezone.now():
                raise ValidationError(_("Cannot create time slots in the past"))

            # Check if slot falls within schedule's time window
            slot_weekday = self.start_datetime.weekday()
            slot_start_time = self.start_datetime.time()
            slot_end_time = self.end_datetime.time()

            if (slot_weekday != self.schedule.weekday or
                slot_start_time < self.schedule.start_time or
                slot_end_time > self.schedule.end_time):
                raise ValidationError(
                    _("Time slot must fall within the schedule's time window"),
                )


class BlackoutDate(TimeStampedModel):
    """
    Represents dates when an instructor is unavailable.
    Used for vacations, sick days, or other exceptions to regular schedule.
    """

    class Meta:
        app_label = "schedules"
        verbose_name = _("Blackout Date")
        verbose_name_plural = _("Blackout Dates")
        ordering = ["start_date"]
        indexes = [
            models.Index(fields=["instructor", "start_date"]),
            models.Index(fields=["is_recurring"]),
        ]

    instructor = models.ForeignKey(
        WellnessInstructor,
        on_delete=models.CASCADE,
        related_name="blackout_dates",
        verbose_name=_("Instructor"),
        help_text=_("The instructor who is unavailable"),
    )
    start_date = models.DateTimeField(
        _("Start Date"),
        help_text=_("Start of unavailability period"),
    )
    end_date = models.DateTimeField(
        _("End Date"),
        help_text=_("End of unavailability period"),
    )
    reason = models.CharField(
        _("Reason"),
        max_length=200,
        help_text=_("Reason for unavailability"),
    )
    is_recurring = models.BooleanField(
        _("Recurring"),
        default=False,
        help_text=_("Whether this blackout date repeats yearly (e.g., holidays)"),
    )

    def __str__(self):
        return f"{self.instructor} - {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}"

    def clean(self):
        """Validate the blackout date."""
        if not self.start_date or not self.end_date:
            raise ValidationError(_("Both start date and end date are required"))

        # Ensure dates are timezone-aware
        if timezone.is_naive(self.start_date):
            self.start_date = timezone.make_aware(self.start_date)
        if timezone.is_naive(self.end_date):
            self.end_date = timezone.make_aware(self.end_date)

        # Validate date range
        if self.start_date >= self.end_date:
            raise ValidationError({
                "end_date": _("End date must be after start date"),
            })

        # Check for overlapping blackout dates
        if self.instructor_id:
            overlapping = BlackoutDate.objects.filter(
                instructor_id=self.instructor_id,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date,
            ).exclude(pk=self.pk if self.pk else None)

            if overlapping.exists():
                raise ValidationError({
                    "start_date": _("This blackout period overlaps with another blackout period"),
                })
