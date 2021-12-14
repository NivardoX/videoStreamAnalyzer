import base64
import datetime
import uuid
from typing import List

import services.alert_service
from consumer import ALERTS_PATH
from app import celery, db

from consumer.analisis import AnalysisFunctions


@celery.task
def analyze_frame(id: str, analyses: List[str], frame: str):
    image_64_decoded = base64.decodebytes(frame.encode())

    for analysis in analyses:
        if AnalysisFunctions[analysis](image_64_decoded):

            try:
                services.alert_service.create_alert({
                    'id': str(uuid.uuid4()),
                    'camera_id': id,
                    'type': analysis,
                    'image': frame
                })
                db.session.commit()
                path = ALERTS_PATH / id
                path.mkdir(parents=True, exist_ok=True)
                with open(path / f'{datetime.datetime.now().isoformat()}.jpg', 'wb+') as f:
                    f.write(image_64_decoded)
            except Exception as e:
                print(e)
                db.session.rollback()

    return frame
