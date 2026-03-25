"""Signal handlers for the wellness_instructors app."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import WellnessInstructor


User = get_user_model()

@receiver(m2m_changed, sender=User.groups.through)
def handle_instructor_group_changes(sender, instance, action, pk_set, **kwargs):
    """Create or manage WellnessInstructor profile when user's groups change."""
    try:
        # Only proceed for actual group additions
        if action != "post_add" or not pk_set:
            return

        # Skip during fixture loading
        if kwargs.get("raw", False):
            return

        with transaction.atomic():
            # Check if the Instructors group was added
            instructor_group = Group.objects.get(name="Instructors")
            if instructor_group.id in pk_set:
                # Ensure we don't create duplicate profiles
                if not hasattr(instance, "wellness_instructor"):
                    WellnessInstructor.objects.create(
                        user=instance,
                        bio="",
                        specializations="general",
                        certification_level="certified",
                    )

                # Remove from Clients group if present, but allow Staff membership
                instance.groups.remove(
                    *Group.objects.filter(name="Clients"),
                )

    except ObjectDoesNotExist:
        # Log error if Instructors group doesn't exist
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "Instructors group does not exist. Please ensure groups are properly configured.",
        )
    except Exception as e:
        # Log any other errors but don't break the application
        from django.core.exceptions import ValidationError
        raise ValidationError(f"Error creating instructor profile: {str(e)}")


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """Handle user save events for instructor profiles."""
    try:
        # Skip during fixture loading
        if kwargs.get("raw", False):
            return

        with transaction.atomic():
            # If this is a new user and they're in the Instructors group
            if created and instance.groups.filter(name="Instructors").exists():
                if not hasattr(instance, "wellness_instructor"):
                    WellnessInstructor.objects.create(
                        user=instance,
                        bio="",
                        specializations="general",
                        certification_level="certified",
                    )

            # If user has an instructor profile, ensure it's saved
            elif hasattr(instance, "wellness_instructor"):
                instance.wellness_instructor.save()

    except Exception as e:
        # Log any other errors but don't break the application
        from django.core.exceptions import ValidationError
        raise ValidationError(f"Error handling user save for instructor: {str(e)}")
