import os
import django
import random
import sys
from pathlib import Path
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Load .env file
try:
    import environ
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
except ImportError:
    pass

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from bookings.models import Booking, BookingStatus, PaymentStatus
from wellness_instructors.models import WellnessInstructor
from locations.models import Location, LocationInstructor, LocationService
from services.models import Service, ServiceCategory, ServicePackage
from schedules.models import Schedule, TimeSlot

def seed_all():
    print("🚀 Starting Comprehensive Database Seeding...")
    
    # 1. Setup Categories and Locations
    individual_cat, _ = ServiceCategory.objects.get_or_create(
        name="Individual Stretch", 
        defaults={"description": "One-on-one sessions", "type": "individual"}
    )
    corporate_cat, _ = ServiceCategory.objects.get_or_create(
        name="Corporate Wellness",
        defaults={"description": "For teams and businesses", "type": "corporate"}
    )
    
    operating_hours = {day: {"open": "08:00", "close": "20:00"} for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
    contact_info = {"phone": "+254701810285", "email": "studio@jpf.com"}
    
    location, _ = Location.objects.get_or_create(
        name="Main Studio", 
        defaults={
            "address": "5th Floor Western Heights, Karuna Road, Westlands, Nairobi",
            "type": "studio",
            "capacity": 10,
            "status": "active",
            "operating_hours": operating_hours,
            "contact_info": contact_info
        }
    )

    # 2. Seed Services from Wellness Solutions Kenya Ltd Profile
    print("📋 Seeding Services from Company Profile...")
    wsk_services = [
        {"name": "Full Body Stretch", "cat": individual_cat, "price": 85.00, "duration": 60, "desc": "Standard 60min assisted wellness session."},
        {"name": "Postural Analysis", "cat": individual_cat, "price": 50.00, "duration": 30, "desc": "Detailed assessment of body alignment to identify imbalances."},
        {"name": "Foot Pressure Analysis", "cat": individual_cat, "price": 50.00, "duration": 30, "desc": "Scientific analysis of weight distribution and gait."},
        {"name": "Ergonomics Assessments", "cat": corporate_cat, "price": 150.00, "duration": 60, "desc": "Optimizing workspaces for health and productivity."},
        {"name": "Corrective Exercise Therapy", "cat": individual_cat, "price": 95.00, "duration": 60, "desc": "Targeted movements to restore functional mobility."},
        {"name": "Nutritional Guidance", "cat": individual_cat, "price": 70.00, "duration": 45, "desc": "Science-based approaches to fuel vitality and health."},
        {"name": "Injury Prevention Workshops", "cat": corporate_cat, "price": 300.00, "duration": 120, "desc": "Educational sessions to reduce physical risks."},
    ]

    service_objs = []
    for s in wsk_services:
        obj, created = Service.objects.get_or_create(
            name=s["name"],
            defaults={
                "category": s["cat"],
                "description": s["desc"],
                "duration": s["duration"],
                "price": s["price"]
            }
        )
        service_objs.append(obj)
        # Ensure LocationService mapping
        LocationService.objects.get_or_create(location=location, service=obj, defaults={"price_adjustment": 0})
        if created: print(f"  [CREATED] Service: {s['name']}")

    # 3. Create Personas
    print("👥 Seeding Demo Personas...")
    personas = [
        {"email": "alex@jpf.com", "name": "Admin Alex", "role": "admin", "is_staff": True},
        {"email": "steve@jpf.com", "name": "Staff Steve", "role": "instructor", "is_staff": True},
        {"email": "sarah@jpf.com", "name": "Sarah Swift", "role": "member", "is_staff": False},
        {"email": "david@jpf.com", "name": "David Desk", "role": "member", "is_staff": False},
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
        if created: print(f"  [CREATED] User: {p['name']}")

    # 4. Setup Instructor Profile
    steve_instructor, _ = WellnessInstructor.objects.get_or_create(
        user=created_users["steve@jpf.com"],
        defaults={"bio": "Senior Therapist", "specializations": "general", "is_available": True}
    )
    loc_inst, _ = LocationInstructor.objects.get_or_create(location=location, instructor=steve_instructor, defaults={"status": "active"})

    # 5. Seed Schedules and Time Slots
    print("📅 Seeding Schedules and Availability...")
    schedule, _ = Schedule.objects.get_or_create(
        instructor=steve_instructor,
        weekday=timezone.now().weekday(),
        defaults={"start_time": "09:00", "end_time": "17:00", "is_active": True}
    )
    
    for day_offset in range(7):
        target_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=day_offset)
        for hour in [9, 10, 11, 13, 14, 15, 16]:
            start = target_date.replace(hour=hour)
            if start < timezone.now(): continue
            TimeSlot.objects.get_or_create(
                schedule=schedule,
                start_datetime=start,
                end_datetime=start + timedelta(hours=1),
                defaults={"status": "available"}
            )

    # 6. Seed Historical Data for Analytics
    print("📊 Seeding Analytics Data...")
    users = [u for u in created_users.values() if not u.is_staff]
    full_body_service = Service.objects.get(name="Full Body Stretch")
    loc_service = LocationService.objects.get(location=location, service=full_body_service)
    
    for weeks_back in range(1, 5):
        for day in range(0, 3):
            client = random.choice(users)
            start_time = (timezone.now() - timedelta(weeks=weeks_back)).replace(hour=9+day, minute=0, second=0)
            Booking.objects.get_or_create(
                booking_number=f"HIST-{weeks_back}-{day}",
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

    # 7. Seed Packages
    print("🛒 Seeding Wellness Packages...")
    packages = [
        {"name": "5-Session Recovery Pack", "sessions": 5, "discount": 10.00},
        {"name": "10-Session Performance Pack", "sessions": 10, "discount": 20.00},
    ]
    for p in packages:
        ServicePackage.objects.get_or_create(
            name=p["name"],
            defaults={
                "service": full_body_service,
                "sessions": p["sessions"],
                "discount_percentage": Decimal(str(p["discount"])),
                "price_per_session": full_body_service.price * (1 - Decimal(str(p["discount"])) / 100),
                "validity_days": 90
            }
        )

    print("✅ Seeding Complete!")

if __name__ == "__main__":
    seed_all()
