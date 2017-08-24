import color

class Oid:

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

    def blacklistInfo(self):
        """
           Print information about blacklisted OID.
        """
        print(color.GREEN + 'Blacklisted OID information :' + color.END)
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
		print(color.BLUE + oid.strip() + ' is blacklisted but can be removed safely because it is an ancien plugin.' + color.END)
	return 0

    def blacklistSearchOid(self, oid):
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
	
    def familyToScan(self,scanAll, familyScan):
	"""
	    It puts the oid of the families to scan according to the arguments:
	    all, default, families in a list later read by the RunScan function.
	"""
	if scanAll: #Let's scan all the families
	    oidListFamily = [ family.keys() for family in self.familyDict.values() ]
	else: #scan families given in argument
	    oidListFamily = [ family.keys() for (name, family) in self.familyDict.items() if name in familyScan]
	oidList = [ x for i in oidListFamily for x in i ]
	return(oidList)
