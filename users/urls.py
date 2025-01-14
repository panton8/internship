from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()
router.register("profile", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
