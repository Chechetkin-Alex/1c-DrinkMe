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
        if product.is_student_special:
            if item.combo_drink is None or item.combo_bakery is None:
                raise serializers.ValidationError("Для комбо нужно выбрать кофе и выпечку")
            if item.quantity > item.combo_drink.stock:
                raise serializers.ValidationError("На складе нет такого количества кофе")
            if item.quantity > item.combo_bakery.stock:
                raise serializers.ValidationError("На складе нет такой выпечки")
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
                combo_drink_name=item.combo_drink.name if item.combo_drink else "",
                combo_bakery_name=item.combo_bakery.name if item.combo_bakery else "",
                milk_type=item.milk_type,
            )
        )
        product.stock -= item.quantity
        product.save(update_fields=["stock"])
        if product.is_student_special:
            item.combo_drink.stock -= item.quantity
            item.combo_drink.save(update_fields=["stock"])
            item.combo_bakery.stock -= item.quantity
            item.combo_bakery.save(update_fields=["stock"])

    OrderItem.objects.bulk_create(order_items)
    cart.items.all().delete()
    return order
