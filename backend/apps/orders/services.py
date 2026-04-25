from django.db import transaction
from rest_framework import serializers

from apps.cart.services import get_or_create_cart
from apps.orders.models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(user):
    cart = get_or_create_cart(user)
    items = list(cart.items.select_related("product").select_for_update())
    if not items:
        raise serializers.ValidationError("Корзина пустая")

    total_price = 0
    for item in items:
        product = item.product
        if not product.is_active or not product.category.is_active:
            raise serializers.ValidationError("В корзине есть недоступный товар")
        if item.quantity > product.stock:
            raise serializers.ValidationError("На складе нет такого количества товара")
        total_price += item.subtotal

    order = Order.objects.create(user=user, total_price=total_price)

    order_items = []
    for item in items:
        product = item.product
        order_items.append(
            OrderItem(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=item.quantity,
                milk_type=item.milk_type,
            )
        )
        product.stock -= item.quantity
        product.save(update_fields=["stock"])

    OrderItem.objects.bulk_create(order_items)
    cart.items.all().delete()
    return order
