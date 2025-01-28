from rest_framework import mixins, viewsets

from library_app.apps.users.models import User
from library_app.apps.users.permissions import IsUserOrCreatingAccountOrReadOnly
from library_app.apps.users.serializers import CreateUserSerializer, UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Updates and retrieves user accounts
    """

    queryset = User.objects.all()
    permission_classes = (IsUserOrCreatingAccountOrReadOnly,)

    def get_serializer_class(self):
        is_creating_a_new_user = self.action == "create"
        if is_creating_a_new_user:
            return CreateUserSerializer
        return UserSerializer
