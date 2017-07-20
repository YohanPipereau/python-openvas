import os, socket, time, sys, select

def SocketConnect(message,unixsocket_path = '/var/run/openvassd.sock'):
    #unixsocket_path is the socket of openvassd which it uses to communicate with redis and any manager
    outputVar=""
    try:
        #Check the existence of the socket
        os.path.isfile(unixsocket_path)
    except OSError:
        print(" This unixsocket does not exist ... default is /var/run/openvassd.sock ")

    ##Instantiate the socket and connect the client to it (the server is openvas-scanner)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(unixsocket_path)
    sock.setblocking(False)
    for line in message.splitlines(True):
	if line == "< OTP/2.0 >\n":
	    sock.send(line)
	    print(line)
	    time.sleep(1)
	else:
	    print(line)
	    sock.send(line)
	    time.sleep(0.01)
    while True:
	try:
	    #outputVar += sock.recv(1024)
	    data = sock.recv(1024)
	    outputVar += data
	    print(data)
  	    r, _, _  = select.select([sock], [], [], 5) #select syscall, check if data arrived
	    do_read = bool(r)
	    if not do_read:
		sock.close()
		return(outputVar)
	except socket.error:
	    pass	
    return(outputVar)
