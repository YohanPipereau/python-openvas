import socket, sys
import color

class IPTool:
    """
	Class to check wether the ip is correct or not in the args of main module
    """

    def __init__(self,address):
        self.address = address #Ip or Domain Name

    def _ValidDN(self):
        """
            Check if a domain name is well solved.
            Entry of the type 0.0 are automatically conpleted to 0.0.0.0.
        """
        self.address = socket.gethostbyname(self.address)
	self.ValidIP() #is the IP received a good IP

    def _ValidIP(self):
        """
            Check if an ip is valid or not.
        """
        try: #try IPv6
            b1 = socket.inet_pton(socket.AF_INET6,self.address)
        except: #try IPv4
            try:
                b2 = socket.inet_pton(socket.AF_INET,self.address)
            except:
                print(color.RED + "Invalid IP format !\nYet, IPv6 and IPv4 handled." + color.END)
                sys.exit(1)

    def ValidDNIP(self):
        """
            Check if Domain Name or IP is valid return IP of Target
        """
        try:
            self._ValidDN()
        except:
            self._ValidIP()
	return(self.address)	
        
