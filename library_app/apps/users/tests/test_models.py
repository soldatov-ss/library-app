from django.test import TestCase
from faker import Faker

from library_app.apps.users.models import User

faker = Faker()


class TestUserModel(TestCase):
    def test_user_model(self):
        user = User.objects.create_user(username=faker.user_name(), password=faker.password())

        self.assertEqual(user.username, user.__str__())
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(username=faker.user_name(), password=faker.password())

        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
