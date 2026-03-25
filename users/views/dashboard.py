from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from bookings.models import Booking, BookingPackage, BookingPayment, BookingStatus, PaymentStatus
from locations.models import Location, LocationService
from schedules.models import BlackoutDate, Schedule, TimeSlot
from wellness_instructors.models import Session, WellnessInstructor


User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_instructor(user):
    return user.is_authenticated and hasattr(user, "wellness_instructor")

class DashboardView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        if request.user.is_staff:
            return redirect("users:admin_dashboard")
        if hasattr(request.user, "wellness_instructor"):
            return redirect("users:instructor_dashboard")
        return redirect("users:client_dashboard")

class AdminDashboardView(TemplateView):
    template_name = "dashboard/admin_dashboard.html"

    @method_decorator(user_passes_test(is_admin))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()

        # Get statistics for the dashboard
        context["total_users"] = User.objects.count()
        context["active_instructors"] = WellnessInstructor.objects.filter(is_active=True).count()

        # Session statistics
        context["active_sessions"] = Session.objects.filter(
            is_active=True,
        ).count()

        # Instructor statistics
        instructors = WellnessInstructor.objects.annotate(
            session_count=Count("sessions"),
            avg_rating=Avg("sessions__rating"),
        )
        context["top_instructors"] = instructors.order_by("-session_count")[:5]

        # Schedule statistics
        context["upcoming_sessions"] = Session.objects.filter(
            start_time__gte=today,
        ).count()

        # Package statistics
        active_packages = BookingPackage.objects.filter(
            active=True,
            expiry_date__gte=today,
        )
        context["active_packages"] = active_packages.count()
        context["expiring_soon"] = active_packages.filter(
            expiry_date__lte=today + timedelta(days=30),
        ).count()

        # Location statistics
        locations = Location.objects.annotate(
            service_count=Count("services"),
            instructor_count=Count("instructors"),
            booking_count=Count("bookings"),
        )
        context["locations"] = locations
        context["total_locations"] = locations.count()

        # Service statistics
        context["service_stats"] = LocationService.objects.select_related(
            "service",
        ).values(
            "service__name",
        ).annotate(
            total_bookings=Count("bookings"),
            avg_price=Avg("price_adjustment"),
            location_count=Count("location", distinct=True),
        ).order_by("-total_bookings")[:5]

        # Payment statistics
        payment_stats = BookingPayment.objects.filter(
            status__in=[PaymentStatus.PAID, PaymentStatus.COMPANY_PAID],
        ).aggregate(
            total_revenue=Sum("amount"),
            total_payments=Count("id"),
        )
        context["total_revenue"] = payment_stats["total_revenue"] or 0
        context["total_payments"] = payment_stats["total_payments"] or 0

        # Recent activity
        context["recent_bookings"] = Booking.objects.select_related(
            "client", "client__user", "service", "instructor", "instructor__user",
        ).filter(
            created__gte=today - timedelta(days=30),
        ).order_by("-created")[:10]

        context["recent_payments"] = BookingPayment.objects.select_related(
            "booking", "booking__client", "booking__client__user",
        ).filter(
            payment_date__gte=today - timedelta(days=30),
        ).order_by("-payment_date")[:10]

        return context

class InstructorDashboardView(TemplateView):
    template_name = "dashboard/instructor_dashboard.html"

    @method_decorator(user_passes_test(is_instructor))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instructor = self.request.user.wellness_instructor
        today = timezone.now()

        # Today's bookings
        context["todays_sessions"] = Booking.objects.filter(
            instructor=instructor,
            start_time__date=today.date(),
            status=BookingStatus.CONFIRMED,
        ).count()

        # Active time slots
        context["available_slots"] = TimeSlot.objects.filter(
            schedule__instructor=instructor,
            start_datetime__gte=today,
            status="available",
        ).count()

        # Booking statistics
        context["total_sessions"] = Booking.objects.filter(
            instructor=instructor,
        ).count()

        context["completed_sessions"] = Booking.objects.filter(
            instructor=instructor,
            status=BookingStatus.COMPLETED,
        ).count()

        context["upcoming_sessions_count"] = Booking.objects.filter(
            instructor=instructor,
            start_time__gte=today,
            status=BookingStatus.CONFIRMED,
        ).count()

        # Recent sessions
        context["recent_sessions"] = Booking.objects.filter(
            instructor=instructor,
        ).select_related(
            "client",
            "client__user",
            "organization",
            "location",
            "service",
        ).order_by("-start_time")[:5]

        # Upcoming sessions
        context["upcoming_sessions"] = Booking.objects.filter(
            instructor=instructor,
            start_time__gte=today,
            status=BookingStatus.CONFIRMED,
        ).select_related(
            "client",
            "client__user",
            "organization",
            "location",
            "service",
        ).order_by("start_time")[:5]

        # Calculate completion rate
        if context["total_sessions"] > 0:
            context["completion_rate"] = (context["completed_sessions"] / context["total_sessions"]) * 100
        else:
            context["completion_rate"] = 0

        # Upcoming blackout dates
        context["upcoming_blackouts"] = BlackoutDate.objects.filter(
            instructor=instructor,
            start_date__gte=today,
        ).order_by("start_date")[:5]

        # Schedule overview
        context["weekly_schedule"] = Schedule.objects.filter(
            instructor=instructor,
            is_active=True,
        ).order_by("weekday", "start_time")

        return context

