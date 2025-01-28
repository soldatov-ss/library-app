from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from library_app.apps.books.models import Book
from library_app.apps.books.permissions import IsAdminUserOrReadOnly, IsAllowedToBorrowBook, IsAllowedToReturnBook
from library_app.apps.books.serializers import BookSerializer
from library_app.apps.loans.models import Loan
from library_app.apps.loans.serializers import LoanSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author"]

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(
                response=LoanSerializer,
                description="Book borrowed successfully",
            ),
            404: OpenApiResponse(
                description="Not found",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="NotFoundResponse",
                        value={"message": "Book is not found."},
                    )
                ],
            ),
        },
    )
    @action(
        detail=True, methods=["post"], permission_classes=[IsAllowedToBorrowBook], url_path="borrow", url_name="borrow"
    )
    def borrow_book(self, request, *args, **kwargs):
        book = self.get_object()

        book.availability = False
        book.save()

        loan = Loan.objects.create(user=request.user, book=book)
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(
                description="Success",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="SuccessResponse",
                        value={"message": "Book returned successfully."},
                    )
                ],
            ),
            404: OpenApiResponse(
                description="Not found",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="NotFoundResponse",
                        value={"message": "Loan is not found."},
                    )
                ],
            ),
        },
    )
    @action(
        detail=True, methods=["post"], permission_classes=[IsAllowedToReturnBook], url_path="return", url_name="return"
    )
    def return_book(self, request, *args, **kwargs):
        book = self.get_object()
        loan = get_object_or_404(Loan, user=request.user, book=book, returned_at__isnull=True)

        loan.returned_at = timezone.now()
        loan.book.availability = True
        loan.book.save()
        loan.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
