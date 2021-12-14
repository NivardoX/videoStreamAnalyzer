from flask import request, jsonify

import services.user_service as user_service
from api.controllers import token_required

from app import flask_app, db


@flask_app.route('/user', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify(current_user.as_dict())


@flask_app.route('/login', methods=['POST'])
def login():
    user = user_service.login(request.json)
    if user is None:
        return "Unauthorized", 401

    data = user.as_dict()
    data['token'] = user.generate_token()
    return jsonify(data)


@flask_app.route('/user', methods=['POST'])
def create_user():
    try:
        user = user_service.create(request.json)
        db.session.commit()
        data = user.as_dict()
        data['token'] = user.generate_token()

    except Exception as e:
        db.session.rollback()
        return str(e), 500
    return jsonify(data)
