from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from wellness_solutions.bookings.models import Booking
from wellness_solutions.instructors.models import Instructor, LocationInstructor
from wellness_solutions.locations.models import Location
from wellness_solutions.schedules.models import Schedule, TimeSlot
from wellness_solutions.services.models import LocationService, Service


User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with sample data for testing"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database with sample data...")

        # Create test users
        self.stdout.write("Creating users...")
        admin_user, created = User.objects.get_or_create(
            email="admin@jpfstretch.com",
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin user: {admin_user.email}"))

        test_user, created = User.objects.get_or_create(
            email="john.doe@example.com",
            defaults={
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
            },
        )
        if created:
            test_user.set_password("testpass123")
            test_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created test user: {test_user.email}"))

        # Create locations
        self.stdout.write("Creating locations...")
        main_location, created = Location.objects.get_or_create(
            name="Wellness Solutions - Downtown",
            defaults={
                "address": "123 Main Street",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94102",
                "phone": "(415) 555-0100",
                "email": "downtown@jpfstretch.com",
                "description": "Our flagship location in the heart of downtown.",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created location: {main_location.name}"))

        north_location, created = Location.objects.get_or_create(
            name="Wellness Solutions - North Beach",
            defaults={
                "address": "456 Beach Road",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94133",
                "phone": "(415) 555-0200",
                "email": "northbeach@jpfstretch.com",
                "description": "Convenient location serving North Beach area.",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created location: {north_location.name}"))

        # Create services
        self.stdout.write("Creating services...")
        services_data = [
            {
                "name": "Deep Tissue Stretch",
                "description": "Intensive wellness session focusing on deep muscle groups",
                "duration": 60,
                "default_price": 120.00,
            },
            {
                "name": "Recovery Stretch",
                "description": "Gentle stretching ideal for post-workout recovery",
                "duration": 45,
                "default_price": 90.00,
            },
            {
                "name": "Flexibility Training",
                "description": "Progressive flexibility improvement program",
                "duration": 60,
                "default_price": 110.00,
            },
            {
                "name": "Sports Stretch",
                "description": "Sport-specific stretching for athletes",
                "duration": 75,
                "default_price": 140.00,
            },
            {
                "name": "Express Stretch",
                "description": "Quick targeted wellness session",
                "duration": 30,
                "default_price": 60.00,
            },
        ]

        services = []
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data["name"],
                defaults={
                    "description": service_data["description"],
                    "duration": service_data["duration"],
                    "default_price": service_data["default_price"],
                    "is_active": True,
                },
            )
            services.append(service)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created service: {service.name}"))

        # Link services to locations
        self.stdout.write("Linking services to locations...")
        for location in [main_location, north_location]:
            for service in services:
                loc_service, created = LocationService.objects.get_or_create(
                    location=location,
                    service=service,
                    defaults={
                        "price": service.default_price,
                        "is_available": True,
                    },
                )
                if created:
                    self.stdout.write(f"  - Linked {service.name} to {location.name}")

        # Create instructors
        self.stdout.write("Creating instructors...")
        instructors_data = [
            {
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.j@jpfstretch.com",
                "phone": "(415) 555-1001",
                "bio": "Certified wellness practitioner with 8 years of experience.",
                "specialization": "Deep tissue and sports stretching",
            },
            {
                "first_name": "Mike",
                "last_name": "Chen",
                "email": "mike.c@jpfstretch.com",
                "phone": "(415) 555-1002",
                "bio": "Former professional athlete specializing in recovery techniques.",
                "specialization": "Recovery and rehabilitation stretching",
            },
            {
                "first_name": "Emily",
                "last_name": "Rodriguez",
                "email": "emily.r@jpfstretch.com",
                "phone": "(415) 555-1003",
                "bio": "Yoga instructor and flexibility coach.",
                "specialization": "Flexibility training and yoga-based stretching",
            },
            {
                "first_name": "David",
                "last_name": "Thompson",
                "email": "david.t@jpfstretch.com",
                "phone": "(415) 555-1004",
                "bio": "Physical therapist with focus on injury prevention.",
                "specialization": "Therapeutic and corrective stretching",
            },
        ]

        instructors = []
        for instructor_data in instructors_data:
            instructor, created = Instructor.objects.get_or_create(
                email=instructor_data["email"],
                defaults={
                    "first_name": instructor_data["first_name"],
                    "last_name": instructor_data["last_name"],
                    "phone": instructor_data["phone"],
                    "bio": instructor_data["bio"],
                    "specialization": instructor_data["specialization"],
                    "is_active": True,
                },
            )
            instructors.append(instructor)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created instructor: {instructor.first_name} {instructor.last_name}"))

        # Link instructors to locations
        self.stdout.write("Linking instructors to locations...")
        # Main location gets all instructors
        for instructor in instructors:
            loc_instructor, created = LocationInstructor.objects.get_or_create(
                location=main_location,
                instructor=instructor,
                defaults={"is_available": True},
            )
            if created:
                self.stdout.write(f"  - Linked {instructor.first_name} to {main_location.name}")

        # North location gets first two instructors
        for instructor in instructors[:2]:
            loc_instructor, created = LocationInstructor.objects.get_or_create(
                location=north_location,
                instructor=instructor,
                defaults={"is_available": True},
            )
            if created:
                self.stdout.write(f"  - Linked {instructor.first_name} to {north_location.name}")

        # Create schedules and time slots
        self.stdout.write("Creating schedules and time slots...")
        today = timezone.now().date()

        # Create schedules for the next 7 days
        for days_ahead in range(7):
            schedule_date = today + timedelta(days=days_ahead)

            for location in [main_location, north_location]:
                schedule, created = Schedule.objects.get_or_create(
                    location=location,
                    date=schedule_date,
                    defaults={"is_active": True},
                )

                if created:
                    self.stdout.write(f"Created schedule for {location.name} on {schedule_date}")

                    # Create time slots for each schedule (9 AM to 6 PM)
                    slot_times = [
                        ("09:00", "10:00"),
                        ("10:00", "11:00"),
                        ("11:00", "12:00"),
                        ("12:00", "13:00"),
                        ("14:00", "15:00"),
                        ("15:00", "16:00"),
                        ("16:00", "17:00"),
                        ("17:00", "18:00"),
                    ]

                    # Get location services and instructors
                    loc_services = LocationService.objects.filter(location=location, is_available=True)
                    loc_instructors = LocationInstructor.objects.filter(location=location, is_available=True)

                    for i, (start_time, end_time) in enumerate(slot_times):
                        # Skip weekends for some slots
                        if schedule_date.weekday() in [5, 6] and i > 3:  # Saturday, Sunday - fewer slots
                            continue

                        # Rotate through services and instructors
                        loc_service = loc_services[i % len(loc_services)] if loc_services else None
                        loc_instructor = loc_instructors[i % len(loc_instructors)] if loc_instructors else None

                        if loc_service and loc_instructor:
                            time_slot = TimeSlot.objects.create(
                                schedule=schedule,
                                start_time=start_time,
                                end_time=end_time,
                                location_service=loc_service,
                                location_instructor=loc_instructor,
                                max_capacity=1,  # One-on-one sessions
                                is_available=True,
                            )
                            self.stdout.write(f"    - Created slot: {start_time}-{end_time}")

        # Create a few sample bookings
        self.stdout.write("Creating sample bookings...")
        upcoming_slots = TimeSlot.objects.filter(
            schedule__date__gte=today,
            is_available=True,
        )[:3]

        for i, slot in enumerate(upcoming_slots):
            booking = Booking.objects.create(
                user=test_user,
                time_slot=slot,
                location_service=slot.location_service,
                location_instructor=slot.location_instructor,
                location=slot.schedule.location,
                booking_date=slot.schedule.date,
                start_time=slot.start_time,
                end_time=slot.end_time,
                status="confirmed" if i == 0 else "pending",
                notes=f"Sample booking {i+1}",
                price=slot.location_service.price if slot.location_service else 100.00,
            )
            # Mark slot as unavailable after booking
            slot.is_available = False
            slot.save()
            self.stdout.write(self.style.SUCCESS(f"Created booking for {test_user.email} on {booking.booking_date}"))

        self.stdout.write(self.style.SUCCESS("\n✅ Database seeded successfully!"))
        self.stdout.write("\nYou can now login with:")
        self.stdout.write("  Admin: admin@jpfstretch.com / admin123")
        self.stdout.write("  User: john.doe@example.com / testpass123")
