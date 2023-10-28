from django.urls import path

from Accounts.views import *

urlpatterns = [
    path('signup/', Signup.as_view()),
    path('signin/', Signin.as_view()),
    path('token/regenerate/', Regenerate_jwt.as_view()),
    path('signout/', Signout.as_view())
]
