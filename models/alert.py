import datetime
import json

from sqlalchemy.dialects import postgresql

from app import db, AlchemyEncoder
from consumer.analisis import AnalysisMessages


class Alert(db.Model):
    id = db.Column(postgresql.UUID, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    image = db.Column(db.Text, nullable=True)
    type = db.Column(db.Text,nullable=False)
    camera_id = db.Column(db.Text, db.ForeignKey('camera.id'), nullable=False)

    def as_dict(self):
        return {
            'id':self.id,
            'time':self.time.isoformat(),
            'image':self.image,
            'type': {'id':self.type,'message':AnalysisMessages[self.type]},
            'camera_id':self.camera_id
        }

    def __repr__(self):
        return '<Alert %r>' % self.id
