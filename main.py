import time

from PodcastManagerAgent import PodcastManagerAgent
from MicrophoneAgent import MicrophoneAgent
from ServoMotorAgent import ServoMotorAgent
from CentralCameraAgent import CentralCameraAgent
from FixedCameraAgent import FixedCameraAgent

from config import SERVER

if __name__ == "__main__":

    microphone1 = MicrophoneAgent(op1=10.0, op2=20.0, jid="m1" + SERVER, password="password")
    future_microphone1 = microphone1.start()
    future_microphone1.result()

    microphone2 = MicrophoneAgent(op1=5.0, op2=5.0, jid="m2" + SERVER, password="password")
    future_microphone2 = microphone2.start()
    future_microphone2.result()

    microphone3 = MicrophoneAgent(op1=7.0, op2=3.0, jid="m3" + SERVER, password="password")
    future_microphone3 = microphone3.start()
    future_microphone3.result()

    podcastmanager = PodcastManagerAgent(jid="podcastmanageragent" + SERVER, password="password")
    future_podcastmanager = podcastmanager.start()
    future_podcastmanager.result()

    servomotor = ServoMotorAgent(jid="servomotoragent" + SERVER, password="password")
    future_servomotor = servomotor.start()
    future_servomotor.result()

    centralcamera = CentralCameraAgent(jid="centralcameraagent" + SERVER, password="password")
    future_centralcamera = centralcamera.start()
    future_centralcamera.result()

    fixedcamera = FixedCameraAgent(jid="fixedcameraagent" + SERVER, password="password")
    future_fixedcamera = fixedcamera.start()
    future_fixedcamera.result()

    try:
        while servomotor.is_alive() or podcastmanager.is_alive() or microphone1.is_alive() or microphone2.is_alive() or microphone3.is_alive() or centralcamera.is_alive() or fixedcamera.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    microphone1.stop()
