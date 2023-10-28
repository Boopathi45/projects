from rest_framework.response import Response
from rest_framework import status
import functools

def user_restriction(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({
                "status":"error",
                "message":"permission denied"
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            return func(request, *args, **kwargs)
    return wrapper