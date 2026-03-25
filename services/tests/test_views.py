"""
Tests for the services app views.
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import CorporateProgram, Organization, Proposal, Service, ServiceCategory


User = get_user_model()


class ServiceViewTests(TestCase):
    """Test cases for service-related views."""

    def setUp(self):
        # Create test user and staff user
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.staff_user = User.objects.create_user(
            email="staffuser@example.com",
            password="staffpass123",
            first_name="Staff",
            last_name="User",
            is_staff=True,
        )

        # Create test category and service
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

    def test_service_list_view(self):
        """Test the service list view."""
        # Login required
        response = self.client.get(reverse("services:service-list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test with staff user
        self.client.login(email="staffuser@example.com", password="staffpass123")
        response = self.client.get(reverse("services:service-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_list.html")
        self.assertContains(response, "Test Service")

    def test_service_detail_view(self):
        """Test the service detail view."""
        self.client.login(email="staffuser@example.com", password="staffpass123")
        response = self.client.get(
            reverse("services:service-detail", kwargs={"pk": self.service.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_detail.html")
        self.assertContains(response, self.service.name)
        self.assertContains(response, self.service.description)

    def test_service_create_view(self):
        """Test the service create view."""
        url = reverse("services:service-create")

        # Test with regular user
        self.client.login(email="testuser@example.com", password="testpass123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test with staff user
        self.client.login(email="staffuser@example.com", password="staffpass123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_form.html")

        # Test creating a service
        data = {
            "category": self.category.pk,
            "name": "New Service",
            "description": "New description",
            "duration": 45,
            "max_participants": 1,
            "base_price": "75.00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(
            Service.objects.filter(name="New Service").exists(),
        )

    def test_service_update_view(self):
        """Test the service update view."""
        url = reverse("services:service-update", kwargs={"pk": self.service.pk})

        # Test with staff user
        self.client.login(email="staffuser@example.com", password="staffpass123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_form.html")

        # Test updating a service
        data = {
            "category": self.category.pk,
            "name": "Updated Service",
            "description": "Updated description",
            "duration": 60,
            "max_participants": 2,
            "base_price": "100.00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, "Updated Service")
        self.assertEqual(self.service.duration, 60)


class CategoryViewTests(TestCase):
    """Test cases for category-related views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.staff_user = User.objects.create_user(
            email="staffuser@example.com",
            password="staffpass123",
            first_name="Staff",
            last_name="User",
            is_staff=True,
        )
        self.category = ServiceCategory.objects.create(
            name="Test Category",
            description="Test description",
            type="individual",
        )

    def test_category_list_view(self):
        """Test the category list view."""
        self.client.login(email="staffuser@example.com", password="staffpass123")
        response = self.client.get(reverse("services:category-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/category_list.html")
        self.assertContains(response, "Test Category")

    def test_category_detail_view(self):
        """Test the category detail view."""
        self.client.login(email="staffuser@example.com", password="staffpass123")
        response = self.client.get(
            reverse("services:category-detail", kwargs={"pk": self.category.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/category_detail.html")
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category.description)

    def test_category_create_view(self):
        """Test the category create view."""
        url = reverse("services:category-create")

        # Test with staff user
        self.client.login(email="staffuser@example.com", password="staffpass123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/category_form.html")

        # Test creating a category
        data = {
            "name": "New Category",
            "description": "New description",
            "type": "group",
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(
            ServiceCategory.objects.filter(name="New Category").exists(),
        )


class OrganizationViewTests(TestCase):
    """Test cases for Organization views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.staff_user = User.objects.create_user(
            email="staffuser@example.com",
            password="staffpass123",
            first_name="Staff",
            last_name="User",
            is_staff=True,
        )
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

        # Create a proposal for testing related data
        self.proposal = Proposal.objects.create(
            organization=self.organization,
            title="Test Proposal",
            date_submitted=timezone.now().date(),
            pricing_details="Test pricing",
            valid_until=timezone.now().date() + timedelta(days=30),
            terms_conditions="Test terms",
        )
        self.proposal.programs.add(self.program)

    def test_organization_list_view(self):
        """Test the organization list view."""
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("services:organization-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/organization_list.html")
        self.assertContains(response, "Test Corp")
        self.assertQuerysetEqual(
            response.context["organizations"],
            [self.organization],
            transform=lambda x: x,
        )

    def test_organization_detail_view(self):
        """Test the organization detail view."""
        self.client.force_login(self.staff_user)
        response = self.client.get(
            reverse("services:organization-detail",
                   kwargs={"pk": self.organization.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/organization_detail.html")
        self.assertContains(response, self.organization.name)

    def test_organization_create_view(self):
        """Test the organization create view."""
        self.client.force_login(self.staff_user)
        data = {
            "name": "New Organization",
            "industry": "Technology",
            "contact_email": "new@example.com",
            "contact_phone": "+1234567890",
            "address": "456 New St",
            "employee_count": 50,
        }
        response = self.client.post(reverse("services:organization-create"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Organization.objects.filter(name="New Organization").exists())

    def test_organization_update_view(self):
        """Test the organization update view."""
        self.client.force_login(self.staff_user)
        data = {
            "name": "Updated Organization",
            "industry": "Healthcare",
            "contact_email": "updated@example.com",
            "contact_phone": "+9876543210",
            "address": "789 Update St",
            "employee_count": 75,
        }
        response = self.client.post(
            reverse("services:organization-update",
                   kwargs={"pk": self.organization.pk}),
            data,
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.name, "Updated Organization")

    def test_organization_create_view_invalid_data(self):
        """Test organization creation with invalid data."""
        self.client.force_login(self.staff_user)
        data = {
            "name": "",  # invalid: empty name
            "employee_count": -1,  # invalid: negative count
            "contact_phone": "invalid",  # invalid: wrong format
            "address": "",  # invalid: empty address
        }
        response = self.client.post(reverse("services:organization-create"), data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])
        self.assertEqual(form.errors["employee_count"], ["Ensure this value is greater than or equal to 0."])
        self.assertEqual(form.errors["contact_phone"], ["Phone number must start with + followed by digits only."])
        self.assertEqual(form.errors["address"], ["This field is required."])

    def test_organization_update_view_invalid_data(self):
        """Test organization update with invalid data."""
        self.client.force_login(self.staff_user)
        data = {
            "name": "",  # invalid: empty name
            "employee_count": -1,  # invalid: negative count
            "contact_phone": "invalid",  # invalid: wrong format
            "address": "",  # invalid: empty address
        }
        response = self.client.post(
            reverse("services:organization-update",
                   kwargs={"pk": self.organization.pk}),
            data,
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])
        self.assertEqual(form.errors["employee_count"], ["Ensure this value is greater than or equal to 0."])
        self.assertEqual(form.errors["contact_phone"], ["Phone number must start with + followed by digits only."])
        self.assertEqual(form.errors["address"], ["This field is required."])

    def test_organization_detail_view_404(self):
        """Test organization detail view with non-existent organization."""
        self.client.force_login(self.staff_user)
        response = self.client.get(
            reverse("services:organization-detail", kwargs={"pk": 99999}),
        )
        self.assertEqual(response.status_code, 404)

    def test_organization_update_view_404(self):
        """Test organization update view with non-existent organization."""
        self.client.force_login(self.staff_user)
        response = self.client.get(
            reverse("services:organization-update", kwargs={"pk": 99999}),
        )
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_access(self):
        """Test access to views when user is not authenticated."""
        self.client.logout()
        urls = [
            reverse("services:organization-list"),
            reverse("services:organization-create"),
            reverse("services:organization-detail", kwargs={"pk": self.organization.pk}),
            reverse("services:organization-update", kwargs={"pk": self.organization.pk}),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login
            self.assertIn("login", response.url)
