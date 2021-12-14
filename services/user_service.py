from werkzeug.security import generate_password_hash

from app import db
from models.camera import UserCamera
from models.user import User
from services.camera_service import get_all_cameras


def get_user_by_id(user_id):
    return User.query.get(user_id)


def update_user(update_user_payload):
    user = User(**update_user_payload)
    db.session.add(
        user
    )

    return user


def create(create_user_payload):

    user = User(**create_user_payload)
    db.session.add(user)
    for camera in get_all_cameras():
        db.session.add(UserCamera(user_id=user.id,camera_id=camera.id))

    return user


def get_all_users():
    return User.query.all()


def login(login_payload):
    user = User.query.filter_by(email=login_payload['email']).one()

    if user.verify_password(login_payload['password']):
        return user
    else:
        return None
