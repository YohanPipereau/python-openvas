import requests, json, smtplib
import Color, ParseScan, Email, datetime
from email.mime.text import MIMEText

class SendFormat:

    def __init__(self,outputScan, target, familyDict):
	parseScanObj = ParseScan.ParseScan(outputScan,target,familyDict)
	self.jsonOutput = parseScanObj.ParserJSON()

    def BuildEmailReport(self):
	"""
	    Build the Report sent by Email with only ALARMs
	"""
        report="Scanned on " + str(datetime.datetime.now())
	tmpDict = json.loads(self.jsonOutput)
	for k in range(len(tmpDict)-1):
	    bodyDict = json.loads(tmpDict[k]['body'])
	    if bodyDict['plugin']['type'] == 'ALARM':
		oidNumber = bodyDict['plugin']['oid']
		nameOfOid = bodyDict['plugin']['name']
		familyOfOid = bodyDict['plugin']['family']
                CVEOfOid = bodyDict['plugin']['CVE']
                BIDOfOid = bodyDict['plugin']['BID']
                URLOfOid = bodyDict['plugin']['URL']
		message = bodyDict['plugin']['message']
		report += "\n***** VULNERABILITY :" + "\n-OID: " + oidNumber + "\n-Name: " + nameOfOid + "\n-Family: " + familyOfOid + '\n-CVE:' + CVEOfOid + '\n-BID:' + BIDOfOid + '\n-URL:' + URLOfOid + "\n" + message
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

    def SendFile(self):
        pass
