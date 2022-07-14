#!/usr/bin/python
#A quick little script that will email out files (usually used for a security camera that uploads files to an FTP directory)
#To use: ./emailSecPics.py file1 file2 file3 ...

import time
import datetime
import sys
import smtplib
from os.path import basename
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication


def main():
	printWithDate("Sending security pics via email: " + str(sys.argv))
	if len(sys.argv) > 1:
		printWithDate("Files present, will send!")
		attachments = sys.argv[1:]
		#printWithDate(str(attachments))
		sendEmailWithAttachments(attachments)


# helper to log our prints with the date
def printWithDate(toPrint):
	print "["+str(datetime.datetime.now())+"] " + toPrint
	sys.stdout.flush() #force to print all messages now


def sendEmailWithAttachments(files):
	email_from = "blah@blah.com" #email username
	server = smtplib.SMTP('smtp.sendgrid.net', 587)#if your using sendgrid to send this
	server.starttls() #use TLS encryption to connect to the mail server
	server.login("<username>", "<password>")
        msg = MIMEMultipart()
 	msg_str = str("Drivway cam activated " + str(datetime.datetime.now()))
	msg.attach(MIMEText(msg_str, 'plain'))
	for f in files or []:
        	with open(f, "rb") as fil:
            		part = MIMEApplication(
                		fil.read(),
                		Name=basename(f)
            		)
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
	msg.add_header('From', email_from)
	msg['Subject'] = msg_str
	to = [] # declare that we're using an array for the "TO:" list
	to.append('email1@blag.com')
	to.append('email2@blag.com')
	server.sendmail(email_from, to, msg.as_string())
	server.quit()
	printWithDate("Email sent!")



if __name__ == "__main__": main()
