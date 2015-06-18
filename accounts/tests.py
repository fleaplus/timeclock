from django.test import TestCase

from .models import TimeclockUser
from .factories import TimeclockUserFactory


class TimeclockUserTestCase(TestCase):

    def test_uses_email_for_username(self):
        user = TimeclockUserFactory()

        self.assertEqual(user.email, user.get_username())
        self.assertEqual(user.USERNAME_FIELD, 'email')

    def test_requires_email(self):
        with(self.assertRaises(ValueError)):
            user = TimeclockUser.objects.create_user(email='')

    def test_normalizes_email(self):
        email = 'test@EXAMPLE.COM'
        user = TimeclockUser.objects.create_user(email=email)

        self.assertEqual(user.email, 'test@example.com')

    def test_user_saved(self):
        email = 'test@example.com'
        TimeclockUser.objects.create_user(email=email)

        self.assertEqual(TimeclockUser.objects.first().email, email)
