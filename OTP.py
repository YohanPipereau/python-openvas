"""
    This module handles OTP communication with the scanner.
"""
import SocketConnect, ParseOid
import Color

def ListFamilies(oidTimeout,initialize_timer):
    """
        This function is called from the main file.
        It is used to retrieve a dictionnary of vulnerabilities oid,name,description,family
    """
    print(Color.GREEN + "Wait, we are retrieving the families and oid of the vulnerabilities ..." + Color.END)
    message= ['< OTP/2.0 >\n','CLIENT <|> NVT_INFO <|> CLIENT\n','CLIENT <|> COMPLETE_LIST <|> CLIENT\n']
    outputVar = SocketConnect.SocketConnect(message,oidTimeout,initialize_timer) #outputVar is the answer of scanner to message
    oid = ParseOid.ParseOid() #Let's parse the answer of the scanner
    oid.Parser(outputVar)
    return(oid.familyDict)

def FamilyToScan(scanAll, familyScan, familyDict):
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

def RunScan(timeout,ipScan,verbose,oidList,initialize_timer):
    """
        Called from the main file.
        It runs the scan by talking to the unixsocket of the scanner, then
        it outputs a file containing all the information of the scanner scan.
    """
    print(Color.GREEN + "Please Wait, while we scan the device ..." + Color.END)
    oidString = ';'.join(oidList)
    with open('conf/scan.conf') as f:
        confFile = f.read().splitlines(True)#Read the content of the configuration file and let the CR !! important
    message = ['< OTP/2.0 >\n','CLIENT <|> PREFERENCES <|>\n','plugin_set <|>' + oidString + "\n"] + confFile +  [str(len(ipScan)) + "\n", ipScan +"\n"]
    outputScan = SocketConnect.SocketConnect(message,timeout,initialize_timer,verbose)
    return(outputScan)
