"""
URL configuration for the services app.
"""

from django.urls import path

from . import views


app_name = "services"

urlpatterns = [
    # Service Categories
    path(
        "categories/",
        views.ServiceCategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "categories/<int:pk>/",
        views.ServiceCategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "categories/create/",
        views.ServiceCategoryCreateView.as_view(),
        name="category-create",
    ),
    path(
        "categories/create/ajax/",
        views.ServiceCategoryAjaxCreateView.as_view(),
        name="category-create-ajax",
    ),
    path(
        "categories/<int:pk>/update/",
        views.ServiceCategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.ServiceCategoryDeleteView.as_view(),
        name="category-delete",
    ),

    # Services
    path("", views.ServiceListView.as_view(), name="service-list"),
    path("create/", views.ServiceCreateView.as_view(), name="service-create"),
    path("<int:pk>/", views.ServiceDetailView.as_view(), name="service-detail"),
    path("<int:pk>/update/", views.ServiceUpdateView.as_view(), name="service-update"),
    path("<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="service-delete"),

    # Service Packages
    path(
        "packages/",
        views.ServicePackageListView.as_view(),
        name="package-list",
    ),
    path(
        "packages/<int:pk>/",
        views.ServicePackageDetailView.as_view(),
        name="package-detail",
    ),
    path(
        "packages/create/",
        views.ServicePackageCreateView.as_view(),
        name="package-create",
    ),
    path(
        "packages/<int:pk>/update/",
        views.ServicePackageUpdateView.as_view(),
        name="package-update",
    ),
    path(
        "packages/<int:pk>/delete/",
        views.ServicePackageDeleteView.as_view(),
        name="package-delete",
    ),

    # Corporate Programs
    path(
        "programs/",
        views.CorporateProgramListView.as_view(),
        name="program-list",
    ),
    path(
        "programs/<int:pk>/",
        views.CorporateProgramDetailView.as_view(),
        name="program-detail",
    ),
    path(
        "programs/create/",
        views.CorporateProgramCreateView.as_view(),
        name="program-create",
    ),
    path(
        "programs/<int:pk>/update/",
        views.CorporateProgramUpdateView.as_view(),
        name="program-update",
    ),
    path(
        "programs/<int:pk>/delete/",
        views.CorporateProgramDeleteView.as_view(),
        name="program-delete",
    ),

    # Organizations
    path(
        "organizations/",
        views.OrganizationListView.as_view(),
        name="organization-list",
    ),
    path(
        "organizations/<int:pk>/",
        views.OrganizationDetailView.as_view(),
        name="organization-detail",
    ),
    path(
        "organizations/create/",
        views.OrganizationCreateView.as_view(),
        name="organization-create",
    ),
    path(
        "organizations/<int:pk>/update/",
        views.OrganizationUpdateView.as_view(),
        name="organization-update",
    ),
    path(
        "organizations/<int:pk>/delete/",
        views.OrganizationDeleteView.as_view(),
        name="organization-delete",
    ),

    # Proposals
    path(
        "proposals/",
        views.ProposalListView.as_view(),
        name="proposal-list",
    ),
    path(
        "proposals/<int:pk>/",
        views.ProposalDetailView.as_view(),
        name="proposal-detail",
    ),
    path(
        "proposals/create/",
        views.ProposalCreateView.as_view(),
        name="proposal-create",
    ),
    path(
        "proposals/<int:pk>/update/",
        views.ProposalUpdateView.as_view(),
        name="proposal-update",
    ),
    path(
        "proposals/<int:pk>/delete/",
        views.ProposalDeleteView.as_view(),
        name="proposal-delete",
    ),
]
