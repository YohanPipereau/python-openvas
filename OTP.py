"""
    This module handles OTP communication with the scanner.
"""

import SocketConnect, ParseOid

def ListFamilies():
    """
        This function is called from the main file.
        It is used to retrieve a dictionnary of vulnerabilities oid,name,description,family
    """
    print("\033[32mWait, we are retrieving the families and oid of the vulnerabilities ...\033[0m")
    message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""    
    outputVar = SocketConnect.SocketConnect(message,3) #outputVar is the answer of scanner to message
    oid = ParseOid.ParseOid(outputVar) #Let's parse the answer of the scanner
    oid.SectionParser()
    return(oid.familyDict)

def familyToScan(scanAll, familyScan, familyDict):
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

def RunScan(timeout,ipScan,verbose,oidList):
    """
        Called from the main file.
        It runs the scan by talking to the unixsocket of the scanner, then
        it outputs a file containing all the information of the scanner scan. 
    """
    print("\033[32mPlease Wait, while we scan the device ...\033[0m")
    oidString = ';'.join(oidList)
    confFile = open("conf/scan.conf").read() #Read the content of the configuration file --> confFile
    message = """< OTP/2.0 >
CLIENT <|> PREFERENCES <|>
plugin_set <|> """ + oidString + "\n" + confFile + str(len(ipScan)) + "\n" +ipScan +"\n"
    outputScan = SocketConnect.SocketConnect(message,timeout,verbose)
    return(outputScan)
