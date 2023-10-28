from django.urls import path
from mail import views
from django.views.generic import TemplateView


appname = 'mail'

urlpatterns = [
    path('sendemail/', views.sendSimpleEmail, name='sendemail'),
    path('', views.samplehtmlemailview, name='sampleview'),
    path('zipmail/', views.zipmailview, name='zipmail')
]
    