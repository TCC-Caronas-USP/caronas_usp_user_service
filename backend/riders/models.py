from django.db import models


class Rider(models.Model):
    email = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    instituto = models.CharField(max_length=30, null=True, blank=True)
    rides_as_driver = models.PositiveIntegerField(default=0)
    rides_as_passenger = models.PositiveIntegerField(default=0)
    ranking = models.FloatField(default=0)


class Vehicle(models.Model):
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=6)
    brand = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=10)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
