from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import RedirectView


class DocumentationView(UserPassesTestMixin, RedirectView):
    """View to handle documentation access.
    
    This view:
    1. Checks if the user has permission to access the docs
    2. Redirects to the documentation server
    """

    def test_func(self):
        """Check if user has permission to access docs."""
        if not settings.DOCS_ACCESS_STAFF_ONLY:
            return self.request.user.is_authenticated
        return (
            self.request.user.is_authenticated and
            (self.request.user.is_staff or self.request.user.is_superuser)
        )

    def get_redirect_url(self, *args, **kwargs):
        """Return the documentation URL."""
        return settings.DOCS_SERVER_URL
