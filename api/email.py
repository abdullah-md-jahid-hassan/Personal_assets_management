from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, to_email, from_email=None, html_message=None):
    """
    Send an email with customizable sender, sender name, HTML content, and reply-to.

    Args:
        subject (str): Email subject.
        message (str): Plain text message.
        to_email (str): Recipient email address.
        from_email (str, optional): Sender email address. Defaults to settings.DEFAULT_FROM_EMAIL.
        html_message (str, optional): HTML version of the message.
    """
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        html_message=html_message
    )