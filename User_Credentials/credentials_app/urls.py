from django.urls import path

from credentials_app.views import *

urlpatterns = [
    path('list/', CredentialView.as_view()),
    path('details/<int:id>', CredentialDetails.as_view()),
    path('share/', ShareCredentials.as_view())
]
