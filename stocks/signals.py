from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from stocks.models import Crypto, Order
from stocks.tasks import complete_auto_order, complete_order


@receiver(post_save, sender=Order)
def close_order(sender, instance, created, **kwargs):
    if created and not instance.is_auto:
        complete_order.delay(instance.pk)
    if created and instance.is_auto:
        complete_auto_order.delay(instance.crypto.pk, instance.crypto.exchange_rate)


@receiver(pre_save, sender=Crypto)
def close_order(sender, instance, **kwargs):
    previous_instance = sender.objects.filter(pk=instance.pk).first()
    if previous_instance and previous_instance.exchange_rate != instance.exchange_rate:
        complete_auto_order.delay(instance.pk, instance.exchange_rate)
