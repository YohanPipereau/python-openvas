#This file is a super class for the oid parser and the scan report parser


class Parse:
    def __init__(self,parserMatch,scanData)
	self.scanData = scanData
	self.parserMatch = parserMatch #when parserMatch is detected -> match section begins

    def SectionParser(self):
	scanList = self.scanData.splitlines(True)
	for line in scanList:
    	    if line == parserMatch:
		ParsingTrigger = True
	 #Every object has a parser which is called if we detect a line which match parserMatch
	    if parsingTrigger == True
		    objectinherited.parser(line)
            #Detect end of the matching section
	    if line == "<|> SERVER":
		ParsingTrigger = False
