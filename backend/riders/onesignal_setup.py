import onesignal
import os

ONESIGNAL_CONFIG = onesignal.Configuration(
    app_key=os.getenv("APP_KEY"),
    user_key=os.getenv("USER_KEY")
)

ONESIGNAL_APP_ID = os.getenv("APP_ID")
