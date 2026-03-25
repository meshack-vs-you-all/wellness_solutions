"""
Decorators for error handling and validation.
"""

import functools
import logging

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from .exceptions import (
    BaseAppError,
    format_error_response,
    handle_validation_error,
)


logger = logging.getLogger(__name__)


def handle_errors(view_func):
    """
    Decorator for handling errors in view functions.
    
    Usage:
        @handle_errors
        def my_view(request):
            # View logic here
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {view_func.__name__}: {str(e)}")
            if isinstance(e, ValidationError):
                return JsonResponse(
                    handle_validation_error(e),
                    status=400,
                )
            if isinstance(e, BaseAppError):
                return JsonResponse(
                    format_error_response(e),
                    status=getattr(e, "status_code", 400),
                )
            return JsonResponse({
                "error": "Internal Server Error",
                "message": _("An unexpected error occurred."),
            }, status=500)
    return wrapper


def validate_request(*validators):
    """
    Decorator for applying multiple validators to a request.
    
    Usage:
        @validate_request(validate_user, validate_input)
        def my_view(request):
            # View logic here
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            for validator in validators:
                try:
                    validator(request, *args, **kwargs)
                except ValidationError as e:
                    return JsonResponse(
                        handle_validation_error(e),
                        status=400,
                    )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_fields(*fields):
    """
    Decorator to validate required fields in request data.
    
    Usage:
        @require_fields('name', 'email')
        def my_view(request):
            # View logic here
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            data = request.POST or request.GET or request.data
            missing_fields = [
                field for field in fields
                if field not in data or not data[field]
            ]
            if missing_fields:
                raise ValidationError({
                    "missing_fields": [
                        f"Field {field} is required"
                        for field in missing_fields
                    ],
                })
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def log_errors(logger_name=None):
    """
    Decorator to log errors with custom logger.
    
    Usage:
        @log_errors('my_logger')
        def my_view(request):
            # View logic here
    """
    def decorator(view_func):
        error_logger = logging.getLogger(logger_name or __name__)

        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            try:
                return view_func(*args, **kwargs)
            except Exception as e:
                error_logger.exception(
                    f"Error in {view_func.__name__}: {str(e)}",
                )
                raise
        return wrapper
    return decorator
