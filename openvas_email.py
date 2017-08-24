import smtplib, color
from email.mime.text import MIMEText

class Email:
    
    """
	This class aims at sending the report by email to local smtp server.
    """

    def __init__(self, msg,destinationAddr, email_from, email_subject):
	msg = sendFormatObj.BuildEmailReport()
        self.msg = MIMEText(msg) #convert to MIME type to set headers To, From, Subject
        self.destinationAddr = destinationAddr
	self.email_from = email_from
	self.email_subject = email_subject

    def SetHeaders(self):
        self.msg['Subject'] = self.email_subject
        self.msg['From'] = self.email_from
        self.msg['To'] = ",".join(self.destinationAddr)

    def SendEmail(self):
        smtpObj = smtplib.SMTP('127.0.0.1')
        self.setHeaders()
        smtpObj.sendmail('openvas@cern.ch', self.destinationAddr,self.msg.as_string())
        smtpObj.quit() #end the SMTP connection
        print(color.GREEN + "Email Sent!" + color.END)


