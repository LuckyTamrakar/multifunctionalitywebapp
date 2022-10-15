from django.core.mail import EmailMessage
import os
class Util:
    @staticmethod
    def sendEmail(data):
        email=EmailMessage(subject=data['subject'],body=data['body'],from_email="tamrakarlucky@yahoo.com",to=[data['to_email']])
        email.send()



