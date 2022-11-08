from typing import Dict, Any

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

from django.core.mail import EmailMessage


def new_send_mail_func(context, subscribers: list):
    """
    Send mail function to the specified email
    """
    try:
        message_template = strip_tags(render_to_string("newsletter.html", context))

        subject = context.get('subject')
        print(subject)
        message = message_template
        email_from = settings.EMAIL_HOST_USER

        for email in subscribers:
            msg = EmailMessage(
                subject,
                message,
                email_from,
                to=[email]
            )
            # print(message)
            # print(msg)
            msg.send()
            # print("email sent successfully")
    except Exception as e:
        print(e)
        return False
