from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.core.mail import EmailMessage


def new_send_mail_func(context, subscribers: list):
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

        for email in subscribers:
            msg = EmailMessage(
                subject,
                message,
                email_from,
                to=[email]
            )

            msg.send()
    except Exception as e:
        print(e)
        return False


def time_taken_to_read(title: str, content: str):
    word_count = len(list((title + content).split()))
    total = (word_count // 200)
    if total < 1:
        return "less than a minute read"
    return f"{total} Minute Read"
