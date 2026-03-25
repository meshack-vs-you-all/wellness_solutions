from django.urls import path

from . import views


app_name = "docs"

urlpatterns = [
    path("", views.DocumentationView.as_view(), name="documentation"),
]
