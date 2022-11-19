from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .services import OneSignalService, RideService
from .exceptions import NoRiderFound
from .models import Rider, Vehicle, Location, Ride, Passenger
from .serializers import RiderSerializer, RiderUpdateSerializer
from .serializers import VehicleSerializer
from .serializers import LocationSerializer
from .serializers import RidesSerializer, RidePostSerializer
from .serializers import PassengerPostSerializer


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

    def create(self, request, *args, **kwargs):
        if 'uid' not in request.data:
            request.data['uid'] = request.auth
        return super().create(request, *args, **kwargs)

    def custom_update(self, request, *args, **kwargs):
        current_rider = get_current_rider(request)

        partial = True
        instance = current_rider
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class VehicleView(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects

    def create(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        if rider.vehicles:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.data['driver'] = rider.id
        return super().create(request, *args, **kwargs)

    def custom_update(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        my_vehicle = rider.vehicles.first()

        partial = True
        instance = my_vehicle
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def custom_destroy(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        my_vehicle = rider.vehicles.first()

        instance = my_vehicle
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationView(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects


class RideView(ModelViewSet):
    serializer_class = RidePostSerializer
    queryset = Ride.objects
    onesignal_service = OneSignalService()
    ride_service = RideService()

    # TODO: é necessário retornar informações dos passageiros de cada carona
    def list(self, request, *args, **kwargs):
        all_rides = Ride.objects.all()
        current_rides = all_rides.filter(start_time__gte=datetime.now())
        serializer = RidesSerializer(
            current_rides, many=True, rider=get_current_rider(request))
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        points = ['starting_point', 'ending_point']
        for point in points:
            dict = request.data[point]
            location = Location(**dict)
            location.save()
            request.data[point] = location.id

        rider = get_current_rider(request)
        request.data['driver'] = rider.id
        return super().create(request, *args, **kwargs)

    def retrieve_self(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        my_rides = Ride.objects.filter(driver=rider)
        # TODO: Avaliar se faz sentido
        # my_current_rides = my_rides.filter(start_time__gte=datetime.now())
        serializer = self.get_serializer(my_rides, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        ride = self.ride_service.get_ride(pk)
        driver = ride.driver
        riders = self.ride_service.get_riders(ride)
        self.onesignal_service.send_ride_cancelled_notification(
            ride=ride, driver=driver, riders=riders)
        return super().destroy(request, pk=pk, *args, **kwargs)


class PassengerView(ModelViewSet):
    serializer_class = PassengerPostSerializer
    queryset = Passenger.objects
    onesignal_service = OneSignalService()
    ride_service = RideService()

    def list(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        passengers = rider.passenger_set.all()
        rides = [passenger.ride for passenger in passengers]
        serializer = RidesSerializer(
            rides, many=True, rider=get_current_rider(request))
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        dict = request.data['meeting_point']
        location = Location(**dict)
        location.save()
        request.data['meeting_point'] = location.id

        rider = get_current_rider(request)
        request.data['rider'] = rider.id

        ride = self.ride_service.get_ride(request.data['ride'])
        driver = ride.driver

        self.onesignal_service.send_new_passenger_notification(
            driver=driver, rider=rider, ride=ride)

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        dict = request.data['meeting_point']
        location = Location(**dict)
        location.save()
        request.data['meeting_point'] = location.id

        rider = get_current_rider(request)
        request.data['passenger'] = rider.id
        return super().partial_update(request, *args, **kwargs)