class ClientDashboardView(TemplateView):
    template_name = "dashboard/client_dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "wellness_instructor"):
            return redirect("users:instructor_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()

        # Get user's sessions
        user_sessions = Session.objects.filter(
            Q(participants=self.request.user) | Q(client=self.request.user),
            is_active=True,
        )

        # Upcoming sessions
        upcoming_sessions = user_sessions.filter(
            start_time__gte=today,
        ).order_by("start_time")
        context["upcoming_sessions"] = upcoming_sessions[:5]
        context["upcoming_sessions_count"] = upcoming_sessions.count()

        # Completed sessions
        completed_sessions = user_sessions.filter(
            start_time__lt=today,
        )
        context["completed_sessions"] = completed_sessions.count()

        # Active packages
        active_packages = BookingPackage.objects.filter(
            owner=self.request.user,
            active=True,
            expiry_date__gte=today,
        ).select_related("service", "service_package")

        context["active_packages"] = [{
            "name": package.name,
            "service": package.service.name,
            "remaining_sessions": package.sessions_remaining(),
            "expiry_date": package.expiry_date,
            "total_sessions": package.total_sessions,
            "used_sessions": package.used_sessions,
        } for package in active_packages]

        # Recent bookings
        recent_bookings = Booking.objects.filter(
            client=self.request.user,
        ).select_related(
            "service", "instructor", "location",
        ).order_by("-created")[:5]

        context["recent_bookings"] = [{
            "booking_number": booking.booking_number,
            "service": booking.service.name,
            "instructor": booking.instructor.user.get_full_name(),
            "status": booking.status,
            "start_time": booking.start_time,
            "location": booking.location.name,
        } for booking in recent_bookings]

        # Payment summary
        recent_payments = BookingPayment.objects.filter(
            booking__client=self.request.user,
        ).select_related("booking").order_by("-payment_date")[:5]

        context["recent_payments"] = [{
            "amount": payment.amount,
            "date": payment.payment_date,
            "status": payment.status,
            "method": payment.payment_method,
            "booking": payment.booking.booking_number,
        } for payment in recent_payments]

        # Calculate total spent
        context["total_spent"] = BookingPayment.objects.filter(
            booking__client=self.request.user,
            status=PaymentStatus.PAID,
        ).aggregate(
            total=Sum("amount"),
        )["total"] or 0

        # Available instructors
        context["available_instructors"] = WellnessInstructor.objects.filter(
            is_available=True,
            is_active=True,
        ).order_by("-years_of_experience")[:5]

        # Progress metrics
        context["progress_metrics"] = [
            {"name": "Sessions Completed", "value": context["completed_sessions"]},
            {"name": "Different Instructors", "value": user_sessions.values("instructor").distinct().count()},
            {"name": "Session Types Tried", "value": user_sessions.values("session_type").distinct().count()},
            {"name": "Active Packages", "value": len(context["active_packages"])},
        ]

        # Calculate progress score
        total_possible_score = 100
        score_components = {
            "sessions": min(context["completed_sessions"] / 10, 1) * 40,  # 40% weight for sessions
            "instructors": min(user_sessions.values("instructor").distinct().count() / 5, 1) * 20,  # 20% weight for instructor variety
            "session_types": min(user_sessions.values("session_type").distinct().count() / 3, 1) * 20,  # 20% weight for session type variety
            "active_packages": min(len(context["active_packages"]), 1) * 20,  # 20% weight for having active packages
        }
        context["progress_score"] = min(int(sum(score_components.values())), total_possible_score)

        return context
