"""
Serializers for the bookings app.
"""

from rest_framework import serializers

from locations.models import LocationInstructor, LocationService

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for bookings."""

    class Meta:
        model = Booking
        fields = [
            "id", "booking_number", "booking_type", "status",
            "payment_status", "start_time", "end_time",
            "total_price", "notes",
        ]
        read_only_fields = ["booking_number", "status", "payment_status"]


class LocationServiceSerializer(serializers.ModelSerializer):
    """Serializer for location services."""

    class Meta:
        model = LocationService
        fields = ["id", "name", "description", "duration", "price"]


class LocationInstructorSerializer(serializers.ModelSerializer):
    """Serializer for location instructors."""
    name = serializers.SerializerMethodField()

    class Meta:
        model = LocationInstructor
        fields = ["id", "name", "bio"]

    def get_name(self, obj):
        """Get instructor's full name."""
        return obj.user.get_full_name()
