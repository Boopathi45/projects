from django.urls import path
from properties.views import *

appname = 'properties'

urlpatterns = [
    path('list/', PropertyListView.as_view()),
    path('details/<int:pk>', PropertyDetailsView.as_view()),
    path('user_details/', UserDetails.as_view()),
]
