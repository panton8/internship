from rest_framework import mixins, permissions, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from stocks.models import Crypto, History, Order, Subscription, Wallet
from stocks.serializers import (AddSubscriptionSerializer,
                                CreateOrderSerializer, CryptoSerializer,
                                HistorySerializer, OrderSerializer,
                                SubscriptionSerializer, WalletSerializer)
from users.models import User


class WalletViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.role != User.Roles.ADMIN:
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
        "destroy": [IsAuthenticated, IsAdminUser],
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
        "destroy": [IsAuthenticated, IsAdminUser],
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
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_classes = {
        "create": AddSubscriptionSerializer,
        "default": SubscriptionSerializer,
    }

    permission_classes = {
        "list": [IsAuthenticated],
        "create": [IsAuthenticated],
        "destroy": [IsAuthenticated],
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
                return Subscription.objects.filter(user=self.request.user)
        return self.queryset


class HistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = History.objects.all()
    serializer_classes = {
        "default": HistorySerializer,
    }

    permission_classes = {
        "list": [IsAuthenticated],
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
                return History.objects.filter(username=self.request.user.username)
        return self.queryset
