from typing import Dict, Any

from django.core.mail import send_mail
from website.celery import app
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

from django.core.mail import EmailMessage


@app.task
def new_send_mail_func(context, subscribers: dict):
    """
    Send mail function to the specified email
    """
    try:
        message_template = strip_tags(
            render_to_string("newsletter.html", context))

        subject = context.get('subject')
        print(subject)
        message = message_template
        email_from = settings.EMAIL_HOST_USER
        print(subscribers)

        for email in subscribers.values():
            msg = EmailMessage(
                subject,
                message,
                email_from,
                to=[email]
            )
            # print(message)
            # print(msg)
            msg.send()
            return {"status": True}
    except Exception as e:
        print(e)
        return {"status": False}


def time_taken_to_read(title: str, content: str):
    word_count = len(list((title + content).split()))
    total = (word_count // 200)
    if total < 1:
        return "less than a minute read"
    return f"{total} Minute Read"
