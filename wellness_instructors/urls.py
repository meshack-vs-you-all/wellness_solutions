"""URLs for the wellness_instructors app."""

from django.urls import path

from . import views


app_name = "wellness_instructors"

urlpatterns = [
    # Instructor URLs
    path("", views.InstructorListView.as_view(), name="instructor-list"),
    path("create/", views.InstructorCreateView.as_view(), name="instructor-create"),
    path("<int:pk>/", views.InstructorDetailView.as_view(), name="instructor-detail"),
    path("<int:pk>/update/", views.InstructorUpdateView.as_view(), name="instructor-update"),
    path("<int:pk>/delete/", views.InstructorDeleteView.as_view(), name="instructor-delete"),

    # Session URLs
    path("sessions/", views.SessionListView.as_view(), name="session-list"),
    path("sessions/create/", views.InstructorSessionCreateView.as_view(), name="session-create"),
    path("sessions/<int:pk>/", views.SessionDetailView.as_view(), name="session-detail"),
    path("sessions/<int:pk>/update/", views.SessionUpdateView.as_view(), name="session-update"),
    path("sessions/<int:pk>/delete/", views.SessionDeleteView.as_view(), name="session-delete"),
]
