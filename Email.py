#This script aims at sending the report by email. Working only if local SMTP configured.

import smtplib

class Email:

    def __init__(self, msg,destinationAddr):
	self.msg = msg #The report to send after parsing and blacklisting
        self.destinationAddr = destinationAddr
	
    #Encoding UTF8
    #Parsing the header: From, To, Subject
    def sendEmail(self):
	smtpObj = smtplib.SMTP('127.0.0.1')
	smtpObj.sendmail("openvas@cern.ch", self.destinationAddr,self.msg)
	smtpObj.quit() #end the SMTP connection


