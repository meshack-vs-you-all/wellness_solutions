"""
Tests for the locations app models.
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .locations.models import Location, LocationInstructor, LocationService
from .services.models import Service, ServiceCategory
from .wellness_instructors.models import WellnessInstructor
from .users.models import User


User = User

class LocationModelTests(TestCase):
    """Test cases for Location model."""

    def setUp(self):
        """Set up test data."""
        self.valid_location_data = {
            "name": "Test Studio",
            "type": "studio",
            "address": "123 Test St",
            "contact_info": {
                "phone": "123-456-7890",
                "email": "test@example.com",
                "emergency_contact": "987-654-3210",
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
            "amenities": {
                "wifi": True,
                "parking": True,
                "lockers": 20,
                "shower": True,
                "accessibility": {
                    "wheelchair_access": True,
                    "elevator": True,
                },
            },
            "status": "active",
        }

    def test_create_location(self):
        """Test creating a location with valid data."""
        location = Location.objects.create(**self.valid_location_data)
        location.full_clean()  # Validate all fields
        self.assertEqual(location.name, "Test Studio")
        self.assertEqual(location.type, "studio")
        self.assertEqual(location.status, "active")
        self.assertTrue(isinstance(location.created, timezone.datetime))
        self.assertTrue(isinstance(location.modified, timezone.datetime))

    def test_invalid_location_type(self):
        """Test creating a location with invalid type."""
        invalid_data = self.valid_location_data.copy()
        invalid_data["type"] = "invalid_type"
        with self.assertRaises(ValidationError) as context:
            location = Location.objects.create(**invalid_data)
            location.full_clean()
        self.assertIn("type", str(context.exception))

    def test_invalid_status(self):
        """Test creating a location with invalid status."""
        invalid_data = self.valid_location_data.copy()
        invalid_data["status"] = "invalid_status"
        with self.assertRaises(ValidationError) as context:
            location = Location.objects.create(**invalid_data)
            location.full_clean()
        self.assertIn("status", str(context.exception))

    def test_negative_capacity(self):
        """Test creating a location with negative capacity."""
        invalid_data = self.valid_location_data.copy()
        invalid_data["capacity"] = -1
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("capacity", str(context.exception))

    def test_zero_capacity(self):
        """Test creating a location with zero capacity."""
        invalid_data = self.valid_location_data.copy()
        invalid_data["capacity"] = 0
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("capacity", str(context.exception))

    def test_invalid_contact_info(self):
        """Test creating a location with invalid contact info."""
        # Test with missing required fields
        invalid_data = self.valid_location_data.copy()
        invalid_data["contact_info"] = {"invalid_key": "value"}
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("contact_info", str(context.exception))

        # Test with invalid email format
        invalid_data = self.valid_location_data.copy()
        invalid_data["contact_info"] = {
            "phone": "123-456-7890",
            "email": "invalid-email",
        }
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("contact_info", str(context.exception))

        # Test with invalid phone format
        invalid_data = self.valid_location_data.copy()
        invalid_data["contact_info"] = {
            "phone": "123",  # Too short
            "email": "test@example.com",
        }
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("contact_info", str(context.exception))

    def test_invalid_operating_hours(self):
        """Test creating a location with invalid operating hours."""
        # Test missing required days
        invalid_data = {
            "name": "Test Studio",
            "type": "studio",
            "capacity": 50,
            "contact_info": {
                "phone": "123-456-7890",
                "email": "test@example.com",
            },
            "operating_hours": {
                "monday": {"open": "09:00", "close": "17:00"},
                # Missing other days
            },
        }
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("operating_hours", str(context.exception))

        # Test invalid time format
        invalid_data["operating_hours"] = {
            "monday": {"open": "25:00", "close": "17:00"},  # Invalid hour
            "tuesday": {"open": "09:00", "close": "17:00"},
            "wednesday": {"open": "09:00", "close": "17:00"},
            "thursday": {"open": "09:00", "close": "17:00"},
            "friday": {"open": "09:00", "close": "17:00"},
            "saturday": {"open": "10:00", "close": "15:00"},
            "sunday": {"open": "10:00", "close": "15:00"},
        }
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("operating_hours", str(context.exception))

        # Test missing open/close times
        invalid_data["operating_hours"] = {
            "monday": {"open": "09:00"},  # Missing close time
            "tuesday": {"open": "09:00", "close": "17:00"},
            "wednesday": {"open": "09:00", "close": "17:00"},
            "thursday": {"open": "09:00", "close": "17:00"},
            "friday": {"open": "09:00", "close": "17:00"},
            "saturday": {"open": "10:00", "close": "15:00"},
            "sunday": {"open": "10:00", "close": "15:00"},
        }
        location = Location(**invalid_data)
        with self.assertRaises(ValidationError) as context:
            location.full_clean()
        self.assertIn("operating_hours", str(context.exception))

    def test_name_uniqueness(self):
        """Test that location names must be unique."""
        # Create first location
        first_location = Location.objects.create(
            name="Test Studio",
            type="studio",
            capacity=50,
            contact_info={
                "phone": "123-456-7890",
                "email": "test@example.com",
            },
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
        )

        # Try to create second location with same name
        duplicate_location = Location(
            name="Test Studio",  # Same name as first location
            type="studio",
            capacity=50,
            contact_info={
                "phone": "123-456-7890",
                "email": "test2@example.com",
            },
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
        )
        with self.assertRaises(ValidationError) as context:
            duplicate_location.full_clean()
        self.assertIn("name", str(context.exception))

    def test_str_representation(self):
        """Test the string representation of the location."""
        location = Location.objects.create(
            name="Test Studio",
            type="studio",
            capacity=50,
            contact_info={
                "phone": "123-456-7890",
                "email": "test@example.com",
            },
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
        )
        expected_str = "Test Studio (Studio)"
        self.assertEqual(str(location), expected_str)

    def test_get_absolute_url(self):
        """Test the get_absolute_url method."""
        location = Location.objects.create(**self.valid_location_data)
        expected_url = f"/locations/{location.pk}/"
        self.assertEqual(location.get_absolute_url(), expected_url)


class LocationServiceModelTests(TestCase):
    """Test cases for LocationService model"""

    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone_number="+1234567890",
            password="testpass123",
        )

        self.category = ServiceCategory.objects.create(
            name="Test Category",
            description="Test category description",
        )

        self.service = Service.objects.create(
            name="Test Service",
            description="Test service description",
            category=self.category,
            base_price=Decimal("50.00"),
            duration=30,
        )

        self.location = Location.objects.create(
            name="Test Location",
            type="studio",
            address="123 Test St",
            status="active",
            capacity=10,
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
            contact_info={
                "email": "test@location.com",
                "phone": "+1234567890",
            },
            amenities={
                "wifi": True,
                "parking": True,
                "lockers": 20,
            },
        )

        self.valid_availability_rules = {
            "schedule_type": "weekly",
            "restrictions": {
                "max_bookings_per_day": 10,
                "min_notice_hours": 24,
                "max_notice_days": 30,
                "booking_window": {
                    "start": "09:00",
                    "end": "17:00",
                },
            },
        }

    def test_create_location_service(self):
        """Test creating a valid LocationService instance"""
        location_service = LocationService.objects.create(
            location=self.location,
            service=self.service,
            price_adjustment=Decimal("10.00"),
            availability_rules=self.valid_availability_rules,
            is_available=True,
            notes="Test notes",
        )
        self.assertEqual(str(location_service), f"{self.service.name} at {self.location.name}")
        self.assertEqual(location_service.price_adjustment, Decimal("10.00"))

    def test_invalid_price_adjustment(self):
        """Test validation for invalid price adjustment"""
        with self.assertRaises(ValidationError):
            location_service = LocationService(
                location=self.location,
                service=self.service,
                price_adjustment=Decimal("150.00"),
                availability_rules=self.valid_availability_rules,
            )
            location_service.full_clean()

    def test_invalid_location_status(self):
        """Test validation for inactive location"""
        self.location.status = "inactive"
        self.location.save()

        with self.assertRaises(ValidationError):
            location_service = LocationService(
                location=self.location,
                service=self.service,
                price_adjustment=Decimal("10.00"),
                availability_rules=self.valid_availability_rules,
            )
            location_service.full_clean()

    def test_invalid_availability_rules(self):
        """Test validation for invalid availability rules"""
        invalid_rules = {
            "schedule_type": "invalid",
            "restrictions": {},
        }

        with self.assertRaises(ValidationError):
            location_service = LocationService(
                location=self.location,
                service=self.service,
                price_adjustment=Decimal("10.00"),
                availability_rules=invalid_rules,
            )
            location_service.full_clean()

    def test_invalid_booking_window(self):
        """Test validation for invalid booking window format"""
        invalid_rules = {
            "schedule_type": "weekly",
            "restrictions": {
                "max_bookings_per_day": 10,
                "min_notice_hours": 24,
                "max_notice_days": 30,
                "booking_window": {
                    "start": "25:00",  # Invalid time
                    "end": "17:00",
                },
            },
        }

        with self.assertRaises(ValidationError):
            location_service = LocationService(
                location=self.location,
                service=self.service,
                price_adjustment=Decimal("10.00"),
                availability_rules=invalid_rules,
            )
            location_service.full_clean()

    def test_unique_together_constraint(self):
        """Test that location and service combination must be unique"""
        LocationService.objects.create(
            location=self.location,
            service=self.service,
            price_adjustment=Decimal("10.00"),
            availability_rules=self.valid_availability_rules,
        )

        with self.assertRaises(IntegrityError):
            LocationService.objects.create(
                location=self.location,
                service=self.service,
                price_adjustment=Decimal("20.00"),
                availability_rules=self.valid_availability_rules,
            )

    def test_free_service_price_adjustment(self):
        """Test that free services cannot have price adjustments"""
        free_service = Service.objects.create(
            name="Free Service",
            description="Test free service",
            category=self.category,
            base_price=Decimal("0.00"),
            duration=30,
        )

        with self.assertRaises(ValidationError):
            location_service = LocationService(
                location=self.location,
                service=free_service,
                price_adjustment=Decimal("10.00"),
                availability_rules=self.valid_availability_rules,
            )
            location_service.full_clean()


class LocationInstructorModelTests(TestCase):
    """Test cases for LocationInstructor model."""

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
            years_of_experience=5,
        )

        self.location = Location.objects.create(
            name="Test Studio",
            type="studio",
            capacity=50,
            contact_info={"phone": "123-456-7890", "email": "test@example.com"},
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
        )

        self.valid_instructor_data = {
            "location": self.location,
            "instructor": self.instructor,
            "is_primary": True,
            "availability_rules": {
                "schedule_type": "weekly",
                "restrictions": {
                    "max_sessions_per_day": 8,
                    "min_notice_hours": 24,
                    "max_notice_days": 30,
                    "availability_window": {
                        "start": "09:00",
                        "end": "17:00",
                    },
                },
            },
            "status": "active",
            "notes": "Test notes",
        }

    def test_create_location_instructor(self):
        """Test creating a location instructor with valid data."""
        location_instructor = LocationInstructor.objects.create(**self.valid_instructor_data)
        self.assertEqual(location_instructor.location, self.location)
        self.assertEqual(location_instructor.instructor, self.instructor)
        self.assertTrue(location_instructor.is_primary)

    def test_invalid_availability_rules(self):
        """Test creating a location instructor with invalid availability rules."""
        with self.assertRaises(ValidationError):
            location_instructor = LocationInstructor.objects.create(
                location=self.location,
                instructor=self.instructor,
                availability_rules={"invalid": "rules"},
            )
            location_instructor.full_clean()

    def test_multiple_primary_locations(self):
        """Test assigning multiple primary locations to an instructor."""
        LocationInstructor.objects.create(
            location=self.location,
            instructor=self.instructor,
            is_primary=True,
            availability_rules={
                "schedule_type": "weekly",
                "restrictions": {
                    "max_sessions_per_day": 8,
                    "min_notice_hours": 24,
                    "max_notice_days": 30,
                    "availability_window": {
                        "start": "09:00",
                        "end": "17:00",
                    },
                },
            },
            status="active",
            notes="Test notes",
        )

        location2 = Location.objects.create(
            name="Test Studio 2",
            type="studio",
            capacity=50,
            contact_info={"phone": "123-456-7890", "email": "test2@example.com"},
            operating_hours={
                "monday": {"open": "09:00", "close": "17:00"},
                "tuesday": {"open": "09:00", "close": "17:00"},
                "wednesday": {"open": "09:00", "close": "17:00"},
                "thursday": {"open": "09:00", "close": "17:00"},
                "friday": {"open": "09:00", "close": "17:00"},
                "saturday": {"open": "10:00", "close": "15:00"},
                "sunday": {"open": "10:00", "close": "15:00"},
            },
        )

        with self.assertRaises(ValidationError):
            LocationInstructor.objects.create(
                location=location2,
                instructor=self.instructor,
                is_primary=True,
                availability_rules={
                    "schedule_type": "weekly",
                    "restrictions": {
                        "max_sessions_per_day": 8,
                        "min_notice_hours": 24,
                        "max_notice_days": 30,
                        "availability_window": {
                            "start": "09:00",
                            "end": "17:00",
                        },
                    },
                },
                status="active",
                notes="Test notes",
            ).full_clean()

    def test_invalid_status(self):
        """Test creating a location instructor with invalid status."""
        with self.assertRaises(ValidationError):
            location_instructor = LocationInstructor.objects.create(
                location=self.location,
                instructor=self.instructor,
                status="invalid_status",
                availability_rules={
                    "schedule_type": "weekly",
                    "restrictions": {
                        "max_sessions_per_day": 8,
                        "min_notice_hours": 24,
                        "max_notice_days": 30,
                        "availability_window": {
                            "start": "09:00",
                            "end": "17:00",
                        },
                    },
                },
            )
            location_instructor.full_clean()
