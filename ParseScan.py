import time,json,collections, socket
import Color

class ParseScan:

    """
        This class aims at parsing the report of the server to 2 format:
        email readable format and elasticsearch Json format
    """

    def __init__(self,outputScan,target,familyDict):
        self.outputScan = outputScan
        self.target = target
        self.report = ""
        with open('conf/blacklist.conf', 'r') as blacklistFile:
            self.blacklist=blacklistFile.read().splitlines()
        self.familyDict = familyDict #required for  name & description of plugin oid

    def searchFamily(self, oid):
        """
            Search for the family of the oid given in argument.
        """
        for k in self.familyDict:
            if oid in self.familyDict[k]:
                    return k
        return None

    def createTemplate(self):
        """
            Create Template Dictionnary which respects Flume default template.
        """
	templateDict = {
'headers' : {
	'timestamp' : str(int(time.time())) ,
	'host' : socket.gethostname()
	}
}
	return templateDict

    def createBody(self):
	"""
	    Create Body Dictionnary inserted in templateDict['body'] as JSON.
	"""
	oidNumber = motivParsed[4].strip()
	familyOfOid = self.searchFamily(oidNumber)
	bodyDict = {
"target" : self.target ,
"plugin" : {
        "name" : self.familyDict[familyOfOid][oidNumber]["name"],
        "description" : self.familyDict[familyOfOid][oidNumber]["description"],
	"family" : familyOfOid,
        "oid" : oidNumber,
        "CVE" : self.familyDict[familyOfOid][oidNumber]["CVE"],
        "BID" : self.familyDict[familyOfOid][oidNumber]['BID'],
        "URL" : self.familyDict[familyOfOid][oidNumber]["URL"],
        "message" : str(motivParsed[3]),
        "type": "LOG" if "LOG <|>" in motiv else "ALARM"
	}
}
	return bodyDict

    def ParserJSON(self):
        """
            ParserJson est le Parser qui renvoie le Json contenant
            les logs du scan.
            Afin de correspondre au JsonHandler de Flume, voici sa forme
            [{
            'headers' : {
                        'timestamp' : timestamp,
                        'host' : host
                        },
	    'body' : bodyJson
            }]
        """
        print(Color.GREEN + "Parsing Scan to create report ...") + Color.END
        jsonDict = [] #jsonDict is an array containing the Json Dictionnary
        scanList = self.outputScan.split("SERVER <|>")
        for motiv in scanList:
	    if "LOG <|>" in motiv or "ALARM <|>" in motiv:
		templateDict = self.createTemplate()
		motivParsed = motiv.split("<|> ")
		jsonDict.append(templateDict.copy())
		self.createBody()
		bodyJson = json.dumps(bodyDict)
                jsonDict[len(jsonDict)-1]["body"] = bodyJson
	#self.jsonOutput & jsonDict does not have ALARM
        self.jsonOutput = json.dumps(jsonDict) #convert the array dictionnary to Json
        return self.jsonOutput
