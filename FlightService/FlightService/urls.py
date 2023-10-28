"""
URL configuration for FlightService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from FlightApp import views
from rest_framework.authtoken.views import obtain_auth_token   # Obtain_Auth_Token is to obtain the token of the authenticate user from the database

router = routers.DefaultRouter()   # routers are used to direct the data to the respective viewsets

router.register('Flights',views.FlightViewSet)
router.register('Passenger',views.PassengerViewSet)
router.register('Reservation',views.ReservationViewSet)

appname = 'FlightApp'

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('FlightService/',include(router.urls)),
    path('FlightService/',include('FlightApp.urls')),
    # path('api_token', obtain_auth_token, name='obtain_auth_token')
]
