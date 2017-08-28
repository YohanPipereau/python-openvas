import sys, re
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
        if not 'PLUGIN_LIST <|>' in scanList[0]:
	    raise Exception('PLUGIN_LIST expected before retrieving OID') 
        else:
	    for line in scanList[1:]:
		self._ParserLine(line)

    def _ParserLine(self,line):
        oidList=line.split(" <|> ")
        if len(oidList) == 10 :
	    oidNumber = oidList[0]
	    oidName = oidList[1]
	    oidFamily = oidList[4]
	    oidCVE = oidList[6]
	    oidBID = oidList[7]	    
	    oidURL = oidList[8]
	    oidDescription = oidList[9]
	    regex = r'cvss_base=(?P<cvss>.[\d\.\d]+)'
	    oidCVSSScore = re.findall(regex,oidList[9])[0]
            if oidFamily in self.familyDict.keys():# oid family already in dict
                    self.familyDict[oidFamily].update( {oidNumber : {"name" : oidName , "description" : oidDescription , "CVE" : oidCVE , "BID" : oidBID, "URL" : oidURL, 'grade' : oidCVSSScore}})
            else: #oid family appended to dict
                self.familyDict.update({ oidFamily : {oidNumber : { "name" : oidName, "description" : oidDescription, "CVE" : oidCVE , "BID" : oidBID , "URL" : oidURL, 'grade' : oidCVSSScore}}})
        else:
            raise Exception("Error! oidList has a size different of 10 characters.")
            sys.exit(-1)
