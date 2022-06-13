import time

from PodcastManagerAgent import PodcastManagerAgent
from MicrophoneAgent import MicrophoneAgent
from ServoMotorAgent import ServoMotorAgent
from config import SERVER

if __name__ == "__main__":

    servomotor = ServoMotorAgent(jid="servomotoragent" + SERVER, password="password")
    future_servomotor = servomotor.start()
    future_servomotor.result()

    podcastmanager = PodcastManagerAgent(jid="podcastmanageragent" + SERVER, password="password")
    future_podcastmanager = podcastmanager.start()
    future_podcastmanager.result()

    microphone = MicrophoneAgent(op1=10.0, op2=20.0, jid="m1" + SERVER, password="password")
    future_microphone = microphone.start()
    future_microphone.result()

    try:
        while servomotor.is_alive() or podcastmanager.is_alive() or microphone.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    microphone.stop()
