from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from stocks.models import Crypto, Order, Subscription, Wallet
from stocks.serializers import (CreateOrderSerializer, CryptoSerializer,
                                OrderSerializer, SubscriptionSerializer,
                                WalletSerializer)
from users.models import User


class WalletViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.role not in [User.Roles.ADMIN, User.Roles.ANALYST]:
                return Wallet.objects.filter(user=self.request.user)
        return self.queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    serializer_classes = {
        "create": CreateOrderSerializer,
        "default": OrderSerializer,
    }

    permission_classes = {
        "list": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsAdminUser],
        "partial_update": [IsAuthenticated, IsAdminUser],
        "destroy": [permissions.IsAuthenticated, permissions.IsAdminUser],
    }

    def get_permissions(self):
        return [
            permission() for permission in self.permission_classes.get(self.action, [])
        ]

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.serializer_classes["default"]
        )

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.role not in [User.Roles.ADMIN, User.Roles.ANALYST]:
                return Order.objects.filter(user=self.request.user)
        return self.queryset


class CryptoViewSet(viewsets.ModelViewSet):
    queryset = Crypto.objects.all()
    serializer_classes = {
        "default": CryptoSerializer,
    }

    permission_classes = {
        "list": [IsAuthenticated],
        "create": [IsAuthenticated, IsAdminUser],
        "update": [IsAuthenticated, IsAdminUser],
        "partial_update": [IsAuthenticated, IsAdminUser],
        "destroy": [permissions.IsAuthenticated, permissions.IsAdminUser],
    }

    def get_permissions(self):
        return [
            permission() for permission in self.permission_classes.get(self.action, [])
        ]

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.serializer_classes["default"]
        )


class SubscriptionViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=...,
    )
    def add(self, request):
        pass
