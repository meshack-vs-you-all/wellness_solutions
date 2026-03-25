from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User


if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """Custom admin view for User model."""

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]
    search_fields = ["first_name", "last_name", "email", "phone_number"]
    ordering = ["email"]
    filter_horizontal = ["groups", "user_permissions"]

    actions = ["make_active", "make_inactive", "add_to_clients", "add_to_instructors", "add_to_staff"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", "date_of_birth")}),
        (
            _("Emergency Contact"),
            {"fields": ("emergency_contact_name", "emergency_contact_phone")},
        ),
        (
            _("Preferences"),
            {"fields": ("preferred_language", "receive_notifications")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    def make_active(self, request, queryset):
        """Batch action to make users active."""
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        """Batch action to make users inactive."""
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected users as inactive"

    def add_to_clients(self, request, queryset):
        """Add selected users to the Clients group."""
        clients_group, _ = Group.objects.get_or_create(name="Clients")
        for user in queryset:
            user.groups.add(clients_group)
    add_to_clients.short_description = "Add selected users to Clients group"

    def add_to_instructors(self, request, queryset):
        """Add selected users to the Instructors group."""
        instructors_group, _ = Group.objects.get_or_create(name="Instructors")
        for user in queryset:
            user.groups.add(instructors_group)
    add_to_instructors.short_description = "Add selected users to Instructors group"

    def add_to_staff(self, request, queryset):
        """Add selected users to the Staff group and make them staff."""
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        for user in queryset:
            user.groups.add(staff_group)
            user.is_staff = True
            user.save()
    add_to_staff.short_description = "Add selected users to Staff group"
