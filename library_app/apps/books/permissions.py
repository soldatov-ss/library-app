from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser

from library_app.apps.books.models import Book


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class IsAllowedToBorrowBook(BasePermission):
    @staticmethod
    def has_permission(request, _):
        return not request.user.is_anonymous and not request.user.is_staff

    @staticmethod
    def has_object_permission(_, __, obj: Book):
        return obj.availability


class IsAllowedToReturnBook(BasePermission):
    @staticmethod
    def has_permission(request, _):
        return not request.user.is_anonymous and not request.user.is_staff

    @staticmethod
    def has_object_permission(_, __, obj: Book):
        return not obj.availability
