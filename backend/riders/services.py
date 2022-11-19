from .onesignal_setup import ONESIGNAL_APP_ID, ONESIGNAL_CONFIG
from .models import Rider, Ride
import onesignal
from onesignal.api import default_api
from onesignal.model.notification import Notification


class RiderService():

    def get_rider_by_email(self, email):
        return Rider.objects.get(email=email)


class VehicleService():

    def get_vehicle_by_rider(self, email):
        return Rider.objects.get(email=email)


class RideService():

    def get_ride(self, ride_id):
        return Ride.objects.get(id=ride_id)


class OneSignalService():

    def send_notification(self, external_user_ids=None, content=None, headings=None, subtitle=None, buttons=None):
        contents = {
            'en': content,
            'pt': content
        }

        with onesignal.ApiClient(ONESIGNAL_CONFIG) as api_client:
            api_instance = default_api.DefaultApi(api_client)
            notification = Notification(
                app_id=ONESIGNAL_APP_ID,
                include_external_user_ids=external_user_ids,
                channel_for_external_user_ids="push",
                contents=contents,
                headings=headings,
                subtitle=subtitle,
                buttons=buttons,
                )
            api_instance.create_notification(notification)

    def send_new_passenger_notification(self, driver: Rider, rider: Rider, ride: Ride):
        external_user_id = driver.email
        rider_first_name = rider.name.split()[0]
        ride_date_string = f"{ride.start_time.day}/{ride.start_time.month}"
        content = f"{rider_first_name} quer entrar na sua carona do dia {ride_date_string}!"
        self.send_notification(external_user_ids=[external_user_id], content=content)

    def send_passenger_reviewed_notification(self, driver: Rider, rider: Rider, ride: Ride, accepted: bool):
        external_user_id = rider.email
        driver_first_name = driver.name.split()[0]
        ride_date_string = f"{ride.start_time.day}/{ride.start_time.month}"
        if accepted:
            content = f"Eba! {driver_first_name} te aceitou na carona do dia {ride_date_string}!"
        else:
            content = f"Infelizmente, {driver_first_name} não te aceitou na carona do dia {ride_date_string}!"
        self.send_notification(external_user_ids=[external_user_id], content=content)
