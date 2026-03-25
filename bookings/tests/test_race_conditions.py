"""
Tests for race conditions and concurrency issues in bookings.
"""
import threading
from datetime import timedelta

import pytest
from django.db import transaction
from django.utils import timezone

from bookings.models import Booking, BookingStatus
from bookings.validators import validate_instructor_availability
from locations.models import Location, LocationInstructor, LocationService
from services.models import Organization, Service
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestDoubleBookingRaceCondition:
    """Test that double bookings are prevented even under concurrent requests."""

    def test_concurrent_booking_creation(self):
        """Test that two concurrent booking requests cannot create overlapping bookings."""
        # Setup
        user1 = UserFactory()
        user2 = UserFactory()
        org = Organization.objects.create(name="Test Org")
        location = Location.objects.create(name="Test Location", organization=org)
        service = Service.objects.create(name="Test Service", organization=org)
        location_service = LocationService.objects.create(
            location=location,
            service=service,
            price=100,
            duration=60,
        )
        instructor_user = UserFactory()
        location_instructor = LocationInstructor.objects.create(
            location=location,
            user=instructor_user,
            is_active=True,
        )

        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time + timedelta(minutes=60)

        # Create bookings concurrently
        results = []
        errors = []

        def create_booking(user):
            try:
                with transaction.atomic():
                    # Check availability
                    validate_instructor_availability(
                        location_instructor,
                        start_time,
                        location_service,
                    )
                    # Create booking
                    booking = Booking.objects.create(
                        client=user,
                        location=location,
                        service=location_service,
                        instructor=location_instructor,
                        start_time=start_time,
                        end_time=end_time,
                        status=BookingStatus.CONFIRMED,
                        base_price=100,
                        total_price=100,
                        payment_status="pending",
                    )
                    results.append(booking)
            except Exception as e:
                errors.append(str(e))

        # Launch two threads simultaneously
        thread1 = threading.Thread(target=create_booking, args=(user1,))
        thread2 = threading.Thread(target=create_booking, args=(user2,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Only one booking should succeed
        assert len(results) == 1, f"Expected 1 booking, got {len(results)}. Errors: {errors}"
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}. Results: {results}"


@pytest.mark.django_db
class TestPaymentIdempotency:
    """Test that duplicate payment processing is prevented."""

    def test_duplicate_transaction_id(self):
        """Test that the same transaction_id cannot be processed twice."""
        from bookings.models import BookingPayment, PaymentStatus

        user = UserFactory()
        org = Organization.objects.create(name="Test Org")
        location = Location.objects.create(name="Test Location", organization=org)
        service = Service.objects.create(name="Test Service", organization=org)
        location_service = LocationService.objects.create(
            location=location,
            service=service,
            price=100,
            duration=60,
        )
        instructor_user = UserFactory()
        location_instructor = LocationInstructor.objects.create(
            location=location,
            user=instructor_user,
            is_active=True,
        )

        booking = Booking.objects.create(
            client=user,
            location=location,
            service=location_service,
            instructor=location_instructor,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            status=BookingStatus.CONFIRMED,
            base_price=100,
            total_price=100,
            payment_status="pending",
        )

        transaction_id = "TEST_TXN_12345"

        # Create first payment
        payment1 = BookingPayment.objects.create(
            booking=booking,
            amount=100,
            payment_method="credit_card",
            transaction_id=transaction_id,
            status=PaymentStatus.PAID,
            payer=user,
        )

        # Attempt to create duplicate payment
        with pytest.raises(Exception):  # Should raise IntegrityError
            BookingPayment.objects.create(
                booking=booking,
                amount=100,
                payment_method="credit_card",
                transaction_id=transaction_id,
                status=PaymentStatus.PAID,
                payer=user,
            )

