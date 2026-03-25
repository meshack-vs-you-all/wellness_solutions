"""
Celery tasks for the bookings app.
"""

from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Booking, BookingStatus
from .notifications import send_reminder_email


@shared_task
def send_booking_reminders():
    """Send reminder emails for bookings scheduled for tomorrow."""
    tomorrow = timezone.now().date() + timedelta(days=1)
    bookings = Booking.objects.filter(
        start_time__date=tomorrow,
        status=BookingStatus.CONFIRMED,
    ).select_related("client", "location", "service", "instructor")

    for booking in bookings:
        send_reminder_email(booking)
