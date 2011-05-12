import smtplib
import yaml
from email.mime.text import MIMEText

msg = MIMEText('Testmessage')

msg['Subject']='New file in directory'
msg['From']='basil.philipp@gmail.com'
msg['To']='basil@forewaystudios.com'

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login('basil.philipp@gmail.com', 'swgwtbkaxzhrtplx')
s.sendmail('basil.philipp@gmail.com', [msg['To']], msg.as_string())
s.quit()
