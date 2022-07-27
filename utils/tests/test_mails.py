from django.core import mail
from django.test import TestCase
from utils import mailer
from parameterized import parameterized
from user.auth import activateLocale


class EmailTest(TestCase):
    @parameterized.expand(
        [
            ("mailing-welcome", {}, "Bienvenue sur la plateforme BIMData.io"),
        ]
    )
    def test_send_email_invitation_with_django(
        self, template_name, context, subject_expected
    ):
        # Send message.
        activateLocale("FR")
        mailer.send_mail(
            template_name, context, [{"email": "test@bimdata.io"}],
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject_expected)
