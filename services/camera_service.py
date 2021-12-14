from models.camera import Camera, UserCamera


def get_cameras_by_user_id(user_id):
    return Camera.query.join(UserCamera).filter_by(user_id=user_id).all()


def get_all_cameras():
    return Camera.query.all()
