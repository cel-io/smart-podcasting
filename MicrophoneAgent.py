import json
import sounddevice as sd
import numpy as np
import time
import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from config import SERVER, IS_DEBUG


class MicrophoneAgent(Agent):
    def __init__(self, jid: str, password: str, pos, initial_pos, device_id, activation_limit, channels):
        super().__init__(jid, password)
        self.pos = pos
        self.initial_pos = initial_pos
        self.device_id = device_id
        self.activation_limit = activation_limit
        self.channels = channels

    class RequestBehav(CyclicBehaviour):
        def __init__(self, pos, initial_pos, device_id, activation_limit, channels):
            super().__init__()
            self.pos = pos
            self.initial_pos = initial_pos
            self.activation_limit = activation_limit
            self.mic_stream = sd.InputStream(
                callback=self.check_sound, device=device_id, channels=channels)
            self.detected_voice = False

        async def send_position(self, initial_pos):
            msg = Message(to="podcastmanageragent" + SERVER)

            body = {
                "type": "camera_position",
                "pos": self.pos,
                "initial_pos": initial_pos
            }

            msg.body = json.dumps(body)
            await self.send(msg)

        def check_sound(self, indata, frames, time, status):
            volume_norm = np.linalg.norm(indata)*10
            if int(volume_norm) > self.activation_limit:
                self.detected_voice = True

        async def on_start(self):
            if self.initial_pos:
                await self.send_position(True)
            self.mic_stream.start()

        async def run(self):
            sd.sleep(250)
            if self.detected_voice:
                await self.send_position(False)
                self.detected_voice = False
                sd.sleep(2000)

        async def on_end(self) -> None:
            self.mic_stream.stop()
            self.mic_stream.close()

    async def setup(self):
        print("Microphone agent started\n")
        requestBehav = self.RequestBehav(
            self.pos, self.initial_pos, self.device_id, self.activation_limit, self.channels)
        self.add_behaviour(requestBehav)
