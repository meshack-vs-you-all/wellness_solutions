"""
URL configuration for the bookings app.
"""

from django.urls import path

from . import api, views


app_name = "bookings"

urlpatterns = [
    # Booking URLs
    path("", views.BookingListView.as_view(), name="booking-list"),
    path("create/", views.BookingCreateView.as_view(), name="booking-create"),
    path("<int:pk>/", views.BookingDetailView.as_view(), name="booking-detail"),
    path("<int:pk>/update/", views.BookingUpdateView.as_view(), name="booking-update"),
    path("<int:pk>/cancel/", views.BookingCancelView.as_view(), name="booking-cancel"),
    path("<int:pk>/payment/", views.BookingPaymentView.as_view(), name="booking-payment"),
    path("time-slots/", views.get_time_slots, name="time-slots"),
    path("completed-sessions/", views.CompletedSessionsView.as_view(), name="completed-sessions"),
    path("upcoming-sessions/", views.UpcomingSessionsView.as_view(), name="upcoming-sessions"),
    path("history/", views.BookingHistoryView.as_view(), name="booking-history"),

    # Instructor-specific URLs
    path("instructor/clients/", views.InstructorClientListView.as_view(), name="instructor-clients"),
    path("instructor/clients/<int:pk>/", views.InstructorClientDetailView.as_view(), name="instructor-client-detail"),

    # API URLs
    path("api/check-availability/", api.check_availability, name="check-availability"),
    path("api/locations/<int:location_id>/services/", api.LocationServiceList.as_view(), name="location-services"),
    path("api/locations/<int:location_id>/instructors/", api.LocationInstructorList.as_view(), name="location-instructors"),
]
