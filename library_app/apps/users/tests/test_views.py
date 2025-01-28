import factory
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from library_app.apps.users.models import User
from library_app.apps.users.tests.factories import UserFactory

fake = Faker()


class TestUserListTestCase(APITestCase):
    """
    Tests /users list operations.
    """

    def setUp(self):
        self.url = reverse("users-list")
        self.user_data = factory.build(dict, FACTORY_CLASS=UserFactory)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=response.data.get("id"))
        self.assertEqual(user.username, self.user_data.get("username"))
        self.assertTrue(check_password(self.user_data.get("password"), user.password))


class TestUserDetailTestCase(APITestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("users-detail", kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user)

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_user(self):
        new_first_name = fake.first_name()
        payload = {"first_name": new_first_name}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.id)
        self.assertEqual(user.first_name, new_first_name)

    def test_user_cannot_update_stranger_profile(self):
        self.client.logout()
        response = self.client.put(self.url, {"first_name": fake.first_name()})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_auth_user_cannot_update_profile(self):
        self.client.force_authenticate(user=UserFactory())
        response = self.client.put(self.url, {"first_name": fake.first_name()})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
