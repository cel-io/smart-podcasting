import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from time import time

from config import SERVER, IS_DEBUG

from collections import deque


class PodcastManagerAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.mqtt_client = None
        self.current_pos = None

    class ReceiveAndRequestBehav(CyclicBehaviour):
        def __init__(self, initial_pos):
            super().__init__()
            self.current_pos = initial_pos
            self.mic_activations = deque([], maxlen=3)
            self.having_conversation = False
            self.conversation_start = None

        async def run(self):
            msg = await self.receive(timeout=100)
            if msg is None:
                return

            # Ignore camera_position mes
            if self.having_conversation and (time() - self.conversation_start) > 10:
                self.having_conversation = False
                self.conversation_start = None
                self.mic_activations = deque([], maxlen=3)
            elif self.having_conversation:
                return

            self.having_conversation = False

            body = json.loads(msg.body)

            if body["type"] == "camera_position":
                if body["pos"] != self.current_pos:
                    send_msg = Message(to="servomotoragent" + SERVER)
                    send_msg.body = msg.body

                    await self.send(send_msg)

                    if body["initial_pos"]:
                        return

                    self.current_pos = body["pos"]
                    await self.check_for_conversation()

        async def check_for_conversation(self):
            # if the queue is empty or the last added mic activation is different from the current one
            if not self.mic_activations or self.mic_activations[len(self.mic_activations) - 1]["pos"] != self.current_pos:
                self.mic_activations.append(
                    {"pos": self.current_pos, "on": time()})

            # At least a back and forth conversation that occured in X senconds
            if len(self.mic_activations) == 3 and (self.mic_activations[2]["on"] - self.mic_activations[0]["on"]) <= 6:
                # Conversation detected
                self.having_conversation = True
                self.conversation_start = time()
                self.current_pos = None

                send_msg = Message(to="servomotoragent" + SERVER)
                send_msg.body = json.dumps({
                    "type": "camera_hide"
                })

                await self.send(send_msg)

    async def setup(self):
        print("Podcast Manager Agent started\n")
        rcv_rqst_behav = self.ReceiveAndRequestBehav(self.current_pos)
        self.add_behaviour(rcv_rqst_behav)
