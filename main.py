import time

from FixedCamAgent import FixedCamAgent
from MicrophoneAgent import MicrophoneAgent
from PodcastManagerAgent import PodcastManagerAgent
from ServoMotorAgent import ServoMotorAgent

from config import SERVER

if __name__ == "__main__":

    fixedcam = FixedCamAgent(jid="fixedcamagent" + SERVER, password="password")
    future_fixedcam = fixedcam.start()
    future_fixedcam.result()

    servo_motor = ServoMotorAgent(
        jid="servomotoragent" + SERVER, password="password")
    future_servomotor = servo_motor.start()
    future_servomotor.result()

    podcast_manager = PodcastManagerAgent(
        jid="podcastmanageragent" + SERVER, password="password")
    future_podcast_manager = podcast_manager.start()
    future_podcast_manager.result()

    microphone1 = MicrophoneAgent(
        jid="m1" + SERVER, password="password", pos=30)
    future_microphone = microphone1.start()
    future_microphone.result()

    microphone2 = MicrophoneAgent(
        jid="m2" + SERVER, password="password", pos=90)
    future_microphone = microphone2.start()
    future_microphone.result()

    microphone3 = MicrophoneAgent(
        jid="m3" + SERVER, password="password", pos=150, initial_pos=True)
    future_microphone = microphone3.start()
    future_microphone.result()

    try:
        while microphone1.is_alive() or microphone2.is_alive() or microphone3.is_alive() or podcast_manager.is_alive() or servo_motor.is_alive() or fixedcam.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    # microphone.stop()
