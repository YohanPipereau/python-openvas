import Color

class BlacklistTools:

    def __init__(self):
	pass

    def searchFamily(self, oid):
        """
            Search for the family of the oid given in argument.
        """
        for k in self.familyDict:
            if oid in self.familyDict[k]:
                    return k
        return None

    def Info(self, familyDict):
        """
           Print information about blacklisted OID.
        """
        print(Color.GREEN + 'Blacklisted OID information' + Color.END)
	with open('conf/blacklist.conf', 'r') as blacklistFile:
	    blacklist = blacklistFile.readlines()
	#Find the blacklisted oid in dictionnary:
	for oid in blacklist:
	    oidFamily = searchFamily(oid)
	    oidName = familyDict[oidFamily][oid]['name']
	    oidDescription = familyDict[oidFamily][oid]['description']
	    oidCVE = familyDict[oidFamily][oid]['CVE']
	    oidBID = familyDict[oidFamily][oid]['BID']
	    oidURL = familyDict[oidFamily][oid]['URL']
	    message = """
	    ** {} , {} **
	    * Family of Vulnerability : {}
	    * CVE : {}
	    * BID : {}
	    * URL : {}
	    * Description: {}
	    """).format(oidName, oidNumber, oidFamily, oidCVE, oidBID, oidURL, oidDescription)
	    print(message)
	return 0
	
    def AddOid(self, number):
	"""
	    Function used to add a new oid to conf/blacklist.conf.
	"""
	pass
