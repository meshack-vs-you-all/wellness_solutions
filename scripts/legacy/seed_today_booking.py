import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from bookings.models import Booking, BookingStatus, PaymentStatus
from schedules.models import TimeSlot
from django.contrib.auth import get_user_model

User = get_user_model()

def seed_today():
    print("Seeding a booking for today...")
    steve = User.objects.get(email="steve@jpf.com").wellness_instructor
    david = User.objects.get(email="david@jpf.com")
    
    # Find a slot for today that is still in the future
    now = timezone.now()
    slot = TimeSlot.objects.filter(
        schedule__instructor=steve,
        start_datetime__gt=now,
        start_datetime__date=now.date(),
        status="available"
    ).first()
    
    if not slot:
        # If no slot today (maybe it's late in the day), find tomorrow
        slot = TimeSlot.objects.filter(
            schedule__instructor=steve,
            start_datetime__gt=now,
            status="available"
        ).first()

    if slot:
        from locations.models import LocationInstructor, LocationService
        loc_inst = LocationInstructor.objects.get(instructor=steve)
        loc_srv = LocationService.objects.first()
        
        Booking.objects.get_or_create(
            booking_number="DEMO-TODAY",
            defaults={
                "client": david,
                "location": loc_inst.location,
                "service": loc_srv,
                "instructor": loc_inst,
                "start_time": slot.start_datetime,
                "end_time": slot.end_datetime,
                "status": BookingStatus.CONFIRMED,
                "payment_status": PaymentStatus.PAID,
                "base_price": 85,
                "total_price": 85
            }
        )
        slot.status = "booked"
        slot.save()
        print(f"Created booking for David at {slot.start_datetime}")
    else:
        print("No slots available to book.")

if __name__ == "__main__":
    seed_today()
