from django.urls import path
from .views import CreateCheckoutSessionView, stripe_webhook

app_name = "payments"

urlpatterns = [
    path("checkout-session/", CreateCheckoutSessionView.as_view(), name="create_checkout_session"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
]
