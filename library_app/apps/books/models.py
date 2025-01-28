from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} - {self.author}"
