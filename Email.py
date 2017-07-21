#This script aims at sending the report by email. Working only if local SMTP configured.

import smtplib

class SendEmail:

    def __init__(self, report,destinationAddr):
	self.report = report #The report to send  before blacklisting
        self.destinationAddr = destinationAddr
	
    def Blacklist(self):
	pass #to implement
	

    #Encoding UTF8
    #Parsing the header: From, To, Subject
    def sendEmail(self):
	smtpObj = SMTP()
	smtpObj.connect(localhost,25) #connect to the localhost SMTP server on default port 25
	msg = 	
	smtpObj.sendmail(sourceAddr, destinationAddr, msg)
	smtpObj.quit() #end the SMTP connection


