from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='Event', blank=True, null=True)
    event_date = models.DateTimeField(null=True)

    def __str__(self):
        return '{}'.format(self.title)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.name)


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.name)


class Attendee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    location = models.TextField(null = True, blank = True)

    def __str__(self):
        return '{}'.format(self.name)


class VenueBooking(models.Model):
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(null=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.venue.name} - {self.date} - {self.time}"


class Registration(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    additional_details = models.TextField(blank=True,null=True)
