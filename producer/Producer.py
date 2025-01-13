import base64
import time

import cv2
from consumer.analisis import AnalysisType
from consumer.tasks import analyze_frame
from producer.ThreadedCamera import ThreadedCamera


def rescale_frame(frame, percent=20):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def convert_frame_to_bin(frame):
    retval, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode("utf-8")


class Producer:
    def __init__(self, id, url, total_images = 5000,analysis_types=tuple([AnalysisType.DICE])):
        self.id = id
        self.url = url
        self.analysis_types = [analysis_type.name for analysis_type in analysis_types]
        self.counter = 0
        self.image_count = total_images

    def start(self):
        streamer = ThreadedCamera(self.url)
        while True and self.counter < self.image_count:
            try:
                frame = streamer.grab_frame()
                if frame is None:
                    continue

                resized_frame = rescale_frame(frame, 20)
                frame_binary = convert_frame_to_bin(resized_frame)

                # send to queue
                print(self.counter)
                analyze_frame.delay(self.id, self.analysis_types, frame_binary)
                time.sleep(0.033333)
                self.counter += 1
            except Exception as e:
                print("ERROR WHILE FETCHING FRAME ", e)
                cap = cv2.VideoCapture(self.url)

        print(f"FINISHED WITH {self.counter}")
