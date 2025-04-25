# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from externals.bimdata_api import ApiClient
from externals.keycloak import get_access_token
from user.models import Notification
from user.models import User


def get_user_from_sub(sub):
    if sub is None:
        return None
    try:
        return User.objects.get(sub=sub)
    except User.DoesNotExist:
        return None


def get_user_from_email(email):
    return User.objects.filter(email=email).first()


class RefreshHandler:
    def __init__(self, notification: Notification):
        self.notification = notification

    def refresh(self, save: bool = False) -> None:
        if self.notification.event_type == "bcf":
            self._refresh_bcf(save)

    def _refresh_bcf(self, save: bool) -> None:
        project = self.notification.payload["topic"]["project"]
        topic = self.notification.payload["topic"]["guid"]
        try:
            viewpoints = ApiClient(get_access_token()).bcf_api.get_viewpoints(
                project, topic, img_format="url"
            )
        except Exception:
            viewpoints = []
        snapshot_data = next(
            (
                viewpoint["snapshot"]["snapshot_data"]
                for viewpoint in viewpoints
                if viewpoint["snapshot"]
            ),
            None,
        )
        if snapshot_data:
            self.notification.payload["topic"]["snapshot_url"] = snapshot_data
            if save:
                self.notification.save()


class WebhookHandler:
    events = {
        "visa.validation.add": "add_validation",
        "visa.validation.remove": "remove_validation",
        "bcf.topic.creation": "add_bcf",
    }

    def __init__(self, data):
        self.event_name = data.get("event_name")
        self.cloud_id = (
            data["cloud_id"] if "cloud_id" in data else data.get("cloud", {}).get("id", None)
        )
        self.payload = data.get("data", {})
        self.payload["cloud_id"] = self.cloud_id

        if self.cloud_id:
            print("Cloud ID:", self.cloud_id)
            print("Project ID:", self.payload["project_id"])
            print("access token:", get_access_token())
            self.payload["project_name"] = ApiClient(
                get_access_token()
            ).collaboration_api.get_project(
                cloud_pk=self.cloud_id, id=self.payload["project_id"]
            )[
                "name"
            ]

    @classmethod
    def get_event(cls, event_name):
        return cls.events.get(event_name, "")

    @classmethod
    def get_event_type(cls, event_name):
        return event_name.split(".")[0]

    def is_valid(self):
        return self.get_event(self.event_name) != ""

    def get_handle_method(self):
        return getattr(self, "handle_" + self.get_event(self.event_name), None)

    def handle(self):
        handler = self.get_handle_method()
        if handler:
            handler()

    def handle_add_validation(self):
        validator = get_user_from_sub(self.payload["validation"]["validator"]["sub"])
        if validator is None:
            return
        self.payload["document_name"] = ApiClient(
            get_access_token()
        ).collaboration_api.get_document(
            cloud_pk=self.cloud_id,
            project_pk=self.payload["project_id"],
            id=self.payload["visa"]["document_id"],
        )[
            "name"
        ]

        Notification.objects.create(
            user=validator,
            cloud_id=self.cloud_id,
            event=self.get_event(self.event_name),
            event_type=self.get_event_type(self.event_name),
            payload=self.payload,
        )

    def handle_remove_validation(self):
        validator = get_user_from_sub(self.payload["validation"]["validator"]["sub"])
        if validator is None:
            return
        notifications = Notification.objects.filter(
            user=validator,
            payload__validation__id=self.payload["validation"]["id"],
            event="add_validation",
        ).order_by("-created_at")
        if len(notifications) > 0:
            add_notification = notifications.first()
            if add_notification.consumed is False:
                add_notification.delete()
                return

    def handle_add_bcf(self):
        if self.payload["topic"]["format"] == "standard":
            assigned_to = get_user_from_email(self.payload["topic"].get("assigned_to"))
            if assigned_to:
                Notification.objects.create(
                    user=assigned_to,
                    cloud_id=self.cloud_id,
                    event=self.get_event(self.event_name),
                    event_type=self.get_event_type(self.event_name),
                    payload=self.payload,
                )
