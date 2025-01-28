from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from library_app.apps.books.models import Book
from library_app.apps.loans.models import Loan
from library_app.apps.loans.serializers import LoanSerializer


class LoanViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        book = get_object_or_404(Book, pk=book_id)

        if not book.availability:
            return Response(
                {"error": "This book is not available."},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.availability = False
        book.save()
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        loan = self.get_object()
        book = loan.book
        if not book.availability:
            book.availability = True
            book.save()

        self.perform_destroy(loan)
        return Response(status=status.HTTP_204_NO_CONTENT)
