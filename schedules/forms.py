from datetime import datetime

from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import BlackoutDate, Schedule, TimeSlot


class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Schedule
        fields = ["weekday", "start_time", "end_time"]
        widgets = {
            "weekday": forms.Select(attrs={
                "class": "form-select",
                "data-tooltip": _("Select the day of the week for your regular schedule"),
            }),
            "start_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-input",
                "data-tooltip": _("Choose when you start working on this day"),
            }),
            "end_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-input",
                "data-tooltip": _("Choose when you finish working on this day"),
            }),
        }
        help_texts = {
            "weekday": _("The day of the week when this schedule applies"),
            "start_time": _("Your working hours start time (e.g., 09:00)"),
            "end_time": _("Your working hours end time (e.g., 17:00)"),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.user and not hasattr(self.user, "wellness_instructor"):
            raise forms.ValidationError(_("You must be registered as an instructor to create schedules."))
        return cleaned_data

    def clean_end_time(self):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(_("End time must be after start time"))
        return end_time

    def clean_weekday(self):
        weekday = self.cleaned_data.get("weekday")
        if weekday not in dict(Schedule.WEEKDAY_CHOICES):
            raise forms.ValidationError(_("Invalid weekday"))
        return weekday

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and hasattr(self.user, "wellness_instructor"):
            instance.instructor = self.user.wellness_instructor
        if commit:
            instance.save()
        return instance

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ["schedule", "start_datetime", "end_datetime", "status"]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_end_datetime(self):
        start_datetime = self.cleaned_data.get("start_datetime")
        end_datetime = self.cleaned_data.get("end_datetime")

        if start_datetime and end_datetime:
            if start_datetime >= end_datetime:
                raise forms.ValidationError("End time must be after start time")
        return end_datetime

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")
        schedule = cleaned_data.get("schedule")

        if start_datetime and end_datetime and schedule:
            if start_datetime.date() != end_datetime.date():
                self.add_error("end_datetime", "Start and end times must be on the same day")

            # Check if the time slot is within the schedule's time range
            if start_datetime.time() < schedule.start_time or end_datetime.time() > schedule.end_time:
                self.add_error("start_datetime", "Time slot must be within the schedule's time range")

            # Check if the weekday matches
            if start_datetime.weekday() != schedule.weekday:
                self.add_error("start_datetime", "Time slot must be on the same weekday as the schedule")

            # Check for overlapping time slots
            overlapping_slots = TimeSlot.objects.filter(
                schedule=schedule,
                start_datetime__lt=end_datetime,
                end_datetime__gt=start_datetime,
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_slots.exists():
                self.add_error("start_datetime", "This time slot overlaps with an existing time slot")

        return cleaned_data

class BlackoutDateForm(forms.ModelForm):
    """Form for creating and updating blackout dates."""

    class Meta:
        model = BlackoutDate
        fields = ["instructor", "start_date", "end_date", "reason"]

    def clean(self):
        """Clean and validate form data."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        instructor = cleaned_data.get("instructor")

        if not start_date or not end_date or not instructor:
            return cleaned_data

        # Convert dates to timezone-aware datetime objects
        start_datetime = timezone.make_aware(
            datetime.combine(start_date, datetime.min.time()),
        )
        end_datetime = timezone.make_aware(
            datetime.combine(end_date, datetime.max.time()),
        )

        # Check if start date is in the past
        if start_datetime < timezone.now():
            self.add_error("start_date", "Start date cannot be in the past.")

        # Check if end date is before start date
        if end_datetime < start_datetime:
            self.add_error("end_date", "End date must be after start date.")

        # Check for overlapping blackout dates
        overlapping = BlackoutDate.objects.filter(
            instructor=instructor,
            start_date__lte=end_datetime,
            end_date__gte=start_datetime,
        )

        # Exclude current instance if updating
        if self.instance.pk:
            overlapping = overlapping.exclude(pk=self.instance.pk)

        if overlapping.exists():
            self.add_error(
                None,
                "This blackout period overlaps with an existing one.",
            )

        return cleaned_data

    def save(self, commit=True):
        """Save the form data to create or update a BlackoutDate instance."""
        instance = super().save(commit=False)

        # Convert dates to datetime objects if they exist
        if self.cleaned_data.get("start_date"):
            instance.start_date = timezone.make_aware(
                datetime.combine(
                    self.cleaned_data["start_date"],
                    datetime.min.time(),
                ),
            )
        if self.cleaned_data.get("end_date"):
            instance.end_date = timezone.make_aware(
                datetime.combine(
                    self.cleaned_data["end_date"],
                    datetime.max.time(),
                ),
            )

        if commit:
            instance.save()
        return instance
