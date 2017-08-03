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
        scanList = scanData.splitlines()
        parsingTrigger = False
        for line in scanList:
            if line == "SERVER <|> PLUGIN_LIST <|>":
                parsingTrigger = True
            elif line == "<|> SERVER": #Detect end of the matching section
                return 0
            elif parsingTrigger == True: #Every object has a parser which is called if we detect a line which match parserMatch
                self.ParserLine(line)

    def ParserLine(self,line):
        oidList=line.split(" <|> ")
        if len(oidList) == 10 :
            oidNumber = oidList[0]
            oidName = oidList[1]
            oidFamily = oidList[4]
            oidDescription = oidList[9]
            if oidFamily in self.familyDict.keys():# oid family already in dict
                    self.familyDict[oidFamily].update( {oidNumber : {"name" : oidName , "description" : oidDescription}})
            else: #oid family appended to dict
                self.familyDict.update({ oidFamily : {oidNumber : { "name" : oidName, "description" : oidDescription}}})
        else:
            print("Error! oidList has a size different of 10 characters.")
            sys.exit(2)


