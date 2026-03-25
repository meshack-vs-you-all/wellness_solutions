"""Signal handlers for the clients app."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import ClientProfile


User = get_user_model()

@receiver(m2m_changed, sender=User.groups.through)
def handle_client_group_changes(sender, instance, action, pk_set, **kwargs):
    """Create or manage ClientProfile when user's groups change."""
    try:
        # Only proceed for actual group additions
        if action != "post_add" or not pk_set:
            return

        # Skip during fixture loading
        if kwargs.get("raw", False):
            return

        with transaction.atomic():
            # Check if the Clients group was added
            clients_group = Group.objects.get(name="Clients")
            if clients_group.id in pk_set:
                # Ensure we don't create duplicate profiles
                if not hasattr(instance, "client_profile"):
                    ClientProfile.objects.create(user=instance)

                # Remove from other role groups if present
                instance.groups.remove(
                    *Group.objects.filter(
                        name__in=["Instructors", "Staff"],
                    ),
                )

    except ObjectDoesNotExist:
        # Log error if Clients group doesn't exist
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "Clients group does not exist. Please ensure groups are properly configured.",
        )
    except Exception as e:
        # Log any other errors but don't break the application
        from django.core.exceptions import ValidationError
        raise ValidationError(f"Error creating client profile: {str(e)}")


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """Handle user save events for client profiles."""
    try:
        # Skip during fixture loading
        if kwargs.get("raw", False):
            return

        with transaction.atomic():
            # If this is a new user and they're in the Clients group
            if created and instance.groups.filter(name="Clients").exists():
                if not hasattr(instance, "client_profile"):
                    ClientProfile.objects.create(user=instance)

            # If user has a client profile, ensure it's saved
            elif hasattr(instance, "client_profile"):
                instance.client_profile.save()

    except Exception as e:
        # Log any errors but don't break the application
        from django.core.exceptions import ValidationError
        raise ValidationError(f"Error handling user save for client: {str(e)}")
