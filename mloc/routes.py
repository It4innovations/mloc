from auth import check_password, generate_token
from db import Database

import datetime
from flask import request, abort, jsonify


def setup_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)

        if username and password:
            db = Database(app)
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
