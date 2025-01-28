from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library_app.apps.books.tests.factories import BookFactory
from library_app.apps.loans.models import Loan
from library_app.apps.loans.serializers import LoanSerializer
from library_app.apps.loans.tests.factories import LoanFactory
from library_app.apps.users.tests.factories import UserFactory


class TestLoanListTestCase(APITestCase):
    """
    Tests /loans list operations.
    """

    def setUp(self):
        self.admin_user = UserFactory(is_staff=True)
        self.normal_user = UserFactory()
        self.book = BookFactory()
        self.loan = LoanFactory(user=self.normal_user, book=self.book)

        self.list_url = reverse("loans-list")

    def test_admin_can_list_loans(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Loan.objects.count())

    def test_non_admin_cannot_list_loans(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_loan_as_admin(self):
        self.client.force_authenticate(self.admin_user)
        payload = {"user": self.normal_user.pk, "book": self.book.pk}
        response = self.client.post(self.list_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Loan.objects.filter(user=self.normal_user, book=self.book).exists())

        self.book.refresh_from_db()
        self.assertFalse(self.book.availability)

    def test_create_loan_fails_when_book_not_available(self):
        self.book.availability = False
        self.book.save()

        self.client.force_authenticate(self.admin_user)
        payload = {"user": self.normal_user.pk, "book": self.book.pk}
        response = self.client.post(self.list_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This book is not available.")
        self.assertTrue(Loan.objects.filter(user=self.normal_user, book=self.book).exists())

    def test_non_admin_cannot_create_loan(self):
        self.client.force_authenticate(self.normal_user)
        payload = {
            "user": self.normal_user.pk,
            "book": self.book.pk,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_auth_user_cannot_create_loan(self):
        payload = {
            "user": self.normal_user.pk,
            "book": self.book.pk,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestLoanDetailTestCase(APITestCase):
    """
    Tests /loans detail operations.
    """

    def setUp(self):
        self.admin_user = UserFactory(is_staff=True)
        self.normal_user = UserFactory()
        self.book = BookFactory(availability=True)
        self.loan = LoanFactory(user=self.normal_user, book=self.book)

        self.detail_url = reverse("loans-detail", kwargs={"pk": self.loan.pk})

    def test_admin_can_retrieve_loan(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.detail_url)
        expected_data = LoanSerializer(self.loan).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_non_admin_cannot_retrieve_loan(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_auth_user_cannot_retrieve_loan(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_delete_loan(self):
        self.client.force_authenticate(self.admin_user)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Loan.objects.filter(pk=self.loan.pk).exists())

        self.book.refresh_from_db()
        self.assertTrue(self.book.availability)

    def test_non_admin_cannot_delete_loan(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_auth_user_cannot_delete_loan(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
