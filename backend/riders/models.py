from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator


# TODO: Modificações nas classes:
#   - Rider:
#       * Corrigir nomenclatura dos Fields
#       * max_value e min_value no Field year
#   - Vehicle:
#       * Corrigir nomenclatura dos Fields

class Rider(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    telefone = models.CharField(max_length=20, blank=False)
    instituto = models.CharField(max_length=30, blank=False)
    curso = models.CharField(max_length=30, blank=False)
    ano = models.PositiveIntegerField(blank=False)
    rides_as_driver = models.PositiveIntegerField(default=0)
    rides_as_passenger = models.PositiveIntegerField(default=0)
    ranking = models.FloatField(default=0)
    image_path = models.CharField(
        max_length=255, default="https://i.imgur.com/V4RclNb.png")
    uid = models.CharField(max_length=255, unique=True, blank=False)


class Vehicle(models.Model):
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=6)
    brand = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=10)
    rider = models.ForeignKey(
        Rider, on_delete=models.CASCADE, related_name='vehicles')


class Location(models.Model):
    address = models.CharField(max_length=255, blank=False)
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)


class Ride(models.Model):
    driver = models.ForeignKey(Rider, on_delete=models.CASCADE)
    starting_point = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='rides_starting_here')
    ending_point = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='rides_ending_here')
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    price = models.DecimalField(validators=[MinValueValidator(
        Decimal('0.00'))], max_digits=4, decimal_places=2, null=False)
    max_passengers = models.PositiveIntegerField(null=False)


class Passenger(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Rider, on_delete=models.CASCADE)
    meeting_point = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('ride', 'passenger'),
        )
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['ride', 'passenger'],
        #         name='unique_ride_passenger_combination'
        #     )
        # ]
