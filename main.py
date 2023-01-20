import signal
import os
import time
import sys
import getopt

import network
import log

cfg_width = "640"
cfg_height = "480"
cfg_framerate = "30"
has_video = "1"
has_audio = "0"

log.debug("Starting...")
log.debug("Hostname: " + network.get_hostname())

# Setup signal handling

def handler(signum, frame):
    log.debug("Stopping...")
    network.server_close()
    exit(1)

signal.signal(signal.SIGINT, handler)

# Command line arguments

# Remove 1st argument from the list of command line arguments
argumentList = sys.argv[1:]
# Options
options = "w:h:f:"
# Long options
long_options = ["width=", "height=", "framerate="]
# Parsing argument
arguments, values = getopt.getopt(argumentList, options, long_options)
# checking each argument
for currentArgument, currentValue in arguments:
    if currentArgument in ("-w", "--width"):
        cfg_width = currentValue
    if currentArgument in ("-h", "--height"):
        cfg_height = currentValue
    if currentArgument in ("-f", "--framerate"):
        cfg_framerate = currentValue

log.debug ("Width: " + cfg_width)
log.debug ("Height: " + cfg_height)
log.debug ("Framerate: " + cfg_framerate)

# Start server

network.receive_tcp(cfg_width, cfg_height, cfg_framerate, has_video, has_audio)

while True:
    time.sleep(0.1)

log.debug("Finished.")