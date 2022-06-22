import json
import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class MicrophoneAgent(Agent):
    def __init__(self, jid: str, password: str, pos, initial_pos=False):
        super().__init__(jid, password)
        self.my_name = jid
        self.pos = pos
        self.initial_pos = initial_pos

    class RequestBehav(CyclicBehaviour):
        def __init__(self, pos, initial_pos):
            super().__init__()
            self.pos = pos
            self.initial_pos = initial_pos

        async def on_start(self):
            if self.initial_pos:
                test = Message(to="podcastmanageragent" + SERVER)
                test.set_metadata("performative", "inform")

                body = {
                    "type": "camera_position",
                    "pos": self.pos
                }

                test.body = json.dumps(body)
                await self.send(test)
                print("Message sent to Podcast Manager!\n")

        async def run(self):
            return

    async def setup(self):
        print("Microphone agent started\n")
        requestBehav = self.RequestBehav(self.pos, self.initial_pos)
        self.add_behaviour(requestBehav)
