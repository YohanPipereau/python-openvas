#This fails handles OTP communication with the scanner
import SocketConnect, ParseOid

def ListFamilies():
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
    if scanAll: #Let's scan all the families
        oidListFamily = [ family.keys() for family in familyDict.values() ]
    else: #scan families given in argument
        oidListFamily = [ family.keys() for (name, family) in familyDict.items() if name in familyScan]
    oidList = [ x for i in oidListFamily for x in i ] 
    return(oidList)

def RunScan(timeout,ipScan,verbose,oidList):
    print("\033[32mPlease Wait, while we scan the device ...\033[0m")
    oidString = ';'.join(oidList)
    confFile = open("conf/scan.conf").read() #Read the content of the configuration file --> confFile
    message = """< OTP/2.0 >
CLIENT <|> PREFERENCES <|>
plugin_set <|> """ + oidString + "\n" + confFile + str(len(ipScan)) + "\n" +ipScan +"\n"
    outputScan = SocketConnect.SocketConnect(message,timeout,verbose)
    return(outputScan)
