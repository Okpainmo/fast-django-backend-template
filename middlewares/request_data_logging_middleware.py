"""
Global Django Middleware for Request Duration Logging

This middleware tracks and logs the duration of each HTTP request processed by the application.
It measures the time between when a request starts and when it completes, providing
valuable insights into request processing times and potential performance bottlenecks.

The middleware:
1. Records the start time when a request begins processing
2. Calculates the total duration when the request completes
3. Logs both the start and end of each request with timing information

Usage:
    Already added: 'middlewares.global__request_duration_logging_middleware.RequestDurationLoggingMiddleware'
    See MIDDLEWARE settings in "settings => base.py"
"""

import time
from django.utils.deprecation import MiddlewareMixin
from utils.logger import logger

log = logger()


class RequestDataLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        # log.info(f"⏱️ Request started: {request.method} {request.path}")
        log.info(f"Request started: {request.method} {request.path}")

    def process_response(self, request, response):
        duration = time.time() - getattr(request, "start_time", time.time())
        # log.info(f"✅ Request finished: {request.method} {request.path} ({duration:.2f}s)")
        log.info(f"Request finished: {request.method} {request.path} ({duration:.2f}s)")
        return response
