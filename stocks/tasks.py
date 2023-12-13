from celery import shared_task
from celery.utils.log import get_task_logger

from crypto_project.celery import app
from stocks.models import History, Order, Wallet

logger = get_task_logger(__name__)


@app.task
def complete_order(order):
    order.fill_amount_or_price()
    order.save()
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
