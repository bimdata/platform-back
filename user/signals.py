# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from utils import mails


@receiver(post_save, sender=User)
def create_root_folder_on_create(sender, instance, created, **kwargs):
    if created:
        mails.send_onboarding(instance)
