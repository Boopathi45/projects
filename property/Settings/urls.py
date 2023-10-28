from django.urls import path

from Settings.views import *

appname = 'Settings'

urlpatterns = [
    path('list/', TurnAroundTime.as_view()),
    path('details/', TurnAroundTimeDetails.as_view()),
    path('get_turn_around_time/', GetTurnAroundTimeView.as_view()),
    path('work_sample_lists/', WorkSampleListView.as_view()),
    path('work_sample_details/<int:id>', WorkSampleDetailView.as_view()),
]
