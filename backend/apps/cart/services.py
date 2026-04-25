from rest_framework import serializers

from apps.cart.models import Cart, CartItem


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def add_product_to_cart(cart, product, quantity, milk_type=CartItem.MilkType.REGULAR):
    if quantity > product.stock:
        raise serializers.ValidationError("На складе нет такого количества товара")

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        milk_type=milk_type,
        defaults={"quantity": quantity},
    )
    if not created:
        new_quantity = item.quantity + quantity
        if new_quantity > product.stock:
            raise serializers.ValidationError("На складе нет такого количества товара")
        item.quantity = new_quantity
        item.save(update_fields=["quantity"])
    return item
