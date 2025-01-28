from django.test import TestCase

from library_app.apps.books.models import Book
from library_app.apps.books.tests.factories import BookFactory


class TestBookModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book = BookFactory()
        BookFactory.create_batch(5)

    def test_book_str(self):
        self.assertEqual(str(self.book), f"{self.book.title} - {self.book.author}")

    def test_book_ordering(self):
        books = Book.objects.all()
        self.assertEqual(list(books), list(books.order_by("-id")))
