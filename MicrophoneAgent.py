import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class MicrophoneAgent(Agent):
    def __init__(self, jid: str, password: str, posX, posY):
        super().__init__(jid, password)
        self.my_name = jid
        self.posX = posX
        self.posY = posY
    
    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class RequestBehav(CyclicBehaviour):
        async def run(self):
            #msg = Message(to="podcastmanageragent" + SERVER)     # Instantiate the message
            msg2 = Message(to="podcastmanageragent" + SERVER)     # Instantiate the message

            #msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg2.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

            msg2.body="Dois microfones detetados"

            #new_msg_object = {
            #    "posX": self.agent.posX,
            #    "posY": self.agent.posY
            #}                  

            #msg_json = json.dumps(new_msg_object)

            #msg.body=msg_json

            #await self.send(msg)
            await self.send(msg2)
            print("Message sent to Podcast Manager!\n")

            # stop agent from behaviour
            await self.agent.stop()
    
    async def setup(self):
        print("Microphone agent started\n")
        requestBehav = self.RequestBehav()
        self.add_behaviour(requestBehav)