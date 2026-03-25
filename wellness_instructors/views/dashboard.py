"""Views for the dashboard."""

from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.utils import timezone
from django.views.generic import TemplateView

from schedules.models import TimeSlot
from wellness_instructors.models import Session, WellnessInstructor


class DashboardView(LoginRequiredMixin, TemplateView):
    """Base dashboard view with common functionality."""

    def get_available_slots_count(self, instructor=None):
        """Get count of available time slots."""
        query = Q(status="available")
        if instructor:
            query &= Q(schedule__instructor=instructor)
        return TimeSlot.objects.filter(query).count()

    def get_context_data(self, **kwargs):
        """Get common context data for all dashboards."""
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # Add organization info if available
        if hasattr(self.request.user, "organization"):
            context["organization"] = self.request.user.organization

        return context


class ClientDashboardView(DashboardView):
    """Client dashboard view."""
    template_name = "dashboard/client_dashboard.html"

    def get_context_data(self, **kwargs):
        """Get context data for client dashboard."""
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # Get upcoming sessions for the client
        upcoming_sessions = Session.objects.filter(
            client=self.request.user,
            time_slot__start_datetime__gte=today,
        ).order_by("time_slot__start_datetime")

        context.update({
            "upcoming_sessions_count": upcoming_sessions.count(),
            "total_sessions": Session.objects.filter(client=self.request.user).count(),
            "available_slots_count": self.get_available_slots_count(),
            "active_instructors_count": WellnessInstructor.objects.filter(is_available=True).count(),
            "upcoming_sessions": upcoming_sessions[:5],  # Latest 5 upcoming sessions
        })

        return context


class InstructorDashboardView(DashboardView):
    """Instructor dashboard view."""
    template_name = "dashboard/instructor_dashboard.html"

    def get_context_data(self, **kwargs):
        """Get context data for instructor dashboard."""
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        instructor = self.request.user.wellness_instructor

        # Get today's sessions
        todays_sessions = Session.objects.filter(
            instructor=instructor,
            time_slot__start_datetime__date=today,
        ).order_by("time_slot__start_datetime")

        # Calculate monthly earnings
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        monthly_earnings = Session.objects.filter(
            instructor=instructor,
            time_slot__start_datetime__date__range=[start_of_month, end_of_month],
            status="completed",
        ).aggregate(total=Sum("price"))["total"] or 0

        # Get recent feedback
        recent_feedback = (
            Session.objects
            .filter(instructor=instructor)
            .exclude(client_feedback="")
            .order_by("-time_slot__start_datetime")[:5]
        )

        context.update({
            "todays_sessions": todays_sessions.count(),
            "todays_sessions_list": todays_sessions,
            "total_clients": Session.objects.filter(instructor=instructor).values("client").distinct().count(),
            "available_slots": self.get_available_slots_count(instructor),
            "monthly_earnings": monthly_earnings,
            "recent_feedback": recent_feedback,
        })

        return context
