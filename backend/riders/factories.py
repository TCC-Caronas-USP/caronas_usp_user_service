from .interactors import CreateVehicleInteractor, CreateRiderInteractor
from .repositories import VehicleRepository, RiderRepository


class CreateVehicleInteractorFactory:
    @staticmethod
    def get():
        vehicle_repository = VehicleRepository()
        return CreateVehicleInteractor(vehicle_repository)


class CreateRiderInteractorFactory:
    @staticmethod
    def get():
        rider_repository = RiderRepository()
        return CreateRiderInteractor(rider_repository)
