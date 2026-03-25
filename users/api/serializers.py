from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer[User]):
    """Serializer for User model."""
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    isAdmin = serializers.BooleanField(source="is_staff", read_only=True)
    isStaff = serializers.BooleanField(source="is_staff", read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="api:user-detail",
        lookup_field="pk"
    )

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "name", "url", 
            "phone_number", "date_of_birth", "role", "isAdmin", "isStaff"
        ]

        extra_kwargs = {
            "email": {"read_only": True},
        }

    def get_name(self, obj: User) -> str:
        """Get user's full name."""
        return obj.get_full_name() or obj.email

    def get_role(self, obj: User) -> str:
        """Determine user's role."""
        if obj.is_staff:
            return "admin"
        if hasattr(obj, 'wellness_instructor'):
            return "instructor"
        return "member"
