import sys, json, os
import OTPSocket, ParseOid, ParseScan, Color, time

class OTP:
    """
	This module handles OTP communication with the scanner.
    """

    def __init__(self, oidTimeout):
        self.sock = OTPSocket.OTPSocket()
	self.oidTimeout = oidTimeout
       
    def BuildNVTDict(self, NVT_CHECKSUM):
	"""
	   function called by ListFamilies
	"""
	self.sock.Send('CLIENT <|> COMPLETE_LIST <|> CLIENT\n')
	rawOid = self.sock.Receive(verbose=False)
	self.sock.Send("\n") #Need to add this to retrieve the config as well 
	self.sock.Receive() #Receive config
	oid = ParseOid.ParseOid() #Let's parse the answer of the scanner
	oid.Parser(rawOid)
        with open('conf/currentnvt.json', 'w+') as nvt_dict_file:
	    json.dump(oid.familyDict, nvt_dict_file)
	with open('conf/nvtchecksum.conf', 'w+') as nvt_checksum_file:
	    nvt_checksum_file.write(NVT_CHECKSUM)
	return(oid.familyDict)
 
    def ListFamilies(self):
	"""
	    This function is called from the main file.
	    It is used to retrieve a dictionnary of vulnerabilities oid,name,description,family
	"""
	print(Color.GREEN + "Wait, we are retrieving the families and oid of the vulnerabilities ..." + Color.END)
	self.sock.Send('CLIENT <|> NVT_INFO <|> CLIENT\n')
	NVT_CHECKSUM = self.sock.Receive().split('<|> ')[1][6:]
	self.sock.Send("\n") #Need to add this to retrieve the config as well 
	self.sock.Receive() #Receive config
	if os.path.isfile('conf/nvtchecksum.conf'):
	    with open('conf/nvtchecksum.conf', 'r') as nvt_checksum_file:
		NVT_CHECKSUM_FILE = nvt_checksum_file.read()
	    if NVT_CHECKSUM_FILE == NVT_CHECKSUM:
	        with open('conf/currentnvt.json', 'r') as nvt_dict_file:
	            familyDict = json.load(nvt_dict_file)
		return(familyDict)
	    else:
	        return(self.BuildNVTDict(NVT_CHECKSUM))
        else:
	    return(self.BuildNVTDict(NVT_CHECKSUM))

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
	    buildJson.AddLine(outputScanLine, verbose)
	jsonOutput = buildJson.FinalOutput()
	return(jsonOutput)
