from firebase_admin import auth, credentials, initialize_app
from rest_framework import authentication
import json
import os
from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken

firebase_config_str = os.environ.get('FIREBASE_CONFIG')
credentials_dict = json.loads(firebase_config_str, strict=False)

cred = credentials.Certificate(credentials_dict)

default_app = initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        return (None, uid)
