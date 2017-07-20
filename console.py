#This aims at parsing the CLI args
import getopt, sys, signal, re, socket
from threading import Thread
from SocketConnect import *
from ParseOid import *

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
    opts , args = getopt.getopt(argv, "f:hi:lo:vs:", ["help", "verbose","list-families","scan-families=","list-oid","socket=","email=","output=","ip="])
    #parse options/arguments given to the program. Use : to indicate a string after the option, and = for the long options
    #the output of getopt is a tuple of list ([],[]). This list contains tuple themselves
except getopt.GetoptError:
    print("""\033[1m\033[31mUnknown option or missing argument ! \033[0m
Sorry, the given option does not exist or is not used properly
Please get some help by running the following arguments: \033[1m -h \033[0m or \033[1m --help \033[0m. """)
    sys.exit(2)
for opt,arg in opts:
    if opt in ('-l','list-families'):
	print("Wait for job to be completed, it can take a few seconds ...")
	message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""
	outputVar = SocketConnect(message,3) #outputVar is the answer of scanner to message
	parserMatch = "SERVER <|> PLUGIN_LIST <|>\n"
	oid = ParseOid(parserMatch,outputVar) #Let's parse the answer of the scanner
	oid.SectionParser()
	for cmpt in range(len(oid.familyArray)-1): #print the families available
	    sys.stdout.write(oid.familyArray[cmpt][0] + "\n")
	sys.exit(0)

    elif opt in ("-h", "--help"):
        print("""
\033[1m OPTIONS \033[0m
    \033[1m -f \033[0m  Specify families for the families for the scan
    \033[1m -h \033[0m  Get some help
    \033[1m -i \033[0m  IP of the host to scan
    \033[1m -l \033[0m  List the families available (ex: Windows, Linux, Cisco, etc)


    \033[1m --help \033[0m          get some help
    \033[1m --list-families \033[0m List the families available (ex: Windows, Linux, Cisco, etc)
    \033[1m --scan-families \033[0m Scan the families given in arguments and separated by a coma , (default is default scan)
    \033[1m --list-oid \033[0m      Output the list of the oid, name of vulnerabilities, and info about it
    \033[1m --email \033[0m         send the report to someone@example.com by email
    \033[1m --ip \033[0m            IP of the host to scan

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

try:
    #Do we have all the required args to run the scan
    runScanBool = not ipScan and not familyScan
    #Then run the scan:
    if not runScanBool:
	print("\033[34mDon't forget to deactivate your firewall !\033[0m")
	print("Wait, we are retrieving the ID of the vulnerabilities to scan ...")
	message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""
	outputVar = SocketConnect(message,3)
	print("fin socket")
	parserMatch = "SERVER <|> PLUGIN_LIST <|>\n"
	oid = ParseOid(parserMatch,outputVar)
	oid.SectionParser()
	print("Please Wait, while we scan the device ...")
	#Put the oid of the Families required in a string oidString
	familyList = [ oid.familyArray[k][0] for k in range (len(oid.familyArray)-1) ]
	familyIndex = [i for i, item in enumerate(familyList) if item in set(familyScan)] 
	#familyIndex=Indexes of familyArray corresponding to family/ies to scan
	oidList = []
	for i in familyIndex:
	    oid.familyArray[i].pop(0)
	    oidList = oidList + oid.familyArray[i]
	oidString = "".join(str(x)+";" for x in oidList)
	oidString = oidString[:-1]
	#Read the content of the configuration file --> confFile
	confFile = open("scan.conf").read()
	#message = open("25478.client.original").read()
	message = """< OTP/2.0 >
CLIENT <|> PREFERENCES <|>
plugin_set <|>""" + oidString + "\n" + confFile + str(len(ipScan)) + "\n" +ipScan +"\n"
	#scan = ParseScan(parserMatch,outputVar)
	outputScan = SocketConnect(message,300,True)

except NameError:
    pass
#    print("\033[1m\033[31mArgument missing !\033[0m\nCheck that you gave the ip & families to scan.")
