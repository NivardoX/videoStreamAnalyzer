from app import db
from models.alert import Alert
from models.camera import Camera, UserCamera


def get_alerts_by_camera_id(camera_id):
    return Alert.query.filter_by(camera_id=camera_id).all()


def get_alerts_by_user_id(user_id):
    return Alert.query.join(Camera).join(UserCamera).filter_by(user_id=user_id).all()


def create_alert(create_alert_payload):
    alert = Alert(**create_alert_payload)
    db.session.add(alert)
    return alert
