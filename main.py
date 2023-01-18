import signal
import subprocess
import os
import time

import network
import log

log.debug("Starting...")
log.debug("Hostname: " + network.get_hostname())

def handler(signum, frame):
    log.debug("Stopping...")
    network.server_close()
    exit(1)

pid = 0

signal.signal(signal.SIGINT, handler)

network.receive_tcp()

cmd = subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-f", "avfoundation", "-framerate", "30", "-i", "0", "out.mpg"])
pid = cmd.pid

log.debug("---")
log.debug("PID: " + str(pid))
log.debug("---")

# Mac: ffmpeg -f avfoundation -framerate 30 -i "0" out.mpg
# ffplay udp://192.168.178.46:8554 -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop
# ffmpeg -f avfoundation -framerate 30 -i "0" -f mpegtsv  udp://192.168.178.46:8554

while True:
    time.sleep(0.1)

log.debug("Finished.")