import factory

from library_app.apps.books.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    author = factory.Faker("name")
    isbn = factory.Sequence(lambda n: f"isbn-{n}")
    page_count = factory.Faker("random_int", min=100, max=1000)
    availability = True
