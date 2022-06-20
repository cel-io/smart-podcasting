import json
import cv2
import serial
import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


def openCamera():
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    cap=cv2.VideoCapture(0)
    #ArduinoSerial=serial.Serial('COM8',9600,timeout=0.1)
    time.sleep(1)

    while cap.isOpened():
        ret, frame= cap.read()
        frame=cv2.flip(frame,1)  #mirror the image
    #print(frame.shape)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces= face_cascade.detectMultiScale(gray,1.1,6)  #detect the face
        for x,y,w,h in faces:
        #sending coordinates to Arduino
            string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
            print(string)
            #ArduinoSerial.write(string.encode('utf-8'))
        #plot the center of the face
            cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
        #plot the roi
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    #plot the squared region in the center of the screen
        cv2.rectangle(frame,(640//2-30,480//2-30),
                 (640//2+30,480//2+30),
                  (255,255,255),3)
    #out.write(frame)
        cv2.imshow('img',frame)

        if cv2.waitKey(1)&0xFF== ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

class ServoMotorAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid
    
    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class RecvBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=100) # wait for a message for 10 seconds
            if msg:
                msg_object = json.loads(msg.body)

                camera1 = openCamera()
                print("Servo Motor: Message received with content: {}\n".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("Servo Motor agent started\n")
        receiveBehav = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehav, template)