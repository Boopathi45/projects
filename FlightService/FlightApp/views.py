from django.shortcuts import render
from rest_framework import viewsets
from FlightApp.models import Flight,Passenger,Reservation
from FlightApp.serializers import FlightSerializer,PassengerSerializer,ReservationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['POST'])

def FindFlights(request):
    flights = Flight.objects.filter(Departure_City=request.data['Departure_City'],Arrival_City=request.data['Arrival_City'],Date_Of_Departure=request.data['Date_Of_Departure'])
    serializer = FlightSerializer(flights)
    return Response(serializer.data,status=status.HTTP_201_CREATED)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    # permission_classes = (IsAuthenticated)

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer