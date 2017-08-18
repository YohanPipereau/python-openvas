import sys
import SocketConnect, ParseOid, ParseScan, Color

class OTP:
    """
	This module handles OTP communication with the scanner.
    """

    def __init__(self, oidTimeout):
        self.sock = SocketConnect.SocketConnect()
	self.oidTimeout = oidTimeout
        
    def ListFamilies(self):
	"""
	    This function is called from the main file.
	    It is used to retrieve a dictionnary of vulnerabilities oid,name,description,family
	"""
	print(Color.GREEN + "Wait, we are retrieving the families and oid of the vulnerabilities ..." + Color.END)
	self.sock.Send('CLIENT <|> NVT_INFO <|> CLIENT\nCLIENT <|> COMPLETE_LIST <|> CLIENT\n')
	self.sock.Receive()
	rawOid = self.sock.Receive(verbose=False)
	self.sock.Send("\n") #Need to add this to retrieve the config as well 
	self.sock.Receive() #Receive config
	oid = ParseOid.ParseOid() #Let's parse the answer of the scanner
	oid.Parser(rawOid)
	return(oid.familyDict)

    def FamilyToScan(self,scanAll, familyScan, familyDict):
	"""
	    Called from the main file.
	    It puts the oid of the families to scan according to the arguments:
	    all, default, families in a list later read by the RunScan function.
	"""
	if scanAll: #Let's scan all the families
	    oidListFamily = [ family.keys() for family in familyDict.values() ]
	else: #scan families given in argument
	    oidListFamily = [ family.keys() for (name, family) in familyDict.items() if name in familyScan]
	oidList = [ x for i in oidListFamily for x in i ]
	return(oidList)

    def RunScan(self,target,verbose,oidList,familyDict):
	"""
	    Called from the main file.
	    It runs the scan by talking to the unixsocket of the scanner, then
	    it outputs a file containing all the information of the scanner scan.
	"""
	print(Color.GREEN + "Please Wait, while we scan the device ..." + Color.END)
	oidString = ';'.join(oidList)
	with open('conf/scan.conf') as f:
	    confFile = f.read() #Read the content of the configuration file and let the CR !! important
	message = 'CLIENT <|> PREFERENCES <|>\nplugin_set <|>' + oidString + "\n" + confFile + str(len(target)) + "\n" + target +"\n"
	self.sock.Send(message)
	buildJson = ParseScan.ParseScan(target, familyDict)
	while not self.sock.stop:
	    outputScanLine = self.sock.Receive(verbose)
	    #print_verbose(outputScanLine)
	    #print(outputScanLine)
	    buildJson.AddLine(outputScanLine)
	jsonOutput = buildJson.FinalOutput()
	return(jsonOutput)
