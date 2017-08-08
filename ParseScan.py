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
            self.blacklist=blacklistFile.read().splitlines() #put the file into a list
        self.familyDict = familyDict #we need the familyDict for the name & description of the plugin oid

    def search(self, oid):
        """
            Search for the family of the oid given in argument.
        """
        for k in self.familyDict:
            if oid in self.familyDict[k]:
                    return k
        return None

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
        jsonDict=[] #jsonDict is an array containing the Json Dictionnary
        templateJson = {}
        templateJson["headers"] = {}
        templateJson["headers"]["timestamp"] = str(int(time.time()))
        templateJson["headers"]["host"] = socket.gethostname()
        print(Color.GREEN + "Parsing Scan to create report ...") + Color.END
        scanList=self.outputScan.split("SERVER <|>")
        for motiv in scanList:
	    if "LOG <|>" in motiv or "ALARM <|>" in motiv:
		motivParsed = motiv.split("<|> ")
		jsonDict.append(templateJson) #append the templateJson dictionnary to the list
		oidNumber = motivParsed[4].strip()
		familyOfOid = self.search(oidNumber)  #We need to find the family of the oid
		bodyDict = {
"target" : self.target ,
"plugin" : {
        "name" : self.familyDict[familyOfOid][oidNumber]["name"],
        "description" : self.familyDict[familyOfOid][oidNumber]["description"],
	"family" : familyOfOid,
        "oid" : oidNumber,
        "message" : str(motivParsed[3]),
        "type": "LOG" if "LOG <|>" in motiv else "ALARM"
}
}
                bodyJson = json.dumps(bodyDict)
                jsonDict[len(jsonDict)-1]["body"] = bodyJson
        self.jsonOutput = json.dumps(jsonDict) #convert the array dictionnary to Json
        return self.jsonOutput
