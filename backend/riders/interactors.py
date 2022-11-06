from .models import Passenger


class CreateVehicleInteractor:

    def __init__(self, vehicle_repository):
        self.vehicle_repository = vehicle_repository

    def set_params(self, vehicle_data):
        self.vehicle_data = vehicle_data

    def execute(self):
        vehicle = self.vehicle_repository.create(**self.vehicle_data)
        return vehicle


class CreateRiderInteractor:

    def __init__(self, rider_repository):
        self.rider_repository = rider_repository

    def set_params(self, rider_data):
        self.rider_data = rider_data

    def execute(self):
        rider = self.rider_repository.create(**self.rider_data)
        return rider


class GetPassengerInteractor:

    def __init__(self) -> None:
        self.passengers = Passenger.objects

    def get_passenger(self, rider, ride):
        return self.passengers.get(rider=rider.id, ride=ride)
