from celery import shared_task
from celery.utils.log import get_task_logger

from stocks.models import Crypto, History, Order, Wallet

logger = get_task_logger(__name__)


@shared_task
def complete_order(order_pk):
    order = Order.objects.get(pk=order_pk)
    user = order.user
    possible_wallet = Wallet.objects.filter(crypto=order.crypto).first()
    if order.order_type == Order.OrderType.PURCHASE:
        user.balance -= order.total_price
        user.save()
        if possible_wallet:
            possible_wallet.amount += order.amount
            possible_wallet.save()
        else:
            Wallet.objects.create(
                user=order.user, crypto=order.crypto, amount=order.amount
            )
    else:
        user.balance += order.total_price
        user.save()
        possible_wallet.amount -= order.amount
        possible_wallet.save()
    History.objects.create(
        username=order.user.username,
        crypto_name=order.crypto.name,
        total_price=order.total_price,
        amount=order.amount,
    )
    Order.objects.get(pk=order.pk).delete()


@shared_task
def complete_auto_order(crypto_pk, new_ex_rate):
    crypto = Crypto.objects.get(pk=crypto_pk)
    crypto.exchange_rate = new_ex_rate
    crypto.save()
    orders = Order.objects.all()
    for order in orders:
        if order.crypto.exchange_rate <= order.desired_exchange_rate:
            user = order.user
            possible_wallet = Wallet.objects.filter(crypto=order.crypto).first()
            order.fill_amount_or_price()
            order.save()
            if order.order_type == Order.OrderType.PURCHASE:
                user.balance -= order.total_price
                user.save()
                if possible_wallet:
                    possible_wallet.amount += order.amount
                    possible_wallet.save()
                else:
                    Wallet.objects.create(
                        user=order.user, crypto=order.crypto, amount=order.amount
                    )
            else:
                user.balance += order.total_price
                user.save()
                possible_wallet.amount -= order.amount
                possible_wallet.save()
            History.objects.create(
                username=order.user.username,
                crypto_name=order.crypto.name,
                total_price=order.total_price,
                amount=order.amount,
            )
            Order.objects.get(pk=order.pk).delete()
