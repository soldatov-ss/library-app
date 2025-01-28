from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from library_app.apps.books.views import BookViewSet
from library_app.apps.loans.views import LoanViewSet
from library_app.apps.users.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"books", BookViewSet, basename="books")
router.register("loans", LoanViewSet, basename="loans")

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API endpoints
    path("", include(router.urls)),
    # API schema and documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Authentication
    path("api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    # Redirect to API root from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
]

# Static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
