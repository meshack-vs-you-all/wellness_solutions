"""Tests for the schedules app models."""
from datetime import time, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ..models import BlackoutDate, Schedule, TimeSlot
from ..wellness_instructors.models import WellnessInstructor
from ..users.tests.factories import UserFactory


class ScheduleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user and instructor for testing
        cls.user = UserFactory()
        cls.instructor = WellnessInstructor.objects.create(user=cls.user)

    def test_schedule_creation(self):
        schedule = Schedule.objects.create(
            instructor=self.instructor,
            weekday=0,  # Monday
            start_time=time(9, 0),  # 9:00 AM
            end_time=time(17, 0),   # 5:00 PM
        )
        self.assertEqual(schedule.weekday, 0)
        self.assertEqual(schedule.start_time.hour, 9)
        self.assertEqual(schedule.end_time.hour, 17)

    def test_invalid_time_range(self):
        with self.assertRaises(ValidationError):
            schedule = Schedule(
                instructor=self.instructor,
                weekday=0,
                start_time=time(17, 0),  # 5:00 PM
                end_time=time(9, 0),     # 9:00 AM
            )
            schedule.full_clean()

    def test_invalid_weekday(self):
        with self.assertRaises(ValidationError):
            schedule = Schedule(
                instructor=self.instructor,
                weekday=7,  # Invalid weekday
                start_time=time(9, 0),
                end_time=time(17, 0),
            )
            schedule.full_clean()

class TimeSlotModelTests(TestCase):
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

    def test_timeslot_creation(self):
        now = timezone.now()
        timeslot = TimeSlot.objects.create(
            schedule=self.schedule,
            start_datetime=now,
            end_datetime=now + timedelta(hours=1),
            status="available",
        )
        self.assertEqual(timeslot.status, "available")

    def test_invalid_datetime_range(self):
        now = timezone.now()
        with self.assertRaises(ValidationError):
            timeslot = TimeSlot(
                schedule=self.schedule,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now,
                status="available",
            )
            timeslot.full_clean()

    def test_status_choices(self):
        now = timezone.now()
        timeslot = TimeSlot.objects.create(
            schedule=self.schedule,
            start_datetime=now,
            end_datetime=now + timedelta(hours=1),
            status="available",
        )
        timeslot.status = "booked"
        timeslot.save()
        self.assertEqual(timeslot.status, "booked")

class BlackoutDateModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.instructor = WellnessInstructor.objects.create(user=cls.user)

    def test_blackoutdate_creation(self):
        now = timezone.now()
        blackout = BlackoutDate.objects.create(
            instructor=self.instructor,
            start_date=now,
            end_date=now + timedelta(days=1),
            reason="Vacation",
            is_recurring=False,
        )
        self.assertEqual(blackout.reason, "Vacation")
        self.assertFalse(blackout.is_recurring)

    def test_invalid_date_range(self):
        now = timezone.now()
        with self.assertRaises(ValidationError):
            blackout = BlackoutDate(
                instructor=self.instructor,
                start_date=now + timedelta(days=1),
                end_date=now,
                reason="Invalid Range",
            )
            blackout.full_clean()
