"""
Views for the services app.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    CorporateProgramForm,
    OrganizationForm,
    ProposalForm,
    ServiceCategoryForm,
    ServiceForm,
    ServicePackageForm,
)
from .models import (
    CorporateProgram,
    Organization,
    Proposal,
    Service,
    ServiceCategory,
    ServicePackage,
)


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to require staff access."""

    def test_func(self):
        return self.request.user.is_staff


# Service Category Views
class ServiceCategoryListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """List all service categories."""

    model = ServiceCategory
    context_object_name = "categories"
    template_name = "services/category_list.html"
    ordering = ["name"]


class ServiceCategoryDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Display service category details."""

    model = ServiceCategory
    context_object_name = "category"
    template_name = "services/category_detail.html"


class ServiceCategoryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Create a new service category."""

    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = "services/category_form.html"
    success_url = reverse_lazy("services:category-list")

    def form_valid(self, form):
        """Handle form submission."""
        response = super().form_valid(form)
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "id": self.object.id,
                "name": self.object.name,
            })
        messages.success(
            self.request,
            _('Service category "%(name)s" was created successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class ServiceCategoryAjaxCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Handle AJAX creation of service categories."""

    model = ServiceCategory
    form_class = ServiceCategoryForm

    def form_valid(self, form):
        """Save the form and return JSON response."""
        self.object = form.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "status": "success",
        })

    def form_invalid(self, form):
        """Return JSON response with form errors."""
        return JsonResponse({
            "status": "error",
            "errors": form.errors,
        }, status=400)


class ServiceCategoryUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Update a service category."""

    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = "services/category_form.html"
    success_url = reverse_lazy("services:category-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Service category "%(name)s" was updated successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class ServiceCategoryDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Delete a service category."""
    model = ServiceCategory
    template_name = "services/category_confirm_delete.html"
    success_url = reverse_lazy("services:category-list")

    def delete(self, request, *args, **kwargs):
        """Delete the object and set success message."""
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            _('Service category "%(name)s" was deleted successfully.') % {"name": obj.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


# Service Views
class ServiceListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """List all services."""

    model = Service
    context_object_name = "services"
    template_name = "services/service_list.html"
    ordering = ["category", "name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Our Services"
        context["page_description"] = "Explore our comprehensive wellness solutions"
        return context


class ServiceDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Display service details."""

    model = Service
    context_object_name = "service"
    template_name = "services/service_detail.html"


class ServiceCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Create a new service."""

    model = Service
    form_class = ServiceForm
    template_name = "services/service_form.html"
    success_url = reverse_lazy("services:service-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(self.request, _("Service created successfully."))
        return response


class ServiceUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Update a service."""

    model = Service
    form_class = ServiceForm
    template_name = "services/service_form.html"
    success_url = reverse_lazy("services:service-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Service "%(name)s" was updated successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class ServiceDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Delete a service."""

    model = Service
    template_name = "services/service_confirm_delete.html"
    success_url = reverse_lazy("services:service-list")

    def delete(self, request, *args, **kwargs):
        """Delete the object and set success message."""
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            _('Service "%(name)s" was deleted successfully.') % {"name": obj.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


# Service Package Views
class ServicePackageListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """List all service packages."""

    model = ServicePackage
    context_object_name = "packages"
    template_name = "services/package_list.html"
    ordering = ["service", "name"]


class ServicePackageDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Display service package details."""

    model = ServicePackage
    context_object_name = "package"
    template_name = "services/package_detail.html"


class ServicePackageCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Create a new service package."""

    model = ServicePackage
    form_class = ServicePackageForm
    template_name = "services/package_form.html"
    success_url = reverse_lazy("services:package-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Service package "%(name)s" was created successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class ServicePackageUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Update a service package."""

    model = ServicePackage
    form_class = ServicePackageForm
    template_name = "services/package_form.html"
    success_url = reverse_lazy("services:package-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Service package "%(name)s" was updated successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class ServicePackageDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Delete a service package."""

    model = ServicePackage
    template_name = "services/package_confirm_delete.html"
    success_url = reverse_lazy("services:package-list")

    def delete(self, request, *args, **kwargs):
        """Delete the object and set success message."""
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            _('Service package "%(name)s" was deleted successfully.') % {"name": obj.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


# Corporate Program Views
class CorporateProgramListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """List all corporate programs."""

    model = CorporateProgram
    context_object_name = "programs"
    template_name = "services/program_list.html"
    ordering = ["name"]


class CorporateProgramDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Display corporate program details."""

    model = CorporateProgram
    context_object_name = "program"
    template_name = "services/program_detail.html"


class CorporateProgramCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Create a new corporate program."""

    model = CorporateProgram
    form_class = CorporateProgramForm
    template_name = "services/program_form.html"
    success_url = reverse_lazy("services:program-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Corporate program "%(name)s" was created successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class CorporateProgramUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Update a corporate program."""

    model = CorporateProgram
    form_class = CorporateProgramForm
    template_name = "services/program_form.html"
    success_url = reverse_lazy("services:program-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Corporate program "%(name)s" was updated successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class CorporateProgramDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Delete a corporate program."""
    model = CorporateProgram
    template_name = "services/program_confirm_delete.html"
    success_url = reverse_lazy("services:program-list")

    def delete(self, request, *args, **kwargs):
        """Delete the object and set success message."""
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            _('Corporate program "%(name)s" was deleted successfully.') % {"name": obj.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


# Organization Views
class OrganizationListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """List all organizations."""

    model = Organization
    context_object_name = "organizations"
    template_name = "services/organization_list.html"
    paginate_by = 10


class OrganizationDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Display organization details."""

    model = Organization
    context_object_name = "organization"
    template_name = "services/organization_detail.html"


class OrganizationCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Create a new organization."""

    model = Organization
    form_class = OrganizationForm
    template_name = "services/organization_form.html"
    success_url = reverse_lazy("services:organization-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Organization "%(name)s" was created successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class OrganizationUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Update an organization."""

    model = Organization
    form_class = OrganizationForm
    template_name = "services/organization_form.html"
    success_url = reverse_lazy("services:organization-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Organization "%(name)s" was updated successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class OrganizationDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Delete an organization."""
    model = Organization
    template_name = "services/organization_confirm_delete.html"
    success_url = reverse_lazy("services:organization-list")

    def delete(self, request, *args, **kwargs):
        """Delete the object and set success message."""
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            _('Organization "%(name)s" was deleted successfully.') % {"name": obj.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


# Proposal Views
class ProposalListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """List all proposals."""

    model = Proposal
    context_object_name = "proposals"
    template_name = "services/proposal_list.html"
    ordering = ["-created"]


class ProposalDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Display proposal details."""

    model = Proposal
    context_object_name = "proposal"
    template_name = "services/proposal_detail.html"


class ProposalCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Create a new proposal."""

    model = Proposal
    form_class = ProposalForm
    template_name = "services/proposal_form.html"
    success_url = reverse_lazy("services:proposal-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Proposal "%(name)s" was created successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class ProposalUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Update a proposal."""

    model = Proposal
    form_class = ProposalForm
    template_name = "services/proposal_form.html"
    success_url = reverse_lazy("services:proposal-list")

    def form_valid(self, form):
        """Save the form and set success message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Proposal "%(name)s" was updated successfully.') % {"name": form.instance.name},
            extra_tags="data-message data-message-type=success",
        )
        return response


class ProposalDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Delete a proposal."""
    model = Proposal
    template_name = "services/proposal_confirm_delete.html"
    success_url = reverse_lazy("services:proposal-list")

    def delete(self, request, *args, **kwargs):
        """Delete the object and set success message."""
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            _('Proposal "%(name)s" was deleted successfully.') % {"name": obj.name},
            extra_tags="data-message data-message-type=success",
        )
        return response
