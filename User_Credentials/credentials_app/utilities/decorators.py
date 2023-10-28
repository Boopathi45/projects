from rest_framework import status
from rest_framework.response import Response
import functools

def useronly_restriction(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        user_obj = request.user
        if not user_obj.is_admin:
            return Response({
                "status" : "error",
                "message" : "Permission denied",
                "data" : {}
            }, status=status.HTTP_403_FORBIDDEN)
        return func(request, *args, **kwargs)
    return wrapper