from django.db import models


# TODO: we can move a project in another cloud. Make sur le cloud_id is updated (when we recieve a webhook?)
# TODO: check if the webhook is correctly updated when a project is moved
# TODO: update project name. Before sending notification?
class Project(models.Model):
    api_id = models.PositiveIntegerField(unique=True)
    cloud_id = models.PositiveIntegerField()
    name = models.CharField(max_length=256)


class Subscription(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    periodic_task = models.ForeignKey(
        "django_celery_beat.PeriodicTask", on_delete=models.CASCADE
    )  # on_delete=models.SET_NULL ?

    file_creation = models.BooleanField(default=False)
    file_deletion = models.BooleanField(default=False)
    file_new_version = models.BooleanField(default=False)
    folder_creation = models.BooleanField(default=False)
    folder_deletion = models.BooleanField(default=False)
    visa_creation = models.BooleanField(default=False)
    visa_deletion = models.BooleanField(default=False)
    visa_validation = models.BooleanField(default=False)
    visa_denied = models.BooleanField(default=False)
    bcf_topic_creation = models.BooleanField(default=False)
    bcf_topic_deletion = models.BooleanField(default=False)
    invitation_accepted = models.BooleanField(default=False)
    meta_building_creation = models.BooleanField(default=False)
    meta_building_deletion = models.BooleanField(default=False)
    model_deletion = models.BooleanField(default=False)
