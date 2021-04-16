from django.shortcuts import render
from django.template.loader import render_to_string
from fluent_buddy.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def sendMail(data):
    subject = 'Registro completado'
    message = 'Gracias por registrarte'
    recepient = data['email']
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [recepient],
        fail_silently = False,
        html_message = render_to_string(
        'emails/signup/index.html',
        {
            'message': message
        }
    ))