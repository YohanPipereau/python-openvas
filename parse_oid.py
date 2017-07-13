#This file aims at parsing the NVT_INFO output to get all the oid

import socket_connect
from threading import Thread

class ParseOid(SocketConnect):

    def __init__(self):
        message="""
        < OTP/2.0 >
        CLIENT <|> NVT_INFO <|> CLIENT
        CLIENT <|> COMPLETE_LIST <|> CLIENT
        """

    #def FamilyParser():

    #parser plugin:


    #SERVER <|> PLUGIN_LIST <|>
    #oid <|> Name of NVT <|> infos <|> Licence of vulnerability <|> Family <|> ID of revision <|> CVE id <|> BID (bugtrack id) <|> URL <|> Description \n
    # <|> SERVER

    #Parse the plugin and put the oid in lists
