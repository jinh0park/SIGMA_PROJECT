import cv2
import os

class Camera:

    def __init__(self):
        capture_width = 1280
        capture_height = 720
        display_width = 1280
        display_height = 720
        framerate = 10
        flip_method = 0
        pipeline = ('nvarguscamerasrc ! '
                    'video/x-raw(memory:NVMM), '
                    'width=(int)%d, height=(int)%d, '
                    'format=(string)NV12, framerate=(fraction)%d/1 ! '
                    'nvvidconv flip-method=%d ! '
                    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
                    'videoconvert ! '
                    'video/x-raw, format=(string)BGR ! appsink' % (capture_width, capture_height, framerate, flip_method, display_width, display_height))
        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    def capture(self):
        ret, img = self.cap.read()
        return img

    def __del__(self):
        self.cap.release()
