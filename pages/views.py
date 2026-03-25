from django.views.generic import TemplateView

from .services.models import Service


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.all()[:3]  # Get first 3 services
        return context
