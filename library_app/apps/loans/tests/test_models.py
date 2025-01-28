from django.test import TestCase
from django.utils.timezone import now

from library_app.apps.books.models import Book
from library_app.apps.loans.models import Loan
from library_app.apps.users.models import User


class LoanModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(title="Sample Book", page_count=100)

    def test_loan_creation(self):
        loan = Loan.objects.create(user=self.user, book=self.book)
        self.assertIsInstance(loan, Loan)
        self.assertEqual(loan.user, self.user)
        self.assertEqual(loan.book, self.book)
        self.assertIsNone(loan.returned_at)
        self.assertIsNotNone(loan.borrowed_at)

    def test_str_representation(self):
        loan = Loan.objects.create(user=self.user, book=self.book)
        expected_str = f"{self.user.username} borrowed {self.book.title}"
        self.assertEqual(str(loan), expected_str)

    def test_loan_ordering(self):
        loan1 = Loan.objects.create(user=self.user, book=self.book, borrowed_at=now())
        loan2 = Loan.objects.create(user=self.user, book=self.book, borrowed_at=now())
        loans = list(Loan.objects.all())
        self.assertEqual(loans[0], loan2)
        self.assertEqual(loans[1], loan1)

    def test_returned_at_field_accepts_null(self):
        loan = Loan.objects.create(user=self.user, book=self.book)
        self.assertIsNone(loan.returned_at)
        loan.returned_at = now()
        loan.save()
        self.assertIsNotNone(loan.returned_at)
