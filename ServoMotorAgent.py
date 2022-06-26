import json
import cv2
import time
import random
import threading

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

from config import SERVER, IS_DEBUG

from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883
rotation_topic = "/camerarotation"
position_topic = "/cameraposition"

client_id = f'servo-motor-{random.randint(0, 1000)}'


class camThread(threading.Thread):
    def __init__(self, preview_name, cam_id, client_mqtt):
        threading.Thread.__init__(self)
        self.preview_name = preview_name
        self.cam_id = cam_id
        self.client_mqtt = client_mqtt

    def run(self):
        print("Starting" + self.preview_name)
        update_camera(self.preview_name, self.cam_id, self.client_mqtt)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def update_camera(preview_name, cam_id, client_mqtt):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    cv2.namedWindow(preview_name)
    cap = cv2.VideoCapture(cam_id)

    cv2.moveWindow(preview_name, -1000, -1000)

    time.sleep(1)
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # mirror the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6)  # detect the face
        for x, y, w, h in faces:
            # sending coordinates to Arduino
            string = 'X{0:d}Y{1:d}'.format((x+w//2), (y+h//2))
            client_mqtt.publish(rotation_topic, string.encode())
            # plot the center of the face
            cv2.circle(frame, (x+w//2, y+h//2), 2, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)

        cv2.rectangle(frame, (640//2-30, 480//2-30),
                      (640//2+30, 480//2+30),
                      (255, 255, 255), 3)
    # out.write(frame)
        cv2.imshow(preview_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyWindow(preview_name)


class ServoMotorAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid

        self.client_mqtt = mqtt_client.Client(client_id)
        self.client_mqtt.on_connect = on_connect
        self.client_mqtt.connect(broker, port)
        self.client_mqtt.loop_start()

    class RecvBehav(CyclicBehaviour):
        def __init__(self, client_mqtt):
            super().__init__()
            self.client_mqtt = client_mqtt
            self.is_showing_cam = False

        async def on_start(self):
            cam_thread = camThread("Central Cam", 1, self.client_mqtt)
            cam_thread.start()

        async def show_cam(self):
            cv2.moveWindow('Central Cam', 40, 50)
            cv2.moveWindow("Fixed Cam", -1000, -1000)
            self.is_showing_cam = True

        async def hide_cam(self):
            cv2.moveWindow('Central Cam', -1000, -1000)
            cv2.moveWindow("Fixed Cam", 40, 50)
            self.is_showing_cam = False

        async def run(self):
            msg = await self.receive(timeout=100)

            if msg is None:
                return

            body = json.loads(msg.body)

            print("ServoMotor received " + body["type"] + " message")
            if body["type"] == "camera_position":
                self.client_mqtt.publish(
                    position_topic, str(body["pos"]).encode())

                if self.is_showing_cam is False and body["initial_pos"] is False:
                    await self.show_cam()
            elif body["type"] == "camera_show":
                await self.show_cam()
            elif body["type"] == "camera_hide":
                await self.hide_cam()

    async def setup(self):
        print("Servo Motor agent started\n")
        receiveBehav = self.RecvBehav(self.client_mqtt)
        self.add_behaviour(receiveBehav)
