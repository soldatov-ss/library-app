from django.test import TestCase

from library_app.apps.books.serializers import BookSerializer
from library_app.apps.books.tests.factories import BookFactory


class TestBookSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = BookFactory()

    def test_book_serializer(self):
        serializer = BookSerializer(instance=self.book)

        self.assertDictEqual(
            serializer.data,
            {
                "id": self.book.id,
                "title": self.book.title,
                "author": self.book.author,
                "isbn": self.book.isbn,
                "page_count": self.book.page_count,
                "availability": self.book.availability,
            },
        )
