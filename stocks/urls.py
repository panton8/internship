from django.urls import include, path
from rest_framework.routers import DefaultRouter

from stocks.views import (CryptoViewSet, OrderViewSet, SubscriptionViewSet,
                          WalletViewSet)

router = DefaultRouter()
router.register("wallet", WalletViewSet)
router.register("orders", OrderViewSet)
router.register("cryptos", CryptoViewSet)
router.register("stocks", SubscriptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
