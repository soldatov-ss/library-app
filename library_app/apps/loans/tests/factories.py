import factory
from django.utils import timezone

from library_app.apps.books.tests.factories import BookFactory
from library_app.apps.loans.models import Loan
from library_app.apps.users.tests.factories import UserFactory


class LoanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Loan

    borrowed_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    returned_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory)
