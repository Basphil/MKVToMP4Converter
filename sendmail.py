import smtplib
import yaml
from email.mime.text import MIMEText


class SendMail:

 
    def __init__(self):
        cfile =  open('email.yml','r')
        self.config = yaml.load(cfile)
       

    def send(self, filename):        
        msg = MIMEText('New file %s in watched directory.\n' % (filename) )
        msg['Subject']='New file in watched directory'
        s = smtplib.SMTP(self.config['domain'], self.config['port'])
        
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.config['user_name'], self.config['password'])
        s.sendmail(self.config['sender'], self.config['recipients'], msg.as_string())
        s.quit()
