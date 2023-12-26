from django.contrib import admin

from stocks.models import Crypto, History, Order, Subscription, Wallet


@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "capacity", "exchange_rate")


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "crypto", "amount")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "crypto",
        "order_type",
        "execution_method",
        "total_price",
        "amount",
        "is_auto",
        "desired_exchange_rate",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "crypto")


@admin.register(History)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "crypto_name",
        "total_price",
        "amount",
        "order_type",
        "execution_method",
        "exchange_rate",
        "date",
    )
