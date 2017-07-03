import os
import sys
import socket

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
#Wiriting in the socket
sock.sendall("< OTP/2.0 >")# to keep the connection to the socket opened you need to write < OTP/2.0 >
message = "CLIENT <|> NVT_INFO"
print >>sys.stderr, 'client : "%s"' % message #prompt
sock.sendall(message)

#Reading in the socket
data = sock.recv(4096)
print >>sys.stderr, 'received "%s"' % data

#to print out the configuration: CLIENT <|> NVT_INFO






# to keep the connection to the socket opened you need to write < OTP/2.0 >
