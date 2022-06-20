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

    servo_motor=ServoMotorAgent(jid="servomotoragent" + SERVER, password="password")
    future_servomotor = servo_motor.start()
    future_servomotor.result()

    podcast_manager = PodcastManagerAgent(jid="podcastmanageragent" + SERVER, password="password")
    future_podcast_manager = podcast_manager.start()
    future_podcast_manager.result()

    microphone = MicrophoneAgent(jid="m1" + SERVER, password="password")
    future_microphone = microphone.start()
    future_microphone.result()

    try:
        while microphone.is_alive() or podcast_manager.is_alive() or servo_motor.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    #microphone.stop()
