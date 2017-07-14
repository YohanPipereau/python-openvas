#This file aims at parsing the NVT_INFO output to get all the oid

from socket_connect import SocketConnect
from threading import Thread
import socket
import sys

class ParseOid(SocketConnect):

    def __init__(self):
        self.message="""
        < OTP/2.0 >
        CLIENT <|> NVT_INFO <|> CLIENT
        CLIENT <|> COMPLETE_LIST <|> CLIENT
        """

        unixsocket_path = "/var/run/openvassd.sock"
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        print >>sys.stderr, 'connecting to %s' % unixsocket_path #make sure any input goes to sderr
        try:
            sock.connect(unixsocket_path)
        except socket.error, msg:
            print >>sys.stderr, msg
            sys.exit(1)

    #def FamilyParser():

    #parser plugin:


    #SERVER <|> PLUGIN_LIST <|>
    #oid <|> Name of NVT <|> infos <|> Licence of vulnerability <|> Family <|> ID of revision <|> CVE id <|> BID (bugtrack id) <|> URL <|> Description \n
    # <|> SERVER

    #Parse the plugin and put the oid in lists
