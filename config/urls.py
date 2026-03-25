"""
URL Configuration for wellness_solutions project.
"""
# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from services.models import Service

class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()[:6]  # Limit to 6 services for the homepage
        return context

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "success-stories/",
        TemplateView.as_view(template_name="pages/success_stories.html"),
        name="success_stories",
    ),
    path(
        "partnerships/",
        TemplateView.as_view(template_name="pages/partnerships.html"),
        name="partnerships",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="pages/contact.html"),
        name="contact",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("docs/", include("docs.urls", namespace="docs")),
    path("instructors/", include("wellness_instructors.urls", namespace="wellness_instructors")),
    path("schedule/", include("schedules.urls", namespace="schedules")),
    path("bookings/", include("bookings.urls", namespace="bookings")),
    path("packages/", include("packages.urls", namespace="packages")),
    path("services/", include("services.urls", namespace="services")),
    path("locations/", include("locations.urls", namespace="locations")),
    path("clients/", include("clients.urls", namespace="clients")),
    path("payments/", include("payments.urls", namespace="payments")),
    path(
        "consultation/",
        TemplateView.as_view(template_name="pages/consultation.html"),
        name="consultation",
    ),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# Import custom API views
from api_views import (
    register_view, login_view, LogoutView, ClassViewSet, BookingViewSet,
    analytics_view, instructor_classes_view,
    notifications_view, shop_products_view, organization_register_view,
    trainer_availability_view, admin_users_view, admin_toggle_user_view,
    admin_export_users_csv_view, admin_all_bookings_view, update_profile_view, 
    instructor_bookings_view, calendar_export_view,
    ai_smart_rebook_view, ai_therapist_match_view, ai_session_insights_view,
)
from rest_framework.routers import DefaultRouter

# Create a router for ViewSets
api_router = DefaultRouter()
api_router.register(r'classes', ClassViewSet, basename='class')
api_router.register(r'bookings', BookingViewSet, basename='booking')

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # Custom API endpoints
    path("api/", include(api_router.urls)),
    path("api/auth/register/", register_view, name="api-register"),
    path("api/auth/logout/", LogoutView.as_view(), name="api-logout"),
    path("api/analytics/", analytics_view, name="api-analytics"),
    path("api/instructor/classes/", instructor_classes_view, name="api-instructor-classes"),
    # Auth endpoints
    path("api/auth-token/", login_view, name="api-login"),
    # New extended endpoints
    path("api/notifications/", notifications_view, name="api-notifications"),
    path("api/shop/products/", shop_products_view, name="api-shop-products"),
    path("api/organizations/register/", organization_register_view, name="api-org-register"),
    path("api/trainers/availability/", trainer_availability_view, name="api-trainer-availability"),
    path("api/admin/users/", admin_users_view, name="api-admin-users"),
    path("api/admin/users/export/csv/", admin_export_users_csv_view, name="api-admin-users-export-csv"),
    path("api/admin/users/<int:user_id>/toggle/", admin_toggle_user_view, name="api-admin-user-toggle"),
    path("api/admin/bookings/", admin_all_bookings_view, name="api-admin-bookings"),
    path("api/users/me/update/", update_profile_view, name="api-user-profile-update"),
    path("api/instructor/bookings/", instructor_bookings_view, name="api-instructor-bookings"),
    path("api/calendar/export/", calendar_export_view, name="api-calendar-export"),
    # AI Powered Features
    path("api/ai/rebook/", ai_smart_rebook_view, name="api-ai-rebook"),
    path("api/ai/match/", ai_therapist_match_view, name="api-ai-match"),
    path("api/ai/insights/<int:booking_id>/", ai_session_insights_view, name="api-ai-insights"),
    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls)), 
                       path("__reload__/", include("django_browser_reload.urls"))] + urlpatterns
