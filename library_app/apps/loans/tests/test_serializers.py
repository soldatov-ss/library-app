from django.utils.timezone import now
from rest_framework.test import APITestCase

from library_app.apps.books.tests.factories import BookFactory
from library_app.apps.loans.serializers import LoanSerializer
from library_app.apps.loans.tests.factories import LoanFactory
from library_app.apps.users.tests.factories import UserFactory


class LoanSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.book = BookFactory()
        self.loan = LoanFactory(user=self.user, book=self.book)

    def test_serialization(self):
        serializer = LoanSerializer(self.loan)
        expected_data = {
            "id": self.loan.id,
            "user": self.loan.user.id,
            "book": self.loan.book.id,
            "borrowed_at": self.loan.borrowed_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "returned_at": self.loan.returned_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialization(self):
        data = {
            "user": self.user.id,
            "book": self.book.id,
            "borrowed_at": now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "returned_at": None,
        }

        serializer = LoanSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        loan = serializer.save()
        self.assertEqual(loan.user.id, self.user.id)
        self.assertEqual(loan.book.id, self.book.id)

    def test_invalid_data(self):
        invalid_data = {
            "user": None,
            "book": None,
            "borrowed_at": None,
            "returned_at": None,
        }

        serializer = LoanSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
        self.assertIn("book", serializer.errors)
