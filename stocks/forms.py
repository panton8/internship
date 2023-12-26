from django.forms import ModelForm

from stocks.models import Crypto, Order, Subscription, Wallet


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class WalletForm(ModelForm):
    class Meta:
        model = Wallet
        fields = "__all__"


class CryptoForm(ModelForm):
    class Meta:
        model = Crypto
        fields = "__all__"


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"
