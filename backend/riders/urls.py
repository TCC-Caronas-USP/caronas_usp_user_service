from django.urls import path

from .views import RiderView, VehicleView, LocationView, RideView  # , PassengerView

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
        'rides/',
        RideView.as_view(
            actions={
                'get': 'list',
                'post': 'create'
            }
        )
    ),
    # path(
    #     'rides/<int:pk>',
    #     RideView.as_view( # A View de Rides precisa de uma correção para lidar com os PATCH
    #         actions={
    #             'patch': 'partial_update',
    #             'delete': 'destroy'
    #         }
    #     )
    # ),
    # path(
    #     'rides/driver',
    #     RideView.as_view(
    #         actions={
    #             'get': '' # Retornar somente as Rides que possuem o id_driver do motorista
    #         }
    #     )
    # ),
    # TODO: Remover request de location/
    path(
        'location/',
        LocationView.as_view(
            actions={
                'get': 'list',
                'post': 'create',
            }
        )
    )
]
