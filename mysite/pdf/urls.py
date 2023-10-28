from django.contrib import admin
from django.urls import path
from pdf import views

app_name='pdf'
urlpatterns = [
    path('',views.intro, name='intro-page'),
    path('accept', views.accept, name='accept'),
    path('<int:id>',views.resume, name='resume'),
    path('lists',views.lists, name='lists')
]
