from flask import jsonify

from api.controllers import token_required
from app import flask_app
from services import alert_service


@flask_app.route("/alerts")
@token_required
def get_alerts(current_user):
    alerts = alert_service.get_alerts_by_user_id(current_user.id)
    return jsonify([
        alert.as_dict() for alert in alerts
    ]
    )
