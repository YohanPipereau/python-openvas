"""
    Class to check wether the ip is correct or not in the args of main module
"""

import socket, sys

class IPTool:

    def __init__(self,address):
        self.address = address

    def ValidDN(self):
        self.address = socket.gethostbyname(self.address)
	self.ValidIP() #is the IP received a good IP

    def ValidIP(self):
        """
            check if an ip is valid or not
        """
        try: #try IPv6
            b1 = socket.inet_pton(socket.AF_INET6,self.address)
        except: #try IPv4
            b2 = socket.inet_pton(socket.AF_INET,self.address)

    def ValidDNIP(self):
        """
            check if arguments given by -i/--ip is right
        """
        try:
            self.ValidDN()
        except:
            try:
                self.ValidIP()
            except:
                print("\033[1m\033[31mInvalid IP format !\033[0m \nYet, IPv6 and IPv4 handled.")
                sys.exit(1)
