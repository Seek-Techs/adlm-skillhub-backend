import logging
import time
import uuid


logger = logging.getLogger('request')


class RequestObservabilityMiddleware:
    """Attach a request id and emit structured request completion logs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        request.request_id = request_id

        response = self.get_response(request)

        duration_ms = (time.perf_counter() - start) * 1000
        response['X-Request-ID'] = request_id

        logger.info(
            'request_completed request_id=%s method=%s path=%s status=%s duration_ms=%.2f',
            request_id,
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )

        return response
