import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.template import engines
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext as _

logger = logging.getLogger("django")


def subjects(template_name):
    subs = {
        "notifications-bcf": _("Nouvelle notification BCF"),
        "notifications-visa": _("Nouvelle notification Visa"),
        "mailing-welcome": _("Bienvenue sur la plateforme BIMData.io"),
    }
    return subs[template_name]


# @params user_ids: a list {email, firstname, lastname, language}
def send_mail(
    template_name, content, users, language=settings.LANGUAGE_CODE, fail_silently=True
):
    language = language or settings.LANGUAGE_CODE
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [
        f"{user.get('firstname')} {user.get('lastname')} <{user.get('email')}>"
        if user.get("firstname")
        else user.get("email")
        for user in users
    ]

    content["bimdata_url"] = settings.PLATFORM_URL

    cur_language = translation.get_language()
    try:
        translation.activate(language)
        template_subject = engines["django"].from_string(subjects(template_name))
        subject = template_subject.render()
        html_content = render_to_string(f"mails/{template_name}.html", content)
    finally:
        translation.activate(cur_language)
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
    email = EmailMessage(
        subject, html_content, from_email, to_emails, connection=connection
    )
    email.content_subtype = "html"
    try:
        email.send()
    except Exception as e:
        if fail_silently:
            logger.warning(f"There was an error sending an email: \n{e}")
        else:
            raise e
    connection.close()
