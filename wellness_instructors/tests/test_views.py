"""Tests for the wellness_instructors views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Session, WellnessInstructor


User = get_user_model()


class InstructorViewTests(TestCase):
    """Test cases for instructor views."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test User",
        )
        self.instructor = WellnessInstructor.objects.create(
            user=self.user,
            bio="Test bio",
            specializations="flexibility",
            certification_level="certified",
            years_of_experience=5,
            is_available=True,
        )
        self.session = Session.objects.create(
            instructor=self.instructor,
            title="Test Session",
            description="Test description",
            session_type="one_on_one",
            difficulty_level="beginner",
            duration=60,
            max_participants=1,
            price=50.00,
            is_active=True,
        )

    def test_instructor_list_view(self):
        """Test the instructor list view."""
        url = reverse("wellness_instructors:instructor-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.instructor.full_name)
        self.assertContains(response, "flexibility")
        self.assertTemplateUsed(response, "wellness_instructors/instructor_list.html")

    def test_instructor_detail_view(self):
        """Test the instructor detail view."""
        url = reverse("wellness_instructors:instructor-detail", args=[self.instructor.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.instructor.full_name)
        self.assertContains(response, self.instructor.bio)
        self.assertContains(response, self.session.title)
        self.assertTemplateUsed(response, "wellness_instructors/instructor_detail.html")

    def test_session_list_view(self):
        """Test the session list view."""
        url = reverse("wellness_instructors:session-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session.title)
        self.assertContains(response, self.instructor.full_name)
        self.assertTemplateUsed(response, "wellness_instructors/session_list.html")

    def test_session_detail_view(self):
        """Test the session detail view."""
        url = reverse("wellness_instructors:session-detail", args=[self.session.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session.title)
        self.assertContains(response, self.session.description)
        self.assertTemplateUsed(response, "wellness_instructors/session_detail.html")
