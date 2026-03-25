"""Views for the wellness_instructors app."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Session, WellnessInstructor


User = get_user_model()


class InstructorListView(ListView):
    """Display a list of all active instructors with filtering capabilities."""
    model = WellnessInstructor
    context_object_name = "instructors"
    paginate_by = 10

    def get_template_names(self):
        """Return different templates for admin and non-admin users."""
        if self.request.user.is_staff:
            return ["wellness_instructors/admin_instructor_list.html"]
        return ["wellness_instructors/instructor_list.html"]

    def get_queryset(self):
        """Return filtered queryset of instructors."""
        queryset = WellnessInstructor.objects.select_related("user")

        # Get filter parameters from request
        name = self.request.GET.get("name", "")
        specialization = self.request.GET.get("specialization", "")
        certification_level = self.request.GET.get("certification_level", "")
        min_experience = self.request.GET.get("min_experience", "")
        is_available = self.request.GET.get("is_available", "")
        min_rate = self.request.GET.get("min_rate", "")
        max_rate = self.request.GET.get("max_rate", "")

        # Apply filters
        if name:
            queryset = queryset.filter(
                Q(user__first_name__icontains=name) |
                Q(user__last_name__icontains=name),
            )
        if specialization:
            queryset = queryset.filter(specializations=specialization)
        if certification_level:
            queryset = queryset.filter(certification_level=certification_level)
        if min_experience:
            queryset = queryset.filter(years_of_experience__gte=int(min_experience))
        if is_available:
            queryset = queryset.filter(is_available=is_available == "true")
        if min_rate:
            queryset = queryset.filter(hourly_rate__gte=float(min_rate))
        if max_rate:
            queryset = queryset.filter(hourly_rate__lte=float(max_rate))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Our Wellness Instructors")
        context["specialization_choices"] = WellnessInstructor.SPECIALIZATION_CHOICES
        context["certification_levels"] = WellnessInstructor.CERTIFICATION_LEVELS
        # Add current filter values to context
        context["current_filters"] = {
            "name": self.request.GET.get("name", ""),
            "specialization": self.request.GET.get("specialization", ""),
            "certification_level": self.request.GET.get("certification_level", ""),
            "min_experience": self.request.GET.get("min_experience", ""),
            "is_available": self.request.GET.get("is_available", ""),
            "min_rate": self.request.GET.get("min_rate", ""),
            "max_rate": self.request.GET.get("max_rate", ""),
        }
        return context


class InstructorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new instructor."""
    model = WellnessInstructor
    template_name = "wellness_instructors/instructor_form.html"
    fields = ["bio", "specializations", "certification_level",
              "years_of_experience", "is_available", "hourly_rate"]

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, _("Instructor created successfully."))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("wellness_instructors:instructor-detail",
                          kwargs={"pk": self.object.pk})


class InstructorDetailView(DetailView):
    """Display detailed information about a specific instructor."""
    model = WellnessInstructor
    context_object_name = "instructor"
    template_name = "wellness_instructors/instructor_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_sessions"] = self.object.sessions.filter(is_active=True)
        return context


class InstructorUpdateView(LoginRequiredMixin, UpdateView):
    """Update instructor details."""
    model = WellnessInstructor
    template_name = "wellness_instructors/instructor_form.html"
    fields = ["bio", "specialization", "certification_level",
              "years_of_experience", "is_available"]

    def get_success_url(self):
        return reverse_lazy("wellness_instructors:instructor-detail",
                          kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _("Instructor profile updated successfully."))
        return super().form_valid(form)


class InstructorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete an instructor."""
    model = WellnessInstructor
    template_name = "wellness_instructors/instructor_confirm_delete.html"
    success_url = reverse_lazy("wellness_instructors:instructor-list")

    def test_func(self):
        return self.request.user.is_staff or self.get_object().user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Instructor deleted successfully."))
        return super().delete(request, *args, **kwargs)


class SessionListView(ListView):
    """Display a list of all active sessions."""
    model = Session
    context_object_name = "sessions"
    paginate_by = 10

    def get_template_names(self):
        """Return different templates for admin and non-admin users."""
        if self.request.user.is_staff:
            return ["wellness_instructors/admin_session_list.html"]
        return ["wellness_instructors/session_list.html"]

    def get_queryset(self):
        """Return filtered queryset of sessions."""
        queryset = Session.objects.all()

        # Get filter parameters
        session_type = self.request.GET.get("session_type")
        instructor = self.request.GET.get("instructor")
        status = self.request.GET.get("status")

        if session_type:
            queryset = queryset.filter(session_type=session_type)
        if instructor:
            queryset = queryset.filter(instructor_id=instructor)
        if status:
            if status == "active":
                queryset = queryset.filter(is_active=True)
            elif status == "upcoming":
                queryset = queryset.filter(
                    time_slot__start_time__gt=timezone.now(),
                    is_active=True,
                )
            elif status == "completed":
                queryset = queryset.filter(
                    time_slot__end_time__lt=timezone.now(),
                )

        return queryset.select_related("instructor", "instructor__user", "time_slot")

    def get_context_data(self, **kwargs):
        """Add additional context for filtering."""
        context = super().get_context_data(**kwargs)
        context["session_types"] = Session.SESSION_TYPES
        context["instructors"] = WellnessInstructor.objects.all()
        return context


class SessionDetailView(DetailView):
    """Display detailed information about a specific session."""
    model = Session
    context_object_name = "session"
    template_name = "wellness_instructors/session_detail.html"


class SessionUpdateView(LoginRequiredMixin, UpdateView):
    """Update session details."""
    model = Session
    template_name = "wellness_instructors/session_form.html"
    fields = ["title", "description", "session_type", "difficulty_level",
              "duration", "max_participants", "price", "is_active"]

    def get_success_url(self):
        return reverse_lazy("wellness_instructors:session-detail",
                          kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _("Session updated successfully."))
        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a session."""
    model = Session
    template_name = "wellness_instructors/session_confirm_delete.html"
    success_url = reverse_lazy("wellness_instructors:session-list")

    def test_func(self):
        return self.request.user.is_staff or self.get_object().instructor.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Session deleted successfully."))
        return super().delete(request, *args, **kwargs)


class InstructorSessionCreateView(LoginRequiredMixin, CreateView):
    """Allow instructors to create new sessions."""
    model = Session
    template_name = "wellness_instructors/session_form.html"
    fields = ["title", "description", "session_type", "difficulty_level",
             "duration", "max_participants", "price", "is_active"]
    success_url = reverse_lazy("wellness_instructors:session-list")

    def form_valid(self, form):
        form.instance.instructor = self.request.user.wellness_instructor
        messages.success(self.request, _("Session created successfully."))
        return super().form_valid(form)
