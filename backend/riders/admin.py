from django.contrib import admin

from .models import Vehicle, Rider


class VehicleAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'brand',
                    'model',
                    'color',
                    'rider',
                    'license_plate')


class RiderAdmin(admin.ModelAdmin):

    list_display = ('email',
                    'cpf',
                    'telefone',
                    'instituto',
                    'rides_as_driver',
                    'rides_as_passenger',
                    'ranking')


admin.site.register(Vehicle, VehicleAdmin)

admin.site.register(Rider, RiderAdmin)
