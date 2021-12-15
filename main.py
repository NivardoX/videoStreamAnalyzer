from threading import Thread

from producer.Producer import Producer
from settings import CAMERAS


def produce(camera):
    producer = Producer(camera['id'], camera['url'])
    producer.start()


if __name__ == '__main__':
    for camera in CAMERAS:
        thread = Thread(target=produce, args=[camera])
        thread.start()
