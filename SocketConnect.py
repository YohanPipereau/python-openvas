"""
    This file contains the Socket tool function to interact with the scanner socket.
"""

import os, socket, time, sys, select

class SocketConnect:

    def __init__(self, initialize_timer, unixsocket_path = '/var/run/openvassd.sock'):
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
        totalsent = 0
        while totalsent < len(message):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

        '''for line in message:
	    print(line)
            if line == "< OTP/2.0 >\n":
                self.sock.send(line)
                time.sleep(self.initialize_timer)
            else:
                self.sock.send(line)
                #time.sleep(0.01)'''

    def Receive(self,timeout, verbose=False):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 2048:
            chunk = self.sock.recv(min(2048 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
        '''outputVar=""
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
		print_verbose(data)
	    except socket.timeout:
		print("timeout")
		self.sock.settimeout(None)
		return(outputVar)'''

    def Close(self):
        self.sock.close()
