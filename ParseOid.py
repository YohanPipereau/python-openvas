import sys
from collections import namedtuple

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
        oid <|> Name of NVT <|> 'infos' <|> Licence of vulnerability <|> Family <|>
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
	    RenameOidList = namedtuple('oidListUseful' , ['oidNumber', 'oidName', 'oidFamily', 'oidCVE', 'oidBID', 'oidURL', 'oidDescription'])
	    a = RenameOidList._make([oidList[0], oidList[1], oidList[4], oidList[6], oidList[7], oidList[8], oidList[9]])
            if a.oidFamily in self.familyDict.keys():# oid family already in dict
                    self.familyDict[a.oidFamily].update( {a.oidNumber : {"name" : a.oidName , "description" : a.oidDescription , "CVE" : a.oidCVE , "BID" : a.oidBID, "URL" : a.oidURL}})
            else: #oid family appended to dict
                self.familyDict.update({ a.oidFamily : {a.oidNumber : { "name" : a.oidName, "description" : a.oidDescription, "CVE" : a.oidCVE , "BID" : a.oidBID , "URL" : a.oidURL}}})
        else:
            print("Error! oidList has a size different of 10 characters.")
            sys.exit(2)


