from platform_back import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import engines


def subjects(template_name):
    subs = {
        "erreur-la-conversion-de-votre-ifc": "Erreur à la conversion de votre IFC",
        "invitation-du-user-ok-cloud": "{{user_name}} a accepté votre invitation dans le cloud {{cloud_name}}",
        "invitation-du-user-ok": "{{user_name}} a accepté votre invitation dans le projet {{project_name}}",
        "votre-ifc-t-converti": "Votre IFC a été converti",
        "emailing-onboarding": "Découvrez dès maintenant la plateforme BIMData.io",
    }
    return subs[template_name]


# @params user_ids: a list {email, first_name, last_name}
def send_mail(template_name, content, users, fake=False):

    to_emails = [
        f"{user.get('first_name')} {user.get('last_name')}"
        if user.get("first_name")
        else user.get("email")
        for user in users
    ]
    from_email = settings.DEFAULT_FROM_EMAIL

    template_subject = engines["django"].from_string(subjects(template_name))
    subject = template_subject.render(content)

    content["bimdata_url"] = settings.APP_URL
    html_content = render_to_string(f"mails/{template_name}.html", content)

    email = EmailMessage(subject, html_content, from_email, to_emails)
    email.content_subtype = "html"
    email.send()
