import logging

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Case, Count, F, IntegerField, Max, Q, QuerySet, Sum, When
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, TemplateView, UpdateView


logger = logging.getLogger(__name__)

from bookings.models import Booking, BookingStatus, Package
from locations.models import Location
from schedules.models import TimeSlot
from wellness_instructors.models import Session, WellnessInstructor

from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()

# Dashboard Views

def is_admin(user):
    """Check if user is an admin."""
    return user.is_authenticated and user.is_staff

def is_instructor(user):
    """Check if user is an instructor."""
    return user.is_authenticated and hasattr(user, "wellness_instructor")

class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view that redirects users to their role-specific dashboard."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        if request.user.is_staff:
            return redirect("users:admin_dashboard")
        if hasattr(request.user, "wellness_instructor"):
            return redirect("users:instructor_dashboard")
        return redirect("users:client_dashboard")

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view for admin users."""
    template_name = "dashboard/admin_dashboard.html"

    @method_decorator(user_passes_test(is_admin))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now()

        # Stats Overview Context
        stats_context = self._get_stats_overview()
        context.update(stats_context)

        # Activities Context
        activities_context = self._get_activities_context()
        context.update(activities_context)

        # Performance Context
        performance_context = self._get_performance_context()
        context.update(performance_context)

        return context

    def _get_stats_overview(self):
        """Get overview statistics with error handling."""
        try:
            thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
            previous_thirty_days = thirty_days_ago - timezone.timedelta(days=30)

            current_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
            previous_users = User.objects.filter(
                date_joined__range=(previous_thirty_days, thirty_days_ago),
            ).count()
            user_growth = ((current_users - previous_users) / max(previous_users, 1)) * 100

            current_bookings = Booking.objects.filter(created_at__gte=thirty_days_ago).count()
            previous_bookings = Booking.objects.filter(
                created_at__range=(previous_thirty_days, thirty_days_ago),
            ).count()
            booking_growth = ((current_bookings - previous_bookings) / max(previous_bookings, 1)) * 100

            return {
                "total_users": User.objects.count(),
                "total_bookings": Booking.objects.count(),
                "user_growth": round(user_growth, 1),
                "booking_growth": round(booking_growth, 1),
            }
        except Exception as e:
            logger.error(f"Error getting stats overview: {str(e)}")
            return {
                "total_users": 0,
                "total_bookings": 0,
                "user_growth": 0,
                "booking_growth": 0,
                "stats_error": True,
            }

    def _get_activities_context(self):
        """Get recent activities across the platform."""
        try:
            bookings = Booking.objects.select_related(
                "client",
                "instructor__instructor__user",
                "service",
            ).order_by("-created_at")[:10]

            activities = []
            for booking in bookings:
                activity = {
                    "user": booking.client,
                    "description": f"Booked a {booking.service.name} session with {booking.instructor.instructor.user.get_full_name()}",
                    "created_at": booking.created_at,
                    "type": "booking",
                }
                activities.append(activity)

            return {"recent_activities": activities}
        except Exception as e:
            logger.error(f"Error getting recent activities: {str(e)}")
            return {"recent_activities": []}

    def _get_performance_context(self):
        """Get performance metrics."""
        try:
            thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
            services = Booking.objects.filter(
                created_at__gte=thirty_days_ago,
            ).values(
                "service__service",
            ).annotate(
                name=F("service__service__name"),
                bookings_count=Count("id"),
                success_rate=Avg(Case(
                    When(status=BookingStatus.COMPLETED, then=100),
                    When(status=BookingStatus.CANCELLED, then=0),
                    default=50,
                    output_field=IntegerField(),
                )),
                revenue=Sum(
                    F("service__service__price") +
                    F("service__price_adjustment") +
                    F("service__service__home_visit_surcharge"),
                ),
            ).filter(
                bookings_count__gt=0,
            ).order_by("-bookings_count")[:5]

            instructors = WellnessInstructor.objects.select_related("user").annotate(
                completed_sessions=Count("sessions", filter=Q(
                    sessions__time_slot__start_datetime__lt=timezone.now(),
                    sessions__is_active=True,
                    sessions__status=BookingStatus.COMPLETED,
                )),
                total_sessions=Count("sessions", filter=Q(
                    sessions__time_slot__start_datetime__lt=timezone.now(),
                    sessions__is_active=True,
                )),
                rating=Avg("instructor_reviews__rating"),
                revenue=Sum(Case(
                    When(
                        instructor_location__bookings__status=BookingStatus.COMPLETED,
                        then=F("instructor_location__bookings__service__service__price") +
                             F("instructor_location__bookings__service__price_adjustment"),
                    ),
                    default=0,
                    output_field=IntegerField(),
                )),
                client_count=Count("instructor_location__bookings__client", distinct=True),
            ).filter(
                user__is_active=True,
                total_sessions__gt=0,
            ).order_by("-rating", "-completed_sessions")[:5]

            return {
                "popular_services": [{
                    "name": service["name"],
                    "bookings_count": service["bookings_count"],
                    "success_rate": int(service["success_rate"]),
                    "revenue": service["revenue"],
                } for service in services],
                "top_instructors": [{
                    "id": instructor.id,
                    "user": instructor.user,
                    "get_full_name": instructor.user.get_full_name(),
                    "avatar": instructor.user.avatar if hasattr(instructor.user, "avatar") else None,
                    "completed_sessions": instructor.completed_sessions,
                    "rating": float(instructor.rating) if instructor.rating else 0.0,
                    "completion_rate": int((instructor.completed_sessions / instructor.total_sessions) * 100) if instructor.total_sessions else 0,
                    "revenue": instructor.revenue or 0,
                    "client_count": instructor.client_count,
                } for instructor in instructors],
            }
        except Exception as e:
            logger.error(f"Error getting performance context: {str(e)}")
            return {
                "popular_services": [],
                "top_instructors": [],
            }

class InstructorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/instructor_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, "wellness_instructor"):
            return redirect("users:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now()

        # Stats Context
        stats_context = {
            "total_sessions": self._get_total_sessions(user),
            "total_clients": self._get_total_clients(user),
            "completion_rate": self._calculate_completion_rate(user),
            "avg_rating": self._get_average_rating(user),
        }
        context.update(stats_context)

        # Schedule Context
        schedule_context = {
            "upcoming_sessions": self._get_upcoming_sessions(user),
            "todays_schedule": self._get_todays_schedule(user),
            "available_slots": self._get_available_slots(user),
        }
        context.update(schedule_context)

        # Clients Context
        clients_context = {
            "recent_clients": self._get_recent_clients(user),
            "client_stats": self._get_client_stats(user),
        }
        context.update(clients_context)

        return context

    def _get_total_sessions(self, user):
        """Get total number of sessions for instructor."""
        return Session.objects.filter(
            instructor__user=user,
            is_active=True,
        ).count()

    def _get_total_clients(self, user):
        """Get total number of unique clients."""
        return User.objects.filter(
            bookings__instructor__instructor=user.wellness_instructor,
        ).distinct().count()

    def _calculate_completion_rate(self, user):
        """Calculate session completion rate."""
        total = Session.objects.filter(
            instructor__user=user,
            is_active=True,
            time_slot__start_datetime__lt=timezone.now(),
        )
        completed = total.filter(status=BookingStatus.COMPLETED)

        if total.count() == 0:
            return 100
        return int((completed.count() / total.count()) * 100)

    def _get_average_rating(self, user):
        """Get instructor's average rating."""
        return WellnessInstructor.objects.filter(
            user=user,
        ).aggregate(
            avg_rating=Avg("instructor_reviews__rating"),
        )["avg_rating"] or 0

    def _get_upcoming_sessions(self, user):
        """Get upcoming sessions."""
        return Session.objects.filter(
            instructor__user=user,
            is_active=True,
            time_slot__start_datetime__gt=timezone.now(),
        ).select_related(
            "time_slot",
            "instructor",
        ).order_by("time_slot__start_datetime")[:5]

    def _get_todays_schedule(self, user):
        """Get today's schedule."""
        today = timezone.now().date()
        return Session.objects.filter(
            instructor__user=user,
            is_active=True,
            time_slot__start_datetime__date=today,
        ).select_related(
            "time_slot",
            "instructor",
        ).order_by("time_slot__start_datetime")

    def _get_available_slots(self, user):
        """Get available time slots."""
        return TimeSlot.objects.filter(
            schedule__instructor=user.wellness_instructor,
            start_datetime__gt=timezone.now(),
            session__isnull=True,
        ).select_related(
            "schedule",
        ).order_by("start_datetime")[:5]

    def _get_recent_clients(self, user):
        """Get recent clients with their session history."""
        return User.objects.filter(
            bookings__instructor__instructor=user.wellness_instructor,
        ).annotate(
            total_sessions=Count("bookings"),
            last_session=Max("bookings__start_time"),
        ).order_by("-last_session")[:5]

    def _get_client_stats(self, user):
        """Get aggregated client statistics."""
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        return {
            "new_clients": User.objects.filter(
                bookings__instructor__instructor=user.wellness_instructor,
                bookings__created_at__gte=thirty_days_ago,
            ).distinct().count(),
            "returning_clients": User.objects.filter(
                bookings__instructor__instructor=user.wellness_instructor,
            ).annotate(
                booking_count=Count("bookings"),
            ).filter(booking_count__gt=1).count(),
        }

class ClientDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view for client users."""
    template_name = "dashboard/client_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "wellness_instructor"):
            return redirect("users:instructor_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now()

        # Stats Context
        stats_context = {
            "total_sessions": self._get_total_sessions(user),
            "total_packages": self._get_total_packages(user),
            "completion_rate": self._calculate_completion_rate(user),
            "progress_score": self._calculate_progress_score(user),
        }
        context.update(stats_context)

        # Packages Context
        packages_context = {
            "active_packages": self._get_active_packages(user),
            "package_usage": self._get_package_usage(user),
            "recommended_packages": self._get_recommended_packages(user),
        }
        context.update(packages_context)

        # Bookings Context
        bookings_context = {
            "upcoming_bookings": self._get_upcoming_bookings(user),
            "recent_bookings": self._get_recent_bookings(user),
            "booking_stats": self._get_booking_stats(user),
        }
        context.update(bookings_context)

        return context

    def _get_total_sessions(self, user):
        """Get total number of completed sessions."""
        return Booking.objects.filter(
            client=user,
            status=BookingStatus.COMPLETED,
        ).count()

    def _get_total_packages(self, user):
        """Get total number of purchased packages."""
        return user.client_packages.count()

    def _calculate_completion_rate(self, user):
        """Calculate booking completion rate."""
        total = Booking.objects.filter(
            client=user,
            start_time__lt=timezone.now(),
        )
        completed = total.filter(status=BookingStatus.COMPLETED)

        if total.count() == 0:
            return 100
        return int((completed.count() / total.count()) * 100)

    def _calculate_progress_score(self, user):
        """Calculate client's progress score based on activity."""
        # Base metrics
        completed_sessions = self._get_total_sessions(user)
        unique_instructors = self._get_unique_instructors(user)
        regular_attendance = self._calculate_attendance_rate(user)

        # Weights for different factors
        session_weight = 0.4
        instructor_weight = 0.3
        attendance_weight = 0.3

        # Calculate individual scores (0-100)
        session_score = min(completed_sessions / 20, 1) * 100  # Cap at 20 sessions
        instructor_score = min(unique_instructors / 5, 1) * 100  # Cap at 5 instructors
        attendance_score = regular_attendance  # Already 0-100

        # Calculate weighted total
        total_score = (
            session_score * session_weight +
            instructor_score * instructor_weight +
            attendance_score * attendance_weight
        )

        return int(total_score)

    def _get_unique_instructors(self, user):
        """Get number of unique instructors client has worked with."""
        return WellnessInstructor.objects.filter(
            instructor_location__bookings__client=user,
        ).distinct().count()

    def _calculate_attendance_rate(self, user):
        """Calculate client's attendance rate."""
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        recent_bookings = Booking.objects.filter(
            client=user,
            start_time__gte=thirty_days_ago,
            start_time__lt=timezone.now(),
        )

        if recent_bookings.count() == 0:
            return 100

        attended = recent_bookings.filter(status=BookingStatus.COMPLETED).count()
        return int((attended / recent_bookings.count()) * 100)

    def _get_active_packages(self, user):
        """Get client's active packages."""
        return user.client_packages.filter(
            expiry_date__gt=timezone.now(),
        ).select_related("package").order_by("expiry_date")

    def _get_package_usage(self, user):
        """Get usage statistics for client's packages."""
        active_packages = self._get_active_packages(user)
        return [{
            "package": package,
            "sessions_used": Booking.objects.filter(
                client=user,
                package=package,
                status=BookingStatus.COMPLETED,
            ).count(),
            "sessions_remaining": package.sessions_remaining,
        } for package in active_packages]

    def _get_recommended_packages(self, user):
        """Get recommended packages based on usage patterns."""
        # Get client's preferred session types
        preferred_services = Booking.objects.filter(
            client=user,
            status=BookingStatus.COMPLETED,
        ).values("service__service__type").annotate(
            count=Count("id"),
        ).order_by("-count")

        if not preferred_services.exists():
            return Package.objects.filter(is_active=True)[:3]

        preferred_type = preferred_services[0]["service__service__type"]
        return Package.objects.filter(
            is_active=True,
            service_type=preferred_type,
        ).order_by("-value_ratio")[:3]

    def _get_upcoming_bookings(self, user):
        """Get upcoming bookings."""
        return Booking.objects.filter(
            client=user,
            start_time__gt=timezone.now(),
            status=BookingStatus.CONFIRMED,
        ).select_related(
            "instructor__instructor__user",
            "service",
            "location",
        ).order_by("start_time")[:5]

    def _get_recent_bookings(self, user):
        """Get recent booking history."""
        return Booking.objects.filter(
            client=user,
            start_time__lt=timezone.now(),
        ).select_related(
            "instructor__instructor__user",
            "service",
            "location",
        ).order_by("-start_time")[:5]

    def _get_booking_stats(self, user):
        """Get aggregated booking statistics."""
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)

        # Combine queries into a single annotated query
        booking_stats = Booking.objects.filter(
            client=user,
            created_at__gte=thirty_days_ago,
        ).aggregate(
            total_this_month=Count("id"),
            completed_this_month=Count("id", filter=Q(status=BookingStatus.COMPLETED)),
        )

        # Get favorite instructor with a single query
        favorite_instructor = WellnessInstructor.objects.filter(
            instructor_location__bookings__client=user,
        ).annotate(
            booking_count=Count("instructor_location__bookings"),
            latest_booking=Max("instructor_location__bookings__created_at"),
        ).select_related(
            "user",
            "user__profile",
        ).order_by("-booking_count").first()

        # Get preferred location with a single query
        preferred_location = Location.objects.filter(
            bookings__client=user,
        ).annotate(
            visit_count=Count("bookings"),
            latest_visit=Max("bookings__created_at"),
        ).order_by("-visit_count").first()

        return {
            "total_this_month": booking_stats["total_this_month"],
            "completed_this_month": booking_stats["completed_this_month"],
            "favorite_instructor": favorite_instructor,
            "preferred_location": preferred_location,
        }

class EmailPreferencesView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View for updating user's email preferences."""
    model = User
    template_name = "users/email_preferences.html"
    fields = ["receive_notifications", "preferred_language"]
    success_message = _("Email preferences successfully updated")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:email-preferences")

# Register the view
email_preferences_view = EmailPreferencesView.as_view()
