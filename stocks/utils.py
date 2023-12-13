from rest_framework import serializers

from stocks.models import Order, Wallet


def order_params_check(validated_data):
    if validated_data.get("is_auto", False) and not validated_data.get(
        "desired_exchange_rate", False
    ):
        raise serializers.ValidationError(
            {"error": "When order is auto desired_exchange_rate must be set."}
        )
    user = validated_data["user"]
    crypto = validated_data["crypto"]
    wallet = Wallet.objects.filter(user=user, crypto=crypto).first()
    if validated_data["order_type"] == Order.OrderType.PURCHASE:
        if (
            validated_data["execution_method"] == Order.ExecutionMethod.BY_PRICE
            and user.balance < validated_data["total_price"]
            or validated_data["execution_method"] == Order.ExecutionMethod.BY_AMOUNT
            and user.balance < validated_data["amount"] * crypto.exchange_rate
        ):
            raise serializers.ValidationError(
                {"error": "Order error. Your balance is not enough"}
            )
    if validated_data["order_type"] == Order.OrderType.SALE:
        if not wallet:
            raise serializers.ValidationError(
                {"error": "Order error. You don't have such crypto"}
            )
        if (
            validated_data["execution_method"] == Order.ExecutionMethod.BY_PRICE
            and validated_data["total_price"] > (wallet.amount * crypto.exchange_rate)
            or validated_data["execution_method"] == Order.ExecutionMethod.BY_AMOUNT
            and wallet.amount < validated_data["amount"]
        ):
            raise serializers.ValidationError(
                {"error": "Order error.  You don't have enough crypto for sale."}
            )