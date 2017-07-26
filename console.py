#This aims at parsing the CLI args
import getopt, sys, signal, re, socket
from threading import Thread
from SocketConnect import *
from ParseOid import *
from ParseScan import *
from Email import *

def valid_ip(address):
    #check if an ip is valid or not
    try: 
        b1 = socket.inet_pton(socket.AF_INET6,address) 
        return True
    except:
    	try:
	    b2 = socket.inet_pton(socket.AF_INET,address)
	    return True
        except:
	    return False

try:
    argv=sys.argv[1:] #put the arguments in a string
    opts , args = getopt.getopt(argv, "af:hi:jls:", ["all","help", "verbose","list-families","scan-families=","socket=","email=","ip=","json"])
    #parse options/arguments given to the program. Use : to indicate a string after the option, and = for the long options
    #the output of getopt is a tuple of list ([],[]). This list contains tuple themselves
except getopt.GetoptError:
    print("""\033[1m\033[31mUnknown option or missing argument ! \033[0m
Sorry, the given option does not exist or is not used properly
Please get some help by running the following arguments: \033[1m -h \033[0m or \033[1m --help \033[0m. """)
    sys.exit(2)
JSONbool = False #default behaviour is without json output
for opt,arg in opts:
    if opt in ('-l','--list-families'):
	print("\033[32mWait for job to be completed, it can take a few seconds ...\033[32m")
	message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""
	outputVar = SocketConnect(message,3) #outputVar is the answer of scanner to message
	parserMatch = "SERVER <|> PLUGIN_LIST <|>\n"
	oid = ParseOid(parserMatch,outputVar) #Let's parse the answer of the scanner
	oid.SectionParser()
	#print the families available:
	print(oid.familyDict.keys())	
	sys.exit(0)

    elif opt in ("-h", "--help"):
        print("""
\033[1m OPTIONS \033[0m
    \033[1m -a \033[0m  Scan all the families
    \033[1m -f \033[0m  Specify families for the families for the scan
    \033[1m -h \033[0m  Get some help
    \033[1m -i \033[0m  IP of the host to scan
    \033[1m -j \033[0m  Output the report in JSON
    \033[1m -l \033[0m  List the families available (ex: Windows, Linux, Cisco, etc)
    \033[1m -s \033[0m  Send the report to someone@example.com by email

 
    \033[1m --all \033[0m 	    Scan all the families
    \033[1m --help \033[0m          get some help
    \033[1m --list-families \033[0m List the families available (ex: Windows, Linux, Cisco, etc)
    \033[1m --scan-families \033[0m Scan the families given in arguments and separated by a coma , (default is default scan)
    \033[1m --email \033[0m         send the report to someone@example.com by email
    \033[1m --ip \033[0m            IP of the host to scan
    \033[1m --json \033[0m          Output the report in JSON

\033[1m EXAMPLES \033[0m
    First, list the available families: python console.py -l
    Then, scan the host with the wanted families:
        """)
        sys.exit(0)

    elif opt in ("-i", "--ip"):
	regbool = valid_ip(arg)
	if regbool == True:
	    #Prepare arguments for the attack
	    ipScan = arg
  	else:
	    print("\033[1m\033[31mInvalid IP format !\033[0m \nYet, IPv6 and IPv4 handled.")
	    sys.exit(1)
		
    elif opt in ("-f","--scan-families"):
	familyScan = arg.split(",")
	scanAll = False

    elif opt in ("-s","--email"):
	destinationList = arg.split(",")

    elif opt in ("-a","--all"):
	scanAll = True

    elif opt in ("-j","--json"):
	JSONbool = True

#Do we have all the required args to run the scan
runScanBool = not ipScan and not familyScan
#Then run the scan:
if not runScanBool:
    print("\033[34mDon't forget to deactivate your firewall !\033[0m")
    print("\033[32mWait, we are retrieving the ID of the vulnerabilities to scan ...\033[0m")
    message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""
    outputVar = SocketConnect(message,3)
    parserMatch = "SERVER <|> PLUGIN_LIST <|>\n"
    oid = ParseOid(parserMatch,outputVar)
    oid.SectionParser()
    print("\033[32mPlease Wait, while we scan the device ...\033[0m")
    familyList = oid.familyDict.keys()
    oidList = []
    if scanAll == True: #Let's scan all the families
	for i in familyList:
	   oidList=oidList + oid.familyDict[i].keys() #output the oid in a list of the i family of familyList
    else:
	for i in familyScan:
	   oidList=oidList + oid.familyDict[i].keys() #output the oid in a list of the i family of familyList
    oidString = ''.join(oidList)
    #Read the content of the configuration file --> confFile
    confFile = open("conf/scan.conf").read()
    message = """< OTP/2.0 >
CLIENT <|> PREFERENCES <|>
plugin_set <|>""" + oidString + "\n" + confFile + str(len(ipScan)) + "\n" +ipScan +"\n"
    outputScan = SocketConnect(message,300,True) #Launch the Socket interaction in verbose mode with a wait time of  300s to detect errors
    ####Parsing the Scan Section
    scanReport = ParseScan(outputScan,ipScan)
    ##### JSON Section
    if JSONbool: #Parse in Json
	scanReport.ParserJSON()
    #####Email Section
    if 'destinationList' in locals():
	scanReport.ParserEmail()
	s = Email(scanReport.report,destinationList)
	s.sendEmail()
	print("\033[32mEmail Sent!\033[0m")
