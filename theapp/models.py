from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=200)
    max_tickets = models.IntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    idLocation = models.ForeignKey(Location,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name+ ' - ' + self.idLocation.name

    
class Ticket(models.Model):
    idEvent = models.ForeignKey(Event,on_delete=models.CASCADE)
    nameUser = models.CharField(max_length=200, default='Kevin Perez')
    numTickets = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default='kevinsteven797@gmail.com')

    def __str__(self):
         return self.idEvent.name 