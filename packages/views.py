"""Views for the packages app."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ClientPackageForm, PackageForm
from .models import ClientPackage, Package


class PackageListView(LoginRequiredMixin, ListView):
    """List all packages."""

    model = Package
    context_object_name = "packages"
    template_name = "packages/package_list.html"
    paginate_by = 20

    def get_queryset(self):
        """Filter packages based on user permissions."""
        queryset = Package.objects.select_related("service_package", "organization")

        if not self.request.user.is_staff:
            # Regular users only see their packages or ones they're assigned to
            queryset = queryset.filter(
                Q(owner=self.request.user) |
                Q(client_assignments__client=self.request.user),
                active=True,
            ).distinct()

        return queryset


class PackageDetailView(LoginRequiredMixin, DetailView):
    """View package details."""

    model = Package
    context_object_name = "package"
    template_name = "packages/package_detail.html"

    def get_context_data(self, **kwargs):
        """Add additional context."""
        context = super().get_context_data(**kwargs)
        context["bookings"] = self.object.bookings.select_related(
            "service", "instructor",
        ).order_by("-start_time")
        return context


class PackageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new package."""

    model = Package
    form_class = PackageForm
    template_name = "packages/package_form.html"
    success_url = reverse_lazy("packages:list")

    def test_func(self):
        """Only staff can create packages."""
        return self.request.user.is_staff

    def form_valid(self, form):
        """Process the valid form data."""
        messages.success(
            self.request,
            _("Package created successfully."),
        )
        return super().form_valid(form)


class PackageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing package."""

    model = Package
    form_class = PackageForm
    template_name = "packages/package_form.html"
    success_url = reverse_lazy("packages:list")

    def test_func(self):
        """Only staff can update packages."""
        return self.request.user.is_staff

    def form_valid(self, form):
        """Process the valid form data."""
        messages.success(
            self.request,
            _("Package updated successfully."),
        )
        return super().form_valid(form)


class PackageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a package."""

    model = Package
    success_url = reverse_lazy("packages:list")

    def test_func(self):
        """Only staff can delete packages."""
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Package deleted successfully."))
        return super().delete(request, *args, **kwargs)


class ClientPackageListView(LoginRequiredMixin, ListView):
    """List packages assigned to clients."""

    model = ClientPackage
    context_object_name = "client_packages"
    template_name = "packages/client_package_list.html"
    paginate_by = 20

    def get_queryset(self):
        """Filter client packages based on user permissions."""
        queryset = ClientPackage.objects.select_related(
            "client", "package", "package__service_package",
        )

        if not self.request.user.is_staff:
            # Regular users only see their assignments
            queryset = queryset.filter(
                Q(client=self.request.user) |
                Q(package__owner=self.request.user),
            )

        return queryset


class ClientPackageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Assign a package to a client."""

    model = ClientPackage
    form_class = ClientPackageForm
    template_name = "packages/client_package_form.html"
    success_url = reverse_lazy("packages:client-list")

    def test_func(self):
        """Only staff can assign packages."""
        return self.request.user.is_staff

    def get_form_kwargs(self):
        """Pass the current user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Process the valid form data."""
        form.instance.assigned_by = self.request.user
        messages.success(
            self.request,
            _("Package assigned successfully."),
        )
        return super().form_valid(form)
