#This file aims at parsing the report of the server to 2 format: email readable format and elasticsearch Json format
#Be careful the JSON parser has been implemented to output a JSON file directly on the server so that it can be used by Flume, it does not include an http sending to an ElasticSearch node.
import time,json

class ParseScan:

    def __init__(self,outputScan):
	self.outputScan = outputScan
	self.report = ""
	self.jsonOutput = ""
    
    def ParserEmail(self):
	print("\033[32mParsing Scan to create report ...\033[0m")
	scanList=self.outputScan.split("SERVER <|>")
	for motiv in scanList:
	    #TIME Flag detected
	    if "TIME <|>" in motiv:
		motivParsed = motiv.split("<|>")
		if "SCAN_START" in motivParsed[1]:
		    self.report += "Scan started on" + motivParsed[2]	
		elif "SCAN_END" in motivParsed[1]:
		    self.report += "Scan ended on" + motivParsed[2]
	    #LOG Flag detected
	    elif "LOG <|>" in motiv:
		motivParsed = motiv.split("<|> ")
		self.report += "\n***** Vulnerability : " + motivParsed[4] + ":\n"
		self.report += motivParsed[3]
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		motivParsed = motiv.split("<|> ")
		self.report += motivParsed[3]

    def ParserJSON(self):
	timestamp = int(time.time() #timestamp is required to sort out scan
	print("\033[32mParsing Scan to create report ...\033[0m")
	scanList=self.outputScan.split("SERVER <|>")
	for motiv in scanList:
	    #TIME Flag detected
	    if "TIME <|>" in motiv:
		motivParsed = motiv.split("<|>")
		if "SCAN_START" in motivParsed[1]:
		    self.jsonOutput += "'start_scan'" + motivParsed[2]	
		elif "SCAN_END" in motivParsed[1]:
		    self.jsonOutput += "'end_scan'" + motivParsed[2]
	    #LOG Flag detected
	    elif "LOG <|>" in motiv:
		motivParsed = motiv.split("<|> ")
		self.jsonOutput += "\n***** Vulnerability : " + motivParsed[4] + ":\n"
		self.jsonOutput += motivParsed[3]
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		motivParsed = motiv.split("<|> ")
		self.jsonOutput += motivParsed[3]

