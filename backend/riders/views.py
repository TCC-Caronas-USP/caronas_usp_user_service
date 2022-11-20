from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .services import OneSignalService, RideService, PassengerService
from .exceptions import NoRiderFound
from .models import Rider, Vehicle, Location, Ride, Passenger
from .serializers import RidePassengersSerializer, RiderSerializer, RiderUpdateSerializer
from .serializers import VehicleSerializer
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
        if rider.vehicles.count():
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


class RideView(ModelViewSet):
    serializer_class = RidePostSerializer
    queryset = Ride.objects
    onesignal_service = OneSignalService()
    ride_service = RideService()

    def list(self, request, *args, **kwargs):
        all_rides = Ride.objects.all()
        current_rides = all_rides.filter(start_time__gte=datetime.now())
        serializer = RidesSerializer(current_rides, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        points = ['starting_point', 'ending_point']
        for point in points:
            dict = request.data[point]
            location = Location(**dict)
            location.save()
            request.data[point] = location.id

        request.data['notification_id'] = 'temp'

        rider = get_current_rider(request)
        request.data['driver'] = rider.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()

        notification_id = self.onesignal_service.schedule_ride_start_notification(
            ride=ride)

        ride.notification_id = notification_id
        ride.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve_self(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        my_rides = Ride.objects.filter(driver=rider)
        serializer = RidesSerializer(my_rides, many=True)
        return Response(serializer.data)

    def custom_retrieve(self, request, pk=None, *args, **kwargs):
        ride = self.ride_service.get_ride(pk)
        serializer = RidePassengersSerializer(ride)
        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        request_rider = get_current_rider(request)
        ride = self.ride_service.get_ride(pk)
        if ride.driver.id != request_rider.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        request_rider = get_current_rider(request)
        ride = self.ride_service.get_ride(pk)
        driver = ride.driver
        if driver.id != request_rider.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        riders = self.ride_service.get_riders(ride)
        self.onesignal_service.send_ride_cancelled_notification(
            ride=ride, driver=driver, riders=riders)
        self.onesignal_service.cancel_notification(ride.notification_id)
        return super().destroy(request, pk=pk, *args, **kwargs)


class PassengerView(ModelViewSet):
    serializer_class = PassengerPostSerializer
    queryset = Passenger.objects
    onesignal_service = OneSignalService()
    ride_service = RideService()
    passenger_service = PassengerService()

    def list(self, request, *args, **kwargs):
        rider = get_current_rider(request)
        passengers = rider.passenger_set.all()
        rides = [passenger.ride for passenger in passengers]
        serializer = RidePassengersSerializer(rides, many=True)
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

    def destroy(self, request, pk=None, *args, **kwargs):
        request_rider = get_current_rider(request)
        passenger_to_destroy = self.passenger_service.get_passenger(pk)
        if passenger_to_destroy.rider.id != request_rider.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def accept(self, request, pk=None, *args, **kwargs):

        request_driver = get_current_rider(request)
        passenger = self.passenger_service.get_passenger(pk)
        ride = passenger.ride

        if ride.driver.id != request_driver.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        passenger.status = 2
        passenger.save()

        ride = passenger.ride
        previous_notification_id = ride.notification_id

        notification_id = self.onesignal_service.schedule_ride_start_notification(
            ride=ride, previous_notification_id=previous_notification_id)

        ride.notification_id = notification_id
        ride.save()

        rider = passenger.rider
        driver = ride.driver

        self.onesignal_service.send_passenger_reviewed_notification(
            accepted=True, rider=rider, ride=ride, driver=driver)

        return Response(status=status.HTTP_200_OK)

    def reject(self, request, pk=None, *args, **kwargs):

        request_driver = get_current_rider(request)
        passenger = self.passenger_service.get_passenger(pk)
        ride = passenger.ride

        if ride.driver.id != request_driver.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        passenger.status = 0
        passenger.save()

        ride = passenger.ride
        rider = passenger.rider
        driver = ride.driver

        self.onesignal_service.send_passenger_reviewed_notification(
            accepted=False, rider=rider, ride=ride, driver=driver)

        return Response(status=status.HTTP_200_OK)
