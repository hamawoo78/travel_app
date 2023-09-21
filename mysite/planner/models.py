from django.db import models
from django.contrib.auth.models import User
from trip.models import Location 

# Create your models here.

class Address(models.Model):
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)    
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    trip = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Plan(models.Model):
    place = models.CharField(max_length=200)
    note = models.CharField(max_length=200)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    trip = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True)


    def __str__(self):
        return self.place