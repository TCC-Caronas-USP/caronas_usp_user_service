from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .exceptions import NoRiderFound
from .models import Rider, Vehicle, Location, Ride, Passenger
from .serializers import RiderSerializer, RiderUpdateSerializer
from .serializers import VehicleSerializer
from .serializers import LocationSerializer
from .serializers import RideGetSerializer, RidePostSerializer
from .serializers import PassengerSerializer


def get_current_rider(request):
    uid = request.auth
    try:
        rider = Rider.objects.get(uid=uid)
    except Rider.DoesNotExist:
        raise NoRiderFound()
    return rider


class RiderView(ModelViewSet):
    serializer_class = RiderSerializer
    queryset = Rider.objects

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PATCH':
            serializer_class = RiderUpdateSerializer
        return serializer_class

    def retrieve_self(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        serializer = self.get_serializer(rider)
        return Response(serializer.data)


class VehicleView(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects


class LocationView(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects


class RideView(ModelViewSet):
    serializer_class = RidePostSerializer
    queryset = Ride.objects

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'GET':
            serializer_class = RideGetSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):

        starting_point_dict = request.data['starting_point']
        ending_point_dict = request.data['ending_point']
        starting_point = Location(**starting_point_dict)
        ending_point = Location(**ending_point_dict)
        starting_point.save()
        ending_point.save()
        request.data['starting_point'] = starting_point.id
        request.data['ending_point'] = ending_point.id

        rider = get_current_rider(request)
        request.data['driver'] = rider.id
        return super().create(request, *args, **kwargs)


class PassengerView(ModelViewSet):
    serializer_class = PassengerSerializer
    queryset = Passenger.objects
