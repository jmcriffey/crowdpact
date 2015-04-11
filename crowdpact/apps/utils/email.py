#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#import smtplib

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


#def send_email(subject, message, from_address, recipients, html_message=None):
#    msg = MIMEMultipart('alternative')
#    msg['Subject'] = subject
#    msg['From'] = from_address
#    msg['To'] = recipients
#
#    msg.attach(MIMEText(message, 'plain'))
#
#    if html_message:
#        msg.attach(MIMEText(html_message, 'html'))
#
#    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
#
#    s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#    s.sendmail(msg['From'], msg['To'], msg.as_string())
#    s.quit()

def send_email(subject, message_txt, from_address, recipients, message_html=None):
    email = EmailMultiAlternatives(subject, message_txt, from_address, recipients)

    if message_html:
        email.attach_alternative(message_html, 'txt/html')

    email.send()
