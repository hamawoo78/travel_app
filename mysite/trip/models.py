from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    destination = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    note = models.CharField(max_length=200)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.destination