import base64
import datetime
from typing import List

from consumer import ALERTS_PATH
from app import app

from consumer.analisis import AnalysisType, AnalysisFunctions


@app.task
def analyze_frame(id: str, analyses: List[str], frame: str):
    image_64_decoded = base64.decodebytes(frame.encode())

    for analysis in analyses:
        if AnalysisFunctions[analysis](image_64_decoded):
            path = ALERTS_PATH / id
            path.mkdir(parents=True, exist_ok=True)
            with open(path / f'{datetime.datetime.now().isoformat()}.jpg', 'wb+') as f:
                f.write(image_64_decoded)

    return frame
