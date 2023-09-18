from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_email(name,email,review):
    try:
        context = {
            'name':name,
            'email':email,
            'review':review
        }

        email_subject = 'Status of Todo has changed'

        email_body = render_to_string('email.txt',context)

        emails =  EmailMessage(email_subject,email_body,settings.DEFAULT_FROM_EMAIL,[email,],)
        
        return emails.send(fail_silently=False)
    except Exception as e:
        print(str(e))
