import os, socket, time, sys, threading, select, multiprocessing
from multiprocessing import Process, Queue

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
    event = multiprocessing.Event()

    def send_msg(sock,message):
        for line in message.splitlines(True):
	    global event
	    event.set()
	    sock.send(line)
	    time.sleep(0.1) #wait a bit cause the receiver is a bit long to write
	    event.clear()
	    event.set()

    def recv_msg(sock,q):
	outputVar = ""
        while True:
	    global event
	    event.wait() #block sender until receiver send set
	    do_read = False
	    try:
	        r, _, _  = select.select([sock], [], [], 5) #select syscall, check if data arrived
		#3 is a timeout of 3s which can be changed if the script stop too early
	        do_read = bool(r) #boolean false if nothing read last second
	    except socket.error:
	       pass
	    if do_read:
	        outputVar += sock.recv(1024)
	    else:
		q.put(outputVar)
		sys.exit(0)

    #Use threads to allow concurrent access to the socket instead of linear access
    sendProcess = Process(target=send_msg, args=(sock,message))
    q = Queue()
    receiveProcess = Process(target=recv_msg, args=(sock,q))
   
    sendProcess.start()
    receiveProcess.start()
    copy = q.get()
    sendProcess.join() #block the main thread until sendProcess is over
    receiveProcess.join()
    
    return(copy)
