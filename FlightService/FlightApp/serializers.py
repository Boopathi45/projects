from FlightApp.models import Flight,Passenger,Reservation
from rest_framework import serializers
import re

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
      
# ---------------------------- Manual validation Section ---------------

    def validated_Flight_Number(self,Flight_Number):
        if(re.match("^[a-zA-Z1-9]*$",Flight_Number)==None):
            raise serializers.ValidationError ("It is not tha valid information provided .. please check and re- enter the value")
        return Flight_Number
    
    
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'