# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.test import TestCase
from unittest.mock import patch
from user.models import User


class TestUserSignals(TestCase):
    @patch("utils.mails.send_onboarding")
    def test_endoard_mail_sent_on_creation(self, mail_onboarding):
        User.objects.create(
            username="1", sub="1", first_name="joe", last_name="John", email="joe@john.com"
        )
        self.assertTrue(mail_onboarding.called)
