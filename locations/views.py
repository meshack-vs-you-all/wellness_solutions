"""
Views for the locations app.
"""

import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import LocationForm, LocationInstructorForm, LocationServiceForm
from .models import Location, LocationInstructor, LocationService


class LocationListView(LoginRequiredMixin, ListView):
    """Display a list of locations."""
    model = Location
    context_object_name = "locations"
    template_name = "locations/location_list.html"
    paginate_by = 10

    def get_queryset(self):
        """Filter locations based on search query."""
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Locations")
        return context


class LocationDetailView(LoginRequiredMixin, DetailView):
    """Display details of a location."""
    model = Location
    context_object_name = "location"
    template_name = "locations/location_detail.html"

    def get_context_data(self, **kwargs):
        """Add services and instructors to context."""
        context = super().get_context_data(**kwargs)
        context["services"] = self.object.services.all()
        context["instructors"] = self.object.location_instructors.all()
        return context


class LocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create a new location."""
    model = Location
    form_class = LocationForm
    template_name = "locations/location_form.html"
    success_url = reverse_lazy("locations:location-list")
    permission_required = "locations.add_location"

    def get_context_data(self, **kwargs):
        """Add form title and weekdays to context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Add Location")
        context["weekdays"] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return context

    def form_valid(self, form):
        """Process valid form data."""
        messages.success(self.request, _("Location created successfully."))
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        self.object = None
        form_class = self.get_form_class()

        # Get data from request
        if request.content_type == "application/json":
            data = json.loads(request.body)
            form = form_class(data)
            if form.is_valid():
                self.object = form.save()
                return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form = form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class LocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Update an existing location."""
    model = Location
    form_class = LocationForm
    template_name = "locations/location_form.html"
    permission_required = "locations.change_location"

    def get_success_url(self):
        """Return to location detail page after successful update."""
        return reverse_lazy("locations:location-detail",
                          kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add form title and weekdays to context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Location")
        context["weekdays"] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return context

    def form_valid(self, form):
        """Process valid form data."""
        messages.success(self.request, _("Location updated successfully."))
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        self.object = self.get_object()
        form_class = self.get_form_class()

        # Get data from request
        if request.content_type == "application/json":
            data = json.loads(request.body)
            form = form_class(data, instance=self.object)
            if form.is_valid():
                self.object = form.save()
                return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form = form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class LocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a location."""
    model = Location
    template_name = "locations/location_confirm_delete.html"
    success_url = reverse_lazy("locations:location-list")
    permission_required = "locations.delete_location"

    def delete(self, request, *args, **kwargs):
        """Process deletion and add success message."""
        messages.success(request, _("Location deleted successfully."))
        return super().delete(request, *args, **kwargs)


class LocationServiceCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                              CreateView):
    """Create a new location service."""
    model = LocationService
    form_class = LocationServiceForm
    template_name = "locations/locationservice_form.html"
    permission_required = "locations.add_locationservice"

    def get_context_data(self, **kwargs):
        """Add form title and location to context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Add Service to Location")
        context["location"] = Location.objects.get(pk=self.kwargs["location_pk"])
        return context

    def form_valid(self, form):
        """Set location and process valid form data."""
        form.instance.location = Location.objects.get(
            pk=self.kwargs["location_pk"],
        )
        messages.success(self.request, _("Service added successfully."))
        return super().form_valid(form)

    def get_success_url(self):
        """Return to location detail page after successful creation."""
        return reverse_lazy("locations:location-detail",
                          kwargs={"pk": self.kwargs["location_pk"]})

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        self.object = None
        form_class = self.get_form_class()

        # Get data from request
        if request.content_type == "application/json":
            data = json.loads(request.body)
            data["location"] = self.kwargs["location_pk"]
            form = form_class(data)
            if form.is_valid():
                self.object = form.save()
                return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form = form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class LocationServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                              UpdateView):
    """Update an existing location service."""
    model = LocationService
    form_class = LocationServiceForm
    template_name = "locations/locationservice_form.html"
    permission_required = "locations.change_locationservice"

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Location Service")
        return context

    def form_valid(self, form):
        """Process valid form data."""
        messages.success(self.request, _("Service updated successfully."))
        return super().form_valid(form)

    def get_success_url(self):
        """Return to location detail page after successful update."""
        return reverse_lazy("locations:location-detail",
                          kwargs={"pk": self.object.location.pk})

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        self.object = self.get_object()
        form_class = self.get_form_class()

        # Get data from request
        if request.content_type == "application/json":
            data = json.loads(request.body)
            form = form_class(data, instance=self.object)
            if form.is_valid():
                self.object = form.save()
                return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form = form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class LocationServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a location service."""
    model = LocationService
    template_name = "locations/locationservice_confirm_delete.html"
    permission_required = "locations.delete_locationservice"

    def get_success_url(self):
        return reverse_lazy("locations:location-detail",
                          kwargs={"pk": self.object.location.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Service removed from location successfully."))
        return super().delete(request, *args, **kwargs)


class LocationInstructorCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                                 CreateView):
    """Create a new location instructor assignment."""
    model = LocationInstructor
    form_class = LocationInstructorForm
    template_name = "locations/locationinstructor_form.html"
    permission_required = "locations.add_locationinstructor"

    def get_context_data(self, **kwargs):
        """Add form title and location to context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Add Instructor to Location")
        context["location"] = Location.objects.get(pk=self.kwargs["location_pk"])
        return context

    def form_valid(self, form):
        """Set location and process valid form data."""
        form.instance.location = Location.objects.get(
            pk=self.kwargs["location_pk"],
        )
        messages.success(self.request, _("Instructor assigned successfully."))
        return super().form_valid(form)

    def get_success_url(self):
        """Return to location detail page after successful creation."""
        return reverse_lazy("locations:location-detail",
                          kwargs={"pk": self.kwargs["location_pk"]})

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        self.object = None
        form_class = self.get_form_class()

        # Get data from request
        if request.content_type == "application/json":
            data = json.loads(request.body)
            data["location"] = self.kwargs["location_pk"]
            form = form_class(data)
            if form.is_valid():
                self.object = form.save()
                return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form = form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class LocationInstructorUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                                 UpdateView):
    """Update an existing location instructor assignment."""
    model = LocationInstructor
    form_class = LocationInstructorForm
    template_name = "locations/locationinstructor_form.html"
    permission_required = "locations.change_locationinstructor"

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Location Instructor")
        return context

    def form_valid(self, form):
        """Process valid form data."""
        messages.success(self.request, _("Instructor assignment updated successfully."))
        return super().form_valid(form)

    def get_success_url(self):
        """Return to location detail page after successful update."""
        return reverse_lazy("locations:location-detail",
                          kwargs={"pk": self.object.location.pk})

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        self.object = self.get_object()
        form_class = self.get_form_class()

        # Get data from request
        if request.content_type == "application/json":
            data = json.loads(request.body)
            form = form_class(data, instance=self.object)
            if form.is_valid():
                self.object = form.save()
                return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form = form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class LocationInstructorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a location instructor."""
    model = LocationInstructor
    template_name = "locations/locationinstructor_confirm_delete.html"
    permission_required = "locations.delete_locationinstructor"

    def get_success_url(self):
        return reverse_lazy("locations:location-detail",
                          kwargs={"pk": self.object.location.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Instructor removed from location successfully."))
        return super().delete(request, *args, **kwargs)
