from django.urls import path

from . import views


app_name = "schedules"

urlpatterns = [
    # Schedule URLs
    path("schedules/", views.ScheduleListView.as_view(), name="schedule-list"),
    path("schedules/create/", views.ScheduleCreateView.as_view(), name="schedule-create"),
    path("schedules/<int:pk>/update/", views.ScheduleUpdateView.as_view(), name="schedule-update"),
    path("schedules/<int:pk>/delete/", views.ScheduleDeleteView.as_view(), name="schedule-delete"),

    # TimeSlot URLs
    path("timeslots/", views.TimeSlotListView.as_view(), name="timeslot-list"),
    path("timeslots/create/", views.TimeSlotCreateView.as_view(), name="timeslot-create"),
    path("timeslots/<int:pk>/update/", views.TimeSlotUpdateView.as_view(), name="timeslot-update"),
    path("timeslots/<int:pk>/delete/", views.TimeSlotDeleteView.as_view(), name="timeslot-delete"),

    # BlackoutDate URLs
    path("blackout-dates/", views.BlackoutDateListView.as_view(), name="blackoutdate-list"),
    path("blackout-dates/create/", views.BlackoutDateCreateView.as_view(), name="blackoutdate-create"),
    path("blackout-dates/<int:pk>/update/", views.BlackoutDateUpdateView.as_view(), name="blackoutdate-update"),
    path("blackout-dates/<int:pk>/delete/", views.BlackoutDateDeleteView.as_view(), name="blackoutdate-delete"),

    # Instructor Availability URLs
    path("instructor/availability/update/", views.InstructorAvailabilityUpdateView.as_view(), name="instructor-availability-update"),
]
