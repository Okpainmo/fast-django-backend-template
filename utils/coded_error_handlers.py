from typing import Any
from django.http import HttpResponse, JsonResponse
from .logger import logger

log = logger()

def error_handler_500(error: Any) -> JsonResponse:
    """
    Handle 500 Internal Server Error responses.
    
    Args:
        error: The error that occurred
        response: Django HttpResponse object
    
    Returns:
        JsonResponse with error details
    """
    if isinstance(error, Exception):
        log.error("Error", error=str(error))
        return JsonResponse({
            'response_message': 'Request was unsuccessful: internal server error',
            'error': str(error)
        }, status=500)
    else:
        log.error("Error", error=str(error))
        return JsonResponse({
            'response_message': 'Request was unsuccessful: internal server error',
            'error': str(error)
        }, status=500)

def error_handler_403(error_message: Any) -> JsonResponse:
    """
    Handle 403 Forbidden responses.
    
    Args:
        error_message: The error message to return
        response: Django HttpResponse object
    
    Returns:
        JsonResponse with error details
    """
    log.error("Forbidden Error", error=str(error_message))
    return JsonResponse({
        'response_message': str(error_message),
        'error': 'FORBIDDEN'
    }, status=403)

def error_handler_401(error_message: Any) -> JsonResponse:
    """
    Handle 401 Unauthorized responses.
    
    Args:
        error_message: The error message to return
        response: Django HttpResponse object
    
    Returns:
        JsonResponse with error details
    """
    log.error("Unauthorized Error", error=str(error_message))
    return JsonResponse({
        'response_message': str(error_message),
        'error': 'UNAUTHORIZED'
    }, status=401)

def error_handler_404(error_message: Any) -> JsonResponse:
    """
    Handle 404 Not Found responses.
    
    Args:
        error_message: The error message to return
        response: Django HttpResponse object
    
    Returns:
        JsonResponse with error details
    """
    log.error("Not Found Error", error=str(error_message))
    return JsonResponse({
        'response_message': str(error_message),
        'error': 'NOT FOUND'
    }, status=404)

def error_handler_400(error_message: Any) -> JsonResponse:
    """
    Handle 400 Bad Request responses.
    
    Args:
        error_message: The error message to return
        response: Django HttpResponse object
    
    Returns:
        JsonResponse with error details
    """
    log.error("Bad Request Error", error=str(error_message))
    return JsonResponse({
        'response_message': str(error_message),
        'error': 'BAD REQUEST'
    }, status=400)