from django.core.mail import EmailMultiAlternatives


def send_email(subject, message_txt, from_address, recipients, message_html=None):
    email = EmailMultiAlternatives(subject, message_txt, from_address, recipients)

    if message_html:
        email.attach_alternative(message_html, 'txt/html')

    email.send()
