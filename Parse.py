#This file is a super class for the oid parser and the scan report parser


class Parse:

    def SectionParser(self):
	scanList = self.scanData.splitlines(True)
	parsingTrigger = False
	for line in scanList:
    	    if line == self.parserMatch:
		parsingTrigger = True
	 #Every object has a parser which is called if we detect a line which match parserMatch
	    if parsingTrigger == True:
		    print("ok")
		    self.Parser(line)
            #Detect end of the matching section
	    if line == "<|> SERVER":
		parsingTrigger = False
