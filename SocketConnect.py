import socket, time, threading, sys

class SocketSend(threading.Thread):


import os
import time
import sys
from threading import Thread
import socket


def SocketConnect():
    #unixsocket_path is the socket of openvassd which it uses to communicate with redis and any manager
    unixsocket_path = '/var/run/openvassd.sock'

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
        for line in open('25478.client'):
            sock.send(line)
            sys.stdout.write(line)
            time.sleep(0.1)

    #Reading in the socket$
    def recv_msg(sock):
        while True:
            data = sock.recv(1024)
            sys.stdout.write(data)

    #Use threads to allow concurrent access to the socket instead of linear access
    Thread(target=send_msg, args=(sock,)).start()
    Thread(target=recv_msg, args=(sock,)).start()
