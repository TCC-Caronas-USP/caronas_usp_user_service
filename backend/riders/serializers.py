from rest_framework import serializers
from .models import Rider, Vehicle


class RiderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rider
        fields = '__all__'
        read_only_fields = ['email', 'name', 'vehicles']


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'


class RiderSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = Rider
        fields = '__all__'
        extra_kwargs = {
            'uid': {'write_only': True}
        }
