from .models import Vehicle, Rider


class VehicleRepository:

    def find_by_rider(self, rider):
        return list(Vehicle.objects.filter(rider=rider))

    def create(self, **vehicle_data):
        vehicle = Vehicle.objects.create(**vehicle_data)
        return vehicle


class RiderRepository:

    def find_by_email(self, email):
        return Rider.objects.get(email=email)

    def create(self, **rider_data):
        rider = Rider.objects.create(**rider_data)
        return rider
