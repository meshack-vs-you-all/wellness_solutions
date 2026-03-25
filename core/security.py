"""
Security middleware and utilities.
"""

import re

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin


class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers and perform security checks.
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

        # Compile patterns for sensitive data
        self.sensitive_patterns = [
            re.compile(pattern) for pattern in [
                r"\b\d{16}\b",  # Credit card numbers
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email addresses
                r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
                r"\b\d{10}\b",  # Phone numbers
            ]
        ]

    def __call__(self, request):
        # Check for suspicious patterns in URL
        path = request.path_info.lower()
        if any(x in path for x in ["../", ";\\"]):
            raise PermissionDenied("Invalid URL")

        # Get response
        response = self.get_response(request)

        # Add security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=()"

        # Add CSP header in non-debug mode
        if not settings.DEBUG:
            csp_policies = [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
                "style-src 'self' 'unsafe-inline'",
                "img-src 'self' data: https:",
                "font-src 'self'",
                "frame-src 'self'",
                "connect-src 'self'",
            ]
            response["Content-Security-Policy"] = "; ".join(csp_policies)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Check for sensitive data in GET parameters.
        """
        if request.GET:
            for key, value in request.GET.items():
                if any(pattern.search(str(value)) for pattern in self.sensitive_patterns):
                    raise PermissionDenied("Invalid request parameters")
        return


def sanitize_input(value):
    """
    Sanitize user input to prevent XSS and injection attacks.
    """
    if not isinstance(value, str):
        return value

    # List of patterns to sanitize
    patterns = [
        (r"<script.*?>.*?</script>", ""),  # Remove script tags
        (r"<.*?javascript:.*?>", ""),  # Remove javascript in tags
        (r"<.*?style=.*?>", ""),  # Remove style attributes
        (r'<.*?on\w+=".*?".*?>', ""),  # Remove event handlers
        (r"<!--.*?-->", ""),  # Remove comments
    ]

    sanitized = value
    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE | re.DOTALL)

    return sanitized


def validate_file_upload(file):
    """
    Validate file uploads for security.
    """
    # Maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        ".jpg", ".jpeg", ".png", ".gif", ".pdf",
        ".doc", ".docx", ".txt", ".csv",
    }

    # Check file size
    if file.size > MAX_FILE_SIZE:
        raise PermissionDenied("File too large")

    # Check file extension
    filename = file.name.lower()
    ext = "." + filename.split(".")[-1] if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise PermissionDenied("Invalid file type")

    # Check file content (basic MIME type check)
    content_type = file.content_type.lower()
    if not any(x in content_type for x in ["image/", "application/", "text/"]):
        raise PermissionDenied("Invalid file content")

    return True
