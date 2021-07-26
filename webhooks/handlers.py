# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from utils import mails
from user.models import IfcMail, User


def handle_org_member(payload):
    mails.send_invitation_accepted(payload.get("data"))


def handler_ifc_process_update(payload):
    data = payload.get("data")
    data["cloud_id"] = payload["cloud_id"]

    if not data.get("creator"):
        return

    if data.get("status") == "C" or data.get("status") == "E":
        try:
            ifc_mail = IfcMail.objects.get(
                user__sub=data["creator"]["sub"], ifc_id=data["id"]
            )
            if data.get("status") == "C" and ifc_mail.last_sent == IfcMail.MAIL_ERRORED:
                ifc_mail.last_sent = IfcMail.MAIL_SUCCESS
                ifc_mail.save()
                mails.send_ifc_ok(data)

        except IfcMail.DoesNotExist:
            user = User.objects.get(sub=data["creator"]["sub"])
            ifc_mail = IfcMail(ifc_id=data["id"], user=user)

            if data.get("status") == "C":
                ifc_mail.last_sent = IfcMail.MAIL_SUCCESS
                ifc_mail.save()
                mails.send_ifc_ok(data)
            else:
                ifc_mail.last_sent = IfcMail.MAIL_ERRORED
                ifc_mail.save()
                mails.send_ifc_ko(data)


def route_webhook(payload):
    event_name = payload.get("event_name")
    if event_name == "org.members":
        handle_org_member(payload)
    elif event_name == "ifc.process_update":
        handler_ifc_process_update(payload)
