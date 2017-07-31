#This script aims at sending the report by email. Working only if local SMTP configured.

import smtplib

from email.parser import Parser
from email.mime.text import MIMEText


class Email:

    def __init__(self, msg,destinationAddr):
        self.msg = MIMEText(msg) #convert to MIME type to set headers To, From, Subject
        self.destinationAddr = destinationAddr

    def setHeaders(self):
	self.msg['Subject'] = 'Openvas Report'
	self.msg['From'] = 'openvas@cern.ch'
	self.msg['To'] = ",".join(self.destinationAddr)

    def sendEmail(self):
        smtpObj = smtplib.SMTP('127.0.0.1')
	self.setHeaders()
        smtpObj.sendmail('openvas@cern.ch', self.destinationAddr,self.msg.as_string())
        smtpObj.quit() #end the SMTP connection
	print("\033[32mEmail Sent!\033[0m")


