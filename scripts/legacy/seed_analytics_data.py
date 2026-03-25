import os
import django
import random
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from bookings.models import Booking, BookingStatus, PaymentStatus
from wellness_instructors.models import WellnessInstructor
from locations.models import Location, LocationInstructor, LocationService
from services.models import Service, ServiceCategory

def seed_dense_history():
    print("📊 Seeding High-Density Historical Data for Analytics...")
    
    # Setup core objects
    category, _ = ServiceCategory.objects.get_or_create(name="Individual Stretch", defaults={"type": "individual"})
    location, _ = Location.objects.get_or_create(name="Main Studio", defaults={"capacity": 10, "type": "studio"})
    service, _ = Service.objects.get_or_create(name="Full Body Stretch", defaults={"category": category, "duration": 60, "price": 85.00})
    
    # Instructor
    steve_user = User.objects.get(email="steve@jpf.com")
    instructor, _ = WellnessInstructor.objects.get_or_create(user=steve_user)
    loc_inst, _ = LocationInstructor.objects.get_or_create(location=location, instructor=instructor)
    loc_service, _ = LocationService.objects.get_or_create(location=location, service=service)

    # 1. Backdate User Registrations (for Growth Charts)
    users = User.objects.exclude(is_staff=True)
    for i, user in enumerate(users):
        user.date_joined = timezone.now() - timedelta(days=random.randint(5, 60))
        user.save()

    # 2. Generate 8 Weeks of Historical Bookings
    print("📅 Generating 30+ historical bookings...")
    booking_count = 0
    for weeks_back in range(1, 9):
        for day in range(0, 5): # Mon-Fri
            # Select a random client for this slot
            client = random.choice(users)
            start_time = (timezone.now() - timedelta(weeks=weeks_back)).replace(hour=9+day, minute=0, second=0)
            
            # Create a COMPLETED booking
            Booking.objects.get_or_create(
                booking_number=f"HIST-{weeks_back}-{day}-{booking_count}",
                defaults={
                    "client": client,
                    "location": location,
                    "service": loc_service,
                    "instructor": loc_inst,
                    "start_time": start_time,
                    "end_time": start_time + timedelta(hours=1),
                    "status": BookingStatus.COMPLETED,
                    "payment_status": PaymentStatus.PAID,
                    "base_price": 85,
                    "total_price": 85,
                    "created_at": start_time - timedelta(days=2)
                }
            )
            booking_count += 1

    # 3. Add some CANCELLED sessions (for realistic analytics)
    for i in range(5):
        client = random.choice(users)
        cancel_date = timezone.now() - timedelta(days=i*2)
        Booking.objects.get_or_create(
            booking_number=f"CANC-{i}",
            defaults={
                "client": client,
                "location": location,
                "service": loc_service,
                "instructor": loc_inst,
                "start_time": cancel_date,
                "end_time": cancel_date + timedelta(hours=1),
                "status": BookingStatus.CANCELLED,
                "payment_status": PaymentStatus.PENDING,
                "base_price": 85,
                "total_price": 85
            }
        )

    print(f"✅ Success: Generated {booking_count} historical records and realistic user growth data.")

if __name__ == "__main__":
    seed_dense_history()
