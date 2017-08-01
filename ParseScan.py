import time,json,collections, requests
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
            for v in self.familyDict[k]:
                if oid == v:
                    return k
        return None

    def ParserEmail(self):
        print(Color.GREEN + "Parsing Scan to create report ..." + Color.END)
        scanList=self.outputScan.split("SERVER <|>")
        for motiv in scanList:
            if "ALARM <|>" in motiv: #ALARM Flag detected
                motivParsed = motiv.split("<|> ")
                oidNumber = motivParsed[4].strip()
                if oidNumber in self.blacklist:
                    print(oidNumber + "blacklisted, then not included in report")
                else:
                    familyOfOid = self.search(oidNumber)  #We need to find the family of the oid
                    nameOfOid = self.familyDict[familyOfOid][oidNumber]["name"]
                    self.report += "\n***** VULNERABILITY : " + motivParsed[4] + nameOfOid + ":\n"
                    self.report += motivParsed[3]
        return(self.report)

    def ParserJSON(self):
        jsonDict=[] #jsonDict is an array containing the Json Dictionnary
        templateJson = {}
        templateJson["headers"] = {}
        templateJson["headers"]["timestamp"] = str(int(time.time()))
        templateJson["headers"]["host"] = "openvas6.cern.ch"
        print(Color.GREEN + "Parsing Scan to create report ...") + Color.END
        scanList=self.outputScan.split("SERVER <|>")
        for motiv in scanList:
            #LOG Flag detected
            if "LOG <|>" in motiv:
                motivParsed = motiv.split("<|> ")
                jsonDict.append(templateJson) #append the templateJson dictionnary to the list
                oidNumber = motivParsed[4].strip()
                familyOfOid = self.search(oidNumber)  #We need to find the family of the oid
                bodyDict = {
"target" : self.target ,
"plugin" : {
        "name" : self.familyDict[familyOfOid][oidNumber]["name"],
        "description" : self.familyDict[familyOfOid][oidNumber]["description"],
        "oid" : oidNumber,
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
                oidNumber = motivParsed[4].strip()
                familyOfOid = self.search(motivParsed[4].strip())  #We need to find the family of the oid
                bodyDict = {
"target" : self.target ,
"plugin" : {
        "name" : self.familyDict[familyOfOid][oidNumber]["name"],
        "description" : self.familyDict[familyOfOid][oidNumber]["description"],
        "oid" : oidNumber,
        "message" : str(motivParsed[3]),
        "type": "ALARM"
}
}
                bodyJson = json.dumps(bodyDict)
                jsonDict[len(jsonDict)-1]["body"] = bodyJson
        self.jsonOutput = json.dumps(jsonDict) #convert the array dictionnary to Json
        print(self.jsonOutput)
        requests.post('http://localhost:5140/post', json={"key": "value"})
        print(Color.GREEN + "JSON Sent!" + Color.END)
