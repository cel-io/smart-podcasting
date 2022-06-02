import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class SumAgent(Agent):

    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid

    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class ReciveBehav(CyclicBehaviour):
        async def run(self):

            msg = await self.receive(timeout=2)  # wait for a message for 10 seconds
            if msg:
                if IS_DEBUG:
                    self.agent.agent_say(msg)
                if str(msg.sender) == "calculatoragent" + SERVER:
                    msg_object = json.loads(msg.body)

                    new_msg = Message(to=str(msg.sender))  # Instantiate the message
                    new_msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

                    result = float(msg_object["op1"]) + float(msg_object["op2"])
                    new_msg_object = {
                        "result": str(result),
                        "originID": msg_object["originID"]
                    }
                    msg_json = json.dumps(new_msg_object)

                    new_msg.body = msg_json  # Set the message content
                    await  self.send(new_msg)
            else:
                self.agent.agent_say("Finishing")
                # self.agent.agent_say("Did not received any message after 10 seconds")
                await self.agent.stop()

    async def setup(self):
        self.agent_say("Agent starting . . .")
        reciveB = self.ReciveBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(reciveB, template)
