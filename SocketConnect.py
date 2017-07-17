import os, socket, time, sys, threading, select
from threading import Thread
#from ParseOid import *

def SocketConnect(message,unixsocket_path = '/var/run/openvassd.sock'):
    #unixsocket_path is the socket of openvassd which it uses to communicate with redis and any manager

    try:
        #Check the existence of the socket
        os.path.isfile(unixsocket_path)
    except OSError:
        print(" This unixsocket does not exist ... default is /var/run/openvassd.sock ")

    ##Instantiate the socket and connect the client to it (the server is openvas-scanner)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(unixsocket_path)
    global event
    event = threading.Event()

    def send_msg(sock,message):
        for line in message.splitlines(True):
	    global event
	    event.set()
	    sock.send(line)
            sys.stdout.write(line)
	    time.sleep(0.1) #wait a bit cause the receiver is a bit long to write
	    event.clear()
	    event.set()

    def recv_msg(sock):
	outputVar = ""
        while True:
	    global event
	    event.wait() #block sender until receiver send set
	    do_read = False
	    try:
	        r, _, _  = select.select([sock], [], [], 1) #select syscall, check if data arrived
	        do_read = bool(r) #boolean false if nothing read last second
	    except socket.error:
	       pass
	    if do_read:
	        outputVar += sock.recv(1024)
	    else:
		return(outputVar)
	
    #Use threads to allow concurrent access to the socket instead of linear access
    Thread(target=send_msg, args=(sock,message)).start()
    Thread(target=recv_msg, args=(sock,)).start()
