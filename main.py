import time

from PodcastManagerAgent import PodcastManagerAgent
from MicrophoneAgent import MicrophoneAgent
from ServoMotorAgent import ServoMotorAgent
from config import SERVER

if __name__ == "__main__":

    sum = ServoMotorAgent(jid="servomotoragent" + SERVER, password="password")
    future_sum = sum.start()
    future_sum.result()

    calculator = PodcastManagerAgent(jid="podcastmanageragent" + SERVER, password="password")
    future_calculator = calculator.start()
    future_calculator.result()

    client = MicrophoneAgent(op1=10.0, op2=20.0, jid="m1" + SERVER, password="password")
    future_client = client.start()
    future_client.result()

    try:
        while sum.is_alive() or calculator.is_alive() or client.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    client.stop()
