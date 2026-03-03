from rest_framework.views import exception_handler


def envelope_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    # If already normalized, keep as-is.
    if isinstance(response.data, dict) and 'error' in response.data and len(response.data) == 1:
        return response

    response.data = {'error': response.data}
    return response
