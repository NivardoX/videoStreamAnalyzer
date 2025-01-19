import datetime

import cv2
from threading import Thread


class ThreadedCamera(object):
    def __init__(self, source=0):
        self.start = None
        self.status = False
        self.frame = None

        self.capture = cv2.VideoCapture(source)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()



    def update(self):
        while True:
            if self.capture.isOpened():
                if self.start is None: self.start=datetime.datetime.now()
                (self.status, self.frame) = self.capture.read()

    def grab_frame(self):
        if self.status:
            return self.frame
        return None
