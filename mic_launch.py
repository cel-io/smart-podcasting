import time
import sys

from MicrophoneAgent import MicrophoneAgent

from config import SERVER

jid = sys.argv[1]
pos = int(sys.argv[2])
initial_pos = sys.argv[3] == "True"
device_id = sys.argv[4][1:-1]
activation_limit = int(sys.argv[5])
channels = int(sys.argv[6])


mic = MicrophoneAgent(
    jid=jid + SERVER, password="password", pos=pos, initial_pos=initial_pos, device_id=device_id, activation_limit=activation_limit, channels=channels)
future_mic = mic.start()
future_mic.result()

try:
    while mic.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping Mic...")
