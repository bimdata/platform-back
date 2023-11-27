from django.core import mail
from django.test import TestCase
from parameterized import parameterized

from utils import mailer


class EmailTest(TestCase):
    @parameterized.expand(
        [
            (
                "mailing-welcome",
                {},
                "Bienvenue sur la plateforme BIMData.io",
            ),
        ]
    )
    def test_send_email_invitation_with_django(
        self, template_name, context, subject_expected
    ):
        # Send message.
        mailer.send_mail(template_name, context, [{"email": "test@bimdata.io"}], "FR")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject_expected)
