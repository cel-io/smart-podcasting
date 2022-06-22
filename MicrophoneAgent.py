import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class MicrophoneAgent(Agent):
    def __init__(self, jid: str, password: str, pos):
        super().__init__(jid, password)
        self.my_name = jid
        self.pos = pos

    class RequestBehav(CyclicBehaviour):
        def set_pos(self, pos):
            self.pos = pos

        async def run(self):
            test = Message(to="podcastmanageragent" + SERVER)
            test.set_metadata("performative", "inform")

            body = {
                "type": "camera_position",
                "pos": self.pos
            }

            test.body = json.dumps(body)
            await self.send(test)
            print("Message sent to Podcast Manager!\n")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("Microphone agent started\n")
        requestBehav = self.RequestBehav()
        requestBehav.set_pos(self.pos)
        self.add_behaviour(requestBehav)
