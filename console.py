#This aims at parsing the CLI args
import getopt, sys
from threading import Thread
from SocketConnect import *
from ParseOid import *

try:
    argv=sys.argv[1:] #put the arguments in a string
    opts , args = getopt.getopt(argv, "f:hi:lo:vs:", ["help", "verbose","list-families","scan-families=","list-oid","socket=","email=","output=","ip="])
    #parse options/arguments given to the program. Use : to indicate a string after the option, and = for the long options
    #the output of getopt is a tuple of list ([],[]). This list contains tuple themselves
except getopt.GetoptError:
    print("""
    Sorry, the given option does not exist.
    Please get some help by running the following arguments: \033[1m -h \033[0m or \033[1m --help \033[0m
    """)
    sys.exit(2)
for opt,arg in opts:
    if opt in ('-l','list-families'):
	message= """< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT
"""
	outputVar = SocketConnect(message)
	parserMatch = "SERVER <|> PLUGIN_LIST <|>"
	oid = ParseOid(parserMatch,outputVar)

    elif opt in ("-h", "--help"):
        print("""
\033[1m OPTIONS \033[0m
    \033[1m -f \033[0m  Specify families for the families for the scan
    \033[1m -h \033[0m  Get some help
    \033[1m -i \033[0m  IP of the host to scan
    \033[1m -l \033[0m  List the families available (ex: Windows, Linux, Cisco, etc)
    \033[1m -o \033[0m  Specify the path to the output file
    \033[1m -v \033[0m  Verbose mode, output the report of the scan in the shell


    \033[1m --help \033[0m          get some help
    \033[1m --verbose \033[0m       verbose mode, Output the whole OTP communication in the SH0ELL
    \033[1m --list-families \033[0m List the families available (ex: Windows, Linux, Cisco, etc)
    \033[1m --scan-families \033[0m Scan the families given in arguments and separated by a coma , (default is default scan)
    \033[1m --list-oid \033[0m      Output the list of the oid, name of vulnerabilities, and info about it
    \033[1m --email \033[0m         send the report to someone@example.com by email
    \033[1m --output \033[0m        specify the path to the output file
    \033[1m --ip \033[0m            IP of the host to scan

\033[1m EXAMPLES \033[0m
    First, list the available families: python console.py -l
    Then, scan the host with the wanted families:
        """)
        sys.exit(1)
