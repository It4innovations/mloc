import datetime

import pytz
from eve.auth import TokenAuth
from flask import current_app as app

from .db import Database
from .settings import AUTH_TOKEN_EXPIRATION_SEC


class Authenticator(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        database = Database.from_app(app)
        session = database.find_item('sessions', 'token', token)
        if session:
            ts_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            time_delta = ts_utc - session['timestamp']
            if time_delta.total_seconds() < AUTH_TOKEN_EXPIRATION_SEC:
                self.set_request_auth_value(session['user_id'])
                return True
        return False
