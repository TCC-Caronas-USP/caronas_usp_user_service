from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status


class VehicleView(ModelViewSet):

    def post(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class RiderView(ModelViewSet):

    def post(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)
