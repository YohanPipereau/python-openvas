"""
    This file contains the Socket tool function to interact with the scanner socket.
"""

import os, socket, time, sys

class SocketConnect:

    def __init__(self, unixsocket_path = '/var/run/openvassd.sock'):
        self.unixsocket_path = unixsocket_path
	try:
             os.path.isfile(unixsocket_path) #Check the existence of the socket
        except OSError:
            print(" This unixsocket does not exist ... default is /var/run/openvassd.sock ")
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(unixsocket_path)


    def Send(self,message):
	"""
	    Send function inspired by official doc.
	    Suited for cases where we don't know the server buffer size.
        """
	print(message)
        totalsent = 0
        while totalsent < len(message):
            sent = self.sock.send(message[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def Receive(self,timeout, verbose=False):
	"""
	    Receive function using timeout because of unknown socket buffer size.
	"""
        outputVar=""
        if verbose == True:
            print_verbose = lambda x: sys.stdout.write(x)
        else:
            print_verbose = lambda x: None
        while True:
	    try:
		self.sock.settimeout(timeout)
		data = self.sock.recv(1024)
		self.sock.settimeout(None)
		outputVar += data
		if "<|> BYE" in data:
		    return(outputVar)
		#print_verbose(data)
	  	print(data)
	    except socket.timeout:
		self.sock.settimeout(None)
		return(outputVar)
    
    def Close(self):
        self.sock.close()
