#This file aims at parsing the report of the server to 2 format: email readable format and elasticsearch Json format
#Be careful the JSON parser has been implemented to output a JSON file directly on the server so that it can be used by Flume using an HTTP request
#the urllib2 lib is called urllib.requests in python3 change it if needed
import time,json,urllib2

class ParseScan:

    def __init__(self,outputScan,target,familyDict):
	self.outputScan = outputScan
	self.target = target
	self.report = ""
	with open('conf/blacklist.conf', 'r') as blacklistFile:
	    self.blacklist=blacklistFile.read().splitlines() #put the file into a list
	self.familyDict = familyDict #we need the familyDict for the name & description of the plugin oid

    def search(self, searchFor):
	for k in self.familyDict:
	    for v in self.familyDict[k]:
		if searchFor in v:
		    return k
	return None   
 
    def ParserEmail(self):
	print("\033[32mParsing Scan to create report ...\033[0m")
	scanList=self.outputScan.split("SERVER <|>")
	for motiv in scanList:
	    #TIME Flag detected
	    if "TIME <|>" in motiv:
		motivParsed = motiv.split("<|>")
		if "SCAN_START" in motivParsed[1]:
		    self.report += "Scan started on" + motivParsed[2] + "\n"	
		elif "SCAN_END" in motivParsed[1]:
		    self.report += "Scan ended on" + motivParsed[2] + "\n"
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		motivParsed = motiv.split("<|> ")
	        print(self.search(motivParsed[4].strip()))
		self.report += "\n***** VULNERABILITY : " + motivParsed[4] + ":\n"
		self.report += motivParsed[3]

    def ParserJSON(self):
	templateJson = {
  "headers" : {
             "timestamp" : str(int(time.time())) ,
             "host" : "openvas6.cern.ch"
             },
  "body" : {}
}
	jsonDict=[] #jsonDict is an array containing the Json Dictionnary
	print("\033[32mParsing Scan to create report ...\033[0m")
	scanList=self.outputScan.split("SERVER <|>")
	for motiv in scanList:
	    #LOG Flag detected
	    if "LOG <|>" in motiv:
		motivParsed = motiv.split("<|> ")
		jsonDict.append(templateJson) #append the templateJson dictionnary to the list
		#We need to find the family of the oid
		print("hello")
		print(search(self.familyDict,motivParsed[4].strip()))
		bodyDict = {
"target" : self.target ,
"plugin" : {
	"name" : {},
	"description" : {},
	"oid" : motivParsed[4].strip(),
	"message" : str(motivParsed[3]),
	"type": "LOG"
}
}
		bodyJson = json.dumps(bodyDict)
		jsonDict[len(jsonDict)-1]["body"] = bodyJson
	    #ALARM Flag detected	
	    elif "ALARM <|>" in motiv:	
		motivParsed = motiv.split("<|> ")
		jsonDict.append(templateJson)
		bodyDict = {
"target" : self.target ,
"plugin" : {
	"name" : {},
	"description" : {},
	"oid" : motivParsed[4].strip(),
	"message" : str(motivParsed[3]),
	"type": "ALARM"
}
}
		bodyJson = json.dumps(bodyDict)
		jsonDict[len(jsonDict)-1]["body"] = bodyJson
	self.jsonOutput = json.dumps(jsonDict) #convert the array dictionnary to Json	
	print(self.jsonOutput)
	req = urllib2.Request("http://localhost:5140", self.jsonOutput, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	print("\033[32mJSON Sent!\033[0m")

#Please make sure flume channel capacity are big enough to send a big json in case there are lot of vulnerabilities
