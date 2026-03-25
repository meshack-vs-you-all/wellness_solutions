"""
Middleware for handling errors and exceptions.
"""

import logging
import traceback

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.db import DatabaseError
from django.http import Http404, JsonResponse
from django.utils.translation import gettext_lazy as _

from .exceptions import (
    BusinessLogicError,
    DataIntegrityError,
    InvalidOperationError,
    PermissionDeniedError,
    RateLimitExceededError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    format_error_response,
    handle_database_error,
    handle_not_found_error,
    handle_permission_error,
    handle_rate_limit_error,
    handle_validation_error,
)


logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    """Middleware for consistent error handling across the application."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """Process exceptions and return appropriate responses."""

        # Skip handling for admin site
        if request.path.startswith("/admin/"):
            return None

        # Initialize error response
        error_response = None
        status_code = 500

        try:
            if isinstance(exception, ValidationError):
                error_response = handle_validation_error(exception)
                status_code = 400

            elif isinstance(exception, PermissionDenied):
                error_response = handle_permission_error(exception)
                status_code = 403

            elif isinstance(exception, Http404) or isinstance(exception, ObjectDoesNotExist):
                error_response = handle_not_found_error(exception)
                status_code = 404

            elif isinstance(exception, DatabaseError):
                error_response = handle_database_error(exception)
                status_code = 500
                logger.error(f"Database error: {str(exception)}\n{traceback.format_exc()}")

            elif isinstance(exception, BusinessLogicError):
                error_response = format_error_response(exception, 400)
                status_code = 400

            elif isinstance(exception, ResourceNotFoundError):
                error_response = handle_not_found_error(exception)
                status_code = 404

            elif isinstance(exception, InvalidOperationError):
                error_response = format_error_response(exception, 400)
                status_code = 400

            elif isinstance(exception, PermissionDeniedError):
                error_response = handle_permission_error(exception)
                status_code = 403

            elif isinstance(exception, DataIntegrityError):
                error_response = format_error_response(exception, 409)
                status_code = 409

            elif isinstance(exception, ServiceUnavailableError):
                error_response = format_error_response(exception, 503)
                status_code = 503

            elif isinstance(exception, RateLimitExceededError):
                error_response = handle_rate_limit_error(exception)
                status_code = 429

            else:
                # Handle unexpected errors
                logger.error(f"Unexpected error: {str(exception)}\n{traceback.format_exc()}")
                error_response = {
                    "error": "Internal Server Error",
                    "message": _("An unexpected error occurred. Please try again later."),
                }
                status_code = 500

            # Log all errors except validation errors
            if status_code >= 500:
                logger.error(
                    f"Error processing request to {request.path}: {str(exception)}\n"
                    f"Status Code: {status_code}\n"
                    f"User: {request.user}\n"
                    f"Method: {request.method}\n"
                    f"Traceback: {traceback.format_exc()}",
                )

            # Return JSON response for API requests
            if request.headers.get("Accept") == "application/json" or request.path.startswith("/api/"):
                return JsonResponse(error_response, status=status_code)

            # For regular requests, add error to messages and let Django handle the response
            from django.contrib import messages
            messages.error(request, error_response.get("message", str(exception)))
            return None

        except Exception as e:
            # Handle errors in the error handler itself
            logger.critical(
                f"Error in error handling middleware: {str(e)}\n{traceback.format_exc()}",
            )
            return JsonResponse(
                {
                    "error": "Critical Error",
                    "message": _("A critical error occurred. Please try again later."),
                },
                status=500,
            )
