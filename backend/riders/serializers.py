from rest_framework import serializers

from .services import RideService

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
    rides_as_passenger = serializers.IntegerField(
        source='get_rides_as_passenger', read_only=True)
    rides_as_driver = serializers.IntegerField(
        source='get_rides_as_driver', read_only=True)

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
        extra_kwargs = {
            'notification_id': {'write_only': True}
        }


class RidesSerializer(serializers.ModelSerializer):
    driver = RiderSerializer(read_only=True)
    starting_point = LocationSerializer(read_only=True)
    ending_point = LocationSerializer(read_only=True)
    passenger_count = serializers.IntegerField(
        source='get_passenger_count', read_only=True)

    class Meta:
        model = Ride
        fields = '__all__'
        extra_kwargs = {
            'notification_id': {'write_only': True}
        }


class PassengerGetSerializer(serializers.ModelSerializer):
    meeting_point = LocationSerializer()

    class Meta:
        model = Passenger
        fields = '__all__'


class PassengerPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = '__all__'


class RiderStatusSerializer(serializers.ModelSerializer):
    passenger = serializers.SerializerMethodField('get_passenger')

    def __init__(self, instance=None, data=..., ride=None, **kwargs):
        self.ride = ride
        super().__init__(instance, data, **kwargs)

    def get_passenger(self, rider):
        ride_service = RideService()
        passenger = ride_service.get_passenger(self.ride, rider)
        return PassengerGetSerializer(passenger).data

    class Meta:
        model = Rider
        fields = '__all__'
        extra_kwargs = {
            'uid': {'write_only': True}
        }


class RidePassengersSerializer(serializers.ModelSerializer):
    riders = serializers.SerializerMethodField('get_riders')
    driver = RiderSerializer(read_only=True)
    starting_point = LocationSerializer(read_only=True)
    ending_point = LocationSerializer(read_only=True)

    def get_riders(self, ride):
        ride_service = RideService()
        riders = ride_service.get_riders(ride)
        return RiderStatusSerializer(riders, many=True, ride=ride).data

    class Meta:
        model = Ride
        fields = '__all__'
        extra_kwargs = {
            'notification_id': {'write_only': True}
        }
