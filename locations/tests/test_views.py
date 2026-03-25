"""
Tests for the locations app views.
"""
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse

from ..locations.models import Location, LocationInstructor, LocationService
from ..services.models import Service, ServiceCategory
from ..wellness_instructors.models import WellnessInstructor


User = get_user_model()

class LocationViewTests(TestCase):
    """Test cases for location views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.location = Location.objects.create(
            name="Test Location",
            type="studio",
            capacity=50,
            contact_info={"phone": "+1234567890", "email": "test@example.com"},
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
            status="active",
        )
        self.category = ServiceCategory.objects.create(
            name="Test Category",
            description="Test category description",
            type="individual",
        )
        self.service = Service.objects.create(
            name="Test Service",
            description="Test service description",
            duration=60,
            max_participants=10,
            base_price="100.00",
            category=self.category,
        )
        # Add necessary permissions
        content_type = ContentType.objects.get_for_model(Location)
        location_permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=["add_location", "change_location", "delete_location"],
        )
        self.user.user_permissions.add(*location_permissions)

        # Add LocationService permissions
        service_content_type = ContentType.objects.get_for_model(LocationService)
        service_permissions = Permission.objects.filter(
            content_type=service_content_type,
            codename__in=["add_locationservice", "change_locationservice", "delete_locationservice"],
        )
        self.user.user_permissions.add(*service_permissions)

        # Add LocationInstructor permissions
        instructor_content_type = ContentType.objects.get_for_model(LocationInstructor)
        instructor_permissions = Permission.objects.filter(
            content_type=instructor_content_type,
            codename__in=["add_locationinstructor", "change_locationinstructor", "delete_locationinstructor"],
        )
        self.user.user_permissions.add(*instructor_permissions)

        self.client.login(email="test@example.com", password="testpass123")

    def test_location_list_view(self):
        """Test location list view."""
        response = self.client.get(reverse("locations:location_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/location_list.html")
        self.assertContains(response, "Test Location")

    def test_location_detail_view(self):
        """Test location detail view."""
        response = self.client.get(
            reverse("locations:location_detail", kwargs={"pk": self.location.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/location_detail.html")
        self.assertContains(response, "Test Location")

    def test_location_create_view(self):
        """Test location create view."""
        location_data = {
            "name": "New Test Location",
            "type": "studio",
            "capacity": 30,
            "contact_info": {
                "phone": "+1234567890",
                "email": "test@example.com",
            },
            "operating_hours": {
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
            "status": "active",
        }
        response = self.client.post(
            reverse("locations:location_create"),
            data=json.dumps(location_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)  # Success response for JSON
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertEqual(Location.objects.count(), 2)  # Including the one from setUp
        location = Location.objects.last()
        self.assertEqual(location.name, "New Test Location")

    def test_location_update_view(self):
        """Test location update view."""
        updated_data = {
            "name": "Updated Location",
            "type": "studio",
            "capacity": 75,
            "contact_info": {
                "phone": "+1234567890",
                "email": "updated@example.com",
            },
            "operating_hours": {
                "monday": {"open": "08:00", "close": "18:00"},
                "tuesday": {"open": "08:00", "close": "18:00"},
                "wednesday": {"open": "08:00", "close": "18:00"},
                "thursday": {"open": "08:00", "close": "18:00"},
                "friday": {"open": "08:00", "close": "18:00"},
                "saturday": {"open": "09:00", "close": "16:00"},
                "sunday": {"open": "09:00", "close": "16:00"},
            },
            "status": "active",
        }
        response = self.client.post(
            reverse("locations:location_update", kwargs={"pk": self.location.pk}),
            data=json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)  # Success response for JSON
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Updated Location")
        self.assertEqual(self.location.capacity, 75)

    def test_location_delete_view(self):
        """Test location delete view."""
        response = self.client.post(
            reverse("locations:location_delete", kwargs={"pk": self.location.pk}),
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Location.objects.count(), 0)

    def test_unauthorized_access(self):
        """Test unauthorized access to views."""
        # Create user without permissions
        user = User.objects.create_user(
            email="noperm@example.com",
            password="testpass123",
            first_name="No",
            last_name="Perm",
        )
        self.client.login(email="noperm@example.com", password="testpass123")

        # Test create view
        response = self.client.get(reverse("locations:location_create"))
        self.assertEqual(response.status_code, 403)

        # Test update view
        response = self.client.get(
            reverse("locations:location_update", kwargs={"pk": self.location.pk}),
        )
        self.assertEqual(response.status_code, 403)

        # Test delete view
        response = self.client.get(
            reverse("locations:location_delete", kwargs={"pk": self.location.pk}),
        )
        self.assertEqual(response.status_code, 403)


class LocationServiceViewTests(TestCase):
    """Test cases for location service views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.category = ServiceCategory.objects.create(
            name="Test Category",
            description="Test category description",
            type="individual",
        )
        self.service = Service.objects.create(
            name="Test Service",
            description="Test service description",
            duration=60,
            max_participants=10,
            base_price="100.00",
            category=self.category,
        )
        self.location = Location.objects.create(
            name="Test Location",
            type="studio",
            capacity=50,
            contact_info={"phone": "+1234567890", "email": "test@example.com"},
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
            status="active",
        )
        # Add necessary permissions
        content_type = ContentType.objects.get_for_model(Location)
        location_permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=["add_location", "change_location", "delete_location"],
        )
        self.user.user_permissions.add(*location_permissions)

        # Add LocationService permissions
        service_content_type = ContentType.objects.get_for_model(LocationService)
        service_permissions = Permission.objects.filter(
            content_type=service_content_type,
            codename__in=["add_locationservice", "change_locationservice", "delete_locationservice"],
        )
        self.user.user_permissions.add(*service_permissions)

        # Add LocationInstructor permissions
        instructor_content_type = ContentType.objects.get_for_model(LocationInstructor)
        instructor_permissions = Permission.objects.filter(
            content_type=instructor_content_type,
            codename__in=["add_locationinstructor", "change_locationinstructor", "delete_locationinstructor"],
        )
        self.user.user_permissions.add(*instructor_permissions)

        self.client.login(email="test@example.com", password="testpass123")

    def test_location_service_create_view(self):
        """Test location service create view."""
        location_service_data = {
            "location": self.location.id,
            "service": self.service.id,
            "price_adjustment": "10.00",
            "availability_rules": {
                "schedule_type": "weekly",
                "restrictions": {
                    "max_bookings_per_day": 5,
                    "min_notice_hours": 24,
                    "max_notice_days": 30,
                    "booking_window": {
                        "start": "2024-01-01",
                        "end": "2024-12-31",
                    },
                },
            },
            "is_available": True,
            "notes": "Test notes",
        }
        response = self.client.post(
            reverse("locations:location_service_create",
                   kwargs={"location_pk": self.location.pk}),
            data=json.dumps(location_service_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)  # Success response for JSON
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertEqual(LocationService.objects.count(), 1)
        location_service = LocationService.objects.first()
        self.assertEqual(location_service.location, self.location)
        self.assertEqual(location_service.service, self.service)

    def test_location_service_update_view(self):
        """Test location service update view."""
        location_service = LocationService.objects.create(
            location=self.location,
            service=self.service,
            price_adjustment="10.00",
            availability_rules={
                "schedule_type": "weekly",
                "restrictions": {
                    "max_bookings_per_day": 5,
                    "min_notice_hours": 24,
                    "max_notice_days": 30,
                    "booking_window": {
                        "start": "2024-01-01",
                        "end": "2024-12-31",
                    },
                },
            },
            is_available=True,
            notes="Test notes",
        )
        updated_data = {
            "location": self.location.id,
            "service": self.service.id,
            "price_adjustment": "20.00",
            "availability_rules": {
                "schedule_type": "weekly",
                "restrictions": {
                    "max_bookings_per_day": 5,
                    "min_notice_hours": 24,
                    "max_notice_days": 30,
                    "booking_window": {
                        "start": "2024-01-01",
                        "end": "2024-12-31",
                    },
                },
            },
            "is_available": True,
            "notes": "Updated notes",
        }
        response = self.client.post(
            reverse("locations:location_service_update",
                   kwargs={"pk": location_service.pk}),
            data=json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)  # Success response for JSON
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        location_service.refresh_from_db()
        self.assertEqual(str(location_service.price_adjustment), "20.00")


class LocationInstructorViewTests(TestCase):
    """Test cases for location instructor views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.instructor = WellnessInstructor.objects.create(
            user=self.user,
            bio="Test bio",
            certification_level="certified",
        )
        self.location = Location.objects.create(
            name="Test Location",
            type="studio",
            capacity=50,
            contact_info={"phone": "+1234567890", "email": "test@example.com"},
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
            status="active",
        )
        # Add necessary permissions
        content_type = ContentType.objects.get_for_model(Location)
        location_permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=["add_location", "change_location", "delete_location"],
        )
        self.user.user_permissions.add(*location_permissions)

        # Add LocationService permissions
        service_content_type = ContentType.objects.get_for_model(LocationService)
        service_permissions = Permission.objects.filter(
            content_type=service_content_type,
            codename__in=["add_locationservice", "change_locationservice", "delete_locationservice"],
        )
        self.user.user_permissions.add(*service_permissions)

        # Add LocationInstructor permissions
        instructor_content_type = ContentType.objects.get_for_model(LocationInstructor)
        instructor_permissions = Permission.objects.filter(
            content_type=instructor_content_type,
            codename__in=["add_locationinstructor", "change_locationinstructor", "delete_locationinstructor"],
        )
        self.user.user_permissions.add(*instructor_permissions)

        self.client.login(email="test@example.com", password="testpass123")

    def test_location_instructor_create_view(self):
        """Test location instructor create view."""
        location_instructor_data = {
            "location": self.location.id,
            "instructor": self.instructor.id,
            "availability_rules": {
                "schedule_type": "weekly",
                "hours": {"monday": ["09:00-17:00"]},
            },
            "is_primary": True,
            "status": "active",
            "notes": "Test notes",
        }
        response = self.client.post(
            reverse("locations:location_instructor_create",
                   kwargs={"location_pk": self.location.pk}),
            data=json.dumps(location_instructor_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)  # Success response for JSON
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertEqual(LocationInstructor.objects.count(), 1)
        location_instructor = LocationInstructor.objects.first()
        self.assertEqual(location_instructor.location, self.location)
        self.assertEqual(location_instructor.instructor, self.instructor)
        self.assertEqual(location_instructor.status, "active")

    def test_location_instructor_update_view(self):
        """Test location instructor update view."""
        location_instructor = LocationInstructor.objects.create(
            location=self.location,
            instructor=self.instructor,
            availability_rules={
                "schedule_type": "weekly",
                "hours": {"monday": ["09:00-17:00"]},
            },
        )
        updated_data = {
            "location": self.location.id,
            "instructor": self.instructor.id,
            "availability_rules": {
                "schedule_type": "weekly",
                "hours": {"monday": ["09:00-17:00"]},
            },
            "is_primary": True,
            "status": "inactive",
            "notes": "Updated notes",
        }
        response = self.client.post(
            reverse("locations:location_instructor_update",
                   kwargs={"pk": location_instructor.pk}),
            data=json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)  # Success response for JSON
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        location_instructor.refresh_from_db()
        self.assertEqual(location_instructor.status, "inactive")
        self.assertEqual(location_instructor.location, self.location)
        self.assertEqual(location_instructor.instructor, self.instructor)
        self.assertTrue(location_instructor.is_primary)
