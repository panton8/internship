from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, RegistrationView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", RegistrationView.as_view()),
    path("signin/", LoginView.as_view()),
]
