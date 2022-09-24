from django.db import models


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


class Vehicle(models.Model):
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=6)
    brand = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=10)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
