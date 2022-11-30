import socket

import log

BUFFER_SIZE = 512

#// The port the camera listens to for commands from client
PORT_LISTEN_COMMAND_TCP = 6090

s = None

def server_close():
    s.close()

def receive_tcp():
    s = socket.socket()
    log.debug("Socket successfully created")
    
    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', PORT_LISTEN_COMMAND_TCP))
    log.debug("socket binded to %s" %(PORT_LISTEN_COMMAND_TCP))

    # put the socket into listening mode
    s.listen(5)
    log.debug("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        log.debug("Got connection")

        buffer = c.recv(BUFFER_SIZE)
        cmd = buffer.decode('utf-8')
        log.debug("Received: " + cmd)
    
        # send a thank you message to the client.
        c.send(b"Thank you for connecting")
    
        log.debug("Close the connection")
        # Close the connection with the client
        c.close()