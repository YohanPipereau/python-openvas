import Color

class BlacklistTools:

    def __init__(self, familyDict):
	self.familyDict = familyDict

    def searchFamily(self, oid):
        """
            Search for the family of the oid given in argument.
        """
        for k in self.familyDict:
            if oid in self.familyDict[k]:
                    return k
        return None

    def Info(self):
        """
           Print information about blacklisted OID.
        """
        print(Color.GREEN + 'Blacklisted OID information :' + Color.END)
	with open('conf/blacklist.conf', 'r') as blacklistFile:
	    blacklist = blacklistFile.readlines()
	#Find the blacklisted oid in dictionnary:
	for oid in blacklist:
	    try:
		oidFamily = self.searchFamily(oid)
		oidName = self.familyDict[oidFamily][oid]['name']
		oidDescription = self.familyDict[oidFamily][oid]['description']
		oidCVE = self.familyDict[oidFamily][oid]['CVE']
		oidBID = self.familyDict[oidFamily][oid]['BID']
		oidURL = self.familyDict[oidFamily][oid]['URL']
		message = """
    ** {0} , {1} **
    * Family of Vulnerability : {2}
    * CVE : {3}
    * BID : {4}
    * URL : {5}
    * Description: {6}""".format(oidName, oidNumber, oidFamily, oidCVE, oidBID, oidURL, oidDescription)
		print(message)
	    except KeyError:
		print(Color.BLUE + oid.strip() + ' is blacklisted but can be removed safely because it is an ancien plugin.' + Color.END)
	return 0
	
    def AddOid(self, number):
	"""
	    Function used to add a new oid to conf/blacklist.conf.
	"""
	pass
