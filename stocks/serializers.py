from django.core.validators import MinValueValidator
from rest_framework import serializers

from stocks.models import Crypto, Order, Subscription, Wallet
from users.serializers import UserSerializer


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ["name", "capacity", "exchange_rate"]


class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer().fields.get("username")
    crypto = CryptoSerializer().fields.get("name")

    class Meta:
        model = Wallet
        fields = ["user", "crypto", "amount"]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer().fields.get("username")
    crypto = CryptoSerializer().fields.get("name")

    class Meta:
        model = Subscription
        fields = ["user", "crypto"]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer().fields.get("username")
    crypto = CryptoSerializer().fields.get("name")

    class Meta:
        model = Order
        fields = ["user", "crypto", "order_type", "total_price", "amount", "is_auto"]


class AdditionalBalanceSerializer(serializers.Serializer):
    additional_balance = serializers.FloatField(validators=[MinValueValidator(0.01)])
