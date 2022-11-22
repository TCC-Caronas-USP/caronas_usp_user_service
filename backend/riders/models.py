from datetime import datetime
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
    phone_number = models.CharField(max_length=255, blank=False)
    course = models.CharField(max_length=255, blank=False)
    college = models.CharField(max_length=255, blank=False)
    ingress_year = models.PositiveIntegerField(blank=False)
    profile_image = models.CharField(
        max_length=255, default="https://i.imgur.com/V4RclNb.png")
    uid = models.CharField(max_length=255, unique=True, blank=False)

    def get_rides_as_passenger(self):
        passengers = self.passenger_set.filter(
            status=2, ride__end_time__lte=datetime.now())
        return passengers.count()

    def get_rides_as_driver(self):
        rides_as_driver = self.ride_set.filter(end_time__lte=datetime.now())
        return rides_as_driver.count()


class Vehicle(models.Model):
    driver = models.ForeignKey(
        Rider, on_delete=models.CASCADE, related_name='vehicles')
    license_plate = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)


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
    notification_id = models.CharField(max_length=255)

    def get_passenger_count(self):
        return self.passenger_set.count()


class Passenger(models.Model):

    class Status(models.IntegerChoices):
        RECUSADO = 0
        EM_ESPERA = 1
        APROVADO = 2

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    meeting_point = models.OneToOneField('Location', on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=Status.choices, null=False, default=Status.EM_ESPERA)

    class Meta:
        unique_together = (
            ('ride', 'rider'),
        )
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['ride', 'passenger'],
        #         name='unique_ride_passenger_combination'
        #     )
        # ]
