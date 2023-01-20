import socket
import subprocess
import os
import signal

import utility
import log

BUFFER_SIZE = 512

# The port the camera listens to for commands from client
PORT_LISTEN_COMMAND_TCP = 6090
# Sender will send back to this server port (STATE)
PORT_LISTEN_SERVER = 6085

SENDER_ID = utility.rand_str(32)

s = None

def get_hostname():
    return socket.gethostname()

def server_close():
    log.debug("Closing socket")
    s.close()

def send_tcp(dst_ip, data):
    dst_port = PORT_LISTEN_SERVER

    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((dst_ip, dst_port))
        tcp_client.send(bytes(data, "utf-8"))
    finally:
        tcp_client.close()

def receive_tcp(cfg_width, cfg_height, cfg_framerate, is_video, is_audio):
    global s
    s = socket.socket()
    log.debug("Socket successfully created")

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', PORT_LISTEN_COMMAND_TCP))
    log.debug("socket bound to %s" %(PORT_LISTEN_COMMAND_TCP))

    # put the socket into listening mode
    s.listen(5)
    log.debug("socket is listening")

    current_state = "IDLE"

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        #log.debug("Got connection from " + addr[0])

        buffer = c.recv(BUFFER_SIZE)
        cmd = buffer.decode('utf-8')
        log.debug("Received: " + cmd)

        if (cmd == "SCAN"):
            hostname = get_hostname()
            sender_id = SENDER_ID
            state = current_state
            width = cfg_width
            height = cfg_height
            has_video = is_video
            has_audio = is_audio
            c.send(bytes("SCAN " + hostname + " " + sender_id + " " + state + " " + width + " " + height + " " + has_video + " " + has_audio, 'utf-8'))
        if (cmd == "START"):
            # STATE senderId 192.168.0.24:V;192.168.0.27:A
            current_state = "CONNECTED"
            send_tcp(addr[0], "STATE " + SENDER_ID + " " + current_state)
        if (cmd.startswith("CONNECT")):
            # CONNECT UDP 192.168.178.46 6201 -1
            splitted = cmd.split(" ")
            url = "udp://" + splitted[2] + ":" + splitted[3]
            cmd = subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-f", "avfoundation", "-framerate", cfg_framerate, "-video_size", "640x480", "-i", "0", "-f", "mpegts", url])
            pid = cmd.pid

            current_state = "CONNECTED;" + splitted[2] + ":V"
            send_tcp(addr[0], "STATE " + SENDER_ID + " " + current_state)

        if (cmd == "RESET"):
            current_state = "CONNECTED"
            os.kill(pid, signal.SIGTERM)
            send_tcp(addr[0], "STATE " + SENDER_ID + " " + current_state)

        if (cmd == "STOP"):
            current_state = "IDLE"
            os.kill(pid, signal.SIGTERM)
            send_tcp(addr[0], "STATE " + SENDER_ID + " " + current_state)

        #log.debug("Close the connection")
        # Close the connection with the client
        c.close()