# This file aims interacting with the socket for reading & writing

import os
import sys
from threading import Thread
import socket

class SocketConnect

    #Default Constructor for console>shell
    def __init__(self):
        #unixsocket_path is the socket of openvassd which it uses to communicate with redis and any manager
        self.unixsocket_path = input("openvassd unixsocket path? Check /etc/openvas/openvassd... Default is /var/run/openvassd.sock")

    ##Check the existence of the socket
    try:
        os.path.isfile(unixsocket_path)
    except OSError:
        print(" This unixsocket does not exist ... default is /var/run/openvassd.sock ")

    ##Instantiate the socket and connect the client to it (the server is openvas-scanner)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print >>sys.stderr, 'connecting to %s' % unixsocket_path #make sure any input goes to sderr
    try:
        sock.connect(unixsocket_path)
    except socket.error, msg:
        print >>sys.stderr, msg
        sys.exit(1)

    ##Writing and Reading in the socket
    #Writing in the socket
    #message = "CLIENT <|> NVT_INFO"
    def send_msg(sock):
        sock.send("< OTP/2.0 >") #to keep the connection opened to the socket you need to write < OTP/2.0 > at the begining
        while True:
            data = sys.stdin.readline()
            sock.send(data)

    #Reading in the socket$
    def recv_msg(sock):
        while True:
            data = sock.recv(1024)
            sys.stdout.write(data)

    Thread(target=send_msg, args=(sock,)).start()
    Thread(target=recv_msg, args=(sock,)).start()
