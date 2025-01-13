import base64
import datetime
import uuid
from typing import List

from billiard.process import current_process
from celery.signals import worker_shutting_down

import services.alert_service
from consumer import ALERTS_PATH, TIMINGS_PATH
from app import celery, db

from consumer.analisis import AnalysisFunctions

timings = {}
@celery.task
def analyze_frame(id: str, analyses: List[str], frame: str, test_id: str,task_created:float) -> None:
    image_64_decoded = base64.decodebytes(frame.encode())
    for analysis in analyses:
        for i in range(1_000_000):
            pass

        if AnalysisFunctions[analysis](image_64_decoded):
            try:
                services.camera_service.create_camera_if_not_exists(id, "camera" + str(id))
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

    path = TIMINGS_PATH / test_id

    path.mkdir(parents=True, exist_ok=True)
    with open(path / f"{str(current_process().index)}.txt","a") as f:
        f.write(f"{(datetime.datetime.now() - datetime.datetime.fromtimestamp(task_created)).microseconds}\n")
    return frame
