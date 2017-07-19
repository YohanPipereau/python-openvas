#This file aims at parsing the NVT_INFO output to get all the oid
from Parse import *

class ParseOid(Parse):
    def __init__(self,parserMatch,scanData):
        self.scanData = scanData
        self.parserMatch = parserMatch #when parserMatch is detected -> match section begins
	self.familyArray = []

    def Parser(self,line):
	oidList=line.split(" <|> ")
	if len(oidList) == 10 :
	    #Create an array with Family as column and oid as lines
	    #Array = [[Family1Name,oid1.1,oid1.2,...],[Family2Name,oid2.1,oid2.2,...],...]
	    familyFound = False #boolean equals False as long as we did not add the oidLine family to the array
	    k=0
	    while k<len(self.familyArray) and familyFound == False :
	        if oidList[4] == self.familyArray[k][0]:
		    #The family of this oid is already in the array
		    self.familyArray[k].append(oidList[0])
		    familyFound = True
		k+=1
	    if familyFound == False:
	        #If we did not find the family then we need to append it to the array
	        self.familyArray.append([oidList[4],oidList[0]])


#oid <|> Name of NVT <|> infos <|> Licence of vulnerability <|> Family <|> ID of revision <|> CVE id <|> BID (bugtrack id) <|> URL <|> Description \n
