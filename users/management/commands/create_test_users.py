from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from wellness_instructors.models import WellnessInstructor


class Command(BaseCommand):
    help = "Creates test users with different roles including a senior instructor"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Ensure groups exist
        clients_group, _ = Group.objects.get_or_create(name="Clients")
        instructors_group, _ = Group.objects.get_or_create(name="Instructors")

        # Test users data
        users_data = [
            {
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "password": "testpass123",
                "is_staff": True,
                "is_superuser": True,
                "is_instructor": True,
            },
            {
                "email": "sarah.instructor@example.com",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "password": "testpass123",
                "is_staff": False,
                "is_superuser": False,
                "is_instructor": True,
                "instructor_details": {
                    "bio": """Sarah Johnson is a certified Master Instructor with over 10 years of experience in flexibility training and therapeutic stretching. 
                    She specializes in both one-on-one sessions and group workshops, focusing on improving mobility, reducing pain, and enhancing athletic performance. 
                    Sarah holds advanced certifications in sports therapy and rehabilitation.""",
                    "specializations": "therapeutic",
                    "certification_level": "master",
                    "years_of_experience": 10,
                    "hourly_rate": 150.00,
                    "is_available": True,
                },
            },
            {
                "email": "instructor1@example.com",
                "first_name": "Instructor",
                "last_name": "One",
                "password": "testpass123",
                "is_staff": False,
                "is_superuser": False,
                "is_instructor": True,
            },
            {
                "email": "instructor2@example.com",
                "first_name": "Instructor",
                "last_name": "Two",
                "password": "testpass123",
                "is_staff": False,
                "is_superuser": False,
                "is_instructor": True,
            },
            {
                "email": "client1@example.com",
                "first_name": "Client",
                "last_name": "One",
                "password": "testpass123",
                "is_staff": False,
                "is_superuser": False,
                "is_instructor": False,
            },
            {
                "email": "client2@example.com",
                "first_name": "Client",
                "last_name": "Two",
                "password": "testpass123",
                "is_staff": False,
                "is_superuser": False,
                "is_instructor": False,
            },
        ]

        for user_data in users_data:
            email = user_data.pop("email")
            password = user_data.pop("password")
            is_instructor = user_data.pop("is_instructor")
            instructor_details = user_data.pop("instructor_details", None)

            # Create user if doesn't exist
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    **user_data,
                )

                # Add user to appropriate group
                if is_instructor:
                    user.groups.add(instructors_group)
                    # Create WellnessInstructor profile if needed
                    if instructor_details:
                        # Create detailed instructor profile
                        WellnessInstructor.objects.get_or_create(
                            user=user,
                            defaults=instructor_details,
                        )
                    else:
                        WellnessInstructor.objects.get_or_create(
                            user=user,
                            defaults={
                                "bio": f"Stretch instructor {user.get_full_name()}",
                                "specializations": "general",
                                "certification_level": "basic",
                                "years_of_experience": 1,
                                "hourly_rate": 100.00,
                                "is_available": True,
                            },
                        )
                else:
                    user.groups.add(clients_group)

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created user: {email}"),
                )
            else:
                self.stdout.write(self.style.WARNING(f"User already exists: {email}"))
