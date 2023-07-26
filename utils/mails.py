# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.conf import settings
from utils.mailer import send_mail


def send_onboarding(user):
    content = {"platform_url": settings.PLATFORM_URL, "user_name": user.first_name}
    send_mail("mailing-welcome", content, [user.to_json()])


def send_notifications(user, event_type, notifications):
    content = {
        "notifications": notifications,
        "platform_url": settings.PLATFORM_URL,
    }
    send_mail(
        f"notifications-{event_type}", content, [user.to_json()], fail_silently=False
    )
