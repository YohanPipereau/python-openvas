import requests, json, smtplib
import Color, ParseScan, Email
from email.mime.text import MIMEText

class SendFormat:

    def __init__(self,outputScan, target, familyDict):
	parseScanObj = ParseScan.ParseScan(outputScan,target,familyDict)
	self.jsonOutput = parseScanObj.ParserJSON()

    def BuildEmailReport(self):
	"""
	    Build the Report sent by Email with only ALARMs
	"""
        report=""
	tmpDict = json.loads(self.jsonOutput)
	for k in range(len(tmpDict)-1):
	    bodyDict = json.loads(tmpDict[k]['body'])
	    print(bodyDict)
	    if bodyDict['plugin']['type'] == 'ALARM':
		oidNumber = bodyDict['plugin']['oid']
		nameOfOid = bodyDict['plugin']['name']
		familyOfOid = bodyDict['plugin']['family']
		message = bodyDict['plugin']['message']
		report += "\n***** VULNERABILITY :" + "\n-OID: " + oidNumber + "\n-Name: " + nameOfOid + "\n-Family: " + familyOfOid + "\n" + message
        return(report)
   
    def SetHeaders(self, email_subject, email_from, destinationAddr):
	msg = self.BuildEmailReport()
	self.msg = MIMEText(msg) #convert to MIME type to set headers To, From, Subject
        self.msg['Subject'] = email_subject
        self.msg['From'] = email_from
        self.msg['To'] = ",".join(destinationAddr)

    def SendEmail(self,email_from,destinationAddr):
        """
            SendEmail() uses the dictionnary the Json of SendFormat and send
            the relevant information by email to the destination address
        """
        smtpObj = smtplib.SMTP('127.0.0.1')
        smtpObj.sendmail(email_from, destinationAddr,self.msg.as_string())
        smtpObj.quit() #end the SMTP connection
        print(Color.GREEN + "Email Sent!" + Color.END)
 
    def SendFlume(self,flumeServer):
        """
	    SendFlume() envoie le JSON au serverFlume.
	"""
        requests.post(flumeServer, json=self.jsonOutput)
        print(Color.GREEN + "JSON Sent!" + Color.END)
