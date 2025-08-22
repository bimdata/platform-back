from bimdata_api_client import ApiException
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.core.management.base import BaseCommand
from django.core.management.base import no_translations
from django.template.loader import render_to_string
from django.utils import translation

from externals import keycloak
from externals.bimdata_api import ApiClient
from notification.models import NotificationHistory
from notification.models import Project
from notification.models import webhook_event_to_subscription


class Command(BaseCommand):
    help = "Send notifications email to defined users of project passed as first argument"

    def add_arguments(self, parser):
        parser.add_argument(
            "project_id",
            type=int,
            help="BIMData API project's id",
        )

    @no_translations
    def handle(self, *args, **options):
        project_id = options["project_id"]
        print(f"Sending mail for project {project_id}")
        project = (
            Project.objects.select_related("subscription").filter(api_id=project_id).first()
        )
        if not project:
            print(f"Unable to find project with id {project_id}")
            return

        subscription = project.subscription

        notifications = NotificationHistory.objects.filter(
            project=project, consumed=False
        ).order_by("created_at")

        if not notifications:
            print("No notifications to send")
            return

        # Updating project name
        project_name = ApiClient(keycloak.get_access_token()).collaboration_api.get_project(
            cloud_pk=project.cloud_id, id=project.api_id
        )["name"]

        if project_name != project.name:
            project.name = project_name
            project.save()

        recipients = []
        for group_id in subscription.recipients_group_ids:
            try:
                group = ApiClient(
                    keycloak.get_access_token()
                ).collaboration_api.get_manage_group(
                    cloud_pk=project.cloud_id,
                    project_pk=project.api_id,
                    id=group_id,
                )
                recipients += list(group.members)
            except ApiException as e:
                # The group has been deleted or the project has been moved to another cloud so the group id is no more correct
                print(f"Exception when calling get_manage_group: {e}")
                print(
                    "It can happend when the group has been deleted or when the project has been moved to another cloud"
                )
                return

        content = self.dispatch_notifications_to_content(notifications)

        from_email = settings.DEFAULT_FROM_EMAIL
        to_emails = [
            (
                f"{user.firstname} {user.lastname} <{user.email}>"
                if user.firstname
                else user.email
            )
            for user in recipients
        ]

        content["project"] = project
        content["platform_url"] = subscription.referer
        content["project_url"] = (
            subscription.referer + f"/spaces/{project.cloud_id}/projects/{project.api_id}"
        )

        with translation.override(subscription.locale):
            subject = render_to_string(
                "mails/project-notification-subject.txt", content
            ).strip()
            html_content = render_to_string("mails/project-notification.html", content)

        if settings.APP_EMAIL_HOST:
            with get_connection(
                host=settings.APP_EMAIL_HOST,
                port=settings.APP_EMAIL_PORT,
                username=settings.APP_EMAIL_HOST_USER,
                password=settings.APP_EMAIL_HOST_PASSWORD,
                use_tls=settings.APP_EMAIL_USE_TLS,
            ) as connection:
                email = EmailMessage(
                    subject, html_content, from_email, to_emails, connection=connection
                )
                email.content_subtype = "html"
                email.send()
        else:
            with get_connection() as connection:
                email = EmailMessage(
                    subject, html_content, from_email, to_emails, connection=connection
                )
                email.content_subtype = "html"
                email.send()

        # Mark all notifications as consumed
        notifications.update(consumed=True)

    def dispatch_notifications_to_content(self, notifications):
        content = {
            "document_creation": [],
            "document_deletion": [],
            "folder_creation": [],
            "folder_deletion": [],
            "visa_creation": [],
            "visa_deletion": [],
            "visa_validation": [],
            "visa_denied": [],
            "bcf_topic_creation": [],
            "bcf_topic_deletion": [],
            "invitation_accepted": [],
            "model_creation": [],
            "model_deletion": [],
            # Events items we want to show differently in mail but have the same event
            "document_new_version": [],
        }

        for notification in notifications:
            event_category = webhook_event_to_subscription[notification.event]
            if event_category == "document_creation":
                if notification.parsed_payload["document"]["history_count"] == 0:
                    content["document_creation"].append(notification.parsed_payload)
                else:
                    content["document_new_version"].append(notification.parsed_payload)
            else:
                content[event_category].append(notification.parsed_payload)

        return content
