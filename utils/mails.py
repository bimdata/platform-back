# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.conf import settings
from utils.mailer import send_mail
from smtplib import SMTPException


def send_onboarding(user):
    try:
        content = {
            "bimdata_url": settings.PLATFORM_URL,
            "user_name": user.first_name
        }
        send_mail("mailing-welcome", content, [user.to_json()])
    except BaseException as e:
        print('[ERROR] An error occurred while sending welcome email: ', e)


def send_invitation_accepted(payload):
    if payload.get("project"):
        mail_content = {
            "user_name": f"{payload['user']['firstname']} {payload['user']['lastname']}",
            "project_name": payload["project"]["name"],
            "cloud_name": payload["cloud"]["name"],
            "project_url": f"{settings.PLATFORM_URL}/spaces/{payload['cloud']['id']}/projects/{payload['project']['id']}",
        }
        send_mail(
            "invitation-du-user-ok", mail_content, [{"email": payload["invitor_email"]}]
        )
    else:
        invitor_content = {
            "user_name": f"{payload['user']['firstname']} {payload['user']['lastname']}",
            "cloud_name": payload["cloud"]["name"],
            "cloud_url": f"{settings.PLATFORM_URL}/spaces/{payload['cloud']['id']}",
        }
        send_mail(
            "invitation-du-user-ok-cloud",
            invitor_content,
            [{"email": payload["invitor"]["email"]}],
        )


def send_ifc_ok(payload):
    content = {
        "ifc_name": payload.get("name"),
        "viewer_url": f"{settings.PLATFORM_URL}/spaces/{payload['cloud_id']}/projects/{payload['project_id']}/viewer/{payload['id']}",
    }
    send_mail(
        "votre-ifc-t-converti", content, [{"email": payload["creator"]["email"]}]
    )


def send_ifc_ko(payload):
    content = {
        "ifc_name": payload.get("name"),
        "project_url": f"{settings.PLATFORM_URL}/spaces/{payload['cloud_id']}/projects/{payload['project_id']}",
    }
    send_mail(
        "erreur-la-conversion-de-votre-ifc", content, [{"email": payload["creator"]["email"]}]
    )
