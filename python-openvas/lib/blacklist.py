from . import color

class Blacklist:

    def __init__(self):
        with open('conf/blacklist.conf', 'r') as blacklistFile:
            self.content = [line.strip() for line in blacklistFile.readlines()]

    def AddOid(self, oidList):
	"""
	    Function used to add a new oid to conf/blacklist.conf.
	"""
        fileContent = set(self.content)
	fileContent.update(set(oidList)) #set don't duplicate an element
	self.content = sorted(fileContent)
        with open('conf/blacklist.conf', 'w') as blacklistFile:
            blacklistFile.write('\n'.join(self.content))
	print(color.GREEN + str(oidList) + ' added to blacklist.conf.' + color.END)

    def RemoveOid(self, oidList):
	"""
	    Function used to remove an oid in conf/blacklist.conf
	"""
        self.content = sorted(set(self.content) - set(oidList))
        with open('conf/blacklist.conf', 'w') as blacklistFile:
            blacklistFile.write('\n'.join(self.content))
	print(color.GREEN + str(oidList) + ' removed from blacklist.conf.' + color.END)

    def BlacklistInfo(self, oidinfo):
        """
            Print Information about blacklisted OID.
        """
        print(color.GREEN + 'Blacklisted OID information :' + color.END)
        for oid in self.content:
            try:
                oidinfo.get(oid)
                message = """
** {0} , {1} **
* Family of Vulnerability : {2}
* CVE : {3}
* BID : {4}
* URL : {5}
* Description: {6}""".format(oidName, oidNumber, oidFamily, oidCVE, oidBID, oidURL, oidDescription)
                print(message)
            except KeyError:
                print(color.BLUE + oid.strip() + ' is blacklisted but can be removed safely because it is an ancient or wrong plugin.' + color.END)
        return 0
