# This file aims interacting with the socket for reading & writing

import os
import sys
import socket

class SocketConnect:

    #Default Constructor for console>shell
    def __init__(self,message):
        unixsocket_path = "/var/run/openvassd.sock" #unixsocket_path is the socket of openvassd which it uses to communicate with redis and any manager
        self.message=message

        ##Create a socket object sock and connect the client to it (the server is openvas-scanner)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        print >>sys.stderr, 'connecting to %s' % unixsocket_path #make sure any input goes to sderr
        try:
            sock.connect(unixsocket_path)
        except socket.error, msg:
            print >>sys.stderr, msg
            sys.exit(1)

    #Writing in the socket
    def send_msg(self):
        for line in self.message:
            sock.send(line)
            sys.stdout.write(line)
            time.sleep(.0100)

    #Reading in the socket and output in sdtout
    def recv_msg(self):
        while True:
            data = sock.recv(1)
            sys.stdout.write(data)
