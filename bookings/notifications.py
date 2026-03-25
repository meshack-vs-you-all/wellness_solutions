"""
Email notifications for the bookings app.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


def send_booking_confirmation(booking):
    """Send booking confirmation email to client."""
    subject = _("Booking Confirmation - {0}").format(booking.booking_number)
    context = {
        "booking": booking,
        "site_name": settings.SITE_NAME,
    }

    html_message = render_to_string(
        "bookings/email/booking_confirmation.html",
        context,
    )
    text_message = render_to_string(
        "bookings/email/booking_confirmation.txt",
        context,
    )

    send_mail(
        subject=subject,
        message=text_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.client.email],
        fail_silently=False,
    )


def send_booking_cancelled(booking):
    """Send booking cancellation email to client."""
    subject = _("Booking Cancelled - {0}").format(booking.booking_number)
    context = {
        "booking": booking,
        "site_name": settings.SITE_NAME,
    }

    html_message = render_to_string(
        "bookings/email/booking_cancelled.html",
        context,
    )
    text_message = render_to_string(
        "bookings/email/booking_cancelled.txt",
        context,
    )

    send_mail(
        subject=subject,
        message=text_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.client.email],
        fail_silently=False,
    )


def send_payment_confirmation(payment):
    """Send payment confirmation email to client."""
    subject = _("Payment Confirmation - {0}").format(payment.booking.booking_number)
    context = {
        "payment": payment,
        "booking": payment.booking,
        "site_name": settings.SITE_NAME,
    }

    html_message = render_to_string(
        "bookings/email/payment_confirmation.html",
        context,
    )
    text_message = render_to_string(
        "bookings/email/payment_confirmation.txt",
        context,
    )

    send_mail(
        subject=subject,
        message=text_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[payment.booking.client.email],
        fail_silently=False,
    )


def send_reminder_email(booking):
    """Send reminder email 24 hours before the booking."""
    subject = _("Reminder: Your Wellness Session Tomorrow - {0}").format(
        booking.booking_number,
    )
    context = {
        "booking": booking,
        "site_name": settings.SITE_NAME,
    }

    html_message = render_to_string(
        "bookings/email/booking_reminder.html",
        context,
    )
    text_message = render_to_string(
        "bookings/email/booking_reminder.txt",
        context,
    )

    send_mail(
        subject=subject,
        message=text_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.client.email],
        fail_silently=False,
    )
