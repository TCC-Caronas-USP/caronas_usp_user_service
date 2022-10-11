from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .exceptions import NoRiderFound
from .models import Rider, Vehicle
from .serializers import RiderSerializer, RiderUpdateSerializer, VehicleSerializer


class VehicleView(ModelViewSet):

    serializer_class = VehicleSerializer
    queryset = Vehicle.objects


class RiderView(ModelViewSet):

    serializer_class = RiderSerializer
    queryset = Rider.objects

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PATCH':
            serializer_class = RiderUpdateSerializer
        return serializer_class

    def retrieve_self(self, request, *args, **kwargs):
        uid = request.auth
        try:
            rider = Rider.objects.get(uid=uid)
        except Rider.DoesNotExist:
            raise NoRiderFound()
        serializer = self.get_serializer(rider)
        return Response(serializer.data)
