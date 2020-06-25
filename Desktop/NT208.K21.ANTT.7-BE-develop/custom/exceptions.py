from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    #create handler for ValidationError exception_class
    handlers = {
        'ValidationError': _handle_generic_error
    }

    #get current exception_class
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # If this exception is one that we can handle, handle it. Otherwise,
        # return the response generated earlier by the default exception 
        # handler.
        return handlers[exception_class](exc, context, response)

    return response

def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response