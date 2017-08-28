import sys, json, os, time
import otpsocket, parseoid, parsescan, color

class OTP:
    """
	This module handles OTP communication with the scanner.
    """

    def __init__(self, unixsocket_path):
        self.sock = otpsocket.OTPSocket(unixsocket_path)

    def GetChecksum(self):
	self.sock.Send('CLIENT <|> NVT_INFO <|> CLIENT\n')
	data = self.sock.Receive()
	if 'NVT_INFO' in data:
	    nvt_checksum = data.split('<|> ')[1][6:]
	    return nvt_checksum
	else:
	    print(color.RED + 'NVT_INFO message expected from server' + color.END)
	    return 1
 
    def BuildNVTDict(self, nvt_checksum):
	"""
	   function called by ListFamilies
	"""
	self.sock.Send('CLIENT <|> COMPLETE_LIST <|> CLIENT\n')
	rawOid = self.sock.Receive(verbose=False)
	self.sock.Send("\n") #Need to add this to retrieve the config as well 
	self.sock.Receive()
	oid = parseoid.ParseOid() #Let's parse the answer of the scanner
	oid.Parser(rawOid)
        with open('conf/currentnvt.json', 'w+') as nvt_dict_file:
	    json.dump(oid.familyDict, nvt_dict_file)
	with open('conf/nvtchecksum.conf', 'w+') as nvt_checksum_file:
	    nvt_checksum_file.write(nvt_checksum)
	return(oid.familyDict)
 
    def ListFamilies(self):
	"""
	    This function is called from the main file.
	    It is used to retrieve a dictionnary of vulnerabilities oid,name,description,family
	"""
	print(color.GREEN + "Wait, we are retrieving the families and oid of the vulnerabilities ..." + color.END)
	nvt_checksum = self.GetChecksum()
	if os.path.isfile('conf/nvtchecksum.conf'):
	    with open('conf/nvtchecksum.conf', 'r') as nvt_checksum_file:
		nvt_checksum_file = nvt_checksum_file.read()
	    if nvt_checksum_file == nvt_checksum:
	        self.sock.Send("\n")
	        test = self.sock.Receive()
	        with open('conf/currentnvt.json', 'r') as nvt_dict_file:
	            familyDict = json.load(nvt_dict_file)
		return(familyDict)
	    else:
	        return(self.BuildNVTDict(nvt_checksum))
        else:
	    return(self.BuildNVTDict(nvt_checksum))

    def RunScan(self,target,verbose,oidList, familyDict):
	"""
	    Called from the main file.
	    It runs the scan by talking to the unixsocket of the scanner, then
	    it outputs a file containing all the information of the scanner scan.
	"""
	try:
	    print(color.GREEN + "Please Wait, while we scan the device ..." + color.END)
	    oidString = ';'.join(oidList)
	    with open('conf/scan.conf') as f:
		confFile = f.read() 
	    message = 'CLIENT <|> PREFERENCES <|>\nplugin_set <|>' + oidString + "\n" + confFile + str(len(target)) + "\n" + target +"\n"
	    self.sock.Send(message)
	    buildJson = parsescan.ParseScan(target, familyDict)
	    while not self.sock.stop:
		outputScanLine = self.sock.Receive(verbose)
		buildJson.AddLine(outputScanLine, verbose)
	    jsonOutput = buildJson.FinalOutput(verbose)
	    return(jsonOutput)
	except KeyboardInterrupt:
	    print(color.BLUE + 'Bye !' + color.END)
	    sys.exit(0)
