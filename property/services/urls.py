from django.urls import path

from properties.views import *
from services.views import *

appname = 'services'
urlpatterns = [
    path('list/', ServicesListView.as_view()),
    path('details/<int:id>', ServicesDetailView.as_view()),
    path('service_editing_Preference_lst/', ServiceEditingPreferenceListView.as_view()),
]