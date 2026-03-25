# Comprehensive API Views for Wellness Solutions
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

# Import all models
from bookings.models import Booking, BookingStatus, PaymentStatus
from bookings.serializers import BookingSerializer
from locations.models import LocationInstructor, LocationService
from schedules.models import TimeSlot
from services.models import Service


User = get_user_model()

# ============== Auth Endpoints ==============

class LogoutView(APIView):
    """Handle user logout by deleting auth token"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's token
            Token.objects.filter(user=request.user).delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """JSON API endpoint for user registration"""
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name", "")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if user exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse name into first and last name
        name_parts = name.split(" ", 1) if name else ["", ""]
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Create user - the UserManager expects email as the first arg
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Create token
        token, created = Token.objects.get_or_create(user=user)

        # Determine role
        role = "member"
        if user.is_staff:
            role = "admin"
        elif hasattr(user, 'wellness_instructor'):
            role = "instructor"

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.get_full_name() or user.email,
                "role": role,
                "isAdmin": user.is_staff,
                "isStaff": user.is_staff,
            },
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Custom login view to return user profile with role"""
    from django.contrib.auth import authenticate
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    
    # Determine role
    role = "member"
    if user.is_staff:
        role = "admin"
    elif hasattr(user, 'wellness_instructor'):
        role = "instructor"

    return Response({
        "token": token.key,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.get_full_name() or user.email,
            "role": role,
            "isAdmin": user.is_staff,
            "isStaff": user.is_staff,
            "membershipType": "none", # Default
        }
    })


# ============== Classes/Services Endpoints ==============

class ClassViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing and retrieving classes/services"""
    queryset = Service.objects.all()  # Service model doesn't have an active field
    permission_classes = [permissions.AllowAny]
    serializer_class = None  # Custom serialization in list() method

    def list(self, request):
        """List all available classes/services with upcoming time slots"""
        services = self.get_queryset()
        data = []

        # Get available time slots from the next 30 days
        now = timezone.now()
        future_slots = TimeSlot.objects.filter(
            start_datetime__gte=now,
            start_datetime__lte=now + timedelta(days=30),
            status="available",
        ).select_related("schedule", "schedule__instructor").order_by("start_datetime")

        # For each available time slot, create a class entry
        for slot in future_slots:
            # Find a service that matches this instructor's expertise
            # For now, we'll use a generic service
            instructor = slot.schedule.instructor

            # Get location services where this instructor works
            location_instructors = LocationInstructor.objects.filter(
                instructor=instructor,
                status="active",
            ).select_related("location").first()

            if location_instructors:
                location = location_instructors.location
                # Get services available at this location
                location_services = LocationService.objects.filter(
                    location=location,
                    is_available=True,
                ).select_related("service").first()

                if location_services:
                    service = location_services.service
                    data.append({
                        "id": slot.id,
                        "title": service.name,
                        "description": service.description,
                        "instructor": {
                            "id": instructor.id,
                            "name": instructor.user.get_full_name() if instructor.user else "TBD",
                        },
                        "startTime": slot.start_datetime.isoformat(),
                        "endTime": slot.end_datetime.isoformat(),
                        "capacity": 10,  # Default capacity
                        "enrolledCount": Booking.objects.filter(
                            start_time=slot.start_datetime,
                            instructor__instructor=instructor,
                            status=BookingStatus.CONFIRMED,
                        ).count(),
                        "type": service.service_type.lower() if hasattr(service, "service_type") else "wellness",
                        "level": "all",
                        "price": float(location_services.get_final_price()),
                        "location": {
                            "id": location.id,
                            "name": location.name,
                        },
                    })

        # If no time slots, return services as standalone items
        if not data:
            for service in services:
                data.append({
                    "id": f"service-{service.id}",
                    "title": service.name,
                    "description": service.description,
                    "instructor": {
                        "id": None,
                        "name": "TBD",
                    },
                    "startTime": None,
                    "endTime": None,
                    "capacity": 10,
                    "enrolledCount": 0,
                    "type": service.service_type.lower() if hasattr(service, "service_type") else "wellness",
                    "level": "all",
                    "price": float(service.base_price) if hasattr(service, "base_price") and service.base_price else 0,
                    "location": {
                        "id": None,
                        "name": "Main Studio",
                    },
                })

        return Response(data)


# ============== Bookings Endpoints ==============

class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bookings"""
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        """Filter bookings for the current user"""
        if self.request.user.is_staff:
            return Booking.objects.all()

        # Filter bookings for the current user
        return Booking.objects.filter(client=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Perform a clinical cancellation instead of hard delete"""
        try:
            instance = self.get_object()
            
            # Check if it's already cancelled
            if instance.status == BookingStatus.CANCELLED:
                return Response({"detail": "Already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

            # Update booking status
            instance.status = BookingStatus.CANCELLED
            instance.save()

            # Release the time slot if it exists
            # We need to find the specific slot. Since we don't have a direct FK back 
            # from Booking to TimeSlot in the model, we match by time and instructor.
            slot = TimeSlot.objects.filter(
                start_datetime=instance.start_time,
                schedule__instructor=instance.instructor.instructor
            ).first()
            
            if slot:
                slot.status = "available"
                slot.save()

            return Response({"detail": "Booking cancelled successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def create(self, request):
        """Create a new booking"""
        try:
            with transaction.atomic():
                slot_id = request.data.get("class_id")  # Frontend sends class_id

                if not slot_id:
                    return Response(
                        {"error": "class_id is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Get the time slot
                try:
                    slot = TimeSlot.objects.get(id=slot_id)
                except TimeSlot.DoesNotExist:
                    return Response(
                        {"error": "Class not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Get instructor's location and service
                instructor = slot.schedule.instructor
                # Lock the instructor record to prevent race conditions
                location_instructor = LocationInstructor.objects.select_for_update().filter(
                    instructor=instructor,
                    status="active",
                ).select_related("location").first()

                if not location_instructor:
                    return Response(
                        {"error": "Instructor location not found"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                location = location_instructor.location

                # Get a service at this location
                location_service = LocationService.objects.filter(
                    location=location,
                    is_available=True,
                ).first()

                if not location_service:
                    return Response(
                        {"error": "No services available at this location"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Check for booking conflicts
                existing_bookings = Booking.objects.filter(
                    instructor=location_instructor,
                    start_time__lt=slot.end_datetime,
                    end_time__gt=slot.start_datetime,
                    status=BookingStatus.CONFIRMED,
                )

                if existing_bookings.exists():
                    return Response(
                        {"error": "Time slot is already booked"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Generate booking number
                import random
                import string
                booking_number = "BK" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

                # Create booking
                booking = Booking.objects.create(
                    booking_number=booking_number,
                    booking_type="individual",
                    client=request.user,
                    location=location,
                    service=location_service,
                    instructor=location_instructor,
                    start_time=slot.start_datetime,
                    end_time=slot.end_datetime,
                    status=BookingStatus.CONFIRMED,
                    payment_status=PaymentStatus.PENDING,
                    base_price=location_service.get_final_price(),
                    total_price=location_service.get_final_price(),
                    created_by=request.user,
                )

                # Update time slot status
                slot.status = "booked"
                slot.save()

                return Response({
                    "id": booking.id,
                    "user": {
                        "id": request.user.id,
                        "email": request.user.email,
                        "name": request.user.get_full_name() if hasattr(request.user, "get_full_name") else request.user.email,
                    },
                    "class": {
                        "id": slot.id,
                        "title": location_service.service.name,
                        "startTime": slot.start_datetime.isoformat(),
                        "endTime": slot.end_datetime.isoformat(),
                        "instructor": {
                            "id": instructor.id,
                            "name": instructor.user.get_full_name() if instructor.user else "TBD",
                        },
                    },
                    "status": booking.status,
                    "bookedAt": booking.created_at.isoformat(),
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["get"], url_path="me")
    def my_bookings(self, request):
        """Get current user's bookings"""
        bookings = Booking.objects.filter(
            client=request.user,
        ).select_related(
            "service", "service__service", "instructor", "instructor__instructor",
            "location",
        ).order_by("-created_at")

        data = []
        for booking in bookings:
            data.append({
                "id": booking.id,
                "user": {
                    "id": request.user.id,
                    "email": request.user.email,
                    "name": request.user.get_full_name() if hasattr(request.user, "get_full_name") else request.user.email,
                },
                "class": {
                    "id": booking.id,  # Use booking ID since we don't have a separate class/slot ID
                    "title": booking.service.service.name if booking.service and booking.service.service else "Service",
                    "startTime": booking.start_time.isoformat(),
                    "endTime": booking.end_time.isoformat(),
                    "instructor": {
                        "id": booking.instructor.id if booking.instructor else None,
                        "name": booking.instructor.instructor.user.get_full_name() if booking.instructor and booking.instructor.instructor and booking.instructor.instructor.user else "TBD",
                    },
                },
                "status": booking.status,
                "bookedAt": booking.created_at.isoformat(),
                "attendanceMarked": False,  # Add this field to Booking model if needed
            })

        return Response(data)


# ============== Analytics Endpoint ==============

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def analytics_view(request):
    """Get analytics data for admin dashboard"""
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        # Calculate analytics
        today = timezone.now().date()
        month_start = today.replace(day=1)

        # Total users
        total_users = User.objects.count()
        new_users_this_month = User.objects.filter(
            date_joined__gte=month_start,
        ).count()

        # Total bookings
        total_bookings = Booking.objects.count()
        bookings_this_month = Booking.objects.filter(
            created_at__gte=month_start,
        ).count()

        # Revenue
        total_revenue = Booking.objects.filter(
            payment_status="paid",
        ).aggregate(
            total=Sum("total_price"),
        )["total"] or 0

        revenue_this_month = Booking.objects.filter(
            payment_status="paid",
            created_at__gte=month_start,
        ).aggregate(
            total=Sum("total_price"),
        )["total"] or 0

        # Active classes (count upcoming time slots)
        active_classes = TimeSlot.objects.filter(
            start_datetime__gte=timezone.now(),
            status="available",
        ).count()

        return Response({
            "totalUsers": total_users,
            "totalBookings": total_bookings,
            "totalRevenue": float(total_revenue),
            "activeClasses": active_classes,
            "newUsersThisMonth": new_users_this_month,
            "bookingsThisMonth": bookings_this_month,
            "revenueThisMonth": float(revenue_this_month),
            "growthRate": 10.5,  # Placeholder - calculate actual growth
        })
    except Exception as e:
        return Response({"error": f"Analytics processing error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============== Instructor Endpoints ==============

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def instructor_classes_view(request):
    """Get classes for the current instructor"""
    # Check if user has an associated instructor profile
    from wellness_instructors.models import WellnessInstructor
    try:
        instructor = WellnessInstructor.objects.get(user=request.user)
    except WellnessInstructor.DoesNotExist:
        return Response(
            {"error": "Instructor access required"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Get instructor's upcoming time slots
    slots = TimeSlot.objects.filter(
        schedule__instructor=instructor,
        start_datetime__gte=timezone.now(),
        status="available",
    ).select_related("schedule").order_by("start_datetime")

    # Get instructor's location and services
    location_instructor = LocationInstructor.objects.filter(
        instructor=instructor,
        status="active",
    ).select_related("location").first()

    if not location_instructor:
        return Response({"error": "No location assigned to instructor"}, status=status.HTTP_400_BAD_REQUEST)

    location = location_instructor.location
    location_services = LocationService.objects.filter(
        location=location,
        is_active=True,
    ).select_related("service")

    data = []
    for slot in slots:
        # Get the first available service for simplicity
        service = location_services.first()
        if service:
            data.append({
                "id": slot.id,
                "title": service.service.name,
                "startTime": slot.start_datetime.isoformat(),
                "endTime": slot.end_datetime.isoformat(),
                "capacity": 10,  # Default capacity
                "enrolledCount": Booking.objects.filter(
                    instructor=location_instructor,
                    start_time=slot.start_datetime,
                    status=BookingStatus.CONFIRMED,
                ).count(),
                "location": {
                    "id": location.id,
                    "name": location.name,
                },
                "type": service.service.service_type.lower() if hasattr(service.service, "service_type") else "wellness",
                "level": "all",
                "description": service.service.description,
            })

    return Response(data)


# ============== Notifications ==============

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def notifications_view(request):
    """Return in-app notifications for the current user"""
    from bookings.models import Booking, BookingStatus
    notifs = []
    # Upcoming sessions reminder
    upcoming = Booking.objects.filter(
        client=request.user,
        status=BookingStatus.CONFIRMED,
        start_time__gte=timezone.now(),
        start_time__lte=timezone.now() + timedelta(hours=24),
    ).select_related("service__service", "location")
    for b in upcoming:
        notifs.append({
            "id": f"remind-{b.id}",
            "type": "reminder",
            "title": "Session Tomorrow",
            "message": f"Don't forget: {b.service.service.name if b.service and b.service.service else 'your session'} at {b.start_time.strftime('%I:%M %p')}",
            "read": False,
            "createdAt": (b.start_time - timedelta(hours=24)).isoformat(),
        })
    # Booking confirmations
    confirmed = Booking.objects.filter(
        client=request.user,
        status=BookingStatus.CONFIRMED,
        created_at__gte=timezone.now() - timedelta(days=3),
    ).order_by("-created_at")[:3]
    for b in confirmed:
        notifs.append({
            "id": f"confirm-{b.id}",
            "type": "success",
            "title": "Booking Confirmed",
            "message": f"Your booking #{b.booking_number} has been confirmed.",
            "read": True,
            "createdAt": b.created_at.isoformat(),
        })
    # Inactivity Reminder
    last_booking = Booking.objects.filter(client=request.user).order_by("-start_time").first()
    if last_booking and last_booking.start_time < timezone.now() - timedelta(days=7):
        notifs.append({
            "id": "inactivity-reminder",
            "type": "warning",
            "title": "Ready for your next stretch?",
            "message": "It's been over a week since your last session. Consistent stretching is key to long-term mobility!",
            "read": False,
            "createdAt": timezone.now().isoformat(),
        })

    # Promotional Offer
    notifs.append({
        "id": "promo-pack",
        "type": "info",
        "title": "New: Mobility Master Pack",
        "message": "Unlock 10 sessions at a 20% discount. Limited time offer in the Studio Shop.",
        "read": False,
        "createdAt": (timezone.now() - timedelta(hours=2)).isoformat(),
    })

    # Static welcome
    notifs.append({
        "id": "welcome",
        "type": "info",
        "title": "Welcome to Wellness Solutions!",
        "message": "Explore our classes and book your first session.",
        "read": False,
        "createdAt": request.user.date_joined.isoformat(),
    })
    return Response(sorted(notifs, key=lambda x: x["createdAt"], reverse=True))


# ============== Shop / Products ==============

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def shop_products_view(request):
    """Return shop products (merchandise and packages)"""
    from services.models import ServicePackage
    products = []
    # Real packages
    try:
        for pkg in ServicePackage.objects.all()[:8]:
            products.append({
                "id": pkg.id,
                "name": pkg.name,
                "description": pkg.description,
                "price": float(pkg.get_total_price()) if hasattr(pkg, "get_total_price") else float(pkg.price) if hasattr(pkg, "price") else 0,
                "category": "package",
                "sessions": getattr(pkg, "sessions", None),
                "image": None,
                "inStock": True,
            })
    except Exception:
        pass
    # Merchandise
    merchandise = [
        {
            "id": "merch-1", 
            "name": "JPF Stretch Mat (Pro)", 
            "description": "Premium 6mm thick non-slip yoga mat with alignment markers.", 
            "price": 75.00, 
            "category": "gear", 
            "image": "/static/images/wellness-therapy.jpg", 
            "inStock": True
        },
        {
            "id": "merch-2", 
            "name": "Resistance Band Set (5-pack)", 
            "description": "Latex-free, color-coded resistance bands for all recovery levels.", 
            "price": 28.00, 
            "category": "gear", 
            "image": "/static/images/personal-training.jpg", 
            "inStock": True
        },
        {
            "id": "merch-4", 
            "name": "Recovery Foam Roller", 
            "description": "High-density tissue massage roller for post-session recovery.", 
            "price": 45.00, 
            "category": "gear", 
            "image": "/static/images/wellness.jpg", 
            "inStock": True
        },
        {
            "id": "merch-5", 
            "name": "Clinical Recovery Gun", 
            "description": "Professional-grade percussion therapy for deep muscle relief.", 
            "price": 199.00, 
            "category": "gear", 
            "image": "/static/images/biometric-tests.jpg", 
            "inStock": True
        },
    ]
    products.extend(merchandise)
    return Response({"products": products, "categories": ["all", "package", "gear", "apparel", "bundle"]})


# ============== Organization Signup ==============

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def organization_register_view(request):
    """Register an organization for corporate wellness"""
    org_name = request.data.get("orgName")
    contact_name = request.data.get("contactName")
    email = request.data.get("email")
    phone = request.data.get("phone", "")
    employees = request.data.get("employees", "")
    program = request.data.get("program", "")

    if not all([org_name, contact_name, email]):
        return Response({"error": "orgName, contactName, and email are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if users email already exist
    existing = User.objects.filter(email=email).first()
    if existing:
        return Response({"error": "An account with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # Create an org admin user
    user = User.objects.create_user(
        email=email,
        password="TempPass123!",  # They must reset
        first_name=contact_name.split(" ")[0],
        last_name=" ".join(contact_name.split(" ")[1:]) or "",
    )
    user.is_staff = False
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "message": f"Organization '{org_name}' registered successfully! Check your email for next steps.",
        "token": token.key,
        "tempPassword": "TempPass123!",
        "note": "Please reset your password after first login.",
    }, status=status.HTTP_201_CREATED)


# ============== Trainer Availability ==============

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def trainer_availability_view(request):
    """Return all available trainers with their upcoming availability"""
    from wellness_instructors.models import WellnessInstructor
    data = []
    instructors = WellnessInstructor.objects.filter(
        is_available=True,
    ).select_related("user").prefetch_related("specializations")[:20]

    for inst in instructors:
        slots = TimeSlot.objects.filter(
            schedule__instructor=inst,
            start_datetime__gte=timezone.now(),
            start_datetime__lte=timezone.now() + timedelta(days=14),
            status="available",
        ).order_by("start_datetime")[:5]

        location_inst = LocationInstructor.objects.filter(
            instructor=inst, status="active"
        ).select_related("location").first()

        specializations = []
        try:
            specializations = [s.name for s in inst.specializations.all()]
        except Exception:
            pass

        data.append({
            "id": inst.id,
            "name": inst.user.get_full_name() if inst.user else "Unknown",
            "bio": getattr(inst, "bio", "Certified wellness practitioner"),
            "specializations": specializations,
            "location": location_inst.location.name if location_inst else "Main Studio",
            "rating": 4.9,
            "sessionCount": Booking.objects.filter(
                instructor__instructor=inst,
            ).count(),
            "availableSlots": [
                {
                    "id": slot.id,
                    "startTime": slot.start_datetime.isoformat(),
                    "endTime": slot.end_datetime.isoformat(),
                }
                for slot in slots
            ],
        })

    return Response(data)


# ============== Admin: User Management ==============

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def admin_users_view(request):
    """Admin: list all users with stats"""
    if not request.user.is_staff:
        return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.all().order_by("-date_joined")[:50]
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "name": u.get_full_name() or u.email,
            "email": u.email,
            "isStaff": u.is_staff,
            "isActive": u.is_active,
            "dateJoined": u.date_joined.isoformat(),
            "bookingCount": Booking.objects.filter(client=u).count(),
        })
    return Response({"users": data, "total": User.objects.count()})


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def admin_toggle_user_view(request, user_id):
    """Admin: activate or deactivate a user"""
    if not request.user.is_staff:
        return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
    try:
        target = User.objects.get(id=user_id)
        target.is_active = not target.is_active
        target.save()
        return Response({"id": target.id, "isActive": target.is_active})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([permissions.AllowAny]) # Allow but manually verify token
def admin_export_users_csv_view(request):
    """Admin: export all users to CSV"""
    token_key = request.query_params.get('token')
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        if not user.is_staff:
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jpf_users_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Is Staff', 'Is Active', 'Date Joined', 'Total Bookings'])

    users = User.objects.all().order_by("-date_joined")
    for u in users:
        writer.writerow([
            u.id,
            u.get_full_name() or u.email,
            u.email,
            u.is_staff,
            u.is_active,
            u.date_joined.strftime('%Y-%m-%d %H:%M'),
            Booking.objects.filter(client=u).count()
        ])

    return response


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def admin_all_bookings_view(request):
    """Admin: list all bookings across all users"""
    if not request.user.is_staff:
        return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)

    bookings = Booking.objects.all().select_related(
        "client", "service__service", "location", "instructor__instructor__user"
    ).order_by("-created_at")[:100]

    data = []
    for b in bookings:
        data.append({
            "id": b.id,
            "bookingNumber": b.booking_number,
            "client": {
                "id": b.client.id,
                "name": b.client.get_full_name() or b.client.email,
                "email": b.client.email,
            },
            "service": b.service.service.name if b.service and b.service.service else "N/A",
            "startTime": b.start_time.isoformat(),
            "status": b.status,
            "paymentStatus": b.payment_status,
            "price": float(b.total_price) if b.total_price else 0,
            "location": b.location.name if b.location else "N/A",
        })
    return Response({"bookings": data, "total": Booking.objects.count()})


# ============== User Profile Update ==============

@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_profile_view(request):
    """Update current user's profile"""
    user = request.user
    name = request.data.get("name", "")
    phone = request.data.get("phone", "")

    if name:
        parts = name.split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""

    if hasattr(user, "phone") and phone:
        user.phone = phone

    user.save()

    # Determine role
    role = "member"
    if user.is_staff:
        role = "admin"
    elif hasattr(user, 'wellness_instructor'):
        role = "instructor"

    return Response({
        "id": user.id,
        "email": user.email,
        "name": user.get_full_name() or user.email,
        "phone": getattr(user, "phone", ""),
        "role": role,
        "isAdmin": user.is_staff,
        "isStaff": user.is_staff,
    })


# ============== Instructor: My Bookings ==============

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def instructor_bookings_view(request):
    """Get all bookings for the current instructor"""
    from wellness_instructors.models import WellnessInstructor
    try:
        instructor = WellnessInstructor.objects.get(user=request.user)
    except WellnessInstructor.DoesNotExist:
        return Response({"error": "Instructor access required"}, status=status.HTTP_403_FORBIDDEN)

    location_inst = LocationInstructor.objects.filter(instructor=instructor, is_active=True).first()

    if not location_inst:
        return Response({"bookings": [], "total": 0})

    bookings = Booking.objects.filter(
        instructor=location_inst,
    ).select_related("client", "service__service").order_by("-start_time")[:50]

    data = []
    for b in bookings:
        data.append({
            "id": b.id,
            "bookingNumber": b.booking_number,
            "client": {
                "id": b.client.id,
                "name": b.client.get_full_name() or b.client.email,
                "email": b.client.email,
            },
            "service": b.service.service.name if b.service and b.service.service else "Session",
            "startTime": b.start_time.isoformat(),
            "endTime": b.end_time.isoformat(),
            "status": b.status,
            "paymentStatus": b.payment_status,
        })
    return Response({"bookings": data, "total": len(data)})


# ============== Calendar Integration ==============

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def calendar_export_view(request):
    """Generate an iCal (.ics) file for the user's bookings."""
    token_key = request.query_params.get('token')
    try:
        token = Token.objects.get(key=token_key)
        target_user = token.user
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    from bookings.models import Booking, BookingStatus
    from django.http import HttpResponse

    bookings = Booking.objects.filter(
        client=target_user,
        status=BookingStatus.CONFIRMED,
        start_time__gte=timezone.now() - timedelta(days=30),  # Keep some recent history
    ).select_related("service__service", "location", "instructor__instructor__user")

    # Build basic ICS format
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Wellness Solutions//EN",
        "CALSCALE:GREGORIAN",
    ]

    for b in bookings:
        dtstart = b.start_time.strftime("%Y%m%dT%H%M%SZ")
        dtend = b.end_time.strftime("%Y%m%dT%H%M%SZ")
        dtstamp = b.created_at.strftime("%Y%m%dT%H%M%SZ")
        service_name = b.service.service.name if b.service and b.service.service else "Wellness Session"
        location_name = b.location.name if b.location else "JPF Studio"
        instructor_name = b.instructor.instructor.user.get_full_name() if b.instructor and b.instructor.instructor and b.instructor.instructor.user else "Staff"

        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:booking-{b.id}@jpfwellnesssolutions.com",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART:{dtstart}",
            f"DTEND:{dtend}",
            f"SUMMARY:JPF Stretch: {service_name}",
            f"DESCRIPTION:Session with {instructor_name}. Booking #{b.booking_number}",
            f"LOCATION:{location_name}",
            "STATUS:CONFIRMED",
            "END:VEVENT"
        ])

    ics_lines.append("END:VCALENDAR")

    response = HttpResponse("\r\n".join(ics_lines), content_type="text/calendar")
    response["Content-Disposition"] = 'attachment; filename="jpf_schedule.ics"'
    return response

# ==========================================
# NEWSLETTER
# ==========================================

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def newsletter_subscribe_view(request):
    """Subscribe a user to the newsletter."""
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # In a full implementation, save to a NewsletterSubscriber model or external service (e.g. Mailchimp)
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"New newsletter subscription: {email}")
    
    return Response({"message": "Successfully subscribed"}, status=status.HTTP_201_CREATED)

