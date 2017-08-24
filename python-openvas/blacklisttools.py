import color

class BlacklistTools:

    def __init__(self, familyDict):
	self.familyDict = familyDict

    def AddOid(self, oidList):
	"""
	    Function used to add a new oid to conf/blacklist.conf.
	"""
	for oid in oidList:
	    isFound, _ = self.searchOid(oid)
	    if isFound:
	       print(color.RED + oid.strip() + ' Already in blacklist.conf.' + color.END) 
	    else:
		with open('conf/blacklist.conf', 'w') as blacklistFile:
		    blacklistFile.write(oid) 
		print(color.GREEN + oid.strip() + ' added to blacklist.conf' + color.END)
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
		print(color.GREEN + oid.strip() + ' removed from blacklist.conf' + color.END)
	    else:
		print(color.RED + oid.strip() + ' is not in blacklist.conf' + color.END)
