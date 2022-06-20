import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class MicrophoneAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid
    
    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class RequestBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="podcastmanageragent" + SERVER)     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Dois microfones detetados"                    # Set the message content

            await self.send(msg)
            print("Message sent to Podcast Manager!\n")

            # stop agent from behaviour
            await self.agent.stop()
    
    async def setup(self):
        print("Microphone agent started\n")
        requestBehav = self.RequestBehav()
        self.add_behaviour(requestBehav)