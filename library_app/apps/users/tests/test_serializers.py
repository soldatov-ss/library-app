from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
from django.test import TestCase

from library_app.apps.users.serializers import CreateUserSerializer
from library_app.apps.users.tests.factories import UserFactory


class TestCreateUserSerializer(TestCase):

    def setUp(self):
        self.user_data = model_to_dict(UserFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = CreateUserSerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_serializer_with_valid_data(self):
        serializer = CreateUserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_hashes_password(self):
        serializer = CreateUserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertTrue(check_password(self.user_data.get("password"), user.password))
