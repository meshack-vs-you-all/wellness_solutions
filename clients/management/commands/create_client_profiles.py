from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from ..models import ClientProfile


User = get_user_model()

class Command(BaseCommand):
    help = "Creates client profiles for existing users that don't have one"

    def handle(self, *args, **kwargs):
        # Create clients group if it doesn't exist
        clients_group, created = Group.objects.get_or_create(name="Clients")
        if created:
            self.stdout.write(self.style.SUCCESS("Created Clients group"))

        # Get all users without client profiles
        users_without_profiles = User.objects.filter(client_profile__isnull=True)
        count = 0

        for user in users_without_profiles:
            ClientProfile.objects.create(user=user)
            user.groups.add(clients_group)
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {count} client profiles",
            ),
        )
