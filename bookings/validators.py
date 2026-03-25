"""
Validators for the bookings app.
"""

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Booking, BookingStatus


def validate_booking_time(start_time, service):
    """
    Validate the booking time.
    
    Args:
        start_time: The proposed booking start time
        service: The service being booked
    
    Raises:
        ValidationError: If the booking time is invalid
    """
    now = timezone.now()

    # Check if booking is in the past
    if start_time < now:
        raise ValidationError(
            _("Cannot create bookings in the past."),
        )

    # Check if booking is too far in the future (e.g., > 3 months)
    max_future = now + timezone.timedelta(days=90)
    if start_time > max_future:
        raise ValidationError(
            _("Cannot create bookings more than 3 months in advance."),
        )

    # Check if booking is during business hours
    if start_time.hour < 6 or start_time.hour >= 22:
        raise ValidationError(
            _("Bookings must be between 6:00 AM and 10:00 PM."),
        )

    # Check if booking is on a valid day (e.g., not Sunday)
    if start_time.weekday() == 6:  # Sunday
        raise ValidationError(
            _("Bookings are not available on Sundays."),
        )


def validate_instructor_availability(instructor, start_time, service):
    """
    Validate instructor availability for the booking time.
    
    Args:
        instructor: The instructor being booked
        start_time: The proposed booking start time
        service: The service being booked
    
    Raises:
        ValidationError: If the instructor is not available
    """
    # Calculate end time based on service duration
    end_time = start_time + timezone.timedelta(minutes=service.duration)

    # Check for overlapping bookings
    overlapping_bookings = Booking.objects.filter(
        instructor=instructor,
        status__in=[BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS],
        start_time__lt=end_time,
        end_time__gt=start_time,
    ).exists()

    if overlapping_bookings:
        raise ValidationError(
            _("Instructor is not available at this time."),
        )

    # Check instructor's working hours
    if not instructor.is_available_at(start_time):
        raise ValidationError(
            _("This time is outside the instructor's working hours."),
        )


def validate_client_eligibility(client, service, start_time):
    """
    Validate if the client is eligible for the booking.
    
    Args:
        client: The client making the booking
        service: The service being booked
        start_time: The proposed booking start time
    
    Raises:
        ValidationError: If the client is not eligible
    """
    # Check if client has any unpaid bookings
    unpaid_bookings = Booking.objects.filter(
        client=client,
        payment_status__in=["UNPAID", "PARTIALLY_PAID"],
        start_time__lt=timezone.now(),
    ).exists()

    if unpaid_bookings:
        raise ValidationError(
            _("Please settle outstanding payments before making new bookings."),
        )

    # Check if client has too many bookings on the same day
    same_day_bookings = Booking.objects.filter(
        client=client,
        start_time__date=start_time.date(),
        status__in=[BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS],
    ).count()

    if same_day_bookings >= 3:
        raise ValidationError(
            _("Maximum of 3 bookings per day allowed."),
        )

    # Check if client meets service prerequisites
    if not service.client_meets_prerequisites(client):
        raise ValidationError(
            _("You do not meet the prerequisites for this service."),
        )

    # Check if client has exceeded weekly booking limit
    week_start = start_time.date() - timezone.timedelta(days=start_time.weekday())
    week_end = week_start + timezone.timedelta(days=7)

    weekly_bookings = Booking.objects.filter(
        client=client,
        start_time__date__range=[week_start, week_end],
        status__in=[BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS],
    ).count()

    if weekly_bookings >= 10:
        raise ValidationError(
            _("Maximum of 10 bookings per week allowed."),
        )
