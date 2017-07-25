#This file aims at parsing the report of the server to 2 format: email readable format and elasticsearch Json format
#Be careful the JSON parser has been implemented to output a JSON file directly on the server so that it can be used by Flume, it does not include an http sending to an ElasticSearch node.
import time,json

class ParseScan:

    def __init__(self,outputScan):
	self.outputScan = outputScan
	self.report = ""
    
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
	self.timestamp = int(time.time()) #timestamp is required to sort out scan
	templateJson = json.dumps({"timestamp": {}, "start_scan" : {}, "end_scan" : {} , "target" : { "host" : {} } , "plugin" : {}})#serialize to json string
	self.jsonOutput = json.loads(templateJson)
	self.jsonOutput["timestamp"]=self.timestamp
	print("\033[32mParsing Scan to create report ...\033[0m")
	scanList=self.outputScan.split("SERVER <|>")
	for motiv in scanList:
	    #TIME Flag detected
	    if "TIME <|>" in motiv:
		motivParsed = motiv.split("<|>")
		if "SCAN_START" in motivParsed[1]:
		    self.jsonOutput["start_scan"] = motivParsed[2]
		elif "SCAN_END" in motivParsed[1]:
		    self.jsonOutput["end_scan"] =  motivParsed[2]
	    #LOG Flag detected
	    elif "LOG <|>" in motiv:
		motivParsed = motiv.split("<|> ")
		type(motivParsed[3])
		self.jsonOutput["plugin"].update({ motivParsed[4].strip() : { "name" : {}, "description" : {} , "message" : motivParsed[3] , "type" : "LOG"}})
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		motivParsed = motiv.split("<|> ")
		self.jsonOutput["plugin"].update({ motivParsed[4].strip() : { "name" : {}, "description" : {} , "message" : {motivParsed[3]} , "type" : "ALARM"}})
