from functools import wraps

import jwt

from app import flask_app
from models.user import User


@flask_app.route("/")
def heartbeat():
    return "beat"


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, flask_app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user = User.query \
                .filter_by(id=data['id']) \
                .first()
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Token is invalid'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated




from .user_controller import *
from .alert_controller import *
from .camera_controller import *
