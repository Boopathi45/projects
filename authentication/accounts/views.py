from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from datetime import timedelta

from accounts.serializers import *
from accounts.models import UserTokenVerify, User
from helper.authentication import custom_authenticate
from helper.utility import random_int, send_verify_otp_mail
from helper.utils import generate_access_token, generate_refresh_token

class Signup(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        user_obj = User.objects.create_user(**serializer_data)
        user_serializer = UserSerializer(user_obj)
        return Response({
            "message": "Registered Successfully",
            "data": {
                "signup_details": user_serializer.data
            }
        }, status=status.HTTP_200_OK)

class Signin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        response = Response()
        user = custom_authenticate(
            username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active == 1:
                user_serializer = UserSerializer(user)
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                user.last_login = timezone.now()
                user.save()
                response.set_cookie(
                    key='refresh_token', value=refresh_token, httponly=True, secure=False, samesite=None)
                response.data = {
                    "message": "Signed in successfully",
                    "data": {
                        "access_token": access_token,
                        "signin_details": user_serializer.data
                    }
                }
                return response
        else:
            return Response({
                "message": "Cannot find the specified user, please enter the valid information",
            }, status=status.HTTP_400_BAD_REQUEST)

class GenerateOtp(APIView):

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_email = serializer.data.get('email')
        user_obj = User.objects.filter(Q(email=to_email)&Q(is_active=True))
        if not user_obj.exists():
            return Response({
                "message":"Invalid E-mail address no records found"
            }, status=status.HTTP_400_BAD_REQUEST)
        one_time_pass = random_int()
        UserTokenVerify.objects.create(email=to_email, verification_code=one_time_pass)
        context = {
            'message': 'Verify Otp for authentication',
            'otp':one_time_pass
        }
        html_message = render_to_string('accounts/otp_verify.html', context)
        text_message = strip_tags(html_message)
        subject = 'Login Credentials'
        from_mail = settings.EMAIL_HOST_USER
        send_verify_otp_mail(subject, text_message, from_mail, to_email, html_message)
        return Response({
            "message":"Otp sent to your registered E-mail address successfully",
        }, status=status.HTTP_200_OK)

class VerifyOtp(APIView):

    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        auth_obj = UserTokenVerify.objects.filter(email=data['email'], verification_code=data['one_time_pass'])
        user_obj = User.objects.filter(Q(email=data['email'])&Q(is_active=True))
        if not user_obj.exists():
            return Response({
                "message":"Invalid E-mail address no records found"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not auth_obj.exists():
            return Response({
                "message":"Invalid otp"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            auth_obj = auth_obj.first()
            auth_time_obj = auth_obj.code_generated_on
            current_time = timezone.now().time()
            past_time = auth_time_obj.time()
            t1 = timedelta(hours=past_time.hour, minutes=past_time.minute, seconds=past_time.second)
            t2 = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
            total_time_diff = abs((t2-t1).total_seconds())
            if not total_time_diff <= 600:
                return Response({
                    "message":"OTP expired"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                auth_obj.delete()
                response = Response()
                user_obj = user_obj.first()
                user_serializer = UserSerializer(user_obj)
                access_token = generate_access_token(user_obj)
                refresh_token = generate_refresh_token(user_obj)
                user_obj.last_login = timezone.now()
                user_obj.save()
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