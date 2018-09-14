from django.conf import settings
from externals import mandrill
from urllib.parse import urlencode


def send_onboarding(user):
    content = {"bimdata_url": settings.APP_URL}
    mandrill.send_mail("emailing-onboarding", content, [user.to_json()])


def send_invitation_accepted(invitor, invited, cloud, project=None):
    invited_name = f"{invited.firstname} {invited.lastname}"
    if project:
        invitor_content = {
            "user_name": invited_name,
            "project_name": project.name,
            "cloud_name": cloud.name,
            "project_url": f"{settings.APP_URL}/cloud/{cloud.pk}/project/{project.pk}/dashboard",
        }
        mandrill.send_mail("invitation-du-user-ok", invitor_content, [invitor.to_json()])
    else:
        invitor_content = {
            "user_name": invited_name,
            "cloud_name": cloud.name,
            "cloud_url": settings.APP_URL,
        }
        mandrill.send_mail("invitation-du-user-ok-cloud", invitor_content, [invitor.to_json()])


def send_invitation_new_user(invitor, invited, cloud, project=None, created=False):
    invitor_name = f"{invitor.firstname} {invitor.lastname}"

    if created:
        qs = urlencode(
            {"invitation_token": invited.invitation_token, "default_email": invited.email}
        )
        content = {"user_name": invitor_name, "signup_url": f"{settings.APP_URL}/login?{qs}"}
        mandrill.send_mail("creation-user-avec-sign-up", content, [invited.to_json()])
    else:
        if project:
            invited_content = {
                "user_name": invitor_name,
                "project_name": project.name,
                "cloud_name": cloud.name,
                "project_url": f"{settings.APP_URL}/cloud/{cloud.pk}/project/{project.pk}/dashboard",
            }
            mandrill.send_mail("user-ajout-un-projet", invited_content, [invited.to_json()])

            send_invitation_accepted(invitor, invited, cloud, project)
        else:
            invited_content = {
                "user_name": invitor_name,
                "cloud_name": cloud.name,
                "cloud_url": settings.APP_URL,
            }
            mandrill.send_mail("user-ajout-un-cloud", invited_content, [invited.to_json()])

            send_invitation_accepted(invitor, invited, cloud)


def send_ifc_ok(user, ifc):
    if not user:
        return
    content = {
        "ifc_name": ifc.name,
        "viewer_url": f"{settings.APP_URL}/cloud/{ifc.project.cloud.pk}/project/{ifc.project.pk}/ifc/{ifc.pk}/viewer",
    }
    mandrill.send_mail("votre-ifc-t-converti", content, [user.to_json()])


def send_ifc_ko(user, ifc):
    if not user:
        return
    content = {
        "ifc_name": ifc.name,
        "project_url": f"{settings.APP_URL}/cloud/{ifc.project.cloud.pk}/project/{ifc.project.pk}/dashboard",
    }
    mandrill.send_mail("erreur-la-conversion-de-votre-ifc", content, [user.to_json()])
