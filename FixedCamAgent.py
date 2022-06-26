import json
import numpy as np
import cv2
import threading


from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class camThread(threading.Thread):
    def __init__(self, preview_name, cam_id):
        threading.Thread.__init__(self)
        self.preview_name = preview_name
        self.cam_id = cam_id

    def run(self):
        print("Starting" + self.preview_name)
        camPreview(self.preview_name, self.cam_id)


def camPreview(preview_name, cam_id):
    cv2.namedWindow(preview_name)
    cam = cv2.VideoCapture(cam_id)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    cv2.moveWindow('Fixed Cam', 40, 50)

    while rval:
        cv2.imshow(preview_name, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(preview_name)


class FixedCamAgent(Agent):

    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)

    class RecieveBehav(CyclicBehaviour):
        async def on_start(self) -> None:
            cam_thread = camThread("Fixed Cam", 0)
            cam_thread.start()

        async def run(self):
            pass

    async def setup(self):
        print("Fixed Cam agent started\n")
        requestBehav = self.RecieveBehav()
        self.add_behaviour(requestBehav)
