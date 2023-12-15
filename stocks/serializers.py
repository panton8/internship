from rest_framework import serializers

from stocks.models import Crypto, History, Order, Subscription, Wallet
from stocks.utils import order_params_check
from users.models import User


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ["name", "code", "capacity", "exchange_rate"]


class WalletSerializer(serializers.ModelSerializer):
    crypto = CryptoSerializer().fields.get("name")

    class Meta:
        model = Wallet
        fields = ["crypto", "amount"]


class SubscriptionSerializer(serializers.ModelSerializer):
    crypto = CryptoSerializer()

    class Meta:
        model = Subscription
        fields = ["crypto"]


class AddSubscriptionSerializer(SubscriptionSerializer):
    user = serializers.CharField(allow_null=True, read_only=True)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        crypto_name = validated_data["crypto"]["name"]
        try:
            validated_data["crypto"] = Crypto.objects.get(name=crypto_name)
        except Crypto.DoesNotExist:
            raise serializers.ValidationError({"error": "Non-existent currency"})
        return Subscription.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    crypto = serializers.CharField(source="crypto.name")

    class Meta:
        model = Order
        fields = [
            "user",
            "crypto",
            "order_type",
            "execution_method",
            "total_price",
            "amount",
            "is_auto",
            "desired_exchange_rate",
        ]

    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)

        user = self.context["request"].user

        if user.role in [User.Roles.USER]:
            representation.pop("user", None)

        return representation


class CreateOrderSerializer(OrderSerializer):
    user = serializers.CharField(allow_null=True, read_only=True)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        crypto_name = validated_data["crypto"]["name"]
        try:
            validated_data["crypto"] = Crypto.objects.get(name=crypto_name)
        except Crypto.DoesNotExist:
            raise serializers.ValidationError({"error": "Non-existent currency"})
        order_params_check(validated_data)
        new_order = Order.objects.create(**validated_data)
        new_order.fill_amount_or_price()
        new_order.save()
        return new_order


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ("username", "crypto_name", "total_price", "amount", "date")

    def to_representation(self, instance):
        representation = super(HistorySerializer, self).to_representation(instance)

        user = self.context["request"].user

        if user.role in [User.Roles.USER]:
            representation.pop("username", None)

        return representation
