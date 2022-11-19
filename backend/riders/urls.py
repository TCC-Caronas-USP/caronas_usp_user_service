from django.urls import path

from .views import RiderView, VehicleView, RideView, PassengerView

urlpatterns = [
    path(
        'riders',
        RiderView.as_view(
            actions={
                'get': 'retrieve_self',
                'post': 'create',
                'patch': 'custom_update'
            }
        )
    ),
    path(
        'vehicles',
        VehicleView.as_view(
            actions={
                'post': 'create',
                'patch': 'custom_update',
                'delete': 'custom_destroy'
            }
        )
    ),
    path(
        'rides',
        RideView.as_view(
            actions={
                'get': 'list',
                'post': 'create'
            }
        )
    ),
    path(
        'rides/<int:pk>',
        RideView.as_view(
            actions={
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'rides/driver',
        RideView.as_view(
            actions={
                'get': 'retrieve_self'
            }
        )
    ),
    path(
        'rides/passenger',
        PassengerView.as_view(
            actions={
                'get': 'list'
            }
        )
    ),
    path(
        'passengers',
        PassengerView.as_view(
            actions={
                'post': 'create'
            }
        )
    ),
    path(
        'passengers/<int:pk>',
        PassengerView.as_view(
            actions={
                'delete': 'destroy'
            }
        )
    ),
    path(
        'passengers/<int:pk>/accept',
        PassengerView.as_view(
            actions={
                'patch': 'accept'
            }
        )
    ),
    path(
        'passengers/<int:pk>/reject',
        PassengerView.as_view(
            actions={
                'patch': 'reject'
            }
        )
    )
]
