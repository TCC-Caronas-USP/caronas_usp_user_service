from django.urls import path

from .views import RiderView, VehicleView, LocationView, RideView, PassengerView

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
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        )
    ),
    # TODO: Remover request de location/
    path(
        'location',
        LocationView.as_view(
            actions={
                'get': 'list',
                'post': 'create',
            }
        )
    )
]
