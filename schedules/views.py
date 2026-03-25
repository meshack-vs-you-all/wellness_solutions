from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import BlackoutDateForm, ScheduleForm, TimeSlotForm
from .models import BlackoutDate, Schedule, TimeSlot


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = "schedules/schedule_list.html"
    context_object_name = "schedules"

    def get_queryset(self):
        return Schedule.objects.filter(instructor__user=self.request.user)

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = "schedules/schedule_form.html"
    success_url = reverse_lazy("schedules:schedule-list")

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "wellness_instructor"):
            messages.error(request, _("You must be registered as an instructor to create schedules."))
            return redirect("users:instructor_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Schedule created successfully."))
        return super().form_valid(form)

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = "schedules/schedule_form.html"
    success_url = reverse_lazy("schedules:schedule-list")

    def get_queryset(self):
        return Schedule.objects.filter(instructor__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Schedule updated successfully.")
        return super().form_valid(form)

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    template_name = "schedules/schedule_confirm_delete.html"
    success_url = reverse_lazy("schedules:schedule-list")

    def get_queryset(self):
        return Schedule.objects.filter(instructor__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Schedule deleted successfully.")
        return super().delete(request, *args, **kwargs)

class TimeSlotListView(LoginRequiredMixin, ListView):
    model = TimeSlot
    template_name = "schedules/timeslot_list.html"
    context_object_name = "timeslots"

    def get_queryset(self):
        return TimeSlot.objects.filter(schedule__instructor__user=self.request.user)

class TimeSlotCreateView(LoginRequiredMixin, CreateView):
    model = TimeSlot
    form_class = TimeSlotForm
    template_name = "schedules/timeslot_form.html"
    success_url = reverse_lazy("schedules:timeslot-list")

    def form_valid(self, form):
        form.instance.schedule.instructor = self.request.user.instructor
        messages.success(self.request, "Time slot created successfully.")
        return super().form_valid(form)

class TimeSlotUpdateView(LoginRequiredMixin, UpdateView):
    model = TimeSlot
    form_class = TimeSlotForm
    template_name = "schedules/timeslot_form.html"
    success_url = reverse_lazy("schedules:timeslot-list")

    def get_queryset(self):
        return TimeSlot.objects.filter(schedule__instructor__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Time slot updated successfully.")
        return super().form_valid(form)

class TimeSlotDeleteView(LoginRequiredMixin, DeleteView):
    model = TimeSlot
    template_name = "schedules/timeslot_confirm_delete.html"
    success_url = reverse_lazy("schedules:timeslot-list")

    def get_queryset(self):
        return TimeSlot.objects.filter(schedule__instructor__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Time slot deleted successfully."))
        return super().delete(request, *args, **kwargs)

class BlackoutDateListView(LoginRequiredMixin, ListView):
    model = BlackoutDate
    template_name = "schedules/blackoutdate_list.html"
    context_object_name = "blackout_dates"

    def get_queryset(self):
        return BlackoutDate.objects.filter(instructor__user=self.request.user)

class BlackoutDateCreateView(LoginRequiredMixin, CreateView):
    model = BlackoutDate
    form_class = BlackoutDateForm
    template_name = "schedules/blackoutdate_form.html"
    success_url = reverse_lazy("schedules:blackoutdate-list")

    def form_valid(self, form):
        form.instance.instructor = self.request.user.instructor
        messages.success(self.request, "Blackout date created successfully.")
        return super().form_valid(form)

class BlackoutDateUpdateView(LoginRequiredMixin, UpdateView):
    model = BlackoutDate
    form_class = BlackoutDateForm
    template_name = "schedules/blackoutdate_form.html"
    success_url = reverse_lazy("schedules:blackoutdate-list")

    def get_queryset(self):
        return BlackoutDate.objects.filter(instructor__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Blackout date updated successfully.")
        return super().form_valid(form)

class BlackoutDateDeleteView(LoginRequiredMixin, DeleteView):
    model = BlackoutDate
    template_name = "schedules/blackoutdate_confirm_delete.html"
    success_url = reverse_lazy("schedules:blackoutdate-list")

    def get_queryset(self):
        return BlackoutDate.objects.filter(instructor__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Blackout date deleted successfully."))
        return super().delete(request, *args, **kwargs)

class InstructorAvailabilityUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "schedules/instructor_availability_form.html"
    success_url = reverse_lazy("users:instructor_dashboard")

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "wellness_instructor"):
            return redirect("users:client_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.wellness_instructor

    def form_valid(self, form):
        availability = form.cleaned_data.get("availability", {})
        instructor = self.get_object()

        # Update availability
        instructor.availability = availability
        instructor.save()

        messages.success(self.request, "Availability updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
