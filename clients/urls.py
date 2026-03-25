from django.urls import path

from . import views


app_name = "clients"

urlpatterns = [
    path(
        "",
        view=views.ClientListView.as_view(),
        name="client-list",
    ),
    path(
        "profile/<int:pk>/",
        view=views.ClientProfileDetailView.as_view(),
        name="client-detail",
    ),
    path(
        "profile/<int:pk>/edit/",
        view=views.ClientProfileUpdateView.as_view(),
        name="client-update",
    ),
    path(
        "session/<int:pk>/",
        view=views.ClientSessionDetailView.as_view(),
        name="session-detail",
    ),
    path(
        "session/<int:pk>/edit/",
        view=views.ClientSessionUpdateView.as_view(),
        name="session-update",
    ),
    path(
        "session/<int:pk>/feedback/",
        view=views.SessionFeedbackView.as_view(),
        name="session-feedback",
    ),
]
