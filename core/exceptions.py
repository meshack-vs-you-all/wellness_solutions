"""
Core exceptions and error handling utilities.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class BaseAppError(Exception):
    """Base exception class for application errors."""
    def __init__(self, message, code=None, params=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.params = params or {}


class BusinessLogicError(BaseAppError):
    """Exception for business logic violations."""


class ResourceNotFoundError(BaseAppError):
    """Exception for missing resources."""


class InvalidOperationError(BaseAppError):
    """Exception for invalid operations."""


class PermissionDeniedError(BaseAppError):
    """Exception for permission/authorization errors."""


class DataIntegrityError(BaseAppError):
    """Exception for data integrity violations."""


class ServiceUnavailableError(BaseAppError):
    """Exception for service availability issues."""


class RateLimitExceededError(BaseAppError):
    """Exception for rate limit violations."""


class APIError(APIException):
    """Base API exception with status code support."""
    def __init__(self, message, code=None, status_code=None):
        super().__init__(message)
        self.status_code = status_code or status.HTTP_400_BAD_REQUEST
        self.code = code


def handle_validation_error(error):
    """Convert ValidationError to a formatted error response."""
    if hasattr(error, "message_dict"):
        return {
            "error": "Validation Error",
            "details": error.message_dict,
        }
    return {
        "error": "Validation Error",
        "details": list(error.messages),
    }


def handle_database_error(error):
    """Handle database-related errors."""
    return {
        "error": "Database Error",
        "message": _("A database error occurred. Please try again."),
        "details": str(error),
    }


def handle_permission_error(error):
    """Handle permission-related errors."""
    return {
        "error": "Permission Denied",
        "message": str(error) or _("You do not have permission to perform this action."),
        "code": getattr(error, "code", None),
    }


def handle_not_found_error(error):
    """Handle resource not found errors."""
    return {
        "error": "Not Found",
        "message": str(error) or _("The requested resource was not found."),
        "code": getattr(error, "code", None),
    }


def handle_rate_limit_error(error):
    """Handle rate limit errors."""
    return {
        "error": "Rate Limit Exceeded",
        "message": str(error) or _("Too many requests. Please try again later."),
        "code": getattr(error, "code", None),
    }


def format_error_response(error, status_code=400):
    """Format error response with consistent structure."""
    return {
        "status": "error",
        "code": status_code,
        "message": str(error),
        "details": getattr(error, "params", None),
    }
