from riders.models import Rider


class RiderService():

    def get_rider_by_email(self, email):
        return Rider.objects.get(email=email)


class VehicleService():

    def get_vehicle_by_rider(self, email):
        return Rider.objects.get(email=email)
