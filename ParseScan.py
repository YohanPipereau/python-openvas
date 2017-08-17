import time,json,collections, socket
import Color, ProgressBar

class ParseScan:

    """
        This class aims at parsing the report of the server to 2 format:
        email readable format and elasticsearch Json format
    """

    def __init__(self,target,familyDict):
        self.target = target
        self.report = ""
        with open('conf/blacklist.conf', 'r') as blacklistFile:
            self.blacklist=blacklistFile.read().splitlines()
        self.familyDict = familyDict #required for  name & description of plugin oid
        self.jsonDict = [] #jsonDict is an array containing the Json Dictionnary

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

    def createBody(self,motiv):
	"""
	    Create Body Dictionnary inserted in templateDict['body'] as JSON.
	"""
	motivParsed = motiv.split("<|> ")
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

    def AddLine(self,outputScanLine):
        """
            ParserJson est le Parser qui renvoie le Json contenant
            les logs du scan.
            Afin de correspondre au JsonHandler de Flume, voici sa forme
        """
        scanList = outputScanLine.split("SERVER <|>")
        for motiv in scanList:
	    if "LOG <|>" in motiv or "ALARM <|>" in motiv:
		templateDict = self.createTemplate()
		self.jsonDict.append(templateDict.copy())
		bodyDict = self.createBody(motiv)
		bodyJson = json.dumps(bodyDict)
                self.jsonDict[len(self.jsonDict)-1]["body"] = bodyJson
	    elif 'STATUS <|>' in motiv:
		ProgressBar.AddLine(motiv)
        return 0

    def FinalOutput(self):
	jsonOutput = json.dumps(self.jsonDict)	
	return jsonOutput

