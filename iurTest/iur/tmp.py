import smtplib

def send_mail_via_com():
	info = ''
	info += ('\n'+u'how are you'+'\n')
	
	 

	gmail_user = 'erica.huang@hp.com'
	gmail_pwd = '@hyukoh09830927'

	smtpserver = smtplib.SMTP('smtp-mail.outlook.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()

	smtpserver.login(gmail_user, gmail_pwd)
	 

	fromaddr = "erica.huang@hp.com"

	toaddrs = ['erica.huang@hp.com']
	 

	msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (fromaddr, ", ".join(toaddrs), u'*********for test'))
	 
	smtpserver.sendmail(fromaddr, toaddrs, msg+info)
	 

	smtpserver.quit()
	print("send email")

send_mail_via_com()