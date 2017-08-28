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
        oidGrade = self.familyDict[oidFamily][oid]["grade"]
	oidInfoDict = { 'family' : oidFamily, 'name' : oidName, 'description' : oidDescription, 'CVE' : oidCVE, 'BID' : oidBID, 'URL' : oidURL, 'grade' : oidGrade}
	return(oidInfoDict)

    def FamilyToScan(self, familyList):
	"""
	    It puts the oid of the families to scan according to family value:
            familyList = None            --> Scan all families known
            familyList = DEFAULT_FAMILY  --> Scan default families
            familyList = [General, ...]  --> Scan families specified
	"""
	if familyList == None: #all families
	    oidListFamily = [ family.keys() for family in self.familyDict.values() ]
	else: #DEFAULT_FAMILY or [General, ...]
	    oidListFamily = [ family.keys() for (name, family) in self.familyDict.items() if name in familyList]
	return([ oid for family in oidListFamily for oid in family ])
