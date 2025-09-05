from celery import shared_task
from django.core.mail import send_mail
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def send_verification_email(email, verification_link):
    try:
        send_mail(
            'Verify Your Account',
            f'Click the link to verify your account: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,  # Use settings for consistency
            [email],
            fail_silently=False,
        )
        logger.info(f"Verification email sent to {email}")
    except Exception as e:
        logger.error(f"Error sending verification email: {str(e)}")