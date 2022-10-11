from rest_framework import status
from rest_framework.exceptions import APIException


class NoRiderFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Rider not found for authentication token provided"
    default_code = "rider_not_found"
