# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from utils.mailer import send_mail


def send_onboarding(user):
    content = {"platform_url": user.initial_referer, "user_name": user.first_name}
    send_mail("mailing-welcome", content, user, language=user.language)


def send_notifications(user, event_type, notifications):
    content = {
        "notifications": notifications,
        "platform_url": user.initial_referer,
    }
    send_mail(
        f"notifications-{event_type}",
        content,
        user,
        language=user.language,
    )
