#This aims at parsing the CLI args
import sys, signal, re, socket, argparse #General module
import SocketConnect, Email, ParseOid, ParseScan, Ipv4v6 #Personnal class

argv=sys.argv[1:] #put the arguments in a string
parser = argparse.ArgumentParser(description="openvas-handler menu")
parser.add_argument('-a', '--all', help='Scan all the families', action='store_true')
parser.add_argument('-f', '--scan-families', metavar="family1,family2", dest='family', type=str, nargs="+", help="Specify families for the families for the scan")
parser.add_argument('-i', '--ip', metavar='8.8.8.8', type=str ,dest='ip', nargs=1, help="IP of the host to scan")
parser.add_argument('-j', '--json', help="Output the report in JSON and send it to flume",action='store_true')
parser.add_argument('-l', '--list-families', help="List the families available (ex: Windows, Linux, Cisco, etc)", action='store_true')
parser.add_argument('-s', '--email', metavar="x1@example.com,x2@example.com", type=str, nargs="+", help="Send the report to someone@example.com by email", dest="email")
parser.add_argument('-t', '--timeout', type=int, nargs=1, help="Set a timeout for the scan depending if the firewall is up or down. Default is 300s.", dest="timeout")
args = parser.parse_args()

if args.list_families:
    print("\033[32mWait, we are retrieving the families and oid of the vulnerabilities ...\033[0m")
    message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""
    outputVar = SocketConnect.SocketConnect(message,3) #outputVar is the answer of scanner to message
    parserMatch = "SERVER <|> PLUGIN_LIST <|>\n"
    oid = ParseOid.ParseOid(parserMatch,outputVar) #Let's parse the answer of the scanner
    oid.SectionParser()
    #print the families available:
    print(oid.familyDict.keys())
    sys.exit(0)

elif args.ip: #Before Giving the ip to the scanner, test if it is a correct ip.
    isIp = Ipv4v6.Ipv4v6(args.ip[0])
    isIp.valid_ip()

if args.ip and args.family: #Check that we have at least an ip and a family to run the scan
    print("\033[34mDon't forget to deactivate your firewall !\033[0m")
    print("\033[32mWait, we are retrieving the families and oid of the vulnerabilities ...\033[0m")
    message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""
    outputVar = SocketConnect.SocketConnect(message,3)
    parserMatch = "SERVER <|> PLUGIN_LIST <|>\n"
    oid = ParseOid.ParseOid(parserMatch,outputVar)
    oid.SectionParser()
    print("\033[32mPlease Wait, while we scan the device ...\033[0m")
    familyList = oid.familyDict.keys()
    oidList = []
    if args.all: #Let's scan all the families
        oidList = [family.keys() for family in oid.familyDict.values()]
        for i in familyList:
            oidList=oidList + oid.familyDict[i].keys() #output the oid in a list of the i family of familyList
    else:
        oidList = [family.keys() for (name, family) in oid.familyDict.items() if name in familyScan]
        for i in familyScan:
            oidList=oidList + oid.familyDict[i].keys() #output the oid in a list of the i family of familyList
    oidString = ';'.join(oidList)
    oidString[:-1] #Remove the first ","
    #Read the content of the configuration file --> confFile
    confFile = open("conf/scan.conf").read()
    message = """< OTP/2.0 >
CLIENT <|> PREFERENCES <|>
plugin_set <|> """ + oidString + "\n" + confFile + str(len(ipScan)) + "\n" +ipScan +"\n"
    outputScan = SocketConnect.SocketConnect(message,300,True) #Launch the Socket interaction in verbose mode with a wait time of  300s to detect errors
    ####Parsing the Scan Section
    scanReport = ParseScan.ParseScan(outputScan,ipScan,oid.familyDict)
    if args.json: #user asked for json sent to flume
        scanReport.ParserJSON()
    if args.email: #If the list of destination email has been given, then...
        reportAfterParsing = scanReport.ParserEmail()
        s = Email.Email(reportAfterParsing,args.email)
        s.sendEmail()
else:
    print("\033[31mArguments missing !\033[0m")
