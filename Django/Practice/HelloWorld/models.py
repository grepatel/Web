from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

# Create your models here.
class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name="departures")
    destination = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}- {self.destination} To {self.origin}"

    def is_valid(self):
        return (self.origin != self.destination) and (self.duration >= 0)

class Passenger(models.Model):
    name = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.name} "
