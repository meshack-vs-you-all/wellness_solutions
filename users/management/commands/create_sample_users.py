"""
Management command to create sample users for development.
"""

import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction

from clients.models import ClientProfile
from wellness_instructors.models import WellnessInstructor
from users.models import User


class Command(BaseCommand):
    help = "Creates sample users for development"

    def validate_phone_number(self, phone):
        """Validate phone number format."""
        if not phone or not re.match(r"^\+\d{10,15}$", phone):
            raise ValidationError(f"Invalid phone number format: {phone}. Must start with + and contain 10-15 digits.")

    def create_user_safely(self, user_data, user_type):
        """Create a user with error handling."""
        try:
            if "phone_number" in user_data:
                self.validate_phone_number(user_data["phone_number"])

            user = User.objects.create(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone_number=user_data.get("phone_number"),
                is_staff=user_data.get("is_staff", False),
            )
            user.set_password(user_data["password"])

            # Add user to appropriate group
            from django.contrib.auth.models import Group
            if user_type == "client":
                group, _ = Group.objects.get_or_create(name="Clients")
            elif user_type == "instructor":
                group, _ = Group.objects.get_or_create(name="Instructors")
            elif user_type == "staff":
                group, _ = Group.objects.get_or_create(name="Staff")

            user.groups.add(group)
            user.save()

            return user
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f"Validation error creating {user_type} {user_data['email']}: {str(e)}"))
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating {user_type} {user_data['email']}: {str(e)}"))
            return None

    def handle(self, *args, **kwargs):
        # Clean up existing non-superuser accounts and their related profiles
        self.stdout.write("Cleaning up existing users and profiles...")

        # Delete all related profiles first
        with transaction.atomic():
            try:
                # Delete all users and profiles
                User.objects.filter(is_superuser=False).delete()
                self.stdout.write("Deleted all non-superuser accounts")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during cleanup: {str(e)}"))
                return

        # Create client users first
        client_users = [
            {
                "email": "client1@example.com",
                "first_name": "John",
                "last_name": "Smith",
                "phone_number": "+1234567892",
                "emergency_contact_name": "Jane Smith",
                "emergency_contact_phone": "+1234567893",
                "notes": "Regular client interested in flexibility improvement",
                "password": "clientpass123",
            },
            {
                "email": "client2@example.com",
                "first_name": "Lisa",
                "last_name": "Brown",
                "phone_number": "+1234567894",
                "emergency_contact_name": "Mike Brown",
                "emergency_contact_phone": "+1234567895",
                "notes": "Focuses on recovery and rehabilitation",
                "password": "clientpass123",
            },
        ]

        # Create client users and profiles first
        for client_data in client_users:
            with transaction.atomic():
                try:
                    user = self.create_user_safely(client_data, "client")
                    if user:
                        self.validate_phone_number(client_data["emergency_contact_phone"])

                        # Create client profile
                        profile = ClientProfile.objects.create(
                            user=user,
                            emergency_contact_name=client_data["emergency_contact_name"],
                            emergency_contact_phone=client_data["emergency_contact_phone"],
                            notes=client_data["notes"],
                        )
                        self.stdout.write(self.style.SUCCESS(f"Created client user: {user.email} with profile"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating client: {str(e)}"))

        # Create instructor users second
        instructor_users = [
            {
                "email": "instructor1@example.com",
                "first_name": "David",
                "last_name": "Wilson",
                "phone_number": "+1234567890",
                "bio": "Certified stretching instructor with 5 years of experience",
                "specializations": "flexibility",
                "certification_level": "certified",
                "years_of_experience": 5,
                "hourly_rate": Decimal("50.00"),
                "password": "instructpass123",
            },
            {
                "email": "instructor2@example.com",
                "first_name": "Emma",
                "last_name": "Garcia",
                "phone_number": "+1234567891",
                "bio": "Specialized in therapeutic stretching and rehabilitation",
                "specializations": "therapeutic",
                "certification_level": "specialist",
                "years_of_experience": 8,
                "hourly_rate": Decimal("60.00"),
                "password": "instructpass123",
            },
        ]

        # Create instructor users and profiles
        for instructor_data in instructor_users:
            with transaction.atomic():
                try:
                    user = self.create_user_safely(instructor_data, "instructor")
                    if user:
                        WellnessInstructor.objects.create(
                            user=user,
                            bio=instructor_data["bio"],
                            specializations=instructor_data["specializations"],
                            certification_level=instructor_data["certification_level"],
                            years_of_experience=instructor_data["years_of_experience"],
                            hourly_rate=instructor_data["hourly_rate"],
                        )
                        self.stdout.write(self.style.SUCCESS(f"Created instructor user: {user.email}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating instructor: {str(e)}"))

        # Create staff users last
        staff_users = [
            {
                "email": "staff1@example.com",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "is_staff": True,
                "phone_number": "+1234567892",
                "password": "staffpass123",
            },
            {
                "email": "staff2@example.com",
                "first_name": "Michael",
                "last_name": "Chen",
                "is_staff": True,
                "phone_number": "+1234567893",
                "password": "staffpass123",
            },
        ]

        # Create staff users
        for staff_data in staff_users:
            with transaction.atomic():
                try:
                    user = self.create_user_safely(staff_data, "staff")
                    if user:
                        self.stdout.write(self.style.SUCCESS(f"Created staff user: {user.email}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating staff user: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Successfully created sample users"))
