"""URLs for the packages app."""

from django.urls import path

from . import views


app_name = "packages"

urlpatterns = [
    # Package management
    path("", views.PackageListView.as_view(), name="list"),
    path("create/", views.PackageCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PackageDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.PackageUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.PackageDeleteView.as_view(), name="delete"),

    # Client package assignments
    path("clients/", views.ClientPackageListView.as_view(), name="client-list"),
    path("clients/assign/", views.ClientPackageCreateView.as_view(), name="client-assign"),
]
