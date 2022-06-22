import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class PodcastManagerAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid
        self.mqtt_client = None

    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class ReceiveAndRequestBehav(CyclicBehaviour):
        async def run(self):

            msg = await self.receive(timeout=100)
            if msg is None:
                return

            body = json.loads(msg.body)

            print("PodcastManager received " + body["type"] + " message")
            if body["type"] == "camera_position":
                test = Message(to="servomotoragent" + SERVER)
                test.set_metadata("performative", "inform")
                test.body = msg.body

                await self.send(test)
                print("Message sent to Servo Motor!\n")

            """
            if(msg2):
                print("PodcastManager: Reiceved message: " + msg2.body + "\n")

                # Dois ou mais microfones
                if(msg2.body == "Dois microfones detetados"):
                    # Instantiate the message
                    msg = Message(to="fixedcamagent" + SERVER)
                    # Set the "inform" FIPA performative
                    msg.set_metadata("performative", "inform")

                    print("Sending message to Fixed Cam. \n")
                    msg.body = msg2.body                  # Set the message content

                    await self.send(msg)
                    print("Message sent to Fixed Cam!\n")

                # Apenas um microfone
                else:

                    new_msg_object = json.loads(msg2.body)

                    # Instantiate the message
                    new_msg = Message(to="servomotoragent" + SERVER)
                    # Set the "inform" FIPA performative
                    new_msg.set_metadata("performative", "inform")

                    msg_json = json.dumps(new_msg_object)
                    #posX = int(msg_object["posX"])
                    #posY = int(msg_object["posY"])

                    print("Sending message to ServoMotor. \n")
                    # msg.body = msg2.body                  # Set the message content

                    new_msg.body = msg_json  # Set the message content

                    await self.send(new_msg)
                    print("Message sent to Servo Motor!\n")
            """
            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("Podcast Manager Agent started\n")
        template = Template()
        template.set_metadata("performative", "inform")
        rcv_rqst_behav = self.ReceiveAndRequestBehav()
        self.add_behaviour(rcv_rqst_behav)
