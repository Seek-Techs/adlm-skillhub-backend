from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_verification_email(email, link):
    send_mail('Verify Your Account', f'Click: {link}', 'prof.seeyouholler@gmail.com', [email])