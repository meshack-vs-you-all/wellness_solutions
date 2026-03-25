"""
Performance optimization utilities and decorators.
"""

import logging
import time
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.db import connection


logger = logging.getLogger(__name__)


def cache_response(timeout=settings.CACHE_TTL, key_prefix="view"):
    """
    Cache the response of a view for a specified time.
    
    Usage:
        @cache_response(timeout=300)
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{request.path}:{request.user.id}"

            # Try to get cached response
            response = cache.get(cache_key)
            if response is not None:
                return response

            # Generate response and cache it
            response = view_func(request, *args, **kwargs)
            cache.set(cache_key, response, timeout)

            return response
        return _wrapped_view
    return decorator


def query_debugger(func):
    """
    Debug database queries for a view.
    
    Usage:
        @query_debugger
        def my_view(request):
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_queries = len(connection.queries)
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        end_queries = len(connection.queries)

        logger.debug(f"""
        Function: {func.__name__}
        Number of Queries: {end_queries - start_queries}
        Execution Time: {(end_time - start_time):.3f}s
        """)

        return result
    return wrapper


def optimize_queryset(queryset, select_related=None, prefetch_related=None):
    """
    Optimize a queryset with select_related and prefetch_related.
    
    Usage:
        queryset = optimize_queryset(
            User.objects.all(),
            select_related=['profile'],
            prefetch_related=['groups']
        )
    """
    if select_related:
        queryset = queryset.select_related(*select_related)
    if prefetch_related:
        queryset = queryset.prefetch_related(*prefetch_related)
    return queryset


def bulk_create_context(objects, batch_size=1000):
    """
    Context manager for efficient bulk creation of objects.
    
    Usage:
        with bulk_create_context(Model) as bulk_creator:
            for item in items:
                bulk_creator.add(Model(field=value))
    """
    class BulkCreator:
        def __init__(self, model_class, batch_size):
            self.model_class = model_class
            self.batch_size = batch_size
            self.objects = []

        def add(self, obj):
            self.objects.append(obj)
            if len(self.objects) >= self.batch_size:
                self.flush()

        def flush(self):
            if self.objects:
                self.model_class.objects.bulk_create(self.objects)
                self.objects = []

    return BulkCreator(objects, batch_size)


def lazy_load(queryset, chunk_size=1000):
    """
    Generator for lazy loading of large querysets.
    
    Usage:
        for item in lazy_load(Model.objects.all()):
            process(item)
    """
    start = 0
    while True:
        chunk = list(queryset[start:start + chunk_size])
        if not chunk:
            break
        yield from chunk
        start += chunk_size


class QueryOptimizer:
    """
    Context manager for optimizing database queries.
    
    Usage:
        with QueryOptimizer() as optimizer:
            # Your database operations here
            results = optimizer.get_stats()
    """

    def __init__(self):
        self.start_queries = 0
        self.start_time = 0

    def __enter__(self):
        self.start_queries = len(connection.queries)
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False

        end_time = time.time()
        end_queries = len(connection.queries)

        self.stats = {
            "query_count": end_queries - self.start_queries,
            "execution_time": end_time - self.start_time,
        }

        return True

    def get_stats(self):
        return self.stats
