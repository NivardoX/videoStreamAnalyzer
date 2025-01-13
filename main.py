from threading import Thread

from producer.Producer import Producer
from settings import CAMERAS


def produce(_camera):
    producer = Producer(_camera['id'], _camera['url'])
    producer.start()


if __name__ == '__main__':
    for camera in CAMERAS:
        thread = Thread(target=produce, args=[camera])
        thread.start()
