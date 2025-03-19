from django.core import mail
from django.test import TestCase

from user.models import User


class EmailTest(TestCase):
    def test_send_email_invitation_with_django(self):
        # Send message.
        User.objects.create(email="test@bimdata.io", language="fr")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Bienvenue sur la plateforme BIMData.io")
