import os
import sys
import json
import requests
import cv2
from flask import Flask, jsonify, request
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

def main(num):
    try:
        capture_and_save()
        coords = request_predict()
        u, v = find_goal_loc_uv(num, coords)
        x, z = uv_to_xz(u, v)
    except Exception as e:
        return {"success": "false", "msg": str(e)}

    y = 30  # constant

    ik = robot.inverse_kinematic([x, y, z])

    if ik['success'] == True:
        thetas = list(map(lambda x : int(x * 10), ik['theta']))
        arduino.runServo(thetas)
        return {"success": "true"}
    else:
        return {"success": "false", "msg": "ik failed"}

# --
app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    num = request.form.get("num")
    res = main(num=num)
    return jsonify(res)

host_addr = "127.0.0.1"
port_num = "7777"

app.run(host=host_addr, port=port_num)

# --
del cam
del arduino
