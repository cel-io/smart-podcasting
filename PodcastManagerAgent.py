import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class PodcastManagerAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid
    
    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    #class RecvBehav(CyclicBehaviour):
    #    async def run(self):
    #        msg = await self.receive(timeout=100) # wait for a message for 10 seconds
    #        if msg:
    #            print("Podcast Manager - Message received with content: {}\n".format(msg.body))
    #        else:
    #            print("Did not received any message after 10 seconds\n")
    #
    #        # stop agent from behaviour
    #        await self.agent.stop()

    class ReceiveAndRequestBehav(CyclicBehaviour):
        async def run(self):

            msg2 = await self.receive(timeout=100) #wait for a message for 10 seconds

            if(msg2):
                print("PodcastManager: Reiceved message: " + msg2.body + "\n")
                msg = Message(to="servomotoragent" + SERVER)     # Instantiate the message
                msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

                print("Sending message to ServoMotor. \n")
                msg.body = msg2.body                  # Set the message content

                await self.send(msg)
                print("Message sent to Servo Motor!\n")

                # stop agent from behaviour
                await self.agent.stop()

    async def setup(self):
        print("Podcast Manager Agent started\n")
        #receiveBehav = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        #self.add_behaviour(receiveBehav, template)
        rcv_rqst_behav = self.ReceiveAndRequestBehav()
        self.add_behaviour(rcv_rqst_behav)