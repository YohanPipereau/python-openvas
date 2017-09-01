import requests, json, smtplib, time, datetime, textwrap
import color
from email.mime.text import MIMEText

class SendFormat:

    def __init__(self, jsonOutput):
        self.jsonOutput = jsonOutput

    def BuildReport(self, tagList):
        """
            Build the Report sent to SendEmail or WriteFile.
            For Emails, only ALARM messages are included. tag = [ALARM]
            For File output, ALARM & LOG messages are included. tagList = [ALARM,LOG]
        """
        report="Scanned on " + str(datetime.datetime.now())
        tmpDict = json.loads(self.jsonOutput)
        for k in range(len(tmpDict)-1):
            d = json.loads(tmpDict[k]['body'])
            if d['plugin']['type'] in tagList:
                report +=  "\n***** %s :\n"     % d['plugin']['type']
                report += "-OID: %s\n"          % d['plugin']['oid']
                report += "-Name: %s\n"         % d['plugin']['name']
                report += "-Danger (/10): %s\n" % d['plugin']['grade']
                report += "-Family: %s\n"       % d['plugin']['family']
                report += "-CVE: %s\n"          % d['plugin']['CVE']
                report += "-BID: %s\n"          % d['plugin']['BID']
                report += "%s\n"                % d['plugin']['URL']
                report += "%s\n"                % d['plugin']['message']
        return(report)

    def SetHeaders(self, email_subject, email_from, destinationAddr):
        msg = self.BuildReport(tagList=['ALARM'])
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
        print(color.GREEN + "Email Sent!" + color.END)

    def SendFlume(self,flumeServer):
        """
            SendFlume() ends JSON to Flume server.
        """
        requests.post(flumeServer, json=self.jsonOutput)
        print(color.GREEN + "JSON Sent!" + color.END)

    def WriteFile(self,outputDirPath):
        """
            SendFile() outputs the same content as Email in a file and gives its location.
        """
        msg = self.BuildReport(tagList=['ALARM','LOG'])
        outputFilePath =  outputDirPath + '/' + str(int(time.time()))
        with open(outputDirPath + '/' + str(int(time.time())),'w+') as fileReport:
            fileReport.write(msg)
        print(color.GREEN + 'Report written in file ' + outputFilePath + color.END)