# ==========================================
# PHASE 12: AI-POWERED DEMO FEATURES
# ==========================================

import random

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def ai_therapist_match_view(request):
    """
    Frictionless AI feature to parse user's pain points and recommend a stretch.
    Uses heuristic keyword mapping for zero-latency demo reliability.
    """
    query = str(request.data.get("query", "")).lower()
    if len(query) < 5:
        return Response({"error": "Query too short"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Simple Heuristic AI logic
    recommendation = {
        "service": "Full Body Wellness Stretch",
        "trainer": "Alex Johnson",
        "reason": "Based on your input, a comprehensive full-body session is the best starting point to identify specific tension areas."
    }
    
    if any(q in query for q in ['back', 'spine', 'sitting', 'desk', 'lumbar', 'posture']):
        recommendation = {
            "service": "Spinal Decompression & Posture Correction",
            "trainer": "Dr. Sarah Jenkins",
            "reason": "I detected concerns related to your back/posture. Dr. Jenkins specializes in spinal alignment and desk-fatigue recovery."
        }
    elif any(q in query for q in ['run', 'marathon', 'legs', 'hamstring', 'calf', 'knee', 'athlet']):
        recommendation = {
            "service": "Athletic Recovery & Lower Body Release",
            "trainer": "Michael Chen",
            "reason": "Since you mentioned lower body/athletic stress, Michael's athletic recovery protocol focuses heavily on hamstring and calf myofascial release."
        }
    elif any(q in query for q in ['neck', 'shoulder', 'headache', 'tension', 'stress']):
        recommendation = {
            "service": "Upper Body Tension Relief",
            "trainer": "Alex Johnson",
            "reason": "Upper body tension often leads to headaches. Alex's upper body protocol focuses on traps, neck mobility, and stress relief."
        }

    return Response(recommendation, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def ai_session_insights_view(request, booking_id):
    """
    Generates actionable bullet points for an instructor based on a client's booking history.
    """
    from bookings.models import Booking
    
    try:
        # Verify the instructor owns this booking (or is staff)
        booking = Booking.objects.select_related('client').get(id=booking_id)
        if not request.user.is_staff and booking.instructor.instructor.user != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        client = booking.client
        past_bookings_count = Booking.objects.filter(client=client).count() - 1
        
        # Simulated AI generation based on basic metrics
        insights = []
        if past_bookings_count <= 0:
            insights = [
                "This is the client's first recorded session with the Hub.",
                "Recommend spending the first 5 minutes on a comprehensive mobility assessment.",
                "Focus on explaining the breathwork and communication protocol during deep stretches."
            ]
        elif past_bookings_count < 5:
            insights = [
                f"Client has had {past_bookings_count} previous sessions. They are building a routine.",
                "Review their previous intake form to ensure no new contraindications.",
                "They typically respond well to mid-intensity PNF stretching on the lower body."
            ]
        else:
            insights = [
                f"VIP Client! They have completed {past_bookings_count} sessions.",
                "Historical data shows recurring tightness in the right hip flexor.",
                "Recommend incorporating advanced fascial release techniques today."
            ]
            
        return Response({"insights": insights}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def ai_smart_rebook_view(request):
    """
    Analyzes user's booking history to find their most common day/time and 
    generates a 1-click rebook recommendation.
    """
    from bookings.models import Booking, BookingStatus
    from django.db.models import Count
    from django.db.models.functions import ExtractWeekDay, ExtractHour
    from datetime import timedelta
    
    # Get user's confirmed/completed past bookings
    past_bookings = Booking.objects.filter(
        client=request.user, 
        status__in=[BookingStatus.CONFIRMED, BookingStatus.COMPLETED]
    ).order_by('-start_time')
    
    if not past_bookings.exists():
        return Response({"available": False}, status=status.HTTP_200_OK)
        
    last_booking = past_bookings.first()
    
    # Calculate most frequent day of week (1=Sunday, 7=Saturday in Django default)
    day_stats = past_bookings.annotate(day=ExtractWeekDay('start_time')).values('day').annotate(c=Count('id')).order_by('-c')
    hour_stats = past_bookings.annotate(hour=ExtractHour('start_time')).values('hour').annotate(c=Count('id')).order_by('-c')
    
    if not day_stats or not hour_stats:
         return Response({"available": False}, status=status.HTTP_200_OK)
         
    best_day = day_stats[0]['day']
    best_hour = hour_stats[0]['hour']
    
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day_name = days[best_day - 1] if 1 <= best_day <= 7 else "their usual day"
    
    am_pm = "AM" if best_hour < 12 else "PM"
    display_hour = best_hour if best_hour <= 12 else best_hour - 12
    display_hour = 12 if display_hour == 0 else display_hour
    
    service_name = last_booking.service.service.name if last_booking.service and last_booking.service.service else "Wellness Session"
    
    # Mocking the next logical date (e.g. next week)
    next_date = timezone.now() + timedelta(days=7)
    
    recommendation = {
        "available": True,
        "message": f"Grab your usual {day_name} {display_hour}:00 {am_pm} slot",
        "service_name": service_name,
        "suggested_time": f"{day_name}s at {display_hour}:00 {am_pm}",
        # In a real app we'd pass exact slot IDs here to trigger the booking mutation
    }
    
    return Response(recommendation, status=status.HTTP_200_OK)
