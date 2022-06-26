import time
import subprocess
import sys

from FixedCamAgent import FixedCamAgent
from PodcastManagerAgent import PodcastManagerAgent
from ServoMotorAgent import ServoMotorAgent
from MicrophoneAgent import MicrophoneAgent

from config import SERVER

if __name__ == "__main__":
    podcast_manager = PodcastManagerAgent(
        jid="podcastmanageragent" + SERVER, password="password")
    future_podcast_manager = podcast_manager.start()
    future_podcast_manager.result()

    fixedcam = FixedCamAgent(jid="fixedcamagent" + SERVER, password="password")
    future_fixedcam = fixedcam.start()
    future_fixedcam.result()

    servo_motor = ServoMotorAgent(
        jid="servomotoragent" + SERVER, password="password")
    future_servomotor = servo_motor.start()
    future_servomotor.result()

    mic1_p = subprocess.Popen(
        [sys.executable, "./mic_launch.py", "m1", "150", "False", '"Conjunto de microfones (Realtek"', "20", "2"])

    mic2_p = subprocess.Popen(
        [sys.executable, "./mic_launch.py", "m2", "90", "False", '"Microfone (2- USB Audio Device) DirectSound"', "20", "2"])

    mic3_p = subprocess.Popen(
        [sys.executable, "./mic_launch.py", "m3", "30", "True", '"Auscultadores com Microfone (Jabra EVOLVE 30 II) DirectSound"', "20", "2"])

    try:
        while podcast_manager.is_alive() or servo_motor.is_alive() or fixedcam.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        # mic1_p.kill()
        # mic2_p.kill()
        # mic3_p.kill()
