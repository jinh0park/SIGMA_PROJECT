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
    try:
        return json.loads(res.text)
    except:
        return {}

def find_goal_loc_uv(num, coords):
    '''
    Coods:
    ┌──────> u
    │ IMG
    ↓
    v
    '''
    assert num in coords, "Cannot find the number."
    v1, u1, v2, u2 = coords[num]
    u = (u1 + u2) / 2
    v = (v1 + v2) / 2
    return u, v

def uv_to_xz(u, v):
    ################
    # TO BE FILLED #
    ################
    return [10, 10] #coordinates

def main(num="3"):
    capture_and_save()
    coords = request_predict()
    u, v = find_goal_loc_uv(num, coords)
    x, z = uv_to_xz(u, v)
    y = 30  # constant

    ik = robot.inverse_kinematic([x, y, z])
    print(ik)

# --
capture_and_save()
request_predict()

# --
del cam
del arduino
