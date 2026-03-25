"""Tests for the schedules app forms."""
from datetime import datetime, time, timedelta

from django.test import TestCase
from django.utils import timezone

from ..wellness_instructors.models import WellnessInstructor
from ..users.tests.factories import UserFactory
from .forms import BlackoutDateForm, ScheduleForm, TimeSlotForm
from .models import BlackoutDate, Schedule


class ScheduleFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.instructor = WellnessInstructor.objects.create(user=cls.user)

    def test_valid_schedule_form(self):
        form_data = {
            "weekday": 0,
            "start_time": "09:00",
            "end_time": "17:00",
            "instructor": self.instructor.id,
        }
        form = ScheduleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_time_range(self):
        form_data = {
            "weekday": 0,
            "start_time": "17:00",
            "end_time": "09:00",
            "instructor": self.instructor.id,
        }
        form = ScheduleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("end_time", form.errors)

    def test_invalid_weekday(self):
        form_data = {
            "weekday": 7,
            "start_time": "09:00",
            "end_time": "17:00",
            "instructor": self.instructor.id,
        }
        form = ScheduleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("weekday", form.errors)

    def test_missing_instructor(self):
        form_data = {
            "weekday": 0,
            "start_time": "09:00",
            "end_time": "17:00",
        }
        form = ScheduleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("instructor", form.errors)

class TimeSlotFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.instructor = WellnessInstructor.objects.create(user=cls.user)
        cls.schedule = Schedule.objects.create(
            instructor=cls.instructor,
            weekday=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )

    def test_valid_timeslot_form(self):
        now = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
        form_data = {
            "schedule": self.schedule.id,
            "start_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "status": "available",
        }
        form = TimeSlotForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_datetime_range(self):
        now = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
        form_data = {
            "schedule": self.schedule.id,
            "start_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "status": "available",
        }
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("end_datetime", form.errors)

    def test_different_days(self):
        now = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
        form_data = {
            "schedule": self.schedule.id,
            "start_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "status": "available",
        }
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("end_datetime", form.errors)

    def test_outside_schedule_time_range(self):
        now = timezone.now().replace(hour=8, minute=0, second=0, microsecond=0)  # Before schedule start time
        form_data = {
            "schedule": self.schedule.id,
            "start_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "status": "available",
        }
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("start_datetime", form.errors)

    def test_wrong_weekday(self):
        # Get next day that's not Monday (weekday 0)
        now = timezone.now()
        while now.weekday() == 0:
            now += timedelta(days=1)
        now = now.replace(hour=10, minute=0, second=0, microsecond=0)

        form_data = {
            "schedule": self.schedule.id,
            "start_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "status": "available",
        }
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("start_datetime", form.errors)

class BlackoutDateFormTests(TestCase):
    """Test cases for BlackoutDateForm."""

    def setUp(self):
        """Set up test data."""
        self.user = UserFactory(
            first_name="Test",
            last_name="Instructor",
        )
        self.instructor = WellnessInstructor.objects.create(
            user=self.user,
            bio="Test instructor bio",
        )
        # Set up future dates for testing
        self.today = timezone.now().date()
        self.tomorrow = self.today + timedelta(days=1)
        self.next_week = self.tomorrow + timedelta(days=7)
        self.next_month = self.tomorrow + timedelta(days=30)

    def test_valid_blackout_date(self):
        """Test form with valid future dates."""
        form_data = {
            "instructor": self.instructor.id,
            "start_date": self.tomorrow,
            "end_date": self.next_week,
            "reason": "Vacation",
        }
        form = BlackoutDateForm(data=form_data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.instructor, self.instructor)
        self.assertEqual(instance.start_date.date(), self.tomorrow)
        self.assertEqual(instance.end_date.date(), self.next_week)

    def test_past_start_date(self):
        """Test form with start date in the past."""
        yesterday = self.today - timedelta(days=1)
        form_data = {
            "instructor": self.instructor.id,
            "start_date": yesterday,
            "end_date": self.next_week,
            "reason": "Invalid dates",
        }
        form = BlackoutDateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("start_date", form.errors)
        self.assertEqual(
            form.errors["start_date"][0],
            "Start date cannot be in the past.",
        )

    def test_end_date_before_start_date(self):
        """Test form with end date before start date."""
        form_data = {
            "instructor": self.instructor.id,
            "start_date": self.next_week,
            "end_date": self.tomorrow,
            "reason": "Invalid dates",
        }
        form = BlackoutDateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)
        self.assertEqual(
            form.errors["end_date"][0],
            "End date must be after start date.",
        )

    def test_overlapping_dates(self):
        """Test form with overlapping blackout dates."""
        # Create an existing blackout date
        BlackoutDate.objects.create(
            instructor=self.instructor,
            start_date=timezone.make_aware(
                datetime.combine(self.tomorrow, datetime.min.time()),
            ),
            end_date=timezone.make_aware(
                datetime.combine(self.next_week, datetime.max.time()),
            ),
            reason="Existing blackout",
        )

        # Try to create an overlapping blackout date
        form_data = {
            "instructor": self.instructor.id,
            "start_date": self.tomorrow + timedelta(days=2),
            "end_date": self.next_week + timedelta(days=2),
            "reason": "Overlapping dates",
        }
        form = BlackoutDateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertEqual(
            form.errors["__all__"][0],
            "This blackout period overlaps with an existing one.",
        )

    def test_missing_required_fields(self):
        """Test form with missing required fields."""
        form_data = {
            "reason": "Missing dates",
        }
        form = BlackoutDateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("instructor", form.errors)
        self.assertIn("start_date", form.errors)
        self.assertIn("end_date", form.errors)

    def test_no_instructor(self):
        """Test form without an instructor."""
        form_data = {
            "start_date": self.tomorrow,
            "end_date": self.next_week,
            "reason": "No instructor",
        }
        form = BlackoutDateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("instructor", form.errors)
