import os
import sys
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
def func():
    capture = cam.capture()
    cv2.imwrite('capture.png', capture)


func()

del cam
del arduino
