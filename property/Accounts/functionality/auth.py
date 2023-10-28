from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from django.db.models import Q
import datetime
from rest_framework.permissions import IsAuthenticated

from Accounts.models import User
from Accounts.serializers import *
from Accounts.utilities.authentication import custom_authenticate
from Accounts.utilities.utils import generate_access_token, generate_refresh_token

class Signup(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegistrationSerializer(
                data=data, context={"request": request})
            if serializer.is_valid():
                serializer_data = serializer.data
                user_obj = User.objects.create_user(**serializer_data)
                user_serializer = UserSerializer(user_obj)
                return Response({
                    "status": "success",
                    "message": "Registered Successfully",
                    "data": {
                        "signup_details": user_serializer.data
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": serializer.errors,
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Signin(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                response = Response()
                user = custom_authenticate(
                    username=data['username'], password=data['password'])
                if user is not None:
                    if user.is_active == 1:
                        user_serializer = UserSerializer(user)
                        access_token = generate_access_token(user)
                        refresh_token = generate_refresh_token(user)
                        user.last_login = datetime.datetime.now()
                        user.save()
                        response.set_cookie(
                            key='refresh_token', value=refresh_token, httponly=True, secure=False, samesite=None)
                        response.data = {
                            "status": "success",
                            "message": "Signed in successfully",
                            "data": {
                                "access_token": access_token,
                                "signin_details": user_serializer.data
                            }
                        }
                        return response
                    elif user.is_active == 0 and not user.last_login:
                        return Response({
                            "status": "error",
                            "message": "Your account is not activated, To continue visit resend mail option",
                            "data": {}
                        }, status=status.HTTP_400_BAD_REQUEST)
                    elif user.is_active == 0:
                        return Response({
                            "status": "error",
                            "message": "Your account is deactivated, please contact network administrator"
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        "status": "error",
                        "message": "Cannot find the specified user. please enter the valid information",
                        "data": {}
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "status": "error",
                    "message": serializer.errors,
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class EditorsView(APIView):
    permission_classes = ({IsAuthenticated})
    def get(self, request):
        editors_obj = User.objects.filter(Q(role_id=4)&Q(is_active=1))
        serializer = UserSerializer(editors_obj, many=True)
        return Response({
            "message":"Editors details fetched successfully",
            "editors":serializer.data
        }, status=status.HTTP_200_OK)
    