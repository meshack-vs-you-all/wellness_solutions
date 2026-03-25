"""
URL configuration for the locations app.
"""

from django.urls import path

from . import views


app_name = "locations"

urlpatterns = [
    # Location views
    path("",
         views.LocationListView.as_view(),
         name="location-list"),
    path("create/",
         views.LocationCreateView.as_view(),
         name="location-create"),
    path("<int:pk>/",
         views.LocationDetailView.as_view(),
         name="location-detail"),
    path("<int:pk>/update/",
         views.LocationUpdateView.as_view(),
         name="location-update"),
    path("<int:pk>/delete/",
         views.LocationDeleteView.as_view(),
         name="location-delete"),

    # Location service management
    path("<int:location_pk>/services/add/",
         views.LocationServiceCreateView.as_view(),
         name="location-service-create"),
    path("services/<int:pk>/update/",
         views.LocationServiceUpdateView.as_view(),
         name="location-service-update"),
    path("services/<int:pk>/delete/",
         views.LocationServiceDeleteView.as_view(),
         name="location-service-delete"),

    # Location instructor management
    path("<int:location_pk>/instructors/add/",
         views.LocationInstructorCreateView.as_view(),
         name="location-instructor-create"),
    path("instructors/<int:pk>/update/",
         views.LocationInstructorUpdateView.as_view(),
         name="location-instructor-update"),
    path("instructors/<int:pk>/delete/",
         views.LocationInstructorDeleteView.as_view(),
         name="location-instructor-delete"),
]
