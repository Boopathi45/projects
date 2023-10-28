from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
import datetime
import jwt, logging

from User_Credentials import settings
from Accounts.serializers import *
from Accounts.utilities.extras import custom_authenticate
from Accounts.utilities.utils import generate_access_token, generate_refresh_token
from credentials_app.models import User, BlacklistToken

app_name = 'Accounts'
logger = logging.getLogger('service')

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
            logger.exception("Exception")
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
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Regenerate_jwt(APIView):
    def get(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                payload = jwt.decode(
                    refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms='HS256')
                black_listt_token_qset = BlacklistToken.objects.filter(
                    token__refresh_token_id=payload['refresh_token_id'])
                if black_listt_token_qset:
                    return Response({
                        "status": "error",
                        "message": "Invalid token",
                        "data": {}
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.filter(id=payload['id']).first()
                    access_token = generate_access_token(user)
                    return Response({
                        "status": "success",
                        "message": "Access token generated successfully",
                        "data": {
                            "access_token": access_token
                        }
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "Authenticate credentials were not provided",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({
                "status": "error",
                "message": "Invalid signature error",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({
                "status": "error",
                "message": "Token expired signature error",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Signout(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            response = Response()
            if refresh_token:
                payload = jwt.decode(
                    refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms='HS256')
                user = User.objects.filter(id=payload['id']).first()
                BlacklistToken.objects.create(token=payload, user=user)
                response.delete_cookie('refresh_token')
                return Response({
                    "status": "success",
                    "message": "Signed out successfully",
                    "data": {}
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "Authentication credentials not provided",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({
                "status": "error",
                "message": "Invalid signature error",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({
                "status": "error",
                "message": "Token expired signature error",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        