"""
Tests for the services app forms.
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..forms import (
    CorporateProgramForm,
    OrganizationForm,
    ProposalForm,
    ServiceCategoryForm,
    ServiceForm,
)
from ..models import CorporateProgram, Organization, Service, ServiceCategory


class ServiceCategoryFormTests(TestCase):
    """Test cases for the ServiceCategoryForm."""

    def test_valid_data(self):
        """Test form with valid data."""
        form = ServiceCategoryForm({
            "name": "Test Category",
            "description": "Test description",
            "type": "individual",
            "is_active": True,
        })
        self.assertTrue(form.is_valid())
        category = form.save()
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.type, "individual")

    def test_blank_data(self):
        """Test form with blank data."""
        form = ServiceCategoryForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            "name": ["This field is required."],
            "description": ["This field is required."],
            "type": ["This field is required."],
        })


class ServiceFormTests(TestCase):
    """Test cases for the ServiceForm."""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Test Category",
            description="Test description",
            type="individual",
        )

    def test_valid_data(self):
        """Test form with valid data."""
        form = ServiceForm({
            "category": self.category.pk,
            "name": "Test Service",
            "description": "Test description",
            "duration": 30,
            "max_participants": 1,
            "base_price": "50.00",
            "is_corporate_eligible": False,
        })
        self.assertTrue(form.is_valid())
        service = form.save()
        self.assertEqual(service.name, "Test Service")
        self.assertEqual(service.duration, 30)
        self.assertEqual(service.base_price, Decimal("50.00"))

    def test_invalid_duration(self):
        """Test form with invalid duration."""
        form = ServiceForm({
            "category": self.category.pk,
            "name": "Test Service",
            "description": "Test description",
            "duration": 10,  # Less than minimum
            "max_participants": 1,
            "base_price": "50.00",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("duration", form.errors)

    def test_invalid_price(self):
        """Test form with invalid price."""
        form = ServiceForm({
            "category": self.category.pk,
            "name": "Test Service",
            "description": "Test description",
            "duration": 30,
            "max_participants": 1,
            "base_price": "-50.00",  # Negative price
        })
        self.assertFalse(form.is_valid())
        self.assertIn("base_price", form.errors)


class CorporateProgramFormTests(TestCase):
    """Test cases for the CorporateProgramForm."""

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

    def test_valid_data(self):
        """Test form with valid data."""
        form = CorporateProgramForm({
            "name": "Test Program",
            "description": "Test description",
            "duration_type": "monthly",
            "assessment_frequency": 30,
            "max_participants": 100,
            "services": [self.service.pk],
            "features": ["Test feature 1", "Test feature 2"],
        })
        self.assertTrue(form.is_valid())
        program = form.save()
        self.assertEqual(program.name, "Test Program")
        self.assertEqual(program.duration_type, "monthly")
        self.assertEqual(program.services.count(), 1)

    def test_invalid_assessment_frequency(self):
        """Test form with invalid assessment frequency."""
        form = CorporateProgramForm({
            "name": "Test Program",
            "description": "Test description",
            "duration_type": "monthly",
            "assessment_frequency": 0,  # Invalid value
            "max_participants": 100,
            "services": [self.service.pk],
            "features": ["Test feature"],
        })
        self.assertFalse(form.is_valid())
        self.assertIn("assessment_frequency", form.errors)


class OrganizationFormTests(TestCase):
    """Test cases for the OrganizationForm."""

    def setUp(self):
        """Set up test data."""
        self.program = CorporateProgram.objects.create(
            name="Test Program",
            description="A test program",
            duration_type="monthly",
            assessment_frequency=30,
            max_participants=50,
        )

        self.valid_data = {
            "name": "Test Corp",
            "industry": "Technology",
            "contact_email": "contact@testcorp.com",
            "contact_phone": "+1234567890",
            "address": "123 Test St, Test City",
            "employee_count": 100,
            "active_programs": [self.program.id],
        }

    def test_valid_form(self):
        """Test form with valid data."""
        form = OrganizationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        organization = form.save()
        self.assertEqual(organization.name, "Test Corp")
        self.assertEqual(organization.employee_count, 100)
        self.assertEqual(organization.active_programs.count(), 1)

    def test_blank_data(self):
        """Test form with blank data."""
        form = OrganizationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  # All required fields
        required_fields = [
            "name", "industry", "contact_email",
            "contact_phone", "address", "employee_count",
        ]
        for field in required_fields:
            self.assertIn(field, form.errors)

    def test_invalid_email(self):
        """Test form with invalid email."""
        invalid_data = self.valid_data.copy()
        invalid_data["contact_email"] = "invalid-email"
        form = OrganizationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("contact_email", form.errors)

    def test_invalid_phone(self):
        """Test form with invalid phone number."""
        invalid_data = self.valid_data.copy()
        invalid_data["contact_phone"] = "123"  # Too short
        form = OrganizationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("contact_phone", form.errors)

    def test_negative_employee_count(self):
        """Test form with negative employee count."""
        invalid_data = self.valid_data.copy()
        invalid_data["employee_count"] = -1
        form = OrganizationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("employee_count", form.errors)

    def test_zero_employee_count(self):
        """Test form with zero employee count."""
        invalid_data = self.valid_data.copy()
        invalid_data["employee_count"] = 0
        form = OrganizationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("employee_count", form.errors)

    def test_update_organization(self):
        """Test updating an existing organization."""
        # First create an organization
        form = OrganizationForm(data=self.valid_data)
        organization = form.save()

        # Now update it
        update_data = self.valid_data.copy()
        update_data["name"] = "Updated Corp"
        update_data["employee_count"] = 200

        update_form = OrganizationForm(data=update_data, instance=organization)
        self.assertTrue(update_form.is_valid())
        updated_org = update_form.save()

        self.assertEqual(updated_org.name, "Updated Corp")
        self.assertEqual(updated_org.employee_count, 200)
        # Ensure other fields remained unchanged
        self.assertEqual(updated_org.industry, self.valid_data["industry"])

    def test_form_widgets(self):
        """Test that form widgets are properly configured."""
        form = OrganizationForm()
        self.assertEqual(form.fields["address"].widget.attrs.get("rows"), 3)

    def test_active_programs_optional(self):
        """Test that active_programs field is optional."""
        data = self.valid_data.copy()
        del data["active_programs"]
        form = OrganizationForm(data=data)
        self.assertTrue(form.is_valid())


class ProposalFormTests(TestCase):
    """Test cases for the ProposalForm."""

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

        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        self.valid_data = {
            "organization": self.organization.id,
            "title": "Test Proposal",
            "date_submitted": timezone.now().date(),
            "programs": [self.program.id],
            "custom_services": "Custom service details",
            "pricing_details": "Pricing information",
            "status": "draft",
            "valid_until": timezone.now().date() + timedelta(days=30),
            "terms_conditions": "Terms and conditions",
        }

    def test_valid_form(self):
        """Test form with valid data."""
        form = ProposalForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        proposal = form.save()
        self.assertEqual(proposal.title, "Test Proposal")
        self.assertEqual(proposal.organization, self.organization)

    def test_blank_data(self):
        """Test form with blank data."""
        form = ProposalForm(data={})
        self.assertFalse(form.is_valid())
        required_fields = [
            "organization", "title", "date_submitted",
            "pricing_details", "valid_until", "terms_conditions",
        ]
        for field in required_fields:
            self.assertIn(field, form.errors)

    def test_invalid_dates(self):
        """Test form with invalid dates."""
        invalid_data = self.valid_data.copy()
        invalid_data["valid_until"] = self.valid_data["date_submitted"] - timedelta(days=1)
        form = ProposalForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_update_proposal(self):
        """Test updating an existing proposal."""
        form = ProposalForm(data=self.valid_data)
        proposal = form.save()

        update_data = self.valid_data.copy()
        update_data["title"] = "Updated Proposal"
        update_data["status"] = "sent"

        update_form = ProposalForm(data=update_data, instance=proposal)
        self.assertTrue(update_form.is_valid())
        updated_proposal = update_form.save()

        self.assertEqual(updated_proposal.title, "Updated Proposal")
        self.assertEqual(updated_proposal.status, "sent")
