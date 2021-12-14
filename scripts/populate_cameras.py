from app import db
from consumer.analisis import AnalysisType
from models.camera import Camera
from settings import CAMERAS

if __name__ == '__main__':
    for camera in CAMERAS:
        db.session.add(Camera(
            id=camera['id'],
            url=camera['url'],
            analisys_types=[AnalysisType.DICE.name, AnalysisType.COVER.name]

        ))
    db.session.commit()
