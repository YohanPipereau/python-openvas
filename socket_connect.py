import os
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

##Writing and Reading the socket
message = "temporary variable"
print >>sys.stderr, 'client : "%s"' % message #prompt
sock.sendall(message)






# to keep the connection to the socket opened you need to write < OTP/2.0 >
