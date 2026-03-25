"""
API views for the bookings app.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Booking, BookingStatus
from .serializers import LocationInstructorSerializer, LocationServiceSerializer


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def check_availability(request):
    """Check if a time slot is available."""
    instructor_id = request.data.get("instructor")
    start_time = request.data.get("start_time")
    end_time = request.data.get("end_time")
    booking_id = request.data.get("booking_id")

    if not all([instructor_id, start_time, end_time]):
        return Response(
            {"error": _("Missing required parameters")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check for conflicting bookings
    conflicts = Booking.objects.filter(
        instructor_id=instructor_id,
        start_time__lt=end_time,
        end_time__gt=start_time,
        status=BookingStatus.CONFIRMED,
    )

    if booking_id:
        conflicts = conflicts.exclude(id=booking_id)

    is_available = not conflicts.exists()

    return Response({
        "available": is_available,
        "message": _("Time slot is available")
        if is_available else _("Time slot is not available"),
    })


class LocationServiceList(generics.ListAPIView):
    """List services available at a location."""
    serializer_class = LocationServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter services by location."""
        location_id = self.kwargs["location_id"]
        return LocationService.objects.filter(
            location_id=location_id,
            active=True,
        )


class LocationInstructorList(generics.ListAPIView):
    """List instructors available at a location."""
    serializer_class = LocationInstructorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter instructors by location."""
        location_id = self.kwargs["location_id"]
        return LocationInstructor.objects.filter(
            location_id=location_id,
            active=True,
        )
