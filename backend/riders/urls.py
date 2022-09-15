from django.urls import path
from .views import VehicleView, RiderView

urlpatterns = [
    path(
        'vehicle/',
        VehicleView.as_view(
            actions={
                'get': 'get',
                'post': 'post',
            }
        ),
    ),
    path(
        'rider/',
        RiderView.as_view(
            actions={
                'get': 'get',
                'post': 'post',
            }
        ),
    ),
]
