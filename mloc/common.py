from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4


def generate_token():
    return str(uuid4().hex)


def hash_password(password):
    return generate_password_hash(password)


def check_password(user, password):
    return check_password_hash(user['password'], password)
