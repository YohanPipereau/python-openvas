import sys

for arg in sys.argv:
    #Get all arguments given to python, the separator for the parsing is a single space
    if arg == "--help" or "-h":
        print("""
        -h : get some help
        -v : verbose mode, output the report of the scan in the shell
        -vv : ultra verbose mode, Output the whole OTP communication in the SHELL
        -o : specify the path to the output file
        -l : List the families available (ex: Windows, Linux, Cisco, etc)
        -f : Specify families for the families for the scan
        -s : specify the unix socket for the communication for the scanner (default is /var/run/openvassd.sock)
        -i : IP of the host to scan

        --help : get some help
        --verbose : verbose mode, Output the whole OTP communication in the SH0ELL
        --list-families : List the families available (ex: Windows, Linux, Cisco, etc)
        --scan-families : Scan the families given in arguments and separated by a coma ,
        --list-oid : Output the list of the oid, name of vulnerabilities, and info about it
        --socket : specify the unix socket for the communication for the scanner (default is /var/run/openvassd.sock)
        --email : send the report to someone@example.com by email
        --ip : IP of the host to scan
        """)
    if arg == "-v" or "--verbose":

    if arg == "-vv":

    if arg == "-o":

    if arg == "-l":

    if arg == "-f":
