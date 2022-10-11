from django.urls import path
from .views import VehicleView, RiderView

urlpatterns = [
    path(
        'vehicle/',
        VehicleView.as_view(
            actions={
                'post': 'create',
            }
        ),
    ),
    path(
        'vehicle/<int:pk>',
        VehicleView.as_view(
            actions={
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        ),
    ),
    path(
        'rider/',
        RiderView.as_view(
            actions={
                'post': 'create',
                'get': 'retrieve_self'
            }
        ),
    ),
    path(
        'rider/<int:pk>',
        RiderView.as_view(
            actions={
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        ),
    ),
]
