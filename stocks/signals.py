from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Crypto, Order
from .tasks import complete_auto_order, complete_order


@receiver(post_save, sender=Order)
def close_order(sender, instance, created, **kwargs):
    if created and not instance.is_auto:
        complete_order.delay(instance.pk)
    if created and instance.is_auto:
        complete_auto_order.delay(instance.pk)
