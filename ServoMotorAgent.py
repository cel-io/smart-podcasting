import json
from socket import timeout
import cv2
import serial
import time
import random
from multiprocessing import Process

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


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def update_camera():
    # We need another client_mqtt since this is ran in another process
    client_mqtt = mqtt_client.Client(client_id)
    client_mqtt.on_connect = on_connect
    client_mqtt.connect(broker, port)
    client_mqtt.loop_start()

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    cap = cv2.VideoCapture(1)

    time.sleep(1)
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # mirror the image
    # print(frame.shape)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6)  # detect the face
        for x, y, w, h in faces:
            # sending coordinates to Arduino
            string = 'X{0:d}Y{1:d}'.format((x+w//2), (y+h//2))
            # print(string)
            client_mqtt.publish(rotation_topic, string.encode())
            # plot the center of the face
            cv2.circle(frame, (x+w//2, y+h//2), 2, (0, 255, 0), 2)
        # plot the roi
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
    # plot the squared region in the center of the screen
        cv2.rectangle(frame, (640//2-30, 480//2-30),
                      (640//2+30, 480//2+30),
                      (255, 255, 255), 3)
    # out.write(frame)
        cv2.imshow('img', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


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

        async def on_start(self):
            camera_process = Process(target=update_camera)
            camera_process.start()

        async def run(self):
            msg = await self.receive(timeout=100)

            if msg is None:
                return

            body = json.loads(msg.body)

            print("ServoMotor received " + body["type"] + " message")
            if body["type"] == "camera_position":
                self.client_mqtt.publish(
                    position_topic, str(body["pos"]).encode())

    async def setup(self):
        print("Servo Motor agent started\n")
        receiveBehav = self.RecvBehav(self.client_mqtt)
        self.add_behaviour(receiveBehav)
