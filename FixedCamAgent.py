import json
import numpy as np
import cv2
import threading


from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


from config import SERVER, IS_DEBUG


class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        print("Starting" + self.previewName)
        camPreview(self.previewName, self.camID)


def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


class FixedCamAgent(Agent):

    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid

    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class RecieveBehav(CyclicBehaviour):
        async def run(self):
            # wait for a message for 10 seconds
            msg = await self.receive(timeout=100)
            if msg:
                print("Fixed Cam: Message received with content: {}\n".format(msg.body))
                thread1 = camThread("Camera 1", 0)
                thread1.start()
            else:
                print("Did not received any message after 10 seconds")

    async def setup(self):
        print("Fixed Cam agent started\n")
        requestBehav = self.RecieveBehav()
        self.add_behaviour(requestBehav)
