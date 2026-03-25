from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ClientProfileForm, ClientSessionForm, SessionFeedbackForm
from .models import ClientProfile, ClientSession


class ClientProfileMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure users can only access their own profiles."""

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied(_("You don't have permission to access this profile."))


class ClientProfileDetailView(ClientProfileMixin, DetailView):
    model = ClientProfile
    context_object_name = "client"
    template_name = "clients/client_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_sessions"] = self.object.sessions.all()[:5]
        return context


class ClientProfileUpdateView(ClientProfileMixin, UpdateView):
    model = ClientProfile
    form_class = ClientProfileForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client-detail")

    def get_success_url(self):
        return reverse_lazy("clients:client-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _("Your profile has been updated successfully."))
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = ClientProfile
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        if self.request.user.is_staff:
            return ClientProfile.objects.all()
        return ClientProfile.objects.filter(user=self.request.user)


class ClientSessionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClientSession
    context_object_name = "session"
    template_name = "clients/session_detail.html"

    def test_func(self):
        obj = self.get_object()
        return (obj.client.user == self.request.user or
                self.request.user.is_staff or
                self.request.user == obj.booking.instructor.user)


class ClientSessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClientSession
    form_class = ClientSessionForm
    template_name = "clients/session_form.html"

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or self.request.user == obj.booking.instructor.user

    def form_valid(self, form):
        messages.success(self.request, _("Session has been updated successfully."))
        return super().form_valid(form)


class SessionFeedbackView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClientSession
    form_class = SessionFeedbackForm
    template_name = "clients/session_feedback.html"

    def test_func(self):
        obj = self.get_object()
        return obj.client.user == self.request.user

    def form_valid(self, form):
        form.instance.status = "completed"
        messages.success(self.request, _("Thank you for your feedback!"))
        return super().form_valid(form)
