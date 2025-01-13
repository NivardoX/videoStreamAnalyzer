import base64
import time
from typing import List

import cv2
import numpy as np

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

def mock_frame(width=640, height=480, color=(0, 0, 255)) -> np.ndarray:
    """
    Create a mock image (NumPy array). By default, it's solid color (BGR).
    Customize or randomize as needed.
    """
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:] = color
    return frame


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


class MockedProducer:
    def __init__(
            self,
            producer_id: str,
            url:str=None,
            total_images: int = 5000,
            fps: float = 30,
            analysis_types=None,
            use_celery=True,

    ):
        """
        :param producer_id: An identifier for this producer.
        :param fps: Desired frames per second.
        :param total_images: How many frames/images to produce in total.
        :param analysis_types: List of analysis types to pass down to the analyzer.
        """
        if analysis_types is None:
            analysis_types = [AnalysisType.DICE]

        self.id = producer_id
        self.fps = fps
        self.total_images = total_images
        self.use_celery = use_celery
        # Convert enum entries to their names (or keep them as Enums if you prefer)
        self.counter = 0
        self.frame = mock_frame()

        # Time between frames = 1 / fps
        self.frame_interval = float(1.0) / float(self.fps)
        self.analysis_types = [analysis_type.name for analysis_type in analysis_types]

        # Metrics storage
        # You can expand or organize this differently as needed.
        self.start_time = None
        self.end_time = None
        self.frame_durations = []  # Track how long each frame processing cycle took.

    def start(self):
        """
        Produce frames at a fixed FPS, mock them, and send them for analysis.
        Collect metrics for each frame produced.
        """
        self.start_time = time.time()  # When production starts

        while self.counter < self.total_images:
            frame_start_time = time.time()

            try:
                # Mock a frame (instead of capturing from a camera)
                frame = self.frame

                # Optionally rescale the frame
                resized_frame = rescale_frame(frame, 20)

                # Convert the frame to binary
                frame_binary = convert_frame_to_bin(resized_frame)

                # Show progress in console
                # print(f"[Producer {self.id}] Producing frame #{self.counter}")

                if self.use_celery:
                    analyze_frame.delay(self.id, self.analysis_types, frame_binary)
                else:
                    analyze_frame(self.id, self.analysis_types, frame_binary)

                # Enforce fixed FPS
                time.sleep(self.frame_interval)
                self.counter += 1

            except Exception as e:
                print("ERROR WHILE FETCHING/SENDING FRAME:", e)
                # Decide whether to break or continue
                break

            # Record how long it took to process this frame iteration
            frame_duration = time.time() - frame_start_time
            self.frame_durations.append(frame_duration)

        self.end_time = time.time()  # When production stops
        # print(f"[Producer {self.id}] FINISHED PRODUCING {self.counter} FRAMES.")

        # Summarize metrics
        self._summarize_metrics()

    def _summarize_metrics(self):
        """
        Summarize and print out collected metrics.
        In practice, you could log these to a file, DB, or another service.
        """
        total_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        average_frame_time = (sum(self.frame_durations) / len(self.frame_durations)) if self.frame_durations else 0

        summary = {
            "producer_id": self.id,
            "frames_produced": self.counter,
            "total_time_sec": total_time,
            "average_time_per_frame_sec": average_frame_time,
            "effective_fps": self.counter / total_time if total_time > 0 else 0,
        }

        print(f"[Producer {self.id} Metrics Summary]")
        for key, value in summary.items():
            print(f"  {key}: {value}")