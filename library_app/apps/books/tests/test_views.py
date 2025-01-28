from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APITestCase

from library_app.apps.books.tests.factories import BookFactory
from library_app.apps.loans.tests.factories import LoanFactory
from library_app.apps.users.tests.factories import UserFactory

faker = Faker()


class TestBookViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.admin = UserFactory(is_staff=True)

        cls.book = BookFactory()
        cls.borrowed_book = BookFactory(availability=False)
        cls.loan = LoanFactory(book=cls.borrowed_book, user=cls.user, returned_at=None)
        BookFactory.create_batch(4)

        cls.data = {
            "title": faker.sentence(),
            "author": faker.name(),
            "isbn": "isbn-123",
            "page_count": faker.random_int(min=100, max=500),
            "availability": faker.random_element(elements=[True, False]),
        }

        cls.url = reverse("books-list")
        cls.detail_url = reverse("books-detail", args=[cls.book.id])
        cls.borrow_url = reverse("books-borrow", args=[cls.book.id])
        cls.return_url = reverse("books-return", args=[cls.borrowed_book.id])

    def test_book_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.book.title)

    def test_book_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 6)

    def test_book_list_filter_by_author(self):
        response = self.client.get(self.url, {"search": self.book.author})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_book_list_filter_by_title(self):
        response = self.client.get(self.url, {"search": self.book.title})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_book_create(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], self.data["title"])

    def test_book_update(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.put(self.detail_url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.data["title"])

    def test_book_delete(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)

    def test_book_borrow_success(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.borrow_url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["book"], self.book.id)

    def test_book_borrow_not_authenticated(self):
        response = self.client.post(self.borrow_url)
        self.assertEqual(response.status_code, 401)

    def test_book_borrow_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.borrow_url)
        self.assertEqual(response.status_code, 403)

    def test_book_borrow_not_available(self):
        self.client.force_authenticate(user=self.user)
        self.book.availability = False
        self.book.save()

        response = self.client.post(self.borrow_url)

        self.assertEqual(response.status_code, 403)

    def test_book_return_not_authenticated(self):
        response = self.client.post(self.return_url)
        self.assertEqual(response.status_code, 401)

    def test_book_return_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.return_url)
        self.assertEqual(response.status_code, 403)

    def test_book_return_already_returned(self):
        self.loan.returned_at = timezone.now()
        self.loan.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.return_url)

        self.assertEqual(response.status_code, 404)

    def test_book_return_wrong_user(self):
        self.client.force_authenticate(user=UserFactory())
        response = self.client.post(self.return_url)
        self.assertEqual(response.status_code, 404)

    def test_book_return_wrong_book(self):
        self.client.force_authenticate(user=self.user)
        wrong_book = BookFactory(availability=False)

        response = self.client.post(reverse("books-return", args=[wrong_book.id]))

        self.assertEqual(response.status_code, 404)

    def test_book_return_success(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.return_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Book returned successfully.")
