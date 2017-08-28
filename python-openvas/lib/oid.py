import color

class OidInfo:

    def __init__(self, familyDict):
	self.familyDict = familyDict

    def _getfamily(self, oid):
        """
            Search for the family of the oid given in argument.
        """
        for k in self.familyDict:
            if oid in self.familyDict[k]:
                    return k
        return None

    def get(self,oid):
        """
            get method retrieves all the available Info about an Oid.
            The output of the method is a dictionnary for performance and readability.
        """
        oidFamily = self._getfamily(oid)
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
#TODO: return dictionaire

    def FamilyToScan(self, family):
	"""
	    It puts the oid of the families to scan according to family value:
            family = None            --> Scan all families known
            family = DEFAULT_FAMILY  --> Scan default families
            family = [General, ...]  --> Scan families specified
	"""
	if family == None: #all families
	    oidListFamily = [ family.keys() for family in self.familyDict.values() ]
	else: #DEFAULT_FAMILY or [General, ...]
	    oidListFamily = [ family.keys() for (name, family) in self.familyDict.items() if name in familyScan]
	return([ oid for family in oidListFamily for oid in family ])

    @staticmethod
    def from_otp(raw):
       pass 
