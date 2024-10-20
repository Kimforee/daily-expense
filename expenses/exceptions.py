from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': response.data.get('detail', 'An error occurred'),
            'status_code': response.status_code,
        }
        return Response(custom_response_data, status=response.status_code)
    
    return Response({
        'error': True,
        'message': 'An unexpected error occurred. Please try again later.',
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
