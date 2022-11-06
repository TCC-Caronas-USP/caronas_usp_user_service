from django.contrib import admin

from .models import Rider, Vehicle, Location, Ride, Passenger


class RiderAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'telefone',
        'instituto',
        'rides_as_driver',
        'rides_as_passenger',
        'ranking'
    )


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'brand',
        'model',
        'color',
        'rider',
        'license_plate'
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'address',
        'lat',
        'lon'
    )


class RideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'driver',
        'starting_point',
        'ending_point',
        'start_time',
        'end_time',
        'price',
        'max_passengers'
    )


class PassengerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ride',
        'rider',
        'meeting_point',
        'status'
    )


admin.site.register(Rider, RiderAdmin)

admin.site.register(Vehicle, VehicleAdmin)

admin.site.register(Location, LocationAdmin)

admin.site.register(Ride, RideAdmin)

admin.site.register(Passenger, PassengerAdmin)
