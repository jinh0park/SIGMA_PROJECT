import os
import sys
import json
import requests
import cv2
from robotics_module.main import Robot
from camera_module.main import Camera
from arduino_module.main import ArduinoControl
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import C

# Declare global variables
arduino = ArduinoControl(C.arduino_port)
cam = Camera()
robot = Robot(C.body_lengths, C.initial_pos)

# --
def capture_and_save():
    capture = cam.capture()
    cv2.imwrite('../ocr_server/capture.png', capture)

def request_predict():
    img_path = "capture.png"
    res = requests.post(C.ocr_server_url + "/predict", data={"img_path": img_path})
    print(res.text)
    return 0

# --
capture_and_save()
request_predict()

# --
del cam
del arduino
