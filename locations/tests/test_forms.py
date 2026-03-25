"""
Tests for the locations app forms.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..services.models import Service, ServiceCategory
from ..wellness_instructors.models import WellnessInstructor
from .forms import LocationForm, LocationInstructorForm, LocationServiceForm
from .models import Location, LocationInstructor, LocationService


User = get_user_model()

class LocationFormTests(TestCase):
    """Test cases for LocationForm."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.valid_form_data = {
            "name": "Test Studio",
            "type": "studio",
            "address": "123 Test St",
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
            "capacity": 50,
            "amenities": {"wifi": True, "parking": True},
            "status": "active",
            "description": "Test Description",
        }

    def test_valid_form(self):
        """Test form with valid data."""
        form = LocationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Test form with missing required fields."""
        required_fields = ["name", "type", "capacity"]
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_form_data.copy()
                invalid_data.pop(field)
                form = LocationForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_invalid_contact_info(self):
        """Test form with invalid contact info."""
        invalid_data = self.valid_form_data.copy()
        invalid_data["contact_info"] = {"phone": "+1234567890"}  # Missing email
        form = LocationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_operating_hours(self):
        """Test form with invalid operating hours."""
        invalid_data = self.valid_form_data.copy()
        invalid_data["operating_hours"] = {"monday": {"open": "09:00"}}  # Missing close time
        form = LocationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_negative_capacity(self):
        """Test form with negative capacity."""
        invalid_data = self.valid_form_data.copy()
        invalid_data["capacity"] = -1
        form = LocationForm(data=invalid_data)
        self.assertFalse(form.is_valid())


class LocationServiceFormTests(TestCase):
    """Test cases for LocationServiceForm."""

    def setUp(self):
        """Set up test data."""
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
        self.valid_form_data = {
            "location": self.location.id,
            "service": self.service.id,
            "price_adjustment": 10.00,
            "availability_rules": {
                "schedule_type": "weekly",
                "restrictions": {"max_bookings_per_day": 5},
            },
            "is_available": True,
            "notes": "Test notes",
        }

    def test_valid_form(self):
        """Test form with valid data."""
        form = LocationServiceForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Test form with missing required fields."""
        required_fields = ["location", "service"]
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_form_data.copy()
                invalid_data.pop(field)
                form = LocationServiceForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_invalid_availability_rules(self):
        """Test form with invalid availability rules."""
        invalid_data = self.valid_form_data.copy()
        invalid_data["availability_rules"] = {"invalid": "rules"}
        form = LocationServiceForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_service(self):
        """Test form with duplicate service at location."""
        LocationService.objects.create(
            location=self.location,
            service=self.service,
        )
        form = LocationServiceForm(data=self.valid_form_data)
        self.assertFalse(form.is_valid())


class LocationInstructorFormTests(TestCase):
    """Test cases for LocationInstructorForm."""

    def setUp(self):
        """Set up test data."""
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
        self.valid_form_data = {
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

    def test_valid_form(self):
        """Test form with valid data."""
        form = LocationInstructorForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Test form with missing required fields."""
        required_fields = ["location", "instructor"]
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_form_data.copy()
                invalid_data.pop(field)
                form = LocationInstructorForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_invalid_availability_rules(self):
        """Test form with invalid availability rules."""
        invalid_data = self.valid_form_data.copy()
        invalid_data["availability_rules"] = {"invalid": "rules"}
        form = LocationInstructorForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_multiple_primary_locations(self):
        """Test form with multiple primary locations for instructor."""
        LocationInstructor.objects.create(
            location=self.location,
            instructor=self.instructor,
            is_primary=True,
            availability_rules={
                "schedule_type": "weekly",
                "hours": {"monday": ["09:00-17:00"]},
            },
        )

        location2 = Location.objects.create(
            name="Test Location 2",
            type="studio",
            capacity=50,
            contact_info={"phone": "+1234567890", "email": "test2@example.com"},
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

        form_data = self.valid_form_data.copy()
        form_data["location"] = location2.id
        form = LocationInstructorForm(data=form_data)
        self.assertFalse(form.is_valid())
