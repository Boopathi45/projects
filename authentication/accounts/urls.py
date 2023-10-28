from django.urls import path

from accounts.views import *

appname = 'accounts'

urlpatterns = [
    path('signup/', Signup.as_view()),
    path('signin/', Signin.as_view()),
    path('generate_otp/', GenerateOtp.as_view()),
    path('verify_otp/', VerifyOtp.as_view()),
]