from django.contrib import admin

from .models import Rider, Vehicle, Location, Ride, Passenger


class RiderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'phone_number',
        'course',
        'college',
        'ingress_year',
        'profile_image',
        'uid'
    )


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'driver',
        'license_plate',
        'brand',
        'model',
        'color'
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
        'max_passengers',
        'notification_id'
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
