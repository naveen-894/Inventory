from datetime import datetime
from core.helpers import api_logging
from core.utils import message_response
from .messages import INVALID_INPUT
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from functools import wraps

def send_validation_error(e):
    validation_error_message = INVALID_INPUT
    if isinstance(e, ValidationError):
        error = e.args[0]
        if 'errors' in error:
            validation_error_message = error.get("errors")
        else:
            validation_error_message = error.get('message')
    return validation_error_message

def api_exception_handler(api_name):
    """
    Decorator to catch api exception
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = None
            # Determine the position of the request object
            request = args[0]
            log_data = [f"info|| {datetime.now()}: {api_name} API called"]
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = send_validation_error(e)
                context = {
                    "request_url": request.META['PATH_INFO'], "error": str(e), "payload": request.data
                }
                log_data.append(f"error || context :{context}")
                api_logging(log_data)
                return Response(message_response(error_message), status=400)
        return wrapper
    return decorator