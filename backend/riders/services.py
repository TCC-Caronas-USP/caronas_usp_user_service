from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.utils.timezone import get_default_timezone
from typing import List
from .onesignal_setup import ONESIGNAL_APP_ID, ONESIGNAL_CONFIG
from .models import Rider, Ride
import onesignal
from onesignal.api import default_api
from onesignal.model.notification import Notification
import logging

logger = logging.getLogger(__name__)


class RiderService():

    def get_rider_by_email(self, email):
        return Rider.objects.get(email=email)


class VehicleService():

    def get_vehicle_by_rider(self, email):
        return Rider.objects.get(email=email)


class RideService():

    def get_ride(self, ride_id):
        return Ride.objects.get(id=ride_id)

    def get_riders(self, ride: Ride):
        passengers = ride.passenger_set.all()
        return [passenger.rider for passenger in passengers]


class OneSignalService():

    def send_notification(self, external_user_ids=None, content=None,
                          headings=None, subtitle=None, buttons=None, send_after=None):
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
                send_after=send_after,
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

    def send_ride_cancelled_notification(self, driver: Rider, riders: List[Rider], ride: Ride):
        external_user_ids = [rider.email for rider in riders]
        driver_first_name = driver.name.split()[0]
        ride_date_string = f"{ride.start_time.day}/{ride.start_time.month}"
        content = f"Infelizmente, {driver_first_name} teve que cancelar a carona do dia {ride_date_string}!"
        self.send_notification(external_user_ids=external_user_ids, content=content)

    def send_ride_start_notification(self, driver: Rider,
                                     riders: List[Rider],
                                     ending_point_address: str,
                                     start_time=str):
        external_user_ids = [rider.email for rider in riders]
        external_user_ids.append(driver.email)
        external_user_ids.append('gabriel.desidera@usp.br')
        content = f"Atenção, a carona para {ending_point_address} irá sair em 10 minutos!"

        naive_ride_datetime = parse_datetime(start_time)
        ride_datetime = naive_ride_datetime.replace(tzinfo=get_default_timezone())
        ride_datetime_minus_10 = ride_datetime - timedelta(minutes=10)

        self.send_notification(external_user_ids=external_user_ids, content=content, send_after=ride_datetime_minus_10)
