from eve.auth import TokenAuth
import db
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from flask import current_app as app
from config import AUTH_TOKEN_EXPIRATION_SEC
import datetime
import pytz


class Authenticator(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        database = db.Database(app)
        session = database.find_item('sessions', 'token', token)
        if session:
            ts_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            time_delta =  ts_utc - session['timestamp']
            if time_delta.total_seconds() < AUTH_TOKEN_EXPIRATION_SEC:
                self.set_request_auth_value(session['user_id'])
                return True
        return False


def generate_token():
    return str(uuid4().hex)


def hash_password(password):
    return generate_password_hash(password)


def check_password(user, password):
    return check_password_hash(user['password'], password)
