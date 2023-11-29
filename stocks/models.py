from django.db import models

from users.models import User


class Crypto(models.Model):
    name = models.CharField()
    capacity = models.FloatField
    exchange_rate = models.FloatField()


class Order(models.Model):
    class Type(models.TextChoices):
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Sale"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=8, choices=Type.choices)
    total_price = models.FloatField(default=0.0)
    amount = models.IntegerField()
    is_auto = models.BooleanField
