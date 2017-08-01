import sys

class ParseOid():
    """
        This class aims at parsing the NVT_INFO output of the scanner to get a
        dictionnary of the oid,

        Format of the dictionnary of families:
        ---------------------------------------
        {
        family1 {
                 oid1 {
                       "name" : name,
                       "description" : desription
                      },
                 ...
                 },
        ...
        }

        Format of the NVT_INFO output of the scanner:
        ---------------------------------------------
        oid <|> Name of NVT <|> infos <|> Licence of vulnerability <|> Family <|>
        ID of revision <|> CVE id <|> BID (bugtrack id) <|> URL <|> Description \n
    """

    def __init__(self):
        self.familyDict = {}

    def Parser(self,scanData):
        scanList = scanData.splitlines(True)
        parsingTrigger = False
        for line in scanList:
            if line == "SERVER <|> PLUGIN_LIST <|>\n":
                parsingTrigger = True
            elif line == "<|> SERVER\n": #Detect end of the matching section
                return 0
            elif parsingTrigger == True: #Every object has a parser which is called if we detect a line which match parserMatch
                self.ParserLine(line)

    def ParserLine(self,line):
        oidList=line.split(" <|> ")
        if len(oidList) == 10 :
            familyFound = False #boolean equals False as long as we did not add the oidLine family to the array
            k=0
            while k<len(self.familyDict.keys()) and familyFound == False: #is the oid family in the family dict?
                if oidList[4] == self.familyDict.keys()[k]:#The family of this oid is already in the array
                    self.familyDict[self.familyDict.keys()[k]].update( {oidList[0] : {"name" : oidList[1] , "description" : oidList[9]}})
                    familyFound = True
                k+=1
            if familyFound == False:#If we did not find the family then we need to append the family to the dict
                self.familyDict.update({oidList[4] : {oidList[0] : { "name" : oidList[1], "description" : oidList[9]}}})
        else:
            print("Error! oidList has a size different of 10 characters.")
            sys.exit(2)


