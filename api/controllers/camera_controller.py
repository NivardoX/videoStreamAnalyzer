from flask import jsonify

from api.controllers import token_required
from app import flask_app
from services import camera_service


@flask_app.route('/cameras', methods=['GET'])
@token_required
def get_cameras(current_user):
    cameras = camera_service.get_cameras_by_user_id(current_user.id)
    return jsonify([
            camera.as_dict() for camera in cameras
        ])

