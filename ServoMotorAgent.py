import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


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