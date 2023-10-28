from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver   # decorator to receive the signals
from rest_framework.authtoken.models import Token   # Token model to auto generate the tokens
from django.conf import settings

# Create your models here.
class Flight(models.Model):

    def __str__(self):
        return self.Operating_Airlines
    
    Flight_Number = models.CharField(max_length=20)
    Operating_Airlines = models.CharField(max_length=20)
    Departure_City = models.CharField(max_length=20)
    Arrival_City = models.CharField(max_length=20)
    Date_Of_Departure = models.DateField()
    Estimation_Of_Departure = models.TimeField()

class Passenger(models.Model):

    def __str__(self):
        return self.First_Name
    
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=20)
    Middle_Name = models.CharField(max_length=20)
    Email = models.EmailField()
    Phone = models.IntegerField()

class Reservation(models.Model):

    def __str__(self):
        return self.flight.Operating_Airlines
    def __str__(self):
        return self.passenger.First_Name
    
    flight = models.OneToOneField(Flight,on_delete=models.CASCADE)
    passenger = models.OneToOneField(Passenger,on_delete=models.CASCADE)

@receiver(post_save,sender=settings.AUTH_USER_MODEL)   # -- ((  authUser - authentication user saved in the database  ))    # decorator receiver for the retrival of the data // post_save = To save the data // 

def createAuthToken(sender,created,instance,**kwargs):
    if created:
        Token.objects.create(user=instance)