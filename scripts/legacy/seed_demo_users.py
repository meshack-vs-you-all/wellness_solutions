import os
import django
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

User = get_user_model()
from bookings.models import Booking, BookingStatus, PaymentStatus
from wellness_instructors.models import WellnessInstructor
from locations.models import Location, LocationInstructor, LocationService
from services.models import Service, ServiceCategory

def seed_demo():
    print("🚀 Starting Advanced Demo Seeding...")
    
    # 1. Setup Categories and Locations
    category, _ = ServiceCategory.objects.get_or_create(
        name="Individual Stretch", 
        defaults={"description": "One-on-one sessions", "type": "individual"}
    )
    
    operating_hours = {day: {"open": "08:00", "close": "20:00"} for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
    contact_info = {"phone": "+1234567890", "email": "studio@jpf.com"}
    
    location, _ = Location.objects.get_or_create(
        name="Main Studio", 
        defaults={
            "address": "123 Wellness Way",
            "type": "studio",
            "capacity": 10,
            "status": "active",
            "operating_hours": operating_hours,
            "contact_info": contact_info
        }
    )
    
    service_obj, _ = Service.objects.get_or_create(
        name="Full Body Stretch", 
        defaults={
            "category": category,
            "description": "Standard 60min session",
            "duration": 60,
            "price": 85.00
        }
    )
    
    # 2. Define the 9 Personas
    personas = [
        {"email": "alex@jpf.com", "name": "Admin Alex", "role": "admin", "is_staff": True},
        {"email": "steve@jpf.com", "name": "Staff Steve", "role": "instructor", "is_staff": True},
        {"email": "sarah@jpf.com", "name": "Sarah Swift", "role": "member", "is_staff": False},
        {"email": "david@jpf.com", "name": "David Desk", "role": "member", "is_staff": False},
        {"email": "elena@jpf.com", "name": "Elena Exec", "role": "member", "is_staff": False},
        {"email": "marcus@jpf.com", "name": "Marcus Medic", "role": "member", "is_staff": False},
        {"email": "chloe@jpf.com", "name": "Chloe Core", "role": "member", "is_staff": False},
        {"email": "james@jpf.com", "name": "James Joy", "role": "member", "is_staff": False},
        {"email": "tom@jpf.com", "name": "Tom Tracker", "role": "member", "is_staff": False},
    ]

    created_users = {}

    for p in personas:
        name_parts = p["name"].split(" ")
        user, created = User.objects.get_or_create(
            email=p["email"],
            defaults={
                "first_name": name_parts[0],
                "last_name": name_parts[1] if len(name_parts) > 1 else "",
                "is_staff": p["is_staff"],
                "is_superuser": p["role"] == "admin"
            }
        )
        user.set_password("demo123")
        user.save()
        created_users[p["email"]] = user
        status = "[CREATED]" if created else "[UPDATED]"
        print(f"{status} {p['name']} ({p['email']})")

    # 3. Setup Instructor Profile for Steve
    instructor_profile, _ = WellnessInstructor.objects.get_or_create(
        user=created_users["steve@jpf.com"],
        defaults={"bio": "Senior Therapist", "specializations": "general"}
    )
    
    # Link instructor to location
    loc_inst, _ = LocationInstructor.objects.get_or_create(
        location=location,
        instructor=instructor_profile,
        defaults={"status": "active"}
    )
    
    # Setup Location Service
    loc_service, _ = LocationService.objects.get_or_create(
        location=location,
        service=service_obj,
        defaults={"price_adjustment": 0}
    )

    # 4. Generate History for David (Smart Rebook Demo)
    david = created_users["david@jpf.com"]
    print("📅 Generating history for David Desk...")
    for i in range(1, 5):
        past_date = timezone.now() - timedelta(weeks=i)
        days_to_monday = past_date.weekday()
        target_date = (past_date - timedelta(days=days_to_monday)).replace(hour=10, minute=0, second=0)
        
        Booking.objects.get_or_create(
            booking_number=f"HIST-D-{i}",
            defaults={
                "client": david,
                "location": location,
                "service": loc_service,
                "instructor": loc_inst,
                "start_time": target_date,
                "end_time": target_date + timedelta(hours=1),
                "status": BookingStatus.COMPLETED,
                "payment_status": PaymentStatus.PAID,
                "base_price": 85,
                "total_price": 85
            }
        )

    # 5. Generate Upcoming for Elena (Cancellation Demo)
    print("📅 Generating upcoming session for Elena Exec...")
    elena = created_users["elena@jpf.com"]
    future_date = timezone.now() + timedelta(days=2)
    Booking.objects.get_or_create(
        booking_number="UP-ELENA-1",
        defaults={
            "client": elena,
            "location": location,
            "service": loc_service,
            "instructor": loc_inst,
            "start_time": future_date,
            "end_time": future_date + timedelta(hours=1),
            "status": BookingStatus.CONFIRMED,
            "payment_status": PaymentStatus.PENDING,
            "base_price": 85,
            "total_price": 85
        }
    )

    print("✅ Seeding Complete. 9 Personas Ready.")

if __name__ == "__main__":
    seed_demo()
