"""
    This file contains the Socket tool function to interact with the scanner socket.
"""

import os, socket, time, sys, select

class SocketConnect:

    def __init__(self, oidTimeout, initialize_timer, unixsocket_path = '/var/run/openvassd.sock'):
        self.oidTimeout = oidTimeout
        self.initialize_timer = initialize_timer
        self.unixsocket_path = unixsocket_path
	try:
             os.path.isfile(unixsocket_path) #Check the existence of the socket
        except OSError:
            print(" This unixsocket does not exist ... default is /var/run/openvassd.sock ")
       ##Instantiate the socket and connect the client to it (the server is openvas-scanner)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(unixsocket_path)


    def Send(self,message):
        for line in message:
            if line == "< OTP/2.0 >":
                self.sock.send(line)
                time.sleep(initialize_timer)
            else:
                    self.sock.send(line)
                    time.sleep(0.01)

    def Receive(self, verbose=False):
        outputVar=""
        if verbose == True:
            print_verbose = lambda x: sys.stdout.write(x)
        else:
            print_verbose = lambda x: None
        while True:
	    try:
		self.sock.settimeout(self.oidTimeout)
		data = self.sock.recv(1024)
		self.sock.settimeout(None)
		outputVar += data
		if "<|> BYE" in data:
		    return(outputVar)
		print_verbose(data)
	    except socket.timeout:
		#print("timeout")
		return(outputVar)

    def Close(self):
        pass #todo
