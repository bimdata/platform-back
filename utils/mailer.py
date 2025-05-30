import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.template.loader import render_to_string
from django.utils import translation

logger = logging.getLogger("django")


def send_mail(
    template_name, content, user, language=settings.LANGUAGE_CODE, fail_silently=True
):
    language = language or settings.LANGUAGE_CODE
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [
        (
            f"{user.first_name} {user.last_name} <{user.email}>"
            if user.first_name
            else user.email
        )
    ]

    content["bimdata_url"] = user.initial_referer

    with translation.override(language):
        subject = render_to_string(f"mails/{template_name}-subject.txt", content).strip()
        html_content = render_to_string(f"mails/{template_name}.html", content)
    if settings.APP_EMAIL_HOST:
        connection = get_connection(
            host=settings.APP_EMAIL_HOST,
            port=settings.APP_EMAIL_PORT,
            username=settings.APP_EMAIL_HOST_USER,
            password=settings.APP_EMAIL_HOST_PASSWORD,
            use_tls=settings.APP_EMAIL_USE_TLS,
        )
    else:
        connection = get_connection()
    email = EmailMessage(subject, html_content, from_email, to_emails, connection=connection)
    email.content_subtype = "html"
    try:
        email.send()
    except Exception as e:
        if fail_silently:
            logger.warning(f"There was an error sending an email: \n{e}")
        else:
            raise e
    connection.close()
