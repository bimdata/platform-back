from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from user.models import User
from utils import mails


@receiver(post_save, sender=User)
def create_root_folder_on_create(sender, instance, created, **kwargs):
    if created:
        mails.send_onboarding(instance)
