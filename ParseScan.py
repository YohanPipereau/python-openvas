#This file aims at parsing the report of the server to 2 format: email readable format and elasticsearch Json format
#Be careful the JSON parser has been implemented to output a JSON file directly on the server so that it can be used by Flume using an HTTP request
#the urllib2 lib is called urllib.requests in python3 change it if needed
import time,json,urllib2

class ParseScan:

    def __init__(self,outputScan):
	self.outputScan = outputScan
	self.report = ""
	with open('conf/blacklist.conf', 'r') as blacklistFile:
	    self.blacklist=myfile.read()
    
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
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		motivParsed = motiv.split("<|> ")
		self.report += "\n***** VULNERABILITY : " + motivParsed[4] + ":\n"
		self.report += motivParsed[3]

    def ParserJSON(self):
	templateJson = [{
  "headers" : {
             "timestamp" : str(int(time.time())) ,
             "host" : "openvas6.cern.ch"
             },
  "body" : {
	     "target" : "" ,
	     "plugin" : {
			"name" : {},
			"description" : {},
			"oid" : {},
			"message" : {},
			"type": {}
			}
  }
}] #template of a new log
	self.jsonOutput = json.dumps(templateJson) #convert to Json	
	jsonDict = json.loads(templateJson) #work on the dict
	print("\033[32mParsing Scan to create report ...\033[0m")
	scanList=self.outputScan.split("SERVER <|>")
	for motiv in scanList:
	    #LOG Flag detected
	    if "LOG <|>" in motiv:
		motivParsed = motiv.split("<|> ")
		jsonDict["body"]["plugin"].update({ motivParsed[4].strip() : { "name" : {}, "description" : {} , "message" : str(motivParsed[3]) , "type" : "LOG"}})
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		motivParsed = motiv.split("<|> ")
		self.jsonOutput["plugin"].update({ motivParsed[4].strip() : { "name" : {}, "description" : {} , "message" : {motivParsed[3]} , "type" : "ALARM"}})
	#req = urllib2.Request("http://localhost:5140", self.jsonOutput, {'Content-Type': 'application/json'})
	#f = urllib2.urlopen(req)
	#response = f.read()
	#f.close()
