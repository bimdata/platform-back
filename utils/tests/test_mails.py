from django.core import mail
from django.test import TestCase
from django.utils.translation import activate
from parameterized import parameterized

from utils import mailer


class EmailTest(TestCase):
    @parameterized.expand(
        [
            (
                "mailing-welcome",
                {"user_name": "Jane"},
                "Bienvenue sur la plateforme BIMData.io Jane",
            ),
        ]
    )
    def test_send_email_invitation_with_django(
        self, template_name, context, subject_expected
    ):
        # Send message.
        activate("FR")
        mailer.send_mail(
            template_name,
            context,
            [{"email": "test@bimdata.io"}],
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject_expected)
