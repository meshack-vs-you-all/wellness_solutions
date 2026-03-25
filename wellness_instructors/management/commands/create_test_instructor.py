"""Management command to create a test instructor user."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from .models import WellnessInstructor


User = get_user_model()


class Command(BaseCommand):
    """Create a test instructor user with a profile."""

    help = "Creates a test instructor user with the specified email and password"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument("email", type=str, help="The email for the instructor")
        parser.add_argument("password", type=str, help="The password for the instructor")
        parser.add_argument("--name", type=str, help="Full name of the instructor")
        parser.add_argument(
            "--specialization",
            type=str,
            choices=[choice[0] for choice in WellnessInstructor.SPECIALIZATION_CHOICES],
            default="general",
            help="Specialization of the instructor",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        email = options["email"]
        password = options["password"]
        name = options.get("name", "")
        specialization = options["specialization"]

        # Create or update user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"name": name, "is_staff": True},
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created instructor user: {email}"),
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"User {email} already exists, updating profile..."),
            )

        # Create or update instructor profile
        instructor, created = WellnessInstructor.objects.get_or_create(
            user=user,
            defaults={
                "specializations": specialization,
                "bio": f"Test instructor specializing in {specialization}",
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created instructor profile for {email}"),
            )
        else:
            instructor.specializations = specialization
            instructor.save()
            self.stdout.write(
                self.style.SUCCESS(f"Updated instructor profile for {email}"),
            )
