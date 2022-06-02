import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class ClientAgent(Agent):

    def __init__(self, op1, op2, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid
        self.op1 = op1
        self.op2 = op2

    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class RequestBehav(OneShotBehaviour):
        async def run(self):
            new_msg = Message(to="calculatoragent" + SERVER)  # Instantiate the message
            new_msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

            new_msg_object = {
                "op1": self.agent.op1,
                "operation": "+",
                "op2": self.agent.op2
            }
            msg_json = json.dumps(new_msg_object)

            new_msg.body = msg_json  # Set the message content
            await self.send(new_msg)

    class ReciveBehav(CyclicBehaviour):
        async def run(self):

            msg = await self.receive(timeout=2)  # wait for a message for 5 seconds
            if msg:
                if IS_DEBUG:
                    self.agent.agent_say(msg)
                self.agent.agent_say(
                    str(self.agent.op1) + " + " + str(self.agent.op2) + " = " + json.loads(msg.body)["result"])
                self.agent.agent_say("Finishing")
                await self.agent.stop()
            else:
                self.agent.agent_say("Did not received any message after 5 seconds")
                await self.agent.stop()

    async def setup(self):
        self.agent_say("Agent starting . . .")
        requestB = self.RequestBehav()
        reciveB = self.ReciveBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(requestB, template)
        self.add_behaviour(reciveB, template)
