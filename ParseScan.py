#This file aims at parsing the report of the server to 2 format: email readable format and elasticsearch Json format

class ParseScan:

    def __init__(self,outputScan):
	self.outputScan = outputScan
	self.report = ""

    def ParserJSON(self):
	print("Parsing Scan to create report ...")
	scanList=self.outputScan.split("SERVER <|>")
	for motiv in scanList:
	    print(motiv)
	    #TIME Flag detected
	    if "TIME <|>" in motiv:
		lineParsed = motiv.split("<|>")
		if "SCAN_START" in lineParsed:
		    self.report += "Scan started on" + motivParsed[4]	
		elif "HOST_END" in lineParsed[2]:
		    self.report += "Scan ended on" + motivParsed[4]
	    #LOG Flag detected
	    elif "LOG <|>" in motiv:
		pass
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		pass
"""
SERVER <|> ALARM <|> 188.185.74.71 <|> 22/tcp <|> Installed version: 6.6.1
Fixed version:     6.9

 <|> 1.3.6.1.4.1.25623.1.0.806049 <|> SERVER
"""


"""
^[SERVER <|> LOG <|> 188.185.74.71 <|> 80/tcp <|> Here is the Nikto report:
- ***** RFIURL is not defined in nikto.conf--no RFI tests will run *****
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          188.185.74.71
+ Target Hostname:    188.185.74.71
+ Target Port:        80
+ Virtual Host:       openvas5.cern.ch
+ Start Time:         2017-07-21 12:53:56 (GMT0)
---------------------------------------------------------------------------
+ Server: No banner retrieved
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Root page / redirects to: https://openvas5.cern.ch:9392/login/login.html
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ ERROR: Error limit (20) reached for host, giving up. Last error: er
ror reading HTTP response
+ Scan terminated:  20 error(s) and 2 item(s) reported on remote host
+ End Time:           2017-07-21 12:55:38 (GMT0) (102 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested

 <|> 1.3.6.1.4.1.25623.1.0.14260 <|> SERVER
"""
