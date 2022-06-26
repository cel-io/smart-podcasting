import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class PodcastManagerAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.mqtt_client = None
        self.current_pos = None

    class ReceiveAndRequestBehav(CyclicBehaviour):
        def __init__(self, initial_pos):
            super().__init__()
            self.current_pos = initial_pos

        async def run(self):
            msg = await self.receive(timeout=100)
            if msg is None:
                return

            body = json.loads(msg.body)

            if body["type"] == "camera_position":
                if body["pos"] != self.current_pos:
                    send_msg = Message(to="servomotoragent" + SERVER)
                    send_msg.body = msg.body

                    await self.send(send_msg)

                    self.current_pos = body["pos"]

    async def setup(self):
        print("Podcast Manager Agent started\n")
        rcv_rqst_behav = self.ReceiveAndRequestBehav(self.current_pos)
        self.add_behaviour(rcv_rqst_behav)
