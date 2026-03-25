from django.urls import path

from .views import (
    AdminDashboardView,
    ClientDashboardView,
    DashboardView,
    InstructorDashboardView,
    email_preferences_view,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)


app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("update-profile/", view=user_update_view, name="update-profile"),
    path("email-preferences/", view=email_preferences_view, name="email-preferences"),
    path("<int:pk>/", view=user_detail_view, name="detail"),

    # Dashboard URLs
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/admin/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("dashboard/instructor/", InstructorDashboardView.as_view(), name="instructor_dashboard"),
    path("dashboard/client/", ClientDashboardView.as_view(), name="client_dashboard"),

    # Instructor URLs
    path("instructor/profile/update/", view=user_update_view, name="instructor-profile-update"),
]
