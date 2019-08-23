import datetime

from flask import abort, jsonify, request

from .common import check_password, generate_token
from .db import Database


def setup_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)

        if username and password:
            db = Database.from_app(app)
            user = db.find_item('users', 'username', username)
            if check_password(user, password):
                token = generate_token()
                session = {
                    'user_id': user['_id'],
                    'token': token,
                    'timestamp': datetime.datetime.utcnow()
                }
                db.create_item('sessions', session)
                return jsonify({'token': token})
            else:
                abort(403)
        else:
            abort(400)
