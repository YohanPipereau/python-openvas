import os, socket, time, sys, threading
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
    #print >>sys.stderr, 'connecting to %s' % unixsocket_path #make sure any input goes to sderr
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
            #time.sleep(.05)
	    event.set()

    def recv_msg(sock):
	outputVar = ""
        while True:
	    global event
	    event.wait() #block sender until receiver send set
            data = sock.recv(1024) #receive buffer of 1024 bits
            #sys.stdout.write(data)
	    outputVar = outputVar + data #We put everything read into this Var
	    outputList = outputVar.splitlines(True)
	    outputLastLine = outputList.pop()
	    #print(len(outputList))
	    print(outputLastLine)

	    #Detect the matching section we want to parse
	    #if data == parserMatch:
	    # 	ParsingTrigger = True
	    #if parsingTrigger == True:
	    ##Every object has a parser which is called if we detect a line which match parserMatch
	    #    object.parser(outputLastLine) 
	    #knowing the end of the matching section

#	    if outputLastLine == "<|> SERVER":
#		ParsingTrigger = False
#		return("""
#l
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#o
#l
#""")

    #Use threads to allow concurrent access to the socket instead of linear access
    Thread(target=send_msg, args=(sock,message)).start()
    Thread(target=recv_msg, args=(sock,)).start()
