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

    def searchOid(self, oid):
	"""
	    Search oid in conf/blacklist.conf. Return True/False if Found/not found
	    and also position of oid in File.
	"""
	with open('conf/blacklist.conf', 'r') as blacklistFile:
	   blacklist = blacklistFile.readlines() 
	for rank in range(len(blacklist)):
	    print(rank)
	    if blacklist[rank].strip() == oid.strip():
		return True, rank
	return False, None
	
    def AddOid(self, oidList):
	"""
	    Function used to add a new oid to conf/blacklist.conf.
	"""
	for oid in oidList:
	    isFound, _ = self.searchOid(oid)
	    if isFound:
	       print(Color.RED + oid.strip() + ' Already in blacklist.conf.' + Color.END) 
	    else:
		with open('conf/blacklist.conf', 'w') as blacklistFile:
		    blacklistFile.write(oid) 
		print(Color.GREEN + oid.strip() + ' added to blacklist.conf' + Color.END)
	return 0

    def RemoveOid(self, oidList):
	"""
	    Function used to remove an oid in conf/blacklist.conf
	"""
	for oid in oidList:
	    isFound , index = self.searchOid(oid)
	    if isFound:
		with open('conf/blacklist.conf', 'r') as blacklistFile:
		    wholeFile = blacklistFile.readlines()
		wholeFile.pop(index)
		with open('conf/blacklist.conf', 'w+') as blacklistFile:
		    for line in wholeFile:
			blacklistFile.write(line)
		print(Color.GREEN + oid.strip() + ' removed from blacklist.conf' + Color.END)
	    else:
		print(Color.RED + oid.strip() + ' is not in blacklist.conf' + Color.END)
