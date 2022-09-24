from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Rider, Vehicle
from .serializers import RiderSerializer, RiderUpdateSerializer, VehicleSerializer


def _validate_user(request):
    return True


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

    def create(self, request, format=None):
        user = _validate_user(request)
        if not user:
            return Response("Error retrieving user", status=status.HTTP_400_BAD_REQUEST)

        return super().create(request)
