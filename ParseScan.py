#This file aims at parsing the report of the server to 2 format: email readable format and elasticsearch Json format

class ParseScan(Parse):

    def __init__(self,parserMatch,outputScan):
	self.parserMatch = parserMatch
	self.outputScan = outputScan

    def Parser(self,line):
	if line 
	scanLineList = line.split(" <|> ")
	
