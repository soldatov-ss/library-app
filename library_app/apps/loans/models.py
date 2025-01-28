from django.db import models
from django.utils.timezone import now

from library_app.apps.books.models import Book
from library_app.apps.users.models import User


class Loan(models.Model):
    borrowed_at = models.DateTimeField(default=now)
    returned_at = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
