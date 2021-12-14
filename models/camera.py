import datetime
import json

from sqlalchemy.dialects import postgresql

from app import db, AlchemyEncoder
from consumer.analisis import AnalysisMessages


class Camera(db.Model):
    id = db.Column(db.Text, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    analisys_types = db.Column(postgresql.ARRAY(db.Text), nullable=False, default=[])

    def as_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'analisys_types': [{'id':type,'message':AnalysisMessages[type]} for type in self.analisys_types]
        }

    def __repr__(self):
        return '<Camera %r>' % self.id


class UserCamera(db.Model):
    camera_id = db.Column(db.Text, db.ForeignKey('camera.id'), nullable=False, primary_key=True)
    user_id = db.Column(postgresql.UUID, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    camera = db.relationship(Camera)

    def as_dict(self):
        return json.loads(json.dumps(self, cls=AlchemyEncoder))

    def __repr__(self):
        return '<UserCamera %r, %r>' % (self.camera_id, self.user_id)
