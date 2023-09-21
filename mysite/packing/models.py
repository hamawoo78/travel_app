from django.db import models
from django.contrib.auth.models import User
from trip.models import Location 


# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=50)
    note = models.TextField(max_length=200)
    is_completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    trip = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['is_completed']