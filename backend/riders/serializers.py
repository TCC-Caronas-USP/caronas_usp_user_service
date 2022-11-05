from rest_framework import serializers

from .models import Rider, Vehicle, Location, Ride, Passenger


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'

# TODO: Trocar o nome para RiderPatchSerializer


class RiderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rider
        fields = '__all__'
        read_only_fields = ['email', 'name', 'vehicles']

# TODO: Trocar o nome para RiderGetSerializer


class RiderSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = Rider
        fields = '__all__'
        extra_kwargs = {
            'uid': {'write_only': True}
        }


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class RidePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'


class RideGetSerializer(serializers.ModelSerializer):
    driver = RiderSerializer(read_only=True)
    starting_point = LocationSerializer(read_only=True)
    ending_point = LocationSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = '__all__'


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = '__all__'
