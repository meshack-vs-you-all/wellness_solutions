"""
Management command to test the booking system.
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from bookings.models import Booking, BookingPackage, BookingStatus
from locations.models import Location, LocationInstructor, LocationService
from services.models import Service, ServicePackage
from wellness_instructors.models import Instructor


User = get_user_model()

class Command(BaseCommand):
    help = "Test the booking system by creating test data and making bookings"

    def handle(self, *args, **options):
        try:
            # 1. Create test service
            service, created = Service.objects.get_or_create(
                name="Test Stretch Service",
                defaults={
                    "description": "Test service for booking system",
                    "duration": 60,
                    "price": Decimal("100.00"),
                    "home_visit_surcharge": Decimal("20.00"),
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} service: {service.name}')

            # 2. Create test location
            location, created = Location.objects.get_or_create(
                name="Test Location",
                defaults={
                    "address": "123 Test St",
                    "city": "Test City",
                    "state": "TS",
                    "zip_code": "12345",
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} location: {location.name}')

            # 3. Create location service
            location_service, created = LocationService.objects.get_or_create(
                location=location,
                service=service,
                defaults={
                    "price_adjustment": Decimal("0.00"),
                    "is_available": True,
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} location service')

            # 4. Create test instructor
            instructor_user, created = User.objects.get_or_create(
                username="testinstructor",
                defaults={
                    "email": "instructor@test.com",
                    "first_name": "Test",
                    "last_name": "Instructor",
                    "is_active": True,
                },
            )
            instructor, created = Instructor.objects.get_or_create(
                user=instructor_user,
                defaults={
                    "bio": "Test instructor bio",
                    "phone": "1234567890",
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} instructor: {instructor.user.get_full_name()}')

            # 5. Create location instructor
            location_instructor, created = LocationInstructor.objects.get_or_create(
                location=location,
                instructor=instructor,
                defaults={
                    "is_available": True,
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} location instructor')

            # 6. Create service package
            service_package, created = ServicePackage.objects.get_or_create(
                name="Test Package",
                defaults={
                    "service": service,
                    "sessions": 10,
                    "price_per_session": Decimal("80.00"),
                    "validity_days": 90,
                    "discount_percentage": Decimal("20.00"),
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} service package: {service_package.name}')

            # 7. Create test client
            client_user, created = User.objects.get_or_create(
                username="testclient",
                defaults={
                    "email": "client@test.com",
                    "first_name": "Test",
                    "last_name": "Client",
                    "is_active": True,
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} client: {client_user.get_full_name()}')

            # 8. Create booking package
            booking_package, created = BookingPackage.objects.get_or_create(
                name="Test Booking Package",
                defaults={
                    "owner": client_user,
                    "service": location_service,
                    "service_package": service_package,
                    "total_sessions": service_package.sessions,
                    "price_per_session": service_package.price_per_session,
                    "total_price": service_package.price_per_session * service_package.sessions,
                    "expiry_date": timezone.now().date() + timedelta(days=90),
                    "active": True,
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} booking package: {booking_package.name}')

            # 9. Create test booking
            start_time = timezone.now().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=1)
            booking, created = Booking.objects.get_or_create(
                client=client_user,
                service=location_service,
                instructor=location_instructor,
                start_time=start_time,
                defaults={
                    "location": location,
                    "package": booking_package,
                    "status": BookingStatus.CONFIRMED,
                    "booking_type": "individual",
                    "end_time": start_time + timedelta(minutes=60),
                    "notes": "Test booking",
                },
            )
            self.stdout.write(f'{"Created" if created else "Found"} booking for tomorrow at 2 PM')

            # 10. Test package validation
            remaining_sessions = booking_package.sessions_remaining()
            is_valid = booking_package.is_valid()
            self.stdout.write(f"Package has {remaining_sessions} sessions remaining")
            self.stdout.write(f'Package is {"valid" if is_valid else "invalid"}')

            self.stdout.write(self.style.SUCCESS("Successfully tested booking system"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
