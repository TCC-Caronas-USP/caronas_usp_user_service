from rest_framework import serializers

from .interactors import GetPassengerInteractor
from .models import Rider, Vehicle, Location, Ride, Passenger


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'


class RiderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rider
        fields = '__all__'
        read_only_fields = ['email', 'name', 'vehicles']


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


# class PassengerGetSerializer(serializers.ModelSerializer):
#     passenger = RiderSerializer(read_only=True)

#     class Meta:
#         model = Passenger
#         fields = ['passenger', 'meeting_point']


class RidesSerializer(serializers.ModelSerializer):
    driver = RiderSerializer(read_only=True)
    starting_point = LocationSerializer(read_only=True)
    ending_point = LocationSerializer(read_only=True)
    status = serializers.SerializerMethodField('get_passenger_status')
    passenger_count = serializers.IntegerField(source='get_passenger_count')

    def __init__(self, instance=None, data=..., rider=None, **kwargs):
        self.rider = rider
        super().__init__(instance, data, **kwargs)

    def get_passenger_status(self, ride):
        interactor = GetPassengerInteractor()
        passenger = interactor.get_passenger(self.rider, ride)
        if not passenger:
            return None
        return passenger.status

    class Meta:
        model = Ride
        fields = '__all__'


class PassengerPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = '__all__'
