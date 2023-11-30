from django.contrib import admin

from stocks.models import Crypto, Order, Subscription, Wallet


@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "exchange_rate")


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "crypto", "amount")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "crypto", "order_type", "total_price", "amount", "is_auto")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "crypto")
