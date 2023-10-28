from django.contrib import admin
from django.urls import path
from FlightApp import views

appname = 'FlightApp'

urlpatterns = [
    path('FindFlights',views.FindFlights, name = 'FindFlights'),
    
]