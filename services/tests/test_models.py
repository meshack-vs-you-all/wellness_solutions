"""
Tests for the services app models.
"""

from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ..models import (
    CorporateProgram,
    Organization,
    Proposal,
    Service,
    ServiceCategory,
)


class ServiceCategoryTests(TestCase):
    """Test cases for the ServiceCategory model."""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Test Category",
            description="Test description",
            type="individual",
            is_active=True,
        )

    def test_string_representation(self):
        """Test the string representation of a category."""
        self.assertEqual(str(self.category), "Test Category (Individual Services)")

    def test_category_creation(self):
        """Test that a category can be created."""
        self.assertTrue(isinstance(self.category, ServiceCategory))
        self.assertEqual(self.category.name, "Test Category")

    def test_category_type_choices(self):
        """Test that invalid category types are rejected."""
        with self.assertRaises(ValidationError):
            category = ServiceCategory(
                name="Invalid Type",
                description="Test",
                type="invalid_type",
            )
            category.full_clean()


class ServiceTests(TestCase):
    """Test cases for the Service model."""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Test Category",
            description="Test description",
            type="individual",
        )
        self.service = Service.objects.create(
            category=self.category,
            name="Test Service",
            description="Test description",
            duration=30,
            max_participants=1,
            base_price=Decimal("50.00"),
        )

    def test_string_representation(self):
        """Test the string representation of a service."""
        self.assertEqual(str(self.service), "Test Service (Test Category)")

    def test_service_creation(self):
        """Test that a service can be created."""
        self.assertTrue(isinstance(self.service, Service))
        self.assertEqual(self.service.name, "Test Service")

    def test_duration_validation(self):
        """Test duration constraints."""
        with self.assertRaises(ValidationError):
            service = Service(
                category=self.category,
                name="Invalid Duration",
                description="Test",
                duration=10,  # Less than minimum
                max_participants=1,
                base_price=Decimal("50.00"),
            )
            service.full_clean()

    def test_max_participants_validation(self):
        """Test max_participants constraints."""
        with self.assertRaises(ValidationError):
            service = Service(
                category=self.category,
                name="Invalid Max Participants",
                description="Test",
                duration=30,
                max_participants=0,  # Invalid value
                base_price=Decimal("50.00"),
            )
            service.full_clean()

    def test_base_price_validation(self):
        """Test base_price constraints."""
        with self.assertRaises(ValidationError):
            service = Service(
                category=self.category,
                name="Invalid Price",
                description="Test",
                duration=30,
                max_participants=1,
                base_price=Decimal("-10.00"),  # Negative price
            )
            service.full_clean()


class CorporateProgramTests(TestCase):
    """Test cases for the CorporateProgram model."""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Corporate Category",
            description="Test description",
            type="corporate",
        )
        self.service = Service.objects.create(
            category=self.category,
            name="Corporate Service",
            description="Test description",
            duration=60,
            max_participants=10,
            base_price=Decimal("100.00"),
            is_corporate_eligible=True,
        )
        self.program = CorporateProgram.objects.create(
            name="Test Program",
            description="Test description",
            duration_type="monthly",
            assessment_frequency=30,
            max_participants=100,
        )
        self.program.services.add(self.service)

    def test_string_representation(self):
        """Test the string representation of a program."""
        self.assertEqual(str(self.program), "Test Program (Monthly)")

    def test_program_creation(self):
        """Test that a program can be created."""
        self.assertTrue(isinstance(self.program, CorporateProgram))
        self.assertEqual(self.program.name, "Test Program")

    def test_services_relationship(self):
        """Test the relationship with services."""
        self.assertEqual(self.program.services.count(), 1)
        self.assertEqual(self.program.services.first(), self.service)


class OrganizationTests(TestCase):
    """Test cases for the Organization model."""

    def setUp(self):
        """Set up test data."""
        self.program = CorporateProgram.objects.create(
            name="Test Program",
            description="A test program",
            duration_type="monthly",
            assessment_frequency=30,
            max_participants=50,
        )

        self.organization = Organization.objects.create(
            name="Test Corp",
            industry="Technology",
            contact_email="contact@testcorp.com",
            contact_phone="+1234567890",
            address="123 Test St, Test City",
            employee_count=100,
        )
        self.organization.active_programs.add(self.program)

    def test_str_representation(self):
        """Test the string representation of an organization."""
        self.assertEqual(str(self.organization), "Test Corp")

    def test_organization_creation(self):
        """Test that an organization can be created with valid data."""
        self.assertTrue(isinstance(self.organization, Organization))
        self.assertEqual(self.organization.name, "Test Corp")
        self.assertEqual(self.organization.industry, "Technology")
        self.assertEqual(self.organization.employee_count, 100)

    def test_organization_programs(self):
        """Test organization's relationship with programs."""
        self.assertEqual(self.organization.active_programs.count(), 1)
        self.assertEqual(
            self.organization.active_programs.first().name,
            "Test Program",
        )

    def test_invalid_employee_count(self):
        """Test validation for invalid employee count."""
        with self.assertRaises(ValidationError):
            organization = Organization(
                name="Invalid Corp",
                industry="Technology",
                contact_email="contact@invalid.com",
                contact_phone="+1234567890",
                address="456 Invalid St",
                employee_count=-1,
            )
            organization.full_clean()

    def test_invalid_email(self):
        """Test validation for invalid email."""
        with self.assertRaises(ValidationError):
            organization = Organization(
                name="Invalid Corp",
                industry="Technology",
                contact_email="invalid-email",
                contact_phone="+1234567890",
                address="456 Invalid St",
                employee_count=50,
            )
            organization.full_clean()

    def test_invalid_phone(self):
        """Test validation for invalid phone number."""
        with self.assertRaises(ValidationError):
            organization = Organization(
                name="Invalid Corp",
                industry="Technology",
                contact_email="contact@invalid.com",
                contact_phone="123",  # Too short
                address="456 Invalid St",
                employee_count=50,
            )
            organization.full_clean()

    def test_required_fields(self):
        """Test that required fields raise validation error when empty."""
        required_fields = ["name", "industry", "contact_email", "contact_phone", "address"]
        for field in required_fields:
            with self.subTest(field=field):
                data = {
                    "name": "Test Corp",
                    "industry": "Technology",
                    "contact_email": "contact@testcorp.com",
                    "contact_phone": "+1234567890",
                    "address": "123 Test St",
                    "employee_count": 100,
                }
                data[field] = ""  # Empty the required field
                organization = Organization(**data)
                with self.assertRaises(ValidationError):
                    organization.full_clean()

    def test_organization_proposals(self):
        """Test organization's relationship with proposals."""
        proposal = Proposal.objects.create(
            organization=self.organization,
            title="Test Proposal",
            date_submitted=timezone.now().date(),
            pricing_details="Test pricing",
            valid_until=timezone.now().date() + timedelta(days=30),
            terms_conditions="Test terms",
        )
        self.assertEqual(self.organization.proposals.count(), 1)
        self.assertEqual(self.organization.proposals.first(), proposal)
