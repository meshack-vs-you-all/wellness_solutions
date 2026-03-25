"""
Signal handlers for the bookings app.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string

from .models import Booking, BookingPayment, PaymentStatus


@receiver(pre_save, sender=Booking)
def generate_booking_number(sender, instance, **kwargs):
    """Generate a unique booking number if not set."""
    if not instance.booking_number:
        # Format: YYYYMMDD-XXXX where X is random
        date_str = timezone.now().strftime("%Y%m%d")
        random_str = get_random_string(4, "0123456789")
        instance.booking_number = f"{date_str}-{random_str}"

        # Ensure uniqueness
        while Booking.objects.filter(booking_number=instance.booking_number).exists():
            random_str = get_random_string(4, "0123456789")
            instance.booking_number = f"{date_str}-{random_str}"


@receiver(post_save, sender=BookingPayment)
def update_booking_payment_status(sender, instance, created, **kwargs):
    """Update booking payment status when a payment is made."""
    if created:
        booking = instance.booking
        total_paid = booking.payments.filter(
            status=PaymentStatus.PAID,
        ).aggregate(
            total=models.Sum("amount"),
        )["total"] or 0

        if total_paid >= booking.total_price:
            booking.payment_status = PaymentStatus.PAID
        elif total_paid > 0:
            booking.payment_status = PaymentStatus.PARTIALLY_PAID
        booking.save()
