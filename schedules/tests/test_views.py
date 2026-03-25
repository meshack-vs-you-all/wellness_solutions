"""Tests for the schedules app views."""
from datetime import time, timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import BlackoutDate, Schedule, TimeSlot
from ..wellness_instructors.models import WellnessInstructor
from ..users.tests.factories import UserFactory


class ScheduleViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.instructor = WellnessInstructor.objects.create(user=self.user)
        self.client.force_login(self.user)

        # Create a test schedule
        self.schedule = Schedule.objects.create(
            instructor=self.instructor,
            weekday=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )

    def test_schedule_list_view(self):
        response = self.client.get(reverse("schedules:schedule-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedules/schedule_list.html")
        self.assertContains(response, "Monday")  # Should show the weekday

    def test_schedule_create_view(self):
        data = {
            "weekday": 1,
            "start_time": "10:00",
            "end_time": "18:00",
            "instructor": self.instructor.id,
        }
        response = self.client.post(reverse("schedules:schedule-create"), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Schedule.objects.filter(weekday=1).exists())

    def test_schedule_update_view(self):
        data = {
            "weekday": 0,
            "start_time": "08:00",
            "end_time": "16:00",
            "instructor": self.instructor.id,
        }
        response = self.client.post(
            reverse("schedules:schedule-update", kwargs={"pk": self.schedule.pk}),
            data,
        )
        self.assertEqual(response.status_code, 302)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.start_time.hour, 8)

    def test_schedule_delete_view(self):
        response = self.client.post(
            reverse("schedules:schedule-delete", kwargs={"pk": self.schedule.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Schedule.objects.filter(pk=self.schedule.pk).exists())

    def test_unauthorized_access(self):
        # Create another user and try to access first user's schedule
        other_user = UserFactory()
        self.client.force_login(other_user)
        response = self.client.get(
            reverse("schedules:schedule-update", kwargs={"pk": self.schedule.pk}),
        )
        self.assertEqual(response.status_code, 404)

class TimeSlotViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.instructor = WellnessInstructor.objects.create(user=self.user)
        self.client.force_login(self.user)

        # Create a test schedule and time slot
        self.schedule = Schedule.objects.create(
            instructor=self.instructor,
            weekday=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        self.timeslot = TimeSlot.objects.create(
            schedule=self.schedule,
            start_datetime=timezone.now(),
            end_datetime=timezone.now() + timedelta(hours=1),
            status="available",
        )

    def test_timeslot_list_view(self):
        response = self.client.get(reverse("schedules:timeslot-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedules/timeslot_list.html")
        self.assertContains(response, "available")  # Should show the status

    def test_timeslot_create_view(self):
        now = timezone.now()
        data = {
            "schedule": self.schedule.id,
            "start_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "status": "available",
        }
        response = self.client.post(reverse("schedules:timeslot-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TimeSlot.objects.filter(schedule=self.schedule).exists())

    def test_timeslot_update_view(self):
        data = {
            "schedule": self.schedule.id,
            "start_datetime": self.timeslot.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": self.timeslot.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "booked",
        }
        response = self.client.post(
            reverse("schedules:timeslot-update", kwargs={"pk": self.timeslot.pk}),
            data,
        )
        self.assertEqual(response.status_code, 302)
        self.timeslot.refresh_from_db()
        self.assertEqual(self.timeslot.status, "booked")

    def test_timeslot_delete_view(self):
        response = self.client.post(
            reverse("schedules:timeslot-delete", kwargs={"pk": self.timeslot.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TimeSlot.objects.filter(pk=self.timeslot.pk).exists())

class BlackoutDateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.instructor = WellnessInstructor.objects.create(user=self.user)
        self.client.force_login(self.user)

        # Create a test blackout date
        self.blackout = BlackoutDate.objects.create(
            instructor=self.instructor,
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=1)).date(),
            reason="Test Vacation",
            is_recurring=False,
        )

    def test_blackoutdate_list_view(self):
        response = self.client.get(reverse("schedules:blackoutdate-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedules/blackoutdate_list.html")
        self.assertContains(response, "Test Vacation")

    def test_blackoutdate_create_view(self):
        now = timezone.now()
        data = {
            "instructor": self.instructor.id,
            "start_date": now.strftime("%Y-%m-%d"),
            "end_date": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            "reason": "New Vacation",
            "is_recurring": False,
        }
        response = self.client.post(reverse("schedules:blackoutdate-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BlackoutDate.objects.filter(reason="New Vacation").exists())

    def test_blackoutdate_update_view(self):
        data = {
            "instructor": self.instructor.id,
            "start_date": self.blackout.start_date.strftime("%Y-%m-%d"),
            "end_date": self.blackout.end_date.strftime("%Y-%m-%d"),
            "reason": "Updated Vacation",
            "is_recurring": True,
        }
        response = self.client.post(
            reverse("schedules:blackoutdate-update", kwargs={"pk": self.blackout.pk}),
            data,
        )
        self.assertEqual(response.status_code, 302)
        self.blackout.refresh_from_db()
        self.assertEqual(self.blackout.reason, "Updated Vacation")
        self.assertTrue(self.blackout.is_recurring)

    def test_blackoutdate_delete_view(self):
        response = self.client.post(
            reverse("schedules:blackoutdate-delete", kwargs={"pk": self.blackout.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BlackoutDate.objects.filter(pk=self.blackout.pk).exists())
